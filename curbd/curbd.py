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
        with open("../curbd/" + program + "/" + self.service + ".json") as f:
            for k, v in json.load(f).items():
                print(k, v)
                self.consul_conn.kv.put(program + "/" + self.service + "/" + k,
                                        v)

    def from_cf(self):
        key_prefix = self.service + "/" if self.service != 'env' else ""
        for o in self.cf_conn.describe_stacks(self.env + "-" + self.service)[0].outputs:
            key = convert(o.key)
            print(key, o.value)
            self.consul_conn.kv.put(key_prefix + key, o.value)


def convert(key):
    """
    Used to convert cf CamelCase keys to underscores
    :param key: key to convert
    :return: key converted from CamelCase to underscores.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
