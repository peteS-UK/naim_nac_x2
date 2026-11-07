"""Balance buttons for Naim NAC."""

from homeassistant import config_entries, core
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.const import CONF_NAME, STATE_UNAVAILABLE
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.event import async_track_state_change_event

from .const import DOMAIN, MANUFACTURER, MODEL, device_unique_id
from .remote import NacRemote

BUTTONS = (
    ButtonEntityDescription(
        key="balance_left", name="Balance left", icon="mdi:arrow-left"
    ),
    ButtonEntityDescription(
        key="balance_right", name="Balance right", icon="mdi:arrow-right"
    ),
)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry, async_add_entities
) -> None:
    """Add balance buttons associated with the preamplifier."""
    async_add_entities(
        NacBalanceButton(entry.data[CONF_NAME], entry.runtime_data, description)
        for description in BUTTONS
    )


class NacBalanceButton(ButtonEntity):
    """Send a balance command using the entry's shared transmitter."""

    _attr_has_entity_name = True
    _attr_available = False

    def __init__(
        self, name: str, remote: NacRemote, description: ButtonEntityDescription
    ) -> None:
        self.entity_description = description
        self._remote = remote
        unique_id = device_unique_id(name)
        self._attr_unique_id = f"{unique_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            name=name,
            manufacturer=MANUFACTURER,
            model=MODEL,
        )

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._remote.emitter:
            self._update_availability()

            @core.callback
            def emitter_changed(event):
                self._update_availability()
                self.async_write_ha_state()

            self.async_on_remove(
                async_track_state_change_event(
                    self.hass, [self._remote.emitter], emitter_changed
                )
            )

    @core.callback
    def _update_availability(self) -> None:
        state = self.hass.states.get(str(self._remote.emitter))
        self._attr_available = state is not None and state.state != STATE_UNAVAILABLE

    async def async_press(self) -> None:
        await self._remote.send(self.entity_description.key, self._context)
