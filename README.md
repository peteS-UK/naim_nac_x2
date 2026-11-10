# Naim NAC 52, 72, 82 Home Assistant Integration

[![Available in Marketplace](https://img.shields.io/badge/Marketplace-Available-41BDF5)](#installation-with-marketplace)
[![maintained](https://img.shields.io/maintenance/yes/2026.svg)](#)
[![maintainer](https://img.shields.io/badge/maintainer-%20%40petes--UK-blue.svg)](#)
[![version](https://img.shields.io/github/v/release/peteS-UK/naim_nac_x2)](#)

A simple media player to control legacy Naim NAC preamps from Home Assistant. Since there's no direct control of these preamps, it sends RC5 commands through a Home Assistant Infrared emitter.

Set up a compatible infrared emitter in Home Assistant before adding the integration, then select that emitter and the six input labels during setup. The default labels are Phono, Tuner, CD, Tape, VCR and AUX; they can be changed to match your preamp. The preamp provides no feedback, so source, mute and balance status cannot be verified.

Use **Configure** on the integration to change the emitter or input labels; input labels must be distinct. Existing configurations retain their labels until changed. The last source selected through Home Assistant is restored after a restart as an assumed state, and may be incorrect if the physical remote or preamp controls were used.

Use the balance left and right buttons, or the `naim_nac_x2.send_command` action with `balance_left` or `balance_right`, to adjust balance. These commands are based on a published Naim preamplifier code list and have not yet been verified on every supported model.

Mute is a toggle: the preamp does not report its mute state, and the media player always reports it as unmuted. Every media player mute or unmute request sends the same toggle command, so repeated requests can produce the opposite of the requested state. Use the `mute` command in the `naim_nac_x2.send_command` action when an explicit toggle is needed.

Existing installations using a Broadlink or Tuya remote must configure an infrared emitter and complete the **Select an infrared emitter** repair. The repair preserves the preamp name, input labels, and entity identity. Until it is completed, the media player is unavailable and cannot send commands.

## Installation with Marketplace

The [Marketplace](https://www.home-assistant.io/integrations/marketplace/) is built into **Home Assistant 2026.11 and later**; no separate store installation is needed.

1. As an administrator, open **Settings → Marketplace** and accept its first-use notice if prompted.
2. Search for **Naim NAC** and open its page.
3. Choose **Install**, review the version, then confirm **Install**. Account setup opens when installation finishes; continue with [Configuration](#configuration). A fresh installation does not need a restart.

Existing HACS installations migrate automatically when you upgrade Home Assistant to 2026.11. Your installed integration and updates carry over; you do not need to reinstall it.

## Installation with HACS

For older versions of Home Assistant, you can install via Home Assistant Community Store - aka [HACS](https://hacs.xyz/).  Search for **Naim NAC** and install the integration.

## Manual Installation
If you want to download the integration manually, create a new folder called naim_nac_x2 under your custom_components folder in your config folder.  If the custom_components folder doesn't exist, create it first.  Once created, download the files and folders from the [github repo](https://github.com/peteS-UK/naim_nac_x2/tree/main/custom_components/naim_nac_x2) into this new naim_nac_x2 folder.

Once downloaded either via HACS or manually, restart your Home Assistant server.

## Configuration

Configuration is done through the Home Assistant UI.  If the configuration page isn't displayed automatically, for example after a Marketplace installation, once you're installed the integration go into your Integrations (under Settings, Devices & Services), select Add Integration, and choose the NAIM NAC integration, or click the shortcut button below (requires My Homeassistant configured).

[![Add Integration to your Home Assistant
instance.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=naim_nac_x2)

This will display the configuration page

<img width="727" height="1005" alt="image" src="https://github.com/user-attachments/assets/f937a3b5-8c61-410c-bbac-1e2766ba805d" />

