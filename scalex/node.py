'''
  @undocumented: __package__
  
  @change:
    - Old API currently not support, only getNodes() is available
'''
import urllib
import urllib2
import json
import time
import datetime
#
from scalex import userinfo

# NODE API
#  4.26 +         //  restNodeController.testgetAllNodes();
#  4.27 +           // restNodeController.testgetNode();
#  4.28 +        restNodeController.testgetNodeupdates();
#  4.29 +         //   restNodeController.testgetNodeAudits();

def getNodes(platform = '', status = ''):
  '''
    Get nodes
    
    @type   platform: string
    @param  platform: optional, valid values are B{Windows} or B{Linux}
    
    @type   status: string
    @param  status: optional, valid values are B{online} or B{offline}

    @rtype: list
    @return: list of nodes
    
    @change: 
      - Add parameter platform and status
  '''
#    FIXME, not add single node id 
#    API : /nodes or /nodes/{id}
#    Method : GET
#    URL Structure: https://<servername>/v0/nodes?access_token=<valid access token>
#    Input params: 
#    platform (optional), valid values Windows or Linux
#    status (optional), valid values online or offline
  assert platform in ['', 'Windows', 'Linux'], 'wrong platform'
  assert status in ['', 'online', 'offline'], 'wrong status'  
  path = '/nodes'
  query = {}
  if platform != '':
    query['platform'] = platform
  if status != '':
    query['status'] = status
  url = userinfo.geturl(path, query)
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def getGroups():
  '''
    Get groups
    
    @rtype: list
    @return: list of groups
    '''
  path = '/groups'
  query = {}
  url = userinfo.geturl(path, query)
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def getNodesOfGroup(group):
  '''
    Get nodes of a given group
    
    @param  group: A group returned by getGroups()
    
    @rtype: list
    @return: list of nodes
  '''
  groupid = group['groupId']
  path = '/groups/%s/nodes' % (str(groupid))
  query = {}
  url = userinfo.geturl(path, query)
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
#  
  return returnData

#FIXME, getUpdates() and getPatches(), one URI
def getUpdates(node):
  '''
    Get updates of a given node
    
    @param node: A node
    
    @rtype: list
    @return: list of updates
    '''
  agentid = node['agentId']
  path = '/nodes/%s/updates' % (str(agentid))
  query = {}
  url = userinfo.geturl(path, query)
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def getPatches(node):
  '''
    Get patches of a given node

    @param node: A node
    
    @rtype: list
    @return: list of patchest

    '''
  return getUpdates(node)

def getAudits(node):
  '''
    Get audits of a given linux node
    
    @param node: A linux node
    
    @rtype: list
    @return: list of audits

  '''
  agentid = node['agentId']
  path = '/nodes/%s/audit' % (str(agentid))
  query = {}
  url = userinfo.geturl(path, query)
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def getAllAgentsWithPatch(patch):
  '''
    FIXME, not finished
    
    @change:
      - Old API getOtherAgentsWithPatch(node,patch)
  '''
  path = '/missingupdates'
  query = {
    'type':'PATCH',
  }
  if 'updaterelease' in str(patch):
    query['type'] = 'UPDATE'
  url = userinfo.geturl(path, query)
  postData = 'list=' + json.dumps(patch)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData
  
