from curbd.curbd import Curbd
from curbd.curbd import CurbdService
from consul import Consul


def new_curbd(options):
    consul_conn = Consul(options.host, options.port)
    service = CurbdService(consul_conn)
    return Curbd(service, options)
