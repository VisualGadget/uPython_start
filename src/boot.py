# This file is executed on every boot (including wake-boot from deep sleep)

import config

# Logging
import esp
esp.osdebug(None)

import os
# os.dupterm(None, 1)  # disable REPL on UART(0)

if getattr(config, 'FILE_LOGGER', False):
    from io import IOBase

    class FileLogger(IOBase):

        NEW_LINE_CODE = ord('\n')

        def __init__(self):
            super().__init__()

            self._f = open('device.log', 'a')

        def write(self, data):
            nb = self._f.write(data)
            if nb and data[-1] == self.NEW_LINE_CODE:
                self._f.flush()

            return nb

        def readinto(self, b: bytearray):
            return None

    os.dupterm(FileLogger(), 1)  # replace REPL on UART(0)


import machine
RCS = ('PWRON_RESET', 'WDT_RESET', 'UNK2', 'UNK3', 'SOFT_RESET', 'DEEPSLEEP_RESET', 'HARD_RESET')
rc = machine.reset_cause()
print('\nReset cause:', RCS[rc])


# Wi-Fi
if config.WIFI_AT_BOOT or config.WEB_REPL_AT_BOOT:
    import wifi
    led_pin = getattr(config, 'PIN_WIFI_LED', None)
    if led_pin is not None:
        from machine import Pin, Signal
        status_led = Signal(led_pin, Pin.OUT, invert=True)
        status_led.off()
    else:
        status_led = None

    wf = wifi.WiFi(status_led=status_led)
    if not wf.connected:
        wf.connect()
        wf.wait_for_connection()

    if config.WEB_REPL_AT_BOOT:
        import webrepl
        webrepl.start(password=config.WEB_REPL_PASSWORD)


# break potential boot loop by giving time to connect and fix
import utime
try:
    for n in range(10, -1, -1):
        print(f'start in {n}s')
        utime.sleep(1)
except OSError:
    from machine import soft_reset
    soft_reset()


import gc
gc.collect()
