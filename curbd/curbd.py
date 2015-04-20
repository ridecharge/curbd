import json
import re


class CurbdJson(object):
    def __init__(self, consul_conn, options):
        self.consul_conn = consul_conn
        self.program = options.program
        try:
            self.config_name = options.service
            self.key_prefix = self.program + "/" + self.config_name + "/"
        except AttributeError:
            self.config_name = options.environment
            self.key_prefix = self.program + "/"

        self.path = "../curbd-config/" + self.program + "/" + self.config_name + ".json"
        self.path_private = "../curbd-config-private/" + self.program + "/" + self.config_name \
                            + ".json"

    def populate(self):
        try:
            populate_json(self.consul_conn, self.path, self.key_prefix)
        except FileNotFoundError:
            populate_json(self.consul_conn, self.path_private, self.key_prefix)


class CurbdCf(object):
    def __init__(self, cf_conn, consul_conn, options):
        self.cf_conn = cf_conn
        self.consul_conn = consul_conn
        self.service_name = options.service_name
        self.env = options.environment
        self.key_prefix = "cf/" + self.service_name + "/"

    def __populate(self, ):
        for o in self.cf_conn.describe_stacks(self.env + "-" + self.service_name)[0].outputs:
            key = convert(o.key)
            print(self.key_prefix + key, o.value)
            self.consul_conn.kv.put(self.key_prefix + key, o.value)

    def populate(self):
        if self.env == 'mock':
            path = "../curbd-config/mock-cf/" + self.service_name + ".json"
            path_private = "../curbd-config-private/mock-cf/" + self.service_name + ".json"
            try:
                populate_json(self.consul_conn, path, self.key_prefix)
            except FileNotFoundError:
                populate_json(self.consul_conn, path_private, self.key_prefix)
        else:
            self.__populate()


def populate_json(consul_conn, path, key_prefix):
    with open(path) as f:
        for k, v in json.load(f).items():
            if isinstance(v, list):
                v = "\n".join(v)
            print(key_prefix + k, v)
            consul_conn.kv.put(key_prefix + k, v)


def convert(key):
    """
    Used to convert cf CamelCase keys to underscores
    :param key: key to convert
    :return: key converted from CamelCase to underscores.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', key)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
