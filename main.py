from mojo import context
context.log.info('USB-SERIAL Example Python')

# MUSE adds the USB-SERIAL driver when you plug in the adapter, but never
# starts it, so the device stays offline. To bring it online and test it,
# EVAL these calls one at a time against the running program:
#
#   status()               log whether USB-SERIAL is online, and its settings
#   force_online()         set the driver online
#   send("test\r\n")       send a string; anything received logs as RX
#
# When the device comes online, handle_online() sets the port to 9600 8N1.
#
# To test without other equipment, connect pins 2 and 3 on the adapter's DB9
# connector. Unplugging the adapter or rebooting the MUSE undoes force_online().

context.log.info('Grab device objects')
if context.devices.has("USB-SERIAL"):
    dvUSB = context.devices.get("USB-SERIAL")
else:
    dvUSB = None
    context.log.error("USB-SERIAL is not defined. Plug in the adapter, then restart this program.")


context.log.info('Define my callbacks')
def handle_online(event):
    context.log.info("USB-SERIAL is online")
    # Match these to whatever is on the other end of the adapter:
    # baudrate, dataBits, stopBits, parity.
    dvUSB.setSerialPortParams(9600, 8, 1, "NONE")
    status()


def handle_offline(event):
    context.log.info("USB-SERIAL is offline")


def handle_received_serial(event):
    context.log.info("RX: " + repr(bytes(event.arguments['data'])))


context.log.info('Define my EVAL functions')
def status():
    if dvUSB is not None:
        context.log.info("USB-SERIAL online:" + str(dvUSB.isOnline())
                         + " baudrate:" + str(dvUSB.baudrate.value)
                         + " dataBits:" + str(dvUSB.dataBits.value)
                         + " stopBits:" + str(dvUSB.stopBits.value)
                         + " parity:" + str(dvUSB.parity.value)
                         + " flowcontrol:" + str(dvUSB.flowcontrol.value))


def force_online():
    if dvUSB is not None:
        # The device has no command to start its driver, so reach the driver
        # through the driver manager instead.
        entry = context.gateway.entry_point
        driver = entry.driverManager().driver(entry.scope(), "USB-SERIAL")
        if driver.isOnline():
            context.log.info("USB-SERIAL is already online")
        else:
            driver.online()
            context.log.info("Called online() on the USB-SERIAL driver, online:" + str(driver.isOnline()))


def send(message):
    if dvUSB is not None:
        # The send command takes a byte array, and latin-1 maps each
        # character to one byte, so you can send binary data with \x escapes.
        try:
            dvUSB.send(message.encode('latin-1'))
            context.log.info("TX: " + repr(message))
        except Exception as e:
            context.log.error("TX failed: " + repr(e))


context.log.info('Set my listeners')
if dvUSB is not None:
    dvUSB.online(handle_online)
    dvUSB.offline(handle_offline)
    dvUSB.receive.listen(handle_received_serial)

context.log.info('USB-SERIAL Example Python script loaded. EVAL status() to begin.')

# leave this as the last line in the Python script
context.run(globals())
