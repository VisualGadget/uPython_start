# This file is executed on every boot (including wake-boot from deep sleep)
# from debug_print import print
import config

import esp
esp.osdebug(None)

# import uos
# uos.dupterm(None, 1) # disable REPL on UART(0)

import wifi
wifi.connect()

if config.WEBREPL_ENABLE:
    import webrepl
    webrepl.start(password=config.WEBREPL_PASSWORD)

# break potential bootloop by giving time to connect and fix
import utime
for n in range(2, -1, -1):
	print(f'start in {n}s')
	utime.sleep_ms(1000)

# import machine
# RCS = ('UNK1', 'WDT_RESET', 'UNK2', 'UNK3', 'SOFT_RESET', 'DEEPSLEEP_RESET', 'HARD_RESET')
# rc = machine.reset_cause()
# print('\nReset cause:', RCS[rc])

import gc
gc.collect()
