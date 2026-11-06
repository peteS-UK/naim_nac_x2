"""The Naim NAC integration."""

from homeassistant import config_entries, core
from homeassistant.const import Platform
from homeassistant.helpers import issue_registry as ir

from .const import CONF_INFRARED_ENTITY_ID, CONF_REMOTE_ENTITY, DOMAIN
from .remote import NacRemote

PLATFORMS = [Platform.MEDIA_PLAYER, Platform.BUTTON]


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""

    data = {**entry.data, **entry.options}
    issue_id = f"reselect_ir_emitter_{entry.entry_id}"
    if entry.data.get(CONF_REMOTE_ENTITY) and not entry.data.get(
        CONF_INFRARED_ENTITY_ID
    ):
        ir.async_create_issue(
            hass,
            DOMAIN,
            issue_id,
            is_fixable=True,
            severity=ir.IssueSeverity.WARNING,
            translation_key="reselect_ir_emitter",
            translation_placeholders={"name": entry.title},
            data={"entry_id": entry.entry_id},
        )
    else:
        ir.async_delete_issue(hass, DOMAIN, issue_id)

    entry.runtime_data = NacRemote(hass, data.get(CONF_INFRARED_ENTITY_ID))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> None:
    """Remove a pending migration issue when its entry is deleted."""
    ir.async_delete_issue(hass, DOMAIN, f"reselect_ir_emitter_{entry.entry_id}")
