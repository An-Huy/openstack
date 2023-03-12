from common.openstackclient import Authentication
from common import log

LOG = log.setup_logging(__name__)

class Openstack(object):

    def __init__(self, region):
        self.ops = Authentication(region)
        self.keystone = self.ops._keystone_client()
        self.glance = self.ops._glance_client()
        self.nova = self.ops._nova_client()
        self.neutron = self.ops._neutron_client()
        self.cinder = self.ops._cinder_client()

    def _get_all_servers(self):
        servers = []
        try:
            list_servers = self.nova.servers.list()
            for server in list_servers:
                ins_id = server._info['id']
                server_info = self._get_server_by_id(ins_id)
                servers.append(server_info)
        except Exception as e:
            LOG.error("%s" %e)
        return server_info
    
    def _get_server_by_id(self, ins_id):
        info = self.nova.servers.get(ins_id)._info
        _id = info['id']
        _name = info['name']
        _status = info['status']
        _vcpus = str(self.nova.flavors.get(info['flavor']['id']).vcpus)
        _ram = str(self.nova.flavors.get(info['flavor']['id']).ram)
        _flavor = _vcpus + 'c_' + _ram + 'g'
        _ip = info['addresses']['public1'][0]['addr']
        sevrer = {
            'id': _id,
            'name': _name,
            'status': _status,
            'flavor': _flavor,
            'ip': _ip
        }
        return sevrer
    
    def _get_flavors(self):
        flavors = []
        list_flavors = self.nova.flavors.list()
        for flavor in list_flavors:
            flavors.append(flavor)
        return flavors
    
ops = Openstack("RegionOne")
print(ops._get_all_servers())
print(ops._get_flavors())