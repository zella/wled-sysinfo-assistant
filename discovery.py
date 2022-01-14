from api import WledApi


class WledDiscovery:

    def __init__(self, worker):
        self.worker = worker

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name))

    def update_service(self, zeroconf, type, name):
        print("Service %s updated" % (name))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        ip = info.parsed_addresses()[0]
        port = info.port
        print("Service found on {}:{}".format(ip, port))
        print("Check wled api availability...")
        is_online = WledApi.is_online(ip, port)
        print("Online: {}".format(is_online))
        if is_online:
            self.worker.setup_api(WledApi(ip, port))
