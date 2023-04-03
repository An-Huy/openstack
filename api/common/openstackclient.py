from common.config import load_config
from keystoneauth1.identity import v3 
from keystoneauth1 import session
from keystoneclient.v3 import client as keystone
from novaclient import client as nova
from cinderclient import client as cinder
from neutronclient.v2_0 import client as neutron
from glanceclient.v2 import client as glance

region = 'RegionOne'

class Authentication(object):

    def __init__(self):
        credentials = load_config("openstack")
        self.credentials = credentials
        
    def get_session(self):
        auth = v3.Password(**self.credentials)
        sess = session.Session(auth=auth)
        return sess
    
    def _keystone_client(self):
        sess = self.get_session()
        return keystone.Client(session=sess, region_name = region)
    
    def _glance_client(self):
        sess = self.get_session()
        return glance.Client('2', session=sess, region_name = region)
    
    def _nova_client(self):
        sess = self.get_session()
        return nova.Client('2', session=sess, region_name = region)
    
    def _cinder_client(self):
        sess = self.get_session()
        return cinder.Client('3', session=sess, region_name = region)
    
    def _neutron_client(self):
        sess = self.get_session()
        return neutron.Client(session=sess, region_name = region)