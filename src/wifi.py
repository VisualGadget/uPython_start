import asyncio
from machine import Pin
import network
import time
import ubinascii

import config


class WiFi():
    # Wi-Fi network adapter management

    def __init__(self, status_led: Pin | None = None):
        self._led = status_led

        # disable access point
        ap = network.WLAN(network.AP_IF)
        ap.active(False)

        self._nic = network.WLAN(network.STA_IF)
        self._nic.active(True)
        network.hostname(f'upython-{self.mac[-4:]}')

    @property
    def connected(self) -> bool:
        return self._nic.isconnected()

    @property
    def mac(self) -> str:
        # WiFi interface MAC
        return ubinascii.hexlify(self._nic.config('mac')).decode()

    def connect(self):
        # Start background connection to WiFI AP
        assert not self.connected

        print('Connecting to WiFi')
        self._nic.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    def wait_for_connection(self):
        while not self.connected:
            if self._led is not None:
                self._led.value(not self._led.value())

            time.sleep(0.3)

        if self._led is not None:
            self._led.off()

        self.print_network_configuration()

    async def wait_for_connection_async(self):
        while not self.connected:
            if self._led is not None:
                self._led.value(not self._led.value())

            await asyncio.sleep(0.3)

        if self._led is not None:
            self._led.off()

        self.print_network_configuration()

    def print_network_configuration(self):
        if_cfg = dict(zip(
            ('IP', 'subnet', 'gateway', 'DNS'),
            self._nic.ifconfig()
        ))
        print(f'Network config: {if_cfg}')
