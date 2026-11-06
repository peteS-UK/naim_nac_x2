import homeassistant.helpers.config_validation as cv
import probatio
from homeassistant import config_entries, core
from homeassistant.components.infrared import async_get_emitters
from homeassistant.const import CONF_NAME
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_INFRARED_ENTITY_ID,
    CONF_INPUT1,
    CONF_INPUT2,
    CONF_INPUT3,
    CONF_INPUT4,
    CONF_INPUT5,
    CONF_INPUT6,
    DOMAIN,
)

INPUT_KEYS = (
    CONF_INPUT1,
    CONF_INPUT2,
    CONF_INPUT3,
    CONF_INPUT4,
    CONF_INPUT5,
    CONF_INPUT6,
)


def config_schema(emitters: list[str], include_name: bool = True) -> probatio.Schema:
    """Build the setup schema for the available infrared emitters."""
    fields = {
        probatio.Required(CONF_INFRARED_ENTITY_ID): EntitySelector(
            EntitySelectorConfig(domain="infrared", include_entities=emitters)
        ),
        probatio.Required(CONF_INPUT1, default="Phono"): SelectSelector(
            SelectSelectorConfig(
                multiple=False,
                options=["Phono", "CD", "Tuner", "Tape", "VCR", "AUX"],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        probatio.Required(CONF_INPUT2, default="Tuner"): SelectSelector(
            SelectSelectorConfig(
                multiple=False,
                options=["Phono", "CD", "Tuner", "Tape", "VCR", "AUX"],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        probatio.Required(CONF_INPUT3, default="CD"): SelectSelector(
            SelectSelectorConfig(
                multiple=False,
                options=["Phono", "CD", "Tuner", "Tape", "VCR", "AUX"],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        probatio.Required(CONF_INPUT4, default="Tape"): SelectSelector(
            SelectSelectorConfig(
                multiple=False,
                options=["Phono", "CD", "Tuner", "Tape", "VCR", "AUX"],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        probatio.Required(CONF_INPUT5, default="VCR"): SelectSelector(
            SelectSelectorConfig(
                multiple=False,
                options=["Phono", "CD", "Tuner", "Tape", "VCR", "AUX"],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
        probatio.Required(CONF_INPUT6, default="AUX"): SelectSelector(
            SelectSelectorConfig(
                multiple=False,
                options=["Phono", "CD", "Tuner", "Tape", "VCR", "AUX"],
                mode=SelectSelectorMode.DROPDOWN,
            )
        ),
    }
    if include_name:
        fields = {probatio.Required(CONF_NAME): cv.string, **fields}
    return probatio.Schema(fields)


def validate_selection(data: dict, emitters: list[str]) -> str | None:
    """Validate emitter and distinct input labels."""
    if data.get(CONF_INFRARED_ENTITY_ID) not in emitters:
        return "invalid_emitter"
    labels = [data[key] for key in INPUT_KEYS]
    if len(set(labels)) != len(labels):
        return "duplicate_inputs"
    return None


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    @staticmethod
    @core.callback
    def async_get_options_flow(config_entry):
        return NacOptionsFlow()

    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface."""
        emitters = async_get_emitters(self.hass)
        if not emitters:
            return self.async_abort(reason="no_emitters")

        errors: dict[str, str] = {}
        if user_input is not None:
            if not user_input.get(CONF_NAME, "").strip():
                errors["base"] = "data"
            elif error := validate_selection(user_input, emitters):
                errors["base"] = error

            if not errors:
                return self.async_create_entry(title="Naim NAC", data=user_input)

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=config_schema(emitters), errors=errors
        )


class NacOptionsFlow(config_entries.OptionsFlowWithReload):
    """Change the emitter and input labels without recreating the entry."""

    async def async_step_init(self, user_input=None):
        entry = self.config_entry
        if not entry.data.get(CONF_INFRARED_ENTITY_ID):
            return self.async_abort(reason="migration_required")
        emitters = async_get_emitters(self.hass)
        if not emitters:
            return self.async_abort(reason="no_emitters")
        errors = {}
        if user_input is not None:
            if error := validate_selection(user_input, emitters):
                errors["base"] = error
            else:
                return self.async_create_entry(title="", data=user_input)
        current = user_input or {**entry.data, **entry.options}
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                config_schema(emitters, include_name=False), current
            ),
            errors=errors,
        )
