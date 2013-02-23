'''
  @undocumented: __package__
  
'''

import urllib
import urllib2
import json
import base64
import time
import datetime
#
from scalex import userinfo

def getProviders():
  '''
    Get list of all providers
    
    @rtype: list
    @return: list of all providers for a Role and User
  '''
  
  path = '/providers'
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def create(name, providerCode, params):
  '''
    Create a provider

    @type   name: string
    @param  name: The name of the provider account

    @type   providerCode: string
    @param  providerCode: The providercode for the cloud provider

    @type   params: dict
    @param  params: Provider-specific Parameters (required for individual providers)
  '''

  validProviderCodes = ['ec2', 'rackspace', 'openstack', 'bluelock', 'vcloud', 'cloudstack', 'dellcloud', 'trmkecloud', 'savvis', 'thecloud', 'hpcloud']
  assert providerCode in validProviderCodes, 'Wrong providerCode'
  params['name'] = name
  params['providerCode'] = providerCode
  postData = json.dumps(params)
  request = urllib2.Request(url, postData)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def update(provider, name = '', providerCode = '', params = {}):
  '''
    Update a provider

    @type   provider: dict
    @param  provider: A provider

    @type   name: string
    @param  name: The name of the provider account

    @type   providerCode: string
    @param  providerCode: The providercode for the cloud provider

    @type   params: dict
    @param  params: Provider-specific Parameters (required for individual providers)
 
  '''
  if providerCode != '':
    validProviderCodes = ['ec2', 'rackspace', 'openstack', 'bluelock', 'vcloud', 'cloudstack', 'dellcloud', 'trmkecloud', 'savvis', 'thecloud', 'hpcloud']
    assert providerCode in validProviderCodes, 'Wrong providerCode'
  #   "provider_id": "529",
  # "costing_enabled": "Y",
  # "provider_code": "ec2",
  # "provider_name": "Amazon"
  if name == '':
    name = provider['provider_name']
  if providerCode == '':
    providerCode = provider['provider_code']
  # FIXME, not 
  print 'FIXME, not implemented'


def delete(provider):
  '''
    Delete a provider

    @type   provider: dict
    @param  provider: The provider you want to delete
  '''

  path = '/providers/' + str(provider['provider_id'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  request.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getEstimatedCost(provider, period = 'MONTHLY', level = 'ROLE'):
  '''
    Gets an estimated cost for a provider

    @type   provider: dict
    @param  provider: The provider

    @type   period: string
    @param  period: Valid values are B{MONTHLY} and B{WEEKLY}

    @type   level: string
    @param  level: Valid values are B{ROLE} and B{USER}
  '''
  assert period in ['MONTHLY', 'WEEKLY'], 'valid period values are MONTHLY and WEEKLY '
  assert level in ['ROLE', 'USER'], 'valid levle values are ROLE and USER '

  path = '/providers/%s/estimatedcost' % (str(provider['provider_id'])) 
  query = {
    'period' : period,
    'level' : level
  }
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getActualCost(provider):
  '''
    Gets the actual cost for a provider

    @type   provider: dict
    @param  provider: The provider
  '''
  path = '/providers/%s/actualcost' % (str(provider['provider_id']))
  query = {
    'providercode' : provider['provider_code']
  }
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getServers(provider):
  '''
    Gets a list of all servers for a single provider
    
    @type   provider: dict
    @param  provider: The provider
  '''
  path = '/providers/%s/servers' % (str(provider['provider_id']))
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def performAction(provider, server, action):
  '''
    Performs an action on a server

    @type   provider: dict
    @param  provider: The provider

    @type   server: dict
    @param  server: Server returned by getServers()

    @type   action: string
    @param  action: Supported actions: B{poweron}, B{poweroff}, B{reboot}, B{delete}

  '''

  validActions = ['poweron', 'poweroff', 'reboot', 'delete']
  assert action in validActions, 'supported actions: poweron, poweroff, reboot, delete'
  path = '/providers/%s/servers/%s' % (str(provider['provider_id']), str(server['id']))
  url = userinfo.geturl(path)
  params = {
    'action' : action,
    'regioncode' : server['regionCode'],
  }
  postData = urllib.urlencode(params)
  request = urllib2.Request(url, postData)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData





