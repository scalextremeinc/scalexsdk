import urllib
import urllib2
import json
import time
import datetime
import base64
#
from scalex import userinfo
import scalex

def getScripts(type = 0):
  '''arguments: type
    0 is myscripts
    1 is orgscripts
    default is 0
    
    RETURN DATA:
    {
    "result": "SUCCESS",
    "data": [
    {
    "parentCompanyId": 0,
    "scriptName": "python_sdk_testcase_scriptname_38882",
    "parentScriptId": 0,
    "scriptDescription": "ZGVzY3JpcHRpb24=",
    "scriptInputParams": [],
    "role": "Admin",
    "companyId": 10361,
    "scriptId": "81",
    "tagList": [],
    "user": "10002",
    "scriptAttachments": [],
    "version": "1"
    },
    '''
  userinfo.check()
  operation = ['userscripts', 'orgscripts']
  if type < 0 or type > len(operation) - 1:
    return
  url = userinfo.domain + '/library'
  value = {
    'companyid':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.username,
    'rid':userinfo.rid,
    'operation':operation[type]
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getContent(script, version = -1):
  '''
  '''
  userinfo.check()
  if version == -1:
    #default version
    version = script['version']
  payload = {
    'scriptid': script['scriptId'],
    'version': version,
  }
  url = userinfo.domain + '/library'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'scriptcontent',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, urllib.urlencode(payload))
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getVersions(script):
  #ttps://manage.scalextreme.com/library?rid=70E1FA13-7F7D-49CE-87DA-9FBF5A9484B7&companyid=10274&user=10002&role=Admin&operation=scriptversions
  userinfo.check()
  url = userinfo.domain + '/library'
  payload = {
    'scriptid': script['scriptId'],
  }
  value = {
   'companyid':userinfo.companyid,
   'user':userinfo.userid,
   'role':userinfo.rolename,
   'operation':'scriptversions',
   'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, urllib.urlencode(payload))
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def run(name, script, targets, version = -1, arguments = [], scheduleType = 0,
        startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0, cronExpr = None, timeZone = 'FIXME', scriptType = None):
  '''
  scheduleType: 0, Run Once
                1, Recurring
                2, Cron Schedule (Advanced)
  '''
  userinfo.check()
  if version == -1:
    # default version
    version = script['version']
  # 
  type = [12, 14, 2]
  if scheduleType == 0:
    if startTime != 0:
      d = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H:%M")
      startTime = int(time.mktime(d.timetuple())*1000)
  elif scheduleType == 1:
    if repeatCount == 0 and endTime == 0:
      #wrong
      pass
    if endTime != 0:
      d = datetime.datetime.strptime(endTime, "%Y-%m-%d-%H:%M")
      endTime = int(time.mktime(d.timetuple())*1000)
    pass
  elif scheduleType == 2:
    #nothing to do 
    pass
  else:
    #wrong argument
    pass
  #  if len(arguments) == 0:
  #    #FIXME
  #    params = getContent(scriptid, version)['data']
  #    for p in params['scriptInputParams']:
  #      arguments.append(p['parameterDefaultValue'])
  if not isinstance(targets, list):
    t = targets
    targets = []
    targets.append(t)
  agents = []
  for n in targets:
    # user can call this function with GROUP_node
    try:
      agents.append(n['agentId'])
    except:
      agents = targets
  payload = {
    "companyId": userinfo.companyid,
    "user": userinfo.userid,
    "role": userinfo.rolename,
    "scriptId": script['scriptId'],
    "version": str(version),
    "scriptArgs": arguments,
    "targets": agents,
    "destInstallDir": None,
    "scheduleType": type[scheduleType],
    "startTime": startTime,
    "endTime": endTime,
    "repeatCount": repeatCount,
    "repeatInterval": repeatInterval,
    "cronExpr": cronExpr,
    "timeZone": timeZone,
    "name": name,
    "description": name,
    "jobId": 0,
    "jobName": None,
    "scriptType": scriptType
  }
  postData = 'operation=runscript&payload=' + json.dumps(payload)
  url = userinfo.domain + '/managescript?rid=' + userinfo.rid
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _isNameExists(name):
  '''
    https://manage.scalextreme.com/library/scriptexists?rid=0&companyid=10274&user=10002&role=Admin
  '''
  postData = 'scriptname=' + name
  url = userinfo.domain + '/library/scriptexists'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  exists = False
  if json.loads(response.read())['data'] == 'Y':
    exists = True
  return exists

def create(name, type, content, description = '', params = [], tags = []):
  '''
    params format
    [
    {"parameterKey":"first int key", "parameterDefaultValue":"1", "parameterDataType":"int", "description":"desc", "requiredFlag":"Y"},
    {"parameterKey":"second str key", "parameterDefaultValue":"string2",  "parameterDataType":"string", "description":"desc", "requiredFlag":"Y"},
    ]
    scripttags	[{"tagName":"amazon ec2", "tagType":null, "activeFlag":null},]
  '''
  userinfo.check()

  #FIXME, no script attachments
  #ttps://manage.scalextreme.com/library?rid=411C2ECD-BDD0-4F61-9F37-E3718F02E084
  
  if _isNameExists(name):
    # FIXME, name exists
    return
  parameters = []
  d = { "taskId":0, "taskParameterId":0, "parameterType":"INPUT", "parameterValue":None }
  if params != []:
    i = 1
    for p in params:
      for k in p:
        d[k] = p[k]
      d['sequenceNumber'] = i
      i += 1
      parameters.append(d)
      
  url = userinfo.domain + '/library?rid=' + userinfo.rid
  value = {
    'companyid':userinfo.companyid,
    'operation':'createscript',
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'scriptname':name,
    'scripttype':type,
    'scriptcontent':base64.b64encode(content),
    'scriptdescription':base64.b64encode(description),
    'scripttags':tags,
    'scriptparams':parameters,
    #
    'inputparams':0,
    'parentCompanyId':0,
    'parentScriptId':0,
  }
  request  = urllib2.Request(url, urllib.urlencode(value))
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def delete(script):
  # ://manage.scalextreme.com/library?rid=a&companyid=10476&user=10473&role=Admin&operation=deletescript&scriptid=115
  #FIXME, 
  userinfo.check()

  url = userinfo.domain + '/library'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'deletescript',
    'scriptid':script['scriptId'],
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request  = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

#def create(name, type, content, description = '', params = [], tags = []):

def update(script, name = '', type = '', content = '', description = '', params = [], tags = [] ):
  # ://manage.scalextreme.com/library?rid=a&companyid=10476&user=10473&role=Admin&operation=deletescript&scriptid=115
  #FIXME, no script attachments
  #ttps://manage.scalextreme.com/library?rid=411C2ECD-BDD0-4F61-9F37-E3718F02E084
  #Session expired
  userinfo.check()

  url = userinfo.domain + '/library?rid=' + userinfo.rid
  content = base64.b64encode(content)
  description = base64.b64encode(description)
  scriptDetail = scalex.script.getContent(script)['data']
  if not name:
    name = script['scriptName']
  if not type:
    type = scriptDetail['scriptType']
  if not content:
    content = scriptDetail['scriptContent'] 
  if not description:
    description = scriptDetail['scriptDescription'] 
  if not params:
    params = scriptDetail['scriptInputParams'] 
  if not tags:
    tags = scriptDetail['scriptTags'] 
  value = {
    'companyid':userinfo.companyid,
    'operation':'updatescript',
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'scriptid':script['scriptId'],
    'version':script['version'],
    'scriptname':name,
    'scripttype':type,
    'scriptcontent':content,
    'scriptdescription':description,
    'scripttags':tags,
    'scriptparams':params,
    'scriptlocation':scriptDetail['scriptLocation'],
    #
    'inputparams':scriptDetail['inputParams'],
    'parentCompanyId':scriptDetail['parentCompanyId'],
    'parentScriptId':scriptDetail['parentScriptId'],
    'purchasedFlag':scriptDetail['purchasedFlag'],
    'parentScriptId':scriptDetail['parentScriptId'],
    'sharedFlag':scriptDetail['sharedFlag'],
    'viewableflag':scriptDetail['viewableFlag'],
  }
  request  = urllib2.Request(url, urllib.urlencode(value))
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData



