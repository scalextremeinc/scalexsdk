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

def getAlerts(page = 1, limit = 30):
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

def enable(node, enable):
  '''
  /monitor/{id}

  '''
  pass


def getEvents(node):
  '''
  /monitor/{id}/events

  '''
  pass

def getMetrics(node):
  '''
  /monitor/{id}/metrics
  '''
  pass
