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

# break potential boot loop by giving time to connect and fix
import utime
for n in range(2, -1, -1):
	print(f'start in {n}s')
	utime.sleep(1)

if config.WIFI_AT_BOOT or config.WEB_REPL_AT_BOOT:
    import wifi
    wf = wifi.WiFi()
    wf.connect()
    wf.wait_for_connection()

if config.WEB_REPL_AT_BOOT:
    import webrepl
    webrepl.start(password=config.WEB_REPL_PASSWORD)

import gc
gc.collect()
