import json
import re


class Curbd(object):
    def __init__(self, cf_conn, consul_conn, options):
        self.cf_conn = cf_conn
        self.consul_conn = consul_conn
        self.env = options.environment
        self.service = options.service
        self.options = options

    def from_json(self):
        program = self.options.program
        key_prefix = program + "/" + self.service + "/"
        path = "../curbd/" + program + "/" + self.service + ".json"
        self.__from_json(path, key_prefix)

    def __from_json(self, path, key_prefix):
        with open(path) as f:
            for k, v in json.load(f).items():
                print(key_prefix + k, v)
                self.consul_conn.kv.put(key_prefix + k, v)

    def __from_cf(self, key_prefix):
        for o in self.cf_conn.describe_stacks(self.env + "-" + self.service)[0].outputs:
            key = convert(o.key)
            print(key_prefix + key, o.value)
            self.consul_conn.kv.put(key_prefix + key, o.value)

    def from_cf(self):
        key_prefix = "cf/" + self.service + "/"
        if self.env == 'mock':
            path = "../curbd/mock-cf/" + self.service + ".json"
            self.__from_json(path, key_prefix)
        else:
            self.__from_cf(key_prefix)


def convert(key):
    """
    Used to convert cf CamelCase keys to underscores
    :param key: key to convert
    :return: key converted from CamelCase to underscores.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
