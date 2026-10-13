# USB-SERIAL

When you plug an FTDI USB-to-serial adapter into a MUSE controller, MUSE adds
the `USB-SERIAL` device but leaves it offline. This program shows how you can bring it online.

## Enable USB-SERIAL

1. Plug in the adapter, then load this program.
2. Using VSCode eval `force_online()`. When the device comes online, the `handle_online()` is called and sets the USB-SERIAL to
   9600 8N1.

To check the device, eval `status()`. To send data, eval `send("test\r\n")`.
Received data logs as `RX`.

Unplugging the adapter takes the device offline again.
