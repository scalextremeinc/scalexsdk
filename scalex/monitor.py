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

def getRollupAlerts(page = 1, limit = 30):
  '''
    Gets a list of all alerts in the organization
    
    @type   page: int
    @param  page: User can choose the page number

    @type   limit: int
    @param  limit: User can limit the number of records returned 

    @rtype: list
    @return: list of all alerts
  '''
  
  path = '/monitor/rollup'
  query = {
    'page' : page,
    'limit' : limit
  }
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getStatus(node):
  '''
    Gets monitoring status for a node/agent

    @param node: A node

    @rtype: dict
    @return: Monitoring status for the node

  '''
  path = '/monitor/' + str(node['agentId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _enable(node, enable):
  '''
    Enables/disables monitoring on a node/agent

    @type   node: dict
    @param  node: A node

    @type   enable: bool
    @param  enable: 
  '''
  path = '/monitor/' + str(node['agentId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  params = {
    'enable' : 'Y' if enable else 'N',
  }
  postData = urllib.urlencode(params)
  response = urllib2.urlopen(request, postData)
  returnData = json.loads(response.read())
  return returnData

def enableMonitoring(node):
  _enable(node, True)

def disableMonitoring(node):
  _enable(node, False)

def getAlertsForNode(node):
  '''
    Gets alerts for a node/agent

    @type   node: dict
    @param  node: A node
  '''
  path = '/monitor/%s/alerts' % (str(node['agentId']))
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def enableAlerts(node):
  '''
    Enable alerts for a node

    @type   node: dict
    @param  node: A node
  '''
  path = '/monitor/%s/alerts/enable' % (str(node['agentId']))
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def disableAlerts(node):
  '''
    Disable alerts for a node

    @type   node: dict
    @param  node: A node
  '''
  path = '/monitor/%s/alerts/disable' % (str(node['agentId']))
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getEvents(node, limit = 25, timestamp = 0):
  '''
    Get events for a node

    @type   node: dict
    @param  node: A node

    @type   limit: int
    @param  limit: limit number of records shown, default is 25.

    @type   timestamp: int
    @param  timestamp: end time in the form of epoch time in milliseconds (ex: 1348784568), default is current time
  '''
  path = '/monitor/%s/events' % (str(node['agentId']))
  query = {
    'limit' : limit
  }
  if timestamp != 0:
    query['timestamp'] = timestamp

  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getMetrics(node):
  '''
    Get metrics for a node

    @type   node: dict
    @param  node: A node
  '''
  path = '/monitor/%s/metrics' % (str(node['agentId']))
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData