from __future__ import annotations

from dataclasses import dataclass

import probatio
from homeassistant import config_entries, core
from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerDeviceClass,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_NAME, STATE_UNAVAILABLE
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import (
    config_validation as cv,
)
from homeassistant.helpers import (
    entity_platform,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.event import async_track_state_change_event
from homeassistant.helpers.restore_state import ExtraStoredData, RestoreEntity

from .const import (
    CONF_INFRARED_ENTITY_ID,
    CONF_INPUT1,
    CONF_INPUT2,
    CONF_INPUT3,
    CONF_INPUT4,
    CONF_INPUT5,
    CONF_INPUT6,
    DOMAIN,
    MANUFACTURER,
    MODEL,
    SERVICE_SEND_COMMAND,
    device_unique_id,
)
from .remote import NacRemote

SUPPORT = (
    MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    data = {**config_entry.data, **config_entry.options}
    _source_map = {
        "one": data[CONF_INPUT1],
        "two": data[CONF_INPUT2],
        "three": data[CONF_INPUT3],
        "four": data[CONF_INPUT4],
        "five": data[CONF_INPUT5],
        "six": data[CONF_INPUT6],
    }
    async_add_entities(
        [
            Device(
                hass,
                data[CONF_NAME],
                data.get(CONF_INFRARED_ENTITY_ID),
                _source_map,
                config_entry.runtime_data,
            )
        ]
    )

    # Register entity services
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SEND_COMMAND,
        {
            probatio.Required("command"): cv.string,
        },
        Device.send_command.__name__,
    )


@dataclass
class SourceData(ExtraStoredData):
    """Persist the physical input even if its label changes."""

    input_key: str | None

    def as_dict(self) -> dict:
        return {"input_key": self.input_key}


class Device(MediaPlayerEntity, RestoreEntity):  # pyright: ignore[reportIncompatibleVariableOverride]
    """Represent a Naim NAC."""

    _attr_assumed_state = True
    _attr_device_class = MediaPlayerDeviceClass.RECEIVER
    _attr_has_entity_name = True
    _attr_icon = "mdi:audio-video"
    _attr_is_volume_muted = False
    _attr_name = None
    _attr_should_poll = False
    _attr_state = MediaPlayerState.ON
    _attr_supported_features = SUPPORT

    def __init__(self, hass, name, infrared_entity_id, source_map, remote=None):
        self._attr_unique_id = device_unique_id(name)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._attr_unique_id)},
            name=name,
            manufacturer=MANUFACTURER,
            model=MODEL,
        )
        self._infrared_entity_id = infrared_entity_id
        self._attr_available = False
        self._remote = remote or NacRemote(hass, infrared_entity_id)
        self._source_map = source_map
        self._attr_source = None
        self._source_key = None
        self._attr_source_list = list(self._source_map.values())

    async def async_select_source(self, source: str) -> None:
        _cmd = [key for key, val in self._source_map.items() if val == source]
        if not _cmd:
            raise ServiceValidationError(f"Unknown source: {source}")
        await self._send_remote_command(_cmd[0])
        self._source_key = _cmd[0]
        self._attr_source = source
        self.async_schedule_update_ha_state()

    async def async_added_to_hass(self) -> None:
        """Track the emitter without removing the entity during migration."""
        await super().async_added_to_hass()
        if extra := await self.async_get_last_extra_data():
            input_key = extra.as_dict().get("input_key")
            if isinstance(input_key, str) and input_key in self._source_map:
                self._source_key = input_key
                self._attr_source = self._source_map[input_key]
        elif last_state := await self.async_get_last_state():
            source = last_state.attributes.get("source")
            if source in self._source_map.values():
                self._attr_source = source
                self._source_key = next(
                    key for key, label in self._source_map.items() if label == source
                )
        if self._infrared_entity_id:
            self._update_emitter_availability()

            @core.callback
            def emitter_changed(event):
                self._update_emitter_availability()
                self.async_write_ha_state()

            self.async_on_remove(
                async_track_state_change_event(
                    self.hass, [self._infrared_entity_id], emitter_changed
                )
            )

    @core.callback
    def _update_emitter_availability(self) -> None:
        state = self.hass.states.get(self._infrared_entity_id)
        self._attr_available = state is not None and state.state != STATE_UNAVAILABLE

    @property
    def extra_restore_state_data(self) -> SourceData:
        return SourceData(self._source_key)

    async def _send_remote_command(self, command):
        await self._remote.send(command, self._context)

    async def async_mute_volume(self, mute: bool) -> None:
        await self._send_remote_command("mute")

    async def async_volume_up(self):
        await self._send_remote_command("vol+")

    async def async_volume_down(self):
        await self._send_remote_command("vol-")

    async def send_command(self, command):
        await self._send_remote_command(command)
        if command in self._source_map:
            self._source_key = command
            self._attr_source = self._source_map[command]
            self.async_write_ha_state()
