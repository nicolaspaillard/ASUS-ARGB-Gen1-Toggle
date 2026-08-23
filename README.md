# ASUS ARGB Gen1 Toggle for OpenRGB

This utility switches ASUS ARGB controllers into Gen1 mode so OpenRGB can control the lighting.

It targets ASUS HID devices (`vendor ID 0x0B05`) and sends the mode-switch packets used by ASUS motherboard RGB controllers. The script then forces a static red state so the motherboard stops reporting a proprietary effect and OpenRGB can take over.

## Why this exists

Some ASUS motherboards expose multiple ARGB protocol modes. OpenRGB works best when the controller is in Gen1 mode. This script sends the required USB HID commands to switch the controller into Gen1 mode before OpenRGB connects.

## Requirements

- Python 3.9+
- `hidapi` Python package
- An ASUS motherboard/controller that exposes an ARGB HID interface
- OpenRGB installed and running

## Install

```bash
pip install hidapi
```

On Windows, this typically works with the standard Python installation used for the script.

## Usage

From the project folder:

```bash
python toggle_gen1.py
```

Then launch OpenRGB and connect to the motherboard/controller.
The script needs to be ran on each startup because the controller resets to rainbow on reboot.

## Notes

- This is an experimental hardware-control utility.
- Some systems may require the controller to be in gen1 static state before OpenRGB can fully control it.
- If the board does not respond, the script may need to be rerun after restarting OpenRGB or after closing ASUS software such as Armoury Crate / Aura.

## Safety

This script writes raw HID packets to ASUS vendor devices. It can change the lighting mode on the controller. Use it only if you understand the device and are comfortable with low-level hardware control.

## Typical workflow

1. Close ASUS RGB software (Armoury Crate / Aura) if it is running.
2. Run the script:
   ```bash
   python toggle_gen1.py
   ```
3. Start OpenRGB.
4. Detect and control the motherboard lighting through OpenRGB.

## Disclaimer

This project is intended for use with OpenRGB and is not an official ASUS or OpenRGB tool. It is provided as-is for enthusiasts and hardware tinkering.
