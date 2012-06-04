import urllib
import urllib2
import json
import time
import datetime
import base64
#
import userinfo

def getScripts(type = 0):
  '''arguments: type
    0 is myscripts
    1 is orgscripts
    default is 0
    '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
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

def getContent(scriptid, version):
  '''arguments: scriptid, version
    '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  payload = {
    'scriptid': scriptid,
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

def getVersions(scriptid):
  #ttps://manage.scalextreme.com/library?rid=70E1FA13-7F7D-49CE-87DA-9FBF5A9484B7&companyid=10274&user=10002&role=Admin&operation=scriptversions
  url = userinfo.domain + '/library'
  payload = {
    'scriptid': scriptid,
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

def run(name, scriptid, version, targets, arguments = [], scheduleType = 0,
        startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0, cronExpr = None, timeZone = ''):
  '''
  scheduleType: 0, Run Once
                1, Recurring
                2, Cron Schedule (Advanced)
  '''
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
  if len(arguments) == 0:
    #FIXME
    params = getContent(scriptid, version)['data']
    for p in params['scriptInputParams']:
      arguments.append(p['parameterDefaultValue'])
  
  payload = {
    "companyId": userinfo.companyid,
    "user": userinfo.userid,
    "role": userinfo.rolename,
    "scriptId": scriptid,
    "version": version,
    "scriptArgs": arguments,
    "targets": targets,
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
    "scriptType": None
  }
  postData = 'operation=runscript&payload=' + json.dumps(payload)
  url = userinfo.domain + '/managescript?rid=' + userinfo.rid
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def create(name, type, content, description = '', params = [], tags = []):
  '''
    scriptparams	[{"taskId":0, "taskParameterId":0, "parameterType":"INPUT", "parameterKey":"KEY1", "parameterDefaultValue":"VALUE", "parameterValue":null, "parameterDataType":"string", "description":"desc", "requiredFlag":"Y", "sequenceNumber":1},]
    scripttags	[{"tagName":"amazon ec2", "tagType":null, "activeFlag":null},]
  '''
  #FIXME, no script attachments
  #ttps://manage.scalextreme.com/library?rid=411C2ECD-BDD0-4F61-9F37-E3718F02E084
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
    'scriptparams':params,
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

def delete(scriptid):
  # ://manage.scalextreme.com/library?rid=a&companyid=10476&user=10473&role=Admin&operation=deletescript&scriptid=115
  #FIXME, 
  url = userinfo.domain + '/library'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'deletescript',
    'scriptid':scriptid,
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request  = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request).read()
  return response

#def create(name, type, content, description = '', params = [], tags = []):

def update(scriptid, version = '', name = '', type = '', content = '', description = '', params = [], tags = [] ):
  # ://manage.scalextreme.com/library?rid=a&companyid=10476&user=10473&role=Admin&operation=deletescript&scriptid=115
  #FIXME, no script attachments
  #ttps://manage.scalextreme.com/library?rid=411C2ECD-BDD0-4F61-9F37-E3718F02E084
  url = userinfo.domain + '/library?rid=' + userinfo.rid
  content = base64.b64encode(content)
  description = base64.b64encode(description)

  if not version:
    version = getVersions(scriptid)['data'][0]['version']
  script = getContent(scriptid, version)['data']
  if not name:
    name = script['scriptName']
  if not type:
    type = script['scriptType']
  if not content:
    content = script['scriptContent'] 
  if not description:
    description = script['scriptDescription'] 
  '''
  sharedFlag	N
  viewableflag	Y
  parentScriptId	0
  purchasedFlag	N
  '''
  value = {
    'companyid':userinfo.companyid,
    'operation':'updatescript',
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'scriptid':scriptid,
    'version':version,
    'scriptname':name,
    'scripttype':type,
    'scriptcontent':content,
    'scriptdescription':description,
    'scripttags':tags,
    'scriptparams':params,
    'scriptlocation':script['scriptLocation'],
    #
    'inputparams':script['inputParams'],
    'parentCompanyId':script['parentCompanyId'],
    'parentScriptId':script['parentScriptId'],
    'purchasedFlag':script['purchasedFlag'],
    'parentScriptId':script['parentScriptId'],
    'sharedFlag':script['sharedFlag'],
    'viewableflag':script['viewableFlag'],
  }
  request  = urllib2.Request(url, urllib.urlencode(value))
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData



