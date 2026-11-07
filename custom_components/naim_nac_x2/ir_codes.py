"""RC5 commands for Naim NAC preamplifiers."""

from infrared_protocols.commands.rc5 import RC5Command

PREAMP_ADDRESS = 0x10

COMMANDS = {
    "vol+": RC5Command(address=PREAMP_ADDRESS, command=0x10, repeat_count=1),
    "vol-": RC5Command(address=PREAMP_ADDRESS, command=0x11, repeat_count=1),
    "mute": RC5Command(address=PREAMP_ADDRESS, command=0x0D, repeat_count=1),
    "balance_left": RC5Command(address=PREAMP_ADDRESS, command=0x1B, repeat_count=1),
    "balance_right": RC5Command(address=PREAMP_ADDRESS, command=0x1A, repeat_count=1),
    "one": RC5Command(address=PREAMP_ADDRESS, command=0x12, repeat_count=1),
    "two": RC5Command(address=PREAMP_ADDRESS, command=0x13, repeat_count=1),
    "three": RC5Command(address=PREAMP_ADDRESS, command=0x14, repeat_count=1),
    "four": RC5Command(address=PREAMP_ADDRESS, command=0x15, repeat_count=1),
    "five": RC5Command(address=PREAMP_ADDRESS, command=0x16, repeat_count=1),
    "six": RC5Command(address=PREAMP_ADDRESS, command=0x17, repeat_count=1),
}
