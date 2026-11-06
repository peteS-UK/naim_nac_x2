"""Constants for the Naim NAC integration."""

DOMAIN = "naim_nac_x2"
DEFAULT_NAME = "Naim NAC"
SERVICE_SEND_COMMAND = "send_command"
CONF_INFRARED_ENTITY_ID = "infrared_entity_id"
CONF_REMOTE_ENTITY = "remote_entity"
CONF_REMOTE_TYPE = "remote_type"
CONF_INPUT1 = "input1"
CONF_INPUT2 = "input2"
CONF_INPUT3 = "input3"
CONF_INPUT4 = "input4"
CONF_INPUT5 = "input5"
CONF_INPUT6 = "input6"
MANUFACTURER = "Naim"
MODEL = "NAC"


def device_unique_id(name: str) -> str:
    """Keep the original name-based identifier for existing devices."""
    return f"{DOMAIN}_" + name.replace(" ", "_").replace("-", "_").replace(":", "_")
