import network
import time
import ubinascii

import config


def wifi_mac(nic: network.WLAN = None) -> str:
    # """
    # WiFi MAC
    # """
    if nic is None:
        nic = network.WLAN()

    return ubinascii.hexlify(nic.config('mac')).decode()


def connect():
    # disable access point
    ap = network.WLAN(network.AP_IF)
    ap.active(False)

    nic = network.WLAN(network.STA_IF)
    mac = wifi_mac(nic)
    network.hostname(f'uPython {mac[-4:]}')

    if not nic.isconnected():
        print('Connecting to WiFi', end='')
        nic.active(True)
        nic.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

        while not nic.isconnected():
            time.sleep(1)
            print('.', end='')

    if_cfg = dict(zip(
        ('IP', 'subnet', 'gateway', 'DNS'),
        nic.ifconfig()
    ))
    print(f'\nNetwork config: {if_cfg}')
