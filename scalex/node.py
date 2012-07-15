'''
  @undocumented: __package__
  
  @todo:
    - Add create/update/delete groups
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

def getAudits(node, type = ''):
  '''
    Get a list of Audit for a single node
    
    @param node: A linux node
    
    @type   type: string
    @param  type: Optional, valid values:
      - B{script}
      - B{template}
      - B{patch}
      - B{update}

    @rtype: list
    @return: list of audits

  '''
  '''
    FIXME, this function need more info
    b) To get a list of Audit for a single node
    
    API :  nodes/{id}/audit
    Method : GET
    URL Structure: https://<servername>/v0/nodes/<id>/updates?access_token=<valid access token>
    //Input : type (optional), valid values are script, template, patch, update etc.,
    Output :
    [{"auditDesc":"Checking listening processes ","auditCheckId":28609,"auditCheckCount":6,"auditLevel":"Warning"},{"auditDesc":"Performing check of `cron' entries...","auditCheckId":28588,"auditCheckCount":2,"auditLevel":"Warning"},{"auditDesc":"Performing common access checks for root (in /etc/default/login, /securetty, and /etc/ttytab...","auditCheckId":28582,"auditCheckCount":2,"auditLevel":"Warning"},{"auditDesc":"Checking accounts from /etc/passwd.","auditCheckId":28575,"auditCheckCount":2,"auditLevel":"Warning"},{"auditDesc":"Checking device permissions...","auditCheckId":28598,"auditCheckCount":7,"auditLevel":"Fail"},{"auditDesc":"Checking for correct umask settings...","auditCheckId":28607,"auditCheckCount":1,"auditLevel":"Fail"},{"auditDesc":"Checking entries from /etc/passwd.","auditCheckId":28549,"auditCheckCount":23,"auditLevel":"Warning"},{"auditDesc":"Performing common access checks for root...","auditCheckId":28621,"auditCheckCount":1,"auditLevel":"Fail"},{"auditDesc":"Checking sshd_config configuration files...","auditCheckId":28617,"auditCheckCount":1,"auditLevel":"Warning"}]
  '''
  agentid = node['agentId']
  path = '/nodes/%s/%s' % (str(agentid), str(type))
  query = {}
  if type != '':
#    assert type in ['script', 'template', 'patch', 'update'], 'type invalid'
    query['type'] = type
  url = userinfo.geturl(path, query)
  print url
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def getAllAgentsWithPatch(patch):
  '''
    Get a list of machines which have the same patches/updates missing    
    
    @param patch: Valid values:
      - patch
      - list of patches
      - update
      - list of updates
    
    @rtype: list
    @return: list of agentId
    
    @change:
      - Old API getOtherAgentsWithPatch(node,patch)
  '''
#    FIXME, BUG with HTTPError: HTTP Error 400: Invalid update list
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

def applyPatches(name, target, patches, startTime = 0):
  '''
    Apply patches for nodes
    
    @param name: Job name
    
    @param target: Target Node
    
    @param patches: patch/patches
    
    @param startTime: Start time formatted like B{2012-12-12-00:00}, default is now
    
    @rtype: dict
    @return: job info
    
  '''
  assert name != '', 'empty job name'
  #  scriptInfo = {'scriptId':0, 'version':None}
  
  if not isinstance(patches, list):
    t = patches
    patches = []
    patches.append(t)
  arguments = []
  for u in patches:
    #    a = list()
    #    a.append(u['name'])
    arguments.append(u['name'].replace(' ', '+'))
  return _scheduleUpdateOrPatches(name, target, arguments, 'applypatch', startTime)

def applyUpdates(name, target, updates, startTime = 0):
  '''
    Apply updates for nodes
    
    @param name: Job name
    
    @param target: Target Node
    
    @param updates: update/updates
    
    @param startTime: Start time formatted like B{2012-12-12-00:00}, default is now
    
    @rtype: dict
    @return: job info
    
  '''
  assert name != '', 'empty job name'
  
  if not isinstance(updates, list):
    t = updates
    updates = []
    updates.append(t)
  arguments = []
  for u in updates:
    a = list()
    a.append(u['name'])
    a.append(u['arch'])
    a.append(u['updateversion'])
    a.append(u['updaterelease'])
    arguments.append('%25%5E%26'.join(a))
  return _scheduleUpdateOrPatches(name, target, arguments, 'applyupdate', startTime)

def _scheduleUpdateOrPatches(name, targets, arguments, scriptType, startTime):
  '''
  '''
  if not isinstance(targets, list):
    t = targets
    targets = []
    targets.append(t)
  
  agents = []
  for n in targets:
    agents.append(n['agentId'])
  if startTime != 0:
    d = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H:%M")
    startTime = int(time.mktime(d.timetuple())*1000)
  
  payload = {
#    "companyId": userinfo.companyid,
#    "user": str(userinfo.userid),
#    "role": userinfo.rolename,
    "scriptId": 0,
    "version": None,
    "scriptArgs": arguments,
    "targets": agents,
    "destInstallDir": None,
    "scheduleType": 12,
    "startTime": startTime,
    "endTime": 0,
    "repeatCount": 0,
    "repeatInterval": 0,
    "cronExpr": None,
    "timeZone": None,
    "name": name,
    "description": name,
    "jobId": 0,
    "jobName": name,
    "scriptType": scriptType
  }
  path = '/jobs'
  url = userinfo.geturl(path)
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

# Group
#
# FIXME
# no create or update groups
# no delete a group

def createGroup(name, parentGroup):
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

def updateGroup(group):
  '''
    FIXME, not finished
  '''
  pass

def deleteGroup(group):
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

def getGroups():
  '''
    Get server groups
    
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

