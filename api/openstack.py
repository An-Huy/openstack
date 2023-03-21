from common.openstackclient import Authentication
from common import log
import time

LOG = log.setup_logging(__name__)

class Openstack(object):

    def __init__(self, region):
        self.ops = Authentication(region)
        self.keystone = self.ops._keystone_client()
        self.glance = self.ops._glance_client()
        self.nova = self.ops._nova_client()
        self.neutron = self.ops._neutron_client()
        self.cinder = self.ops._cinder_client()

    def _get_all_servers(self, page: int = 1, limit: int = 5):
        try:
            servers = self.nova.servers.list(search_opts={'all_tenants': 1, 'availability_zone': 'nova'}, limit=limit + 1)
            offset = (page - 1) * limit
            server_infos = []
            while offset < len(servers) and len(server_infos) < limit:
                server_info = self._get_server_by_id(servers[offset]._info['id'])
                server_infos.append(server_info)
                offset += 1
            return server_infos
        except Exception as e:
            LOG.error("Failed to get instances info: %s" % e)
    
    def _get_server_by_id(self, ins_id):
        try: 
            info = self.nova.servers.get(ins_id)._info
            _id = info['id']
            _name = info['name']
            _status = info['status']
            _flavor = self.nova.flavors.get(info['flavor']['id']).name
            server_network = ""

            for key in info["addresses"].keys():
                server_network = key +": " + info["addresses"][key][0]["addr"] +" , "+ server_network
                _ip = info["addresses"][key][0]["addr"]
                sevrer = {
                    'id': _id,
                    'name': _name,
                    'status': _status,
                    'flavor': _flavor,
                    'ip': _ip
                }
            return sevrer
        except Exception as e:
            LOG.error('Failed to get instance info: %s' %e)
    
    def _get_images(self):
        images = {}
        list_images = self.glance.images.list(search_opts={'all_tenants': 1, 'availability_zone': 'nova'})
        for image in list_images:
            images[image['id']] = str(image['name']) 
        return images
    
    def _get_flavors(self):
        flavors = {}
        list_flavors = self.nova.flavors.list()
        for flavor in list_flavors:
            flavors[flavor.id] = str(flavor.name)
        return flavors
   
    def _get_networks(self):
        networks = {}
        subnets = self.neutron.list_subnets()['subnets']
        for subnet in subnets:          
            networks[subnet['network_id']] = str(subnet['cidr']) 
        return networks
    
    def _create_server(self, name, image, flavor , network):
        server = self.nova.servers.create(name=name, image=image, flavor=flavor, nics=[{'net-id': network}])
        while True:
            info = self.nova.servers.get(server.id)
            if info.status == 'ACTIVE':
                break
            elif info.status == 'ERROR':
                raise Exception("Server creation failed")
            time.sleep(5)
        server_info = self._get_server_by_id(server.id)
        return server_info
    
    def _resize_server(self, ins_id, flavor):
        server = self.nova.servers.resize(ins_id, flavor)
        while True:
            info = self.nova.servers.get(server.id)
            if info.status == 'ACTIVE':
                raise Exception("Resize successfully")
            elif info.status == 'ERROR':
                raise Exception("Resize failed")
            time.sleep(5)
        server_info = self._get_server_by_id(server.id)
        return server_info

    def _start_server(self, ins_id):
        return self.nova.servers.start(ins_id)
    
    def _stop_server(self, ins_id):
        return self.nova.servers.stop(ins_id)
    
    # Func to delete server, use with caution
    def _delete_server(self, ins_id):
        return self.nova.servers.delete(ins_id)