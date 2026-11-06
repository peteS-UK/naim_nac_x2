# Naim NAC 52, 72, 82 Home Assistant Integration

A simple media player to control legacy Naim NAC preamps from Home Assistant. Since there's no direct control of these preamps, it sends RC5 commands through a Home Assistant Infrared emitter.

Set up a compatible infrared emitter in Home Assistant before adding the integration, then select that emitter and the six input labels during setup. The default labels are Phono, Tuner, CD, Tape, VCR and AUX; they can be changed to match your preamp. The preamp provides no feedback, so source, mute and balance status cannot be verified.

Use **Configure** on the integration to change the emitter or input labels; input labels must be distinct. Existing configurations retain their labels until changed. The last source selected through Home Assistant is restored after a restart as an assumed state, and may be incorrect if the physical remote or preamp controls were used.

Use the balance left and right buttons, or the `naim_nac_x2.send_command` action with `balance_left` or `balance_right`, to adjust balance. These commands are based on a published Naim preamplifier code list and have not yet been verified on every supported model.

Mute is a toggle: the preamp does not report its mute state, and the media player always reports it as unmuted. Every media player mute or unmute request sends the same toggle command, so repeated requests can produce the opposite of the requested state. Use the `mute` command in the `naim_nac_x2.send_command` action when an explicit toggle is needed.

Existing installations using a Broadlink or Tuya remote must configure an infrared emitter and complete the **Select an infrared emitter** repair. The repair preserves the preamp name, input labels, and entity identity. Until it is completed, the media player is unavailable and cannot send commands.

## Installation

The preferred installation approach is via Home Assistant Community Store - aka [HACS](https://hacs.xyz/). The [repo](https://github.com/peteS-UK/naim_nac_x2) is installable as a [Custom Repo](https://hacs.xyz/docs/faq/custom_repositories) via HACS.

If you want to download the integration manually, create a new folder called naim_nac_x2 under your custom_components folder in your config folder. If the custom_components folder doesn't exist, create it first. Once created, download the files and folders from the [github repo](https://github.com/peteS-UK/naim_nac_x2/tree/main/custom_components/naim_nac_x2) into this new naim_nac_x2 folder.

Once downloaded either via HACS or manually, restart your Home Assistant server.
