import machine
import utime

import config


if config.WATCHDOG_ENABLE:
    print('using watchdog')
    wdt_class = machine.WDT
else:
    # fake watchdog
    class WDT:
        def feed(self):
            pass
    wdt_class = WDT

watchdog = wdt_class()  # global use instance


def sleep_s(interval: int):
    while True:
        watchdog.feed()

        if interval <= 0:
            return

        utime.sleep(1)
        interval -= 1


def retry_on_error(func):
    def looped_call(*args, **kwargs):
        n = 1
        while True:
            if n > 1:
                print(f'Attempt #{n}')
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if n > 50:
                    raise e
                print(f'Function {str(func)} failed {n} times')
                sleep_s(n)
                n += 1

    return looped_call


@retry_on_error
def sync_time():
    """
    Synchronize local time with NTP server
    """
    import ntptime

    print(f'begin clock synchronization using {config.NTP_SERVER}')
    ntptime.host = config.NTP_SERVER

    t = ntptime.time()
    tz_sec = config.TIME_ZONE * 60 * 60
    tm = utime.localtime(t + tz_sec)
    tm = tm[0:3] + (0,) + tm[3:6] + (0,)
    machine.RTC().datetime(tm)
    print('clock is synchronized')
