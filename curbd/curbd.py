import json
import os


class Curbd(object):
    ENVIRONMENTS = ['stage', 'prod']

    def __init__(self, service, options):
        self.service = service
        key_prefix = options.key_prefix.strip('/')
        self.path = os.path.normpath(
            "../curbd-config/" + key_prefix + "/" + options.config +
            ".json")

        split = key_prefix.split('/', 1)
        if len(split) == 1:
            prefix = key_prefix
            postfix = options.config + "/"
        else:
            prefix = split[0]
            postfix = split[1] + "/" + options.config + "/"

        # Here we strip out the environment if its part of the prefix
        # since each env will have a consul cluster we don't want it included.
        if prefix in Curbd.ENVIRONMENTS:
            self.key_prefix = postfix
        else:
            self.key_prefix = prefix + "/" + postfix

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
