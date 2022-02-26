""
import time
from threading import Thread

import psutil as psutil
from zeroconf import Zeroconf, ServiceBrowser

from api import WledApi
from discovery import WledDiscovery
from led_updater import WledChart
from led_updater_v2 import WledChartV2
from settings_frame import SettingsFrame


class WledWorker(Thread):

    def __init__(self, notify_window, settings_frame: SettingsFrame):
        Thread.__init__(self, daemon=True)
        self._notify_window = notify_window
        self.settings_frame = settings_frame
        self.api = None
        self.stop = False

    def run(self):
        zeroconf = None
        # TODO требуется перезапуск при смене ip адреса. Переделать, шоб заного инициализировалось
        if (self.settings_frame.settings.ip_auto):
            zeroconf = self.__init_discovery()
        else:
            self.setup_api(WledApi(self.settings_frame.settings.ip, 80))
            ip, port = self.settings_frame.settings.ip, 80
            while not WledApi.is_online(ip, port) or not self.ready():
                self.settings_frame.set_status('Wait wled service...')
                ip, port = self.settings_frame.settings.ip, 80
                time.sleep(1)


        while not self.ready():
            self.settings_frame.set_status('Wait wled service...')
            time.sleep(1)
        self.settings_frame.set_hiperlink(self.api.ip, self.api.port)
        self.settings_frame.set_status('Connected')
        cpu_led = WledChartV2(self.api,
                              segment_id=0,
                              width_x=self.settings_frame.settings.segment_y,
                              width_y=self.settings_frame.settings.segment_x,
                              is_zigzag=self.settings_frame.settings.is_zig_zag)
        mem_led = WledChartV2(self.api,
                              segment_id=1,
                              width_x=self.settings_frame.settings.segment_y,
                              width_y=self.settings_frame.settings.segment_x,
                              is_zigzag=self.settings_frame.settings.is_zig_zag)
        # cpu_led = WledChart(self.api, segment_id=0, x=self.settings_frame.settings.segment_x, y=self.settings_frame.settings.segment_y)
        # mem_led = WledChart(self.api, segment_id=1, x=self.settings_frame.settings.segment_x, y=self.settings_frame.settings.segment_y)

        cpu_led.clear()
        mem_led.clear()

        while True and not self.stop:
            if not self.settings_frame.settings.on:
                time.sleep(2)
                continue
            cpu = psutil.cpu_percent() / 100
            mem = psutil.virtual_memory().percent / 100  # TODO multiple sysinfos
            # print('cpu: {}, mem: {}'.format(cpu, mem))
            cpu_led.update_leds(percent=cpu, color=self.settings_frame.settings.proc_color)
            mem_led.update_leds(percent=mem, color=self.settings_frame.settings.mem_color)
            time.sleep(self.settings_frame.settings.refresh_speed)

        if zeroconf:
            zeroconf.close()

    def close(self):
        self.stop = True

    def ready(self) -> bool:
        return self.api is not None

    def setup_api(self, api: WledApi):
        self.api = api

    def __init_discovery(self):
        zeroconf = Zeroconf()
        listener = WledDiscovery(self)
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
        return zeroconf
