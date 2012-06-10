import urllib
import urllib2
import json
import time
import datetime
#
from scalex import userinfo

def getNodes():
  userinfo.check()
  
  url = userinfo.domain + '/scalex/acl/nodelistbyrole?rid=%s' % (userinfo.rid)
  value = {
    'companyId':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.userid
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData

def isWindows(node):
  iswin = False
  if 'Windows' in str(node):
    iswin = True
  return iswin

def isUnix(node):
  return not isWindows(node)

def getOverviewOfAudits(node):
  '''
  https://manage.scalextreme.com/scalex/tigeraudit/auditoverview?rid=A&companyid=10274&user=10002&role=Admin&agentid=40
  '''
  userinfo.check()
  path = '/scalex/tigeraudit/auditoverview'
  url = userinfo.domain + path
  
  value = {
      'companyid':userinfo.companyid,
      'role':userinfo.rolename,
      'user':userinfo.userid,
      'rid':userinfo.rid,
      'agentid':node['agentId'],
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getAudits(node):
  '''
  https://manage.scalextreme.com/scalex/tigeraudit/auditresults?rid=22A&companyid=10274&user=10002&role=Admin&agentid=40&auditanalid=196
  '''
  userinfo.check()

  overview = getOverviewOfAudits(node)['data']
  if overview == {}:
    return {u'data': [], u'result': u'SUCCESS'}
    
  path = '/scalex/tigeraudit/auditresults'
  url = userinfo.domain + path
  
  value = {
      'companyid':userinfo.companyid,
      'role':userinfo.rolename,
      'user':userinfo.userid,
      'rid':userinfo.rid,
      'agentid':node['agentId'],
      'auditanalid':overview['auditAnalId'],
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getOtherAgentsWithPatch(node, patches):
  '''
https://manage.scalextreme.com/scalex/search/searchOtherAgentsWithPatch?
    rid=0F72B45B-935E-44BD-89D6-0F6EACE26C08&
    organizationId=10274&
    user=10002&
    role=Admin&
    agentId=181&
    clause=AND&
    type=UPDATE
https://manage.scalextreme.com/scalex/search/searchOtherAgentsWithPatch?
    organizationId=10274&
    clause=AND&
    role=Admin&
    user=10002&
    rid=39305f26-2e81-435e-8177-3f5a1371db8a&
    agentid=40&
    type=UPDATE


    windows
    
    https://manage.scalextreme.com/scalex/search/searchOtherAgentsWithPatch?rid=0F72B45B-935E-44BD-89D6-0F6EACE26C08&organizationId=10274&user=10002&role=Admin&agentId=88&clause=AND&type=PATCH
    
    patchList=[{"name":"Security Update for Microsoft .NET Framework 3.5.1 on Windows 7 and Windows Server 2008 R2 SP1 for x64-based Systems (KB2633873)"}]
  '''
  userinfo.check()
  
  path = '/scalex/search/searchOtherAgentsWithPatch'
  url = userinfo.domain + path
  if isWindows(node):
    type = 'PATCH'
  else:
    type = 'UPDATE'
  value = {
    'organizationId':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.userid,
    'rid':userinfo.rid,
    'agentId':node['agentId'],
    'clause':'AND',
    'type':type,
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
#      
  updates = []
  if not isinstance(patches, list):
    p = patches
    patches = []
    patches.append(p)
  for u in patches:
    d = {}
    d['name'] = u['name']
    if isUnix(node):
      d['arch'] = u['arch']
      d['updateVersion'] = u['updateversion']
      d['updateRelease'] = u['updaterelease']
    updates.append(d)

  postData = 'patchList=' + json.dumps(updates)
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getUpdates(node):
  '''
  https://manage.scalextreme.com/patchupdate/updatelist?rid=042F8639-FF15-445A-95F9-E03B7DABA6F0&companyid=10274&user=10002&role=Admin&agentid=40&patchanalysisid=316
  '''
  return _getlist(node)

def getPatches(node):
  '''
  https://manage.scalextreme.com/patchupdate/patchlist?rid=042F8639-FF15-445A-95F9-E03B7DABA6F0&companyid=10274&user=10002&role=Admin&agentid=88&patchanalysisid=167
  '''
  return _getlist(node)

def applyPatches(name, node, patches, startTime = 0):
  '''
  windows
  '''
  assert name != '', 'empty job name'
  scriptInfo = {'scriptId':0, 'version':None}

  if not isinstance(patches, list):
    t = patches
    patches = []
    patches.append(t)
  arguments = []
  for u in patches:
    a = list()
    a.append(u['name'])
    arguments.append(a.replace(' ', '+'))
  return _scheduleUpdateOrPatches(name, node, arguments, 'applypatch', startTime)
                                  
def applyUpdates(name, node, updates, startTime = 0):
  '''
    unix
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
  return _scheduleUpdateOrPatches(name, node, arguments, 'applyupdate', startTime)

def _scheduleUpdateOrPatches(name, targets, arguments, scriptType, startTime):
  '''
    payload = {
    "companyId": 10274,
    "user": "10002",
    "role": "Admin",
    "scriptId": 0,
    "version": null,
    "scriptArgs": ["aws-apitools-as%25%5E%26noarch%25%5E%261.0.49.1%25%5E%261.6.amzn1"],
    "targets": [40],
    "destInstallDir": null,
    "scheduleType": 12,
    "startTime": 1342260060000,
    "endTime": 0,
    "repeatCount": 0,
    "repeatInterval": 0,
    "cronExpr": null,
    "timeZone": null,
    "name": "asdfsadfasdf",
    "description": "asdfsadfasdf",
    "jobId": 0,
    "jobName": null,
    "scriptType": "applyupdate"
  }
  '''
  userinfo.check()
  
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
    "companyId": userinfo.companyid,
    "user": str(userinfo.userid),
    "role": userinfo.rolename,
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
    "jobName": None,
    "scriptType": scriptType
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managescript/runscript?rid=' + userinfo.rid
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getOverviewOfUpdatesOrPatches(node):
  '''
    os: 0 is *nix by default, 1 is windows
  https://manage.scalextreme.com/patchupdate/updateoverview?rid=1&companyid=&user=&role=Admin&agentid=40
  https://manage.scalextreme.com/patchupdate/patchoverview?rid=1&companyid=&user=&role=Admin&agentid=82
  '''
  userinfo.check()
  if 'Windows' in str(node):
    os = 1
  else:
    os = 0
  path = ['/patchupdate/updateoverview', '/patchupdate/patchoverview']
  url = userinfo.domain + path[os]

  value = {
    'companyid':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.userid,
    'rid':userinfo.rid,
    'agentid':node['agentId'],
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _getlist(node):
  '''
    For Internal Use ONLY
    
    https://manage.scalextreme.com/patchupdate/patchlist?rid=042F8639-FF15-445A-95F9-E03B7DABA6F0&companyid=10274&user=10002&role=Admin&agentid=88&patchanalysisid=167
    
    https://manage.scalextreme.com/patchupdate/updatelist?rid=042F8639-FF15-445A-95F9-E03B7DABA6F0&companyid=10274&user=10002&role=Admin&agentid=40&patchanalysisid=316
    '''
  overview = getOverviewOfUpdatesOrPatches(node)['data']
  if overview == {}:
    return {u'data': [], u'result': u'SUCCESS'}

  if 'Windows' in str(node):
    os = 1
  else:
    os = 0
  path = ['/patchupdate/updatelist', '/patchupdate/patchlist']
  url = userinfo.domain + path[os]
  value = {
    'companyid':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.userid,
    'rid':userinfo.rid,
    'agentid':node['agentId'],
    'patchanalysisid':overview['patchanalysisid'],
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

