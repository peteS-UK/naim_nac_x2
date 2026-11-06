"""Shared RC5 transmitter for a NAC entry."""

import asyncio

from homeassistant.components.infrared import async_send_command
from homeassistant.core import Context, HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from infrared_protocols.commands.rc5 import RC5Command

from .ir_codes import COMMANDS


class NacRemote:
    """Serialize all commands and share the RC5 toggle between entities."""

    def __init__(self, hass: HomeAssistant, emitter: str | None) -> None:
        self.hass = hass
        self.emitter = emitter
        self._lock = asyncio.Lock()
        self._toggle = 1

    async def send(self, command: str, context: Context | None = None) -> None:
        command = {"volume_up": "vol+", "volume_down": "vol-"}.get(command, command)
        if command not in COMMANDS:
            raise ServiceValidationError(f"Unknown command: {command}")
        if not self.emitter:
            raise ServiceValidationError("An infrared emitter is required")
        template = COMMANDS[command]
        async with self._lock:
            self._toggle = 1 - self._toggle
            rc5_command = RC5Command(
                address=template.address,
                command=template.command,
                toggle=self._toggle,
                modulation=template.modulation,
                repeat_count=template.repeat_count,
            )
            await async_send_command(
                self.hass, self.emitter, rc5_command, context=context
            )
