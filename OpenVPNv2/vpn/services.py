import pexpect

import subprocess,os  , sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'OpenVPNv2.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
import pickle
from django.conf import settings
from django.db import connection
from django.conf import settings
from vpn.models import Revoke

def generate_certs(data,path):
    """

    :type data: object
    """
    print data.items()
    os.chdir('{0}easy-rsa/'.format(path))
    child = pexpect.spawn('/bin/bash')
    child.sendline('source ./vars')
    child.sendline('./build-key {0}'.format(data['name_certificate']))
    for i in range(10):
        child.sendline('')
    child.sendline('y')
    child.sendline('y')

def revoke_certs(data,path):
    """
    in this case we revoke users openvpn certificates
    :type data: object
    """
    print dict(data.items())
    os.chdir('{0}easy-rsa/'.format(path))
    child = pexpect.spawn('/bin/bash')
    child.sendline('source ./vars')
    child.sendline('./revoke-full {0}'.format(data['name_certificate']))
    child.sendline('\n')

def stats_certs(path,vpn_id):
    dir_vpn = '{0}easy-rsa/keys/index.txt'.format(path)
    print dir_vpn
    file = open(dir_vpn, 'r')
    name=''
    all_entry = Revoke.objects.filter(certs_revoke_name='{}'.format(name))
    for line in file:

        status = line[0]
        print status
        start = line.index('/CN=') + len('/CN=')
        end = line.index('/name=')
        slise = line[start:end]
        if  Revoke.objects.filter(certs_revoke_name='{0}'.format(slise)):
            print 'ok'
        else:
            b = Revoke(certs_revoke_name=slise,certs_revoke_status=status,certs_general_id=vpn_id)
            print ('{0}''{1}'.format(slise, status))
            b.save()
            print 'srez',slise

        print 'srez',slise

def status_vpn():
    data='TEST'
    return data
