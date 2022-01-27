import json
import os
from dataclasses import dataclass

from appdirs import *


# TODO version

@dataclass
class WledSettingsData:
    proc_color: list
    mem_color: list
    on: bool
    ip: str
    ip_auto: bool
    refresh_speed: int
    segment_x: int
    segment_y: int
    is_zig_zag: bool


class WledSettings:

    @staticmethod
    def config_file():
        dir = user_config_dir("WledController", "zella")
        return os.path.join(dir, "config.ini")

    @staticmethod
    def default_settings() -> WledSettingsData:
        return WledSettingsData(proc_color=[0, 0, 255],
                                mem_color=[0, 255, 0],
                                on=True,
                                ip='127.0.0.1',
                                ip_auto=True,
                                refresh_speed=1,
                                segment_x=4,
                                segment_y=4,
                                is_zig_zag=False)

    @staticmethod
    def load_settings() -> WledSettingsData:
        try:
            conf_file = WledSettings.config_file()
            print('Loading config {}'.format(conf_file))

            if not os.path.isfile(conf_file):
                setting = WledSettings.default_settings()
                WledSettings.save_settings(setting)

            with open(WledSettings.config_file()) as f:
                data = json.load(f)

                settings = WledSettingsData(on=data['on'],
                                            proc_color=data['proc_color'],
                                            mem_color=data['mem_color'],
                                            ip=data['ip'],
                                            ip_auto=data['ip_auto'],
                                            refresh_speed=data['refresh_speed'],
                                            segment_x=data['segment_x'],
                                            segment_y=data['segment_y'],
                                            is_zig_zag=data['is_zig_zag'])
                # validation
                if len(settings.proc_color) != 3 or len(settings.mem_color) != 3:
                    print(settings)
                    raise ValueError("- Wrong Settings")
                return settings
        except Exception as e:
            print(e)
            return WledSettings.default_settings()

    @staticmethod
    def save_settings(settings: WledSettingsData):
        data = {
            'on': settings.on,
            'proc_color': settings.proc_color,
            'mem_color': settings.mem_color,
            'ip': settings.ip,
            'ip_auto': settings.ip_auto,
            'refresh_speed': settings.refresh_speed,
            'segment_x': settings.segment_x,
            'segment_y': settings.segment_y,
            'is_zig_zag': settings.is_zig_zag
        }
        config = WledSettings.config_file()
        os.makedirs(os.path.dirname(config), exist_ok=True)
        with open(config, 'w+') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
