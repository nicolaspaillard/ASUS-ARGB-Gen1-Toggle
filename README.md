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

- To run the compiled executable: no additional Python packages are required — use the bundled `Asus ARGB Toggler.exe`.
- If you prefer to run from source, install the runtime dependency:

```bash
pip install hidapi
```

On Windows, the `pip` step is only necessary when running the `.py` source directly.

## Usage

Run the compiled executable from the project folder (or from the installed location):

```powershell
'.\Asus ARGB Toggler.exe'
```

This defaults to scanning for ASUS ARGB HID devices, switching them to Gen1 mode, and forcing a static red state so OpenRGB can take over.

### Command line arguments

```powershell
'.\Asus ARGB Toggler.exe' --add-startup
'.\Asus ARGB Toggler.exe' --remove-startup
```

- `--add-startup`: adds a shortcut to Windows Startup so the script runs automatically at login.
- `--remove-startup`: removes the Startup shortcut created by the script.

If you run the script with no arguments, it performs the hardware toggle immediately. The script needs to be run on each startup because the controller resets to rainbow on reboot.

## Included Wireshark dumps

This project includes captured USB traffic in the `pcap/` and `pcap/pcapng/` folders. These Wireshark captures document the ASUS ARGB control sequences used to switch protocol modes and force a static red state.

## Notes

- Tested on a TUF 7690 Plus, Z790 should work too, sent bytes are the same.
- This is an experimental hardware-control utility.
- Some systems may require the controller to be in gen1 static state before OpenRGB can fully control it.
- If the board does not respond, the script may need to be rerun after restarting OpenRGB or after closing ASUS software such as Armoury Crate / Aura.

## Safety

This script writes raw HID packets to ASUS vendor devices. It can change the lighting mode on the controller. Use it only if you understand the device and are comfortable with low-level hardware control.

## Typical workflow

1. Close ASUS RGB software (Armoury Crate / Aura) if it is running.
2. Run the compiled executable:
   ```powershell
   .\Asus ARGB Toggler.exe
   ```
3. Start OpenRGB.
4. Detect and control the motherboard lighting through OpenRGB.

## Disclaimer

This project is intended for use with OpenRGB and is not an official ASUS or OpenRGB tool. It is provided as-is for enthusiasts and hardware tinkering.
