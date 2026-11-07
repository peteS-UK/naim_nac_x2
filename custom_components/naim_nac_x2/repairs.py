"""Repair flows for Naim NAC."""

import probatio
from homeassistant.components.infrared import async_get_emitters
from homeassistant.components.repairs import RepairsFlow, RepairsFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.helpers.selector import EntitySelector, EntitySelectorConfig

from .const import CONF_INFRARED_ENTITY_ID, CONF_REMOTE_ENTITY, CONF_REMOTE_TYPE


class ReselectIREmitterFlow(RepairsFlow):
    """Replace a legacy remote with an infrared emitter."""

    def __init__(self, entry_id: str) -> None:
        self._entry_id = entry_id

    async def async_step_init(self, user_input=None) -> RepairsFlowResult:
        return await self.async_step_confirm(user_input)

    async def async_step_confirm(self, user_input=None) -> RepairsFlowResult:
        entry = self.hass.config_entries.async_get_entry(self._entry_id)
        if entry is None:
            return self.async_abort(reason="entry_not_found")

        emitters = async_get_emitters(self.hass)
        if not emitters:
            return self.async_abort(reason="no_emitters")

        errors = {}
        if user_input is not None:
            emitter = user_input.get(CONF_INFRARED_ENTITY_ID)
            if emitter not in emitters:
                errors["base"] = "invalid_emitter"
            else:
                data = {
                    key: value
                    for key, value in entry.data.items()
                    if key not in (CONF_REMOTE_ENTITY, CONF_REMOTE_TYPE)
                }
                data[CONF_INFRARED_ENTITY_ID] = emitter
                self.hass.config_entries.async_update_entry(entry, data=data)
                if not await self.hass.config_entries.async_reload(entry.entry_id):
                    return self.async_abort(reason="reload_failed")
                return self.async_create_entry(data={})

        return self.async_show_form(
            step_id="confirm",
            data_schema=probatio.Schema(
                {
                    probatio.Required(CONF_INFRARED_ENTITY_ID): EntitySelector(
                        EntitySelectorConfig(
                            domain="infrared", include_entities=emitters
                        )
                    )
                }
            ),
            errors=errors,
            description_placeholders={"name": entry.title},
        )


async def async_create_fix_flow(
    hass: HomeAssistant, issue_id: str, data: dict[str, str | int | float | None] | None
) -> RepairsFlow:
    """Create the migration repair flow."""
    assert data is not None
    return ReselectIREmitterFlow(str(data["entry_id"]))
