#!/usr/bin/env python

# Includes
import os
import keystoneauth1.identity.v3 as identity
import keystoneauth1.session as session
import keystoneclient.v3.client as keclient
import neutronclient.v2_0.client as neclient
import novaclient.client as noclient

# Function to populate credentials from Operating System Enviroment Variables
def get_os_kuser_creds():
    cred_dict = {}
    cred_dict['username'] = os.environ['OS_USERNAME']
    cred_dict['password'] = os.environ['OS_PASSWORD']
    cred_dict['auth_url'] = os.environ['OS_AUTH_URL']
    cred_dict['project_id'] = os.environ['OS_PROJECT_ID']
    cred_dict['user_domain_name'] = os.environ['OS_USER_DOMAIN_NAME']
    return cred_dict

# Collect credentials from OS Enviroment variables.
kusercreds = get_os_kuser_creds()

# Keystone - Create authentication identity and session
auth = identity.Password(**kusercreds)
sess = session.Session(auth=auth)

# Servers
nova = noclient.Client(2, session=sess)
# Networking
neutron = neclient.Client(session=sess)

# Debug output
#print "DEBUG : kusercreds : ",kusercreds
#nets = neutron.list_networks()
#print nets

app_prefix="app001-"

#router = neutron.show_router(router_id)

# For as many instances as requested by the user, create networks and server.
for x in range(0,3):
  body_router = {'router':{'name': app_prefix + "router" + str(x), 'admin_state_up': True, 'external_gateway_info': {"network_id":"***************************************"}  }}
  router = neutron.create_router(body_router)

  # Create the network
  body_network = {'network': {'name': "net" + str(x), 'admin_state_up': True}}
  network = neutron.create_network(body_network)

  # Retrive created network
  created_network = neutron.list_networks(name="net" + str(x))
  print created_network

  # Retrive the network ID from the results
  returned_network_id = created_network['networks'][0]['id']
  print returned_network_id

  # Create the subnet
  body_subnet = {'subnets': [{'cidr': "192.168." + str(x) +".0/24", 'ip_version': 4, 'network_id': returned_network_id}]}
  subnet = neutron.create_subnet(body_subnet)

  # Create port
#  body_port = {"port": {"admin_state_up": True, "device_id": server_id, "name": "port" + str(x), "network_id": returned_network_id }}
#  port = neutron.create_port(body_port)

  # Create server
#  nova_client.servers.create(name="vm2", image=image, flavor=flavor, key_name="keypair-1", nics=nics)






