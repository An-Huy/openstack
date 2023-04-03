from common.openstackclient import Authentication
from common import log
import time

LOG = log.setup_logging(__name__)

class Openstack(object):

    def __init__(self):
        self.ops = Authentication()
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
            _lan_ip = ""
            _wan_ip = ""

            for key in info["addresses"].keys():
                server_network = key +": " + info["addresses"][key][0]["addr"] +" , "+ server_network
                if 'internal' in key:
                    _lan_ip = info["addresses"][key][0]["addr"]
                elif 'public' in key:
                    _wan_ip = info["addresses"][key][0]["addr"]
                sevrer = {
                    'id': _id,
                    'name': _name,
                    'status': _status,
                    'flavor': _flavor,
                    'lan': _lan_ip,
                    'wan': _wan_ip
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

    def _create_volume(self, name, size, image):
        volume_name = str(name) + '_Volume'
        volume = self.cinder.volumes.create(name=name, size=size, imageRef=image)
        self.cinder.volumes.set_bootable(volume.id, True)
        while True:
            info = self.cinder.volumes.get(volume.id)
            if info.status == "available":
                break
            elif info.status == "error":
                raise Exception("Volume creation failed") 
        return volume.id

    def _create_server(self, name, size, image, flavor, network):
        volume_id = self._create_volume(name, size, image)
        block_device = { 
            'vda': str(volume_id) 
        }
        server = self.nova.servers.create(  name=name, 
                                            flavor=flavor, 
                                            image='', 
                                            block_device_mapping=block_device, 
                                            nics=[{'net-id': network}]
                                        )
        while True:
            info = self.nova.servers.get(server.id)
            if info.status == 'ACTIVE':
                break
            elif info.status == 'ERROR':
                raise Exception("Server creation failed")
            time.sleep(5)
        server_info = self._get_server_by_id(server.id)
        return server_info
   
    def _list_server_port(self, ins_id):
        server_port = {} 
        ports = self.neutron.list_ports(device_id=ins_id)['ports'] 
        for port in ports: 
            server_port[port['id']] = str(port['fixed_ips'][0]['ip_address']) 
        return server_port

    def _create_port_for_server(self, ins_id, network_id):
        port_info = { 
            'port': {
                'network_id': network_id }
            }

        port_id = self.neutron.create_port(port_info)['port']['id']
        self.nova.servers.interface_attach(ins_id, port_id, net_id="", fixed_ip="")
        time.sleep(10)
        server = self._get_server_by_id(ins_id)
        return server

    def _detach_port_for_server(self, ins_id, port_id):
        self.nova.servers.interface_detach(ins_id, port_id)
        time.sleep(10)
        server = self._get_server_by_id(ins_id)
        return server

    def _console_url(self, ins_id):
        _console = self.nova.servers.get(ins_id).get_vnc_console(console_type='novnc')
        console_url = _console['console']['url']
        return console_url

    def _start_server(self, ins_id):
        self.nova.servers.start(ins_id)
        while True:
            info = self.nova.servers.get(ins_id)
            if info.status == 'ACTIVE':
                break
        return {'status': info.status}

    def _stop_server(self, ins_id):
        self.nova.servers.stop(ins_id)
        while True:
            info = self.nova.servers.get(ins_id)
            if info.status == 'SHUTOFF':
                break
        return {'status': info.status}
    
    # Func to delete server, use with caution
    def _delete_server(self, ins_id):
        info = self.nova.servers.get(ins_id)._info
        volume_id = info['os-extended-volumes:volumes_attached'][0]['id']
        self.nova.servers.delete(ins_id)
        while True:
            volume = self.cinder.volumes.get(volume_id)._info
            if volume['status'] == 'available':
                self.cinder.volumes.delete(volume_id, cascade=True)
                break