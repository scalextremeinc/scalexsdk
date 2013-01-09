'''
  @undocumented: __package__
  @undocumented: create
  @undocumented: update
'''

import urllib
import urllib2
import json
import base64
import time
import datetime
#
from scalex import userinfo

def getGroups():
  '''
    Get list of groups
    
    @rtype: list
    @return: list of all groups for a Role and User
  '''
  
  path = '/groups'
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
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
  url = userinfo.geturl(path)
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  #  
  return returnData

# FIXME
# no create and update

def create(name, parentGroup):
  '''
    FIXME, not finished
  '''
  '''  {\"groupType\":0,
  \"groupId\":0, 
  \"groupName\":\"PacaficServers\",
  \"parentGroupId\":1,
  \"groupParent\":\"All Servers\",
  \"companyId\":0,
  \"organizationId\":0,
  \"groupItemList\":[{\"groupId\":0,  \"companyId\":0,  \"groupItem\":\"124\",  \"organizationId\":0,  \"groupItemType\":0}]
  }"
  '''
  path = '/groups'
  url = userinfo.geturl(path)
  payload = {
    "groupType": 0,
    "groupId": 0,
    "groupName": None,
    "PacaficServers": arguments,
    "parentGroupId": agents,
    "groupParent": None,
    "companyId": 12,
    "organizationId": startTime,
    "groupItemList": 0,
  }
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def update(group):
  '''
  '''
  pass

def delete(group):
  '''
    Delete a server group
    
    @param group: The group you want to delete
  '''
  path = '/groups/' + str(group['groupId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  request.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

