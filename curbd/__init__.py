from curbd.curbd import CurbdJson
from curbd.curbd import CurbdCf
from boto import cloudformation
import consul


def new_curbd(options):
    consul_conn = consul.Consul(options.host, options.port)
    if options.subcommand == 'from_json':
        return CurbdJson(consul_conn, options)
    if options.subcommand == 'from_cf':
        cf_conn = None
        if options.environment != 'mock':
            cf_conn = cloudformation.connect_to_region(options.region)
        return CurbdCf(cf_conn, consul_conn, options)
    raise BaseException('No valid Curbd impl for the subcommand')
