from __future__ import annotations

import logging

import voluptuous as vol
from homeassistant import config_entries, core
from homeassistant.components.media_player import (
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from homeassistant.const import CONF_NAME
from homeassistant.helpers import (
    config_validation as cv,
    entity_platform,
)
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, SERVICE_SEND_COMMAND, CONF_BROADLINK

_LOGGER = logging.getLogger(__name__)

COMMANDS = {
    "volume_up": "JgA0ABsfHB8bIDkeHB8cHxweHjo6HhwfHB8bAAujGx8cHxsfOR8cHxsfHB8cPDkfGyAcHh0ADQUAAAAA",
    "volume_down": "JgA0AB4fHh0eHTsdHR4eHR0eHjo3Ih0eHjocAAt2GyAdHh4cPB0dHh4dHh0eOjsdHxwfOhsADQUAAAAA",
    "mute": "JgAwABwfOT05HxwfHB8cHxwfHDwcHzk9HAALdhsgOjw5HxwfGyAbIBsgGz0cHzk9GwANBQAAAAAAAAAA",
    "one": "JgA0ABwfHB4cHzkgHB8bHx0fGz05Hxw9OgALkhwfGyAbIDkfHB8cIBogHDw6Hxw8OQAMqQoADQUAAAAA",
    "two": "JgAwABsgOjs5IBwfGyEbHxw8Oh4dPBohGwALdh0eOT06HhwfHB8cHxw8OSAcPBwfHAANBQAAAAAAAAAA",
    "three": "JgAwABwgGyAaIDofGyAaIRogHDw4PjkgGgALlRwfGx8cIDchGyAbIBsfHTw5PTkfHAANBQAAAAAAAAAA",
    "four": "JgAsABwgOTw5IBsgGx8dIBs8OT04PRwAC3YbIDo7OSAbIRogHCAaPTo8OT0bAA0FAAAAAAAAAAAAAAAA",
    "five": "JgAwABsgHCAcHjkfGyAbIBsgGz05PRwfOQALkxwgHB4cIDggGx8cHx4dHD06OxwfOQANBQAAAAAAAAAA",
    "six": "JgA0ABwfGyAcHzkfHR4cHxsgGz05PR4dHB8dAAt0HB8cHx0eOR8cHxwfHR4cPTk5Hx8cHx4ADQUAAAAA",
}

SOURCE_MAP = {
    "one": "Phono",
    "two": "CD",
    "three": "Tuner",
    "four": "Tape",
    "five": "VCR",
    "six": "AUX",
}

SUPPORT_NAC = (
    MediaPlayerEntityFeature.VOLUME_STEP
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
)


async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
) -> None:
    async_add_entities(
        [
            NAC_Device(
                hass, config_entry.data[CONF_NAME], config_entry.data[CONF_BROADLINK]
            )
        ]
    )

    # Register entity services
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SEND_COMMAND,
        {
            vol.Required("command"): cv.string,
        },
        NAC_Device.send_command.__name__,
    )


class NAC_Device(MediaPlayerEntity):
    # Representation of a NAC

    def __init__(self, hass, name, broadlink_entity):
        self._hass = hass
        self._state = MediaPlayerState.IDLE
        self._entity_id = "media_player.naim_nac"
        self._unique_id = "naim_nac_" + name.replace(" ", "_").replace(
            "-", "_"
        ).replace(":", "_")
        self._device_class = "receiver"
        self._name = name
        self._broadlink_entity = broadlink_entity
        self._muted = False
        self._source = None
        self._sources = list(SOURCE_MAP.values())

    async def async_select_source(self, source: str) -> None:
        self._source = source
        _cmd = [key for key, val in SOURCE_MAP.items() if val == source]
        await self._send_broadlink_command(_cmd[0])
        self.async_schedule_update_ha_state()

    @property
    def source_list(self):
        return self._sources

    @property
    def source(self):
        return self._source

    @property
    def should_poll(self):
        return False

    @property
    def icon(self):
        return "mdi:audio-video"

    @property
    def state(self) -> MediaPlayerState:
        return MediaPlayerState.ON

    @property
    def name(self):
        # return self._device.name
        return None

    @property
    def has_entity_name(self):
        return True

    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self._unique_id)
            },
            name=self._name,
            manufacturer="Naim",
            model="NAC",
        )

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def device_class(self):
        return self._device_class

    @entity_id.setter
    def entity_id(self, entity_id):
        self._entity_id = entity_id

    @property
    def supported_features(self) -> MediaPlayerEntityFeature:
        return SUPPORT_NAC

    async def _send_broadlink_command(self, command):
        await self._hass.services.async_call(
            "remote",
            "send_command",
            {
                "entity_id": self._broadlink_entity,
                "num_repeats": "1",
                "delay_secs": "0.4",
                "command": f"b64:{COMMANDS[command]}",
            },
        )

    @property
    def is_volume_muted(self):
        return self._muted

    async def async_mute_volume(self, mute: bool) -> None:
        await self._send_broadlink_command("mute")
        self._muted = not self._muted
        self.async_schedule_update_ha_state()

    async def async_volume_up(self):
        await self._send_broadlink_command("volume_up")

    async def async_volume_down(self):
        await self._send_broadlink_command("volume_down")

    async def send_command(self, command):
        await self._send_broadlink_command(command)
