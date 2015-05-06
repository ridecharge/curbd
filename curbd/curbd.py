import json
import os


class Curbd(object):
    def __init__(self, service, options):
        self.service = service
        self.key_prefix = options.program + "/" + options.config + "/"
        self.path = os.path.normpath(
            "../curbd-config/" + options.environment + "/" + options.program + "/"
            + options.config + ".json")

    def populate(self):
        self.service.populate_json(self.path, self.key_prefix)


class CurbdService():
    def __init__(self, consul_conn, dry_run=False):
        self.consul_conn = consul_conn
        self.dry_run = dry_run

    def populate_json(self, path, key_prefix):
        with open(path) as f:
            json_data = json.load(f)
            self.__populate_json(json_data, key_prefix)

    def __populate_json(self, json_data, key_prefix):
        for k, v in json_data.items():
            if isinstance(v, dict):
                self.__populate_json(v, key_prefix + k + "/")
            else:
                if isinstance(v, list):
                    v = "\n".join(v)
                print(key_prefix + k, v)
                if not self.dry_run:
                    self.consul_conn.kv.put(key_prefix + k, v)
