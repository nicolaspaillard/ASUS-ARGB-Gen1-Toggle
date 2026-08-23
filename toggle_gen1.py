#!/usr/bin/env python3
import sys
import time
import hid


def send(dev, data_bytes):
    # All packets are padded with 00
    dev.write(bytes(data_bytes) + b"\x00" * (65 - len(data_bytes)))


def set_gen1(dev):
    # Packet 1: "begin transaction" - opens the mode-switch sequence.
    # ec=report id, 3f=sub-command family, aa=begin-transaction opcode.
    send(dev, [0xEC, 0x3F, 0xAA])
    time.sleep(0.01)
    # Packet 2: "set protocol" - the actual mode-set command.
    # ec=report id, 3e=set-protocol opcode, 52 53="magic"/auth bytes
    send(dev, [0xEC, 0x3E, 0x52, 0x53])
    time.sleep(0.01)
    # Packet 3: "commit" - finalizes/applies the transaction.
    # ec=report id, 3f=same sub-command family as packet 1, 55=commit opcode.
    send(dev, [0xEC, 0x3F, 0x55])
    time.sleep(0.01)


def set_gen2(dev):
    # Packet 1: "begin transaction" - opens the mode-switch sequence.
    # ec=report id, 3f=sub-command family, aa=begin-transaction opcode.
    send(dev, [0xEC, 0x3F, 0xAA])
    time.sleep(0.01)
    # Packet 2: "set protocol" - the actual mode-set command.
    # ec=report id, 3e=set-protocol opcode, 52 53="magic"/auth bytes, 01=each header
    send(dev, [0xEC, 0x3E, 0x52, 0x53, 0x01, 0x01, 0x01])
    time.sleep(0.01)
    # Packet 3: "commit" - finalizes/applies the transaction.
    # ec=report id, 3f=same sub-command family as packet 1, 55=commit opcode.
    send(dev, [0xEC, 0x3F, 0x55])
    time.sleep(0.01)


def set_rainbow(dev):
    for h in range(3):
        # ec=report id, 35=SendEffect opcode, h=header/channel index, 00=unused (always zero), 05=mode (AURA_MODE_RAINBOW), next 3=r g b (unused in rainbow mode)
        send(dev, [0xEC, 0x35, h, 0x00, 0x05])
        time.sleep(0.01)


def set_static(dev, num_headers=10):
    for h in range(num_headers):
        # ec=report id, 35=SendEffect opcode, h=header/channel index, 00=unused (always zero), 00=mode (OFF), ff=red (green and blue omitted=00)
        send(dev, [0xEC, 0x35, h, 0x00, 0x00, 0xFF])
        time.sleep(0.01)
        # ec=report id, 40=AURA_CONTROL_MODE_DIRECT, 80 | h=top bit (0x80): "apply/render now" - low bits (h): header/channel index
        # 00=starting LED offset, 20=LED count (max 20: header 5 B + 20*3 B colors = 65 B), FF1900 * 20=LEDs orange color code
        send(dev, [0xEC, 0x40, 0x80 | h, 0x00, 20] + [0xFF, 0x19, 0x00] * 20)
        time.sleep(0.01)


def main():
    # 0x0B05 = ASUS vendor ID
    for controller in hid.enumerate(0x0B05):
        device = hid.device()
        try:
            device.open_path(controller["path"])
        except OSError as e:
            print(f"Open error: {e}")
        try:
            set_gen1(device)
            # static mode so OpenRGB can take over
            set_static(device)
        finally:
            device.close()


if __name__ == "__main__":
    main()
