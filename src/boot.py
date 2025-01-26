# This file is executed on every boot (including wake-boot from deep sleep)
import config

import esp
esp.osdebug(None)

# import uos
# uos.dupterm(None, 1)  # disable REPL on UART(0)

import machine
RCS = ('PWRON_RESET', 'WDT_RESET', 'UNK2', 'UNK3', 'SOFT_RESET', 'DEEPSLEEP_RESET', 'HARD_RESET')
rc = machine.reset_cause()
print('\nReset cause:', RCS[rc])

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
    for n in range(5, -1, -1):
        print(f'start in {n}s')
        utime.sleep(1)
except OSError:
    from machine import soft_reset
    soft_reset()

import gc
gc.collect()
