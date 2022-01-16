import requests


class WledApi:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __url(self):
        return 'http://{}:{}'.format(self.ip, self.port)

    # https://github.com/Aircoookie/WLED/issues/1885
    def set_state(self, params):
        params.update({"v": False})
        r = requests.post('http://{}:{}/json/state'.format(self.ip, self.port), json=params, timeout=10)
        return r.status_code

    def reboot(self):
        params = ({'v': False, 'rb': True})
        r = requests.post('http://{}:{}/json/state'.format(self.ip, self.port), json=params, timeout=4)
        return r.status_code

    @staticmethod
    def is_online(ip, port):
        try:
            r = requests.get('http://{}:{}/win'.format(ip, port), timeout=10)
            code = r.status_code
            if code == 200:
                return True
            else:
                return False
        except Exception:
            return False
