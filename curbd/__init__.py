from curbd.curbd import Curbd
import consul
from boto import cloudformation

def new_curbd(options):
    cf_conn = cloudformation.connect_to_region(options.region)
    consul_conn = consul.Consul(options.host, options.port)
    return Curbd(cf_conn, consul_conn, options)
