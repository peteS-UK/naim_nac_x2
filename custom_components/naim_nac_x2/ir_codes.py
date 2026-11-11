"""RC5 commands for Naim NAC preamplifiers."""

from .codes.naim.gen1_preamp import NaimGen1PreampCode as Code

COMMANDS = {
    "vol+": Code.VOLUME_UP.to_command(repeat_count=1),
    "vol-": Code.VOLUME_DOWN.to_command(repeat_count=1),
    "mute": Code.MUTE.to_command(repeat_count=1),
    "balance_left": Code.BALANCE_LEFT.to_command(repeat_count=1),
    "balance_right": Code.BALANCE_RIGHT.to_command(repeat_count=1),
    "one": Code.INPUT_1.to_command(repeat_count=1),
    "two": Code.INPUT_2.to_command(repeat_count=1),
    "three": Code.INPUT_3.to_command(repeat_count=1),
    "four": Code.INPUT_4.to_command(repeat_count=1),
    "five": Code.INPUT_5.to_command(repeat_count=1),
    "six": Code.INPUT_6.to_command(repeat_count=1),
}
