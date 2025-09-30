# Naim NAC 52, 72, 82 Home Assistant Integration

A simple media player to control legacy Naim NAC preamps from Home Assistant. Since there's no direct control of these preamps, this uses a Broadlink or Tuya remote device to send the IR commands to the device.

## Installation

The preferred installation approach is via Home Assistant Community Store - aka [HACS](https://hacs.xyz/). The [repo](https://github.com/peteS-UK/naim_nac_x2) is installable as a [Custom Repo](https://hacs.xyz/docs/faq/custom_repositories) via HACS.

If you want to download the integration manually, create a new folder called naim_nac_x2 under your custom_components folder in your config folder. If the custom_components folder doesn't exist, create it first. Once created, download the files and folders from the [github repo](https://github.com/peteS-UK/naim_nac_x2/tree/main/custom_components/naim_nac_x2) into this new naim_nac_x2 folder.

Once downloaded either via HACS or manually, restart your Home Assistant server.
