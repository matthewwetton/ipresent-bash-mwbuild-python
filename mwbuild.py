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
print "DEBUG : kusercreds : ",kusercreds

# Keystone - Create authentication identity and session
auth = identity.Password(**kusercreds)
sess = session.Session(auth=auth)

# Networking
neutron = neclient.Client(session=sess)
nets = neutron.list_networks()
print nets


