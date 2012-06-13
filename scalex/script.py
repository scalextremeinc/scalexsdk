import urllib
import urllib2
import json
import time
import datetime
import base64
#
from scalex import userinfo
import scalex

def getScripts(script = '', version = 0):
  '''
    API : /scripts
    Method : GET
    URL structure : https://<servername>/v0/scripts?access_token=<valid access token>
    Input params : version (optional) parameter
  '''
  path = '/scripts'
  query = {}
  if script != '':
    path = '/scripts/' + str(script['scriptId'])
    if version != 0:
      query['version'] = version
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getContent(script, version = -1):
  '''
    API : /scripts or /scripts/{id}
    Method : GET
    URL structure : https://<servername>/v0/scripts?access_token=<valid access token>
    Input params : version (optional) parameter
  '''
  scriptid = script['scriptId']
  path = '/scripts/%s' % (str(scriptid))
  query = {
  }
  if version != -1:
    query['version'] = version
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getVersions(script):
  '''
    API : /scripts/versions?id=1234
    Method : GET
  '''
  path = '/scripts/%s/versions' % (str(script['scriptId']))
  query = {
  }
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def run(name, script, targets, version = -1, arguments = [], scheduleType = 0,
        startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0, cronExpr = None, timeZone = 'FIXME', scriptType = None):
  '''
    FIXME, what about VERSION??
    API : /jobs
    Method : POST
    URL structure: https://<servername>/v0/jobs
    Input param: Following json payload
    {
    "name":"Sample Job",
    "scriptId":2446,
    "targets":[140],
    "scriptArgs":["Test1","Test2"],
    "type":"script",
    "repeatCount":0,
    "serverGroups":[],
    "endTime":0,
    "startTime":1339353250011,
    "scheduleType":12,
    "taskParameters":[],
    "repeatInterval":0
    }

  scheduleType: 0, Run Once
                1, Recurring
                2, Cron Schedule (Advanced)
  '''
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
    agents.append(n['agentId'])
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
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _isNameExists(name):
  '''
FIXME
  '''
  path = '/scripts'
  url = userinfo.geturl(path)
  payload = {
    "scriptName":name,
    "scriptType":type,
    "scriptDescription":base64.b64encode(description),
    "scriptInputParams":[],
    "tagList":[],
    "scriptAttachments":[],
    "scriptContent":base64.b64encode(content),
  }
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def create(name, type, content, description = '', params = [], tags = []):
  '''
    FIXME, not complete
    API : /scripts
    Method : POST
    URL Structure: https://<servername>/v0/scripts?access_token=<valid token generated by authentication>
    Input : Json payload like 
    {
    "scriptName":"Test script",
    "scriptType":"bat",
    "scriptDescription":"",
    "scriptInputParams":[],
    "tagList":[],
    "scriptAttachments":[],
    "scriptContent":"bGluZTEKbGluZTIKbGluZTMKbGluZTQKbGluZTUKZWNobyAnSGknCg=="
    }
  '''
  #FIXME, no script attachments, no tags, no params
  #ttps://manage.scalextreme.com/library?rid=411C2ECD-BDD0-4F61-9F37-E3718F02E084
  
#  if _isNameExists(name):
#    # FIXME, name exists
#    return
  path = '/scripts'
  url = userinfo.geturl(path)
  payload = {
    "scriptName":name,
    "scriptType":type,
    "scriptDescription":base64.b64encode(description),
    "scriptInputParams":[],
    "tagList":[],
    "scriptAttachments":[],
    "scriptContent":base64.b64encode(content),
  }
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def delete(script):
  '''
    API : /scripts/1234 or /scripts?id=1234
    Method : DELETE
  '''
  path = '/scripts/' + str(script['scriptId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  request.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def update(script, name = '', type = '', content = '', description = '', params = [], tags = [] ):
  '''
    FIXME, not complete
    API : /scripts/1234
    Method : POST
    URL Structure: https://<servername>/v0/scripts?access_token=<valid token generated by authentication>
    Input : Json payload like 
    {
    "scriptName":"Test script",
    "scriptType":"bat",
    "scriptDescription":"",
    "scriptInputParams":[],
    "tagList":[],
    "scriptAttachments":[],
    "scriptContent":"bGluZTEKbGluZTIKbGluZTMKbGluZTQKbGluZTUKZWNobyAnSGknCg=="
    }
  '''
  #FIXME, no script attachments
  path = '/scripts/' + str(script['scriptId'])
  parameters = []
  url = userinfo.geturl(path)
  payload = {
    "scriptName":name,
    "scriptType":type,
    "scriptDescription":base64.b64encode(description),
    "scriptInputParams":[],
    "tagList":[],
    "scriptAttachments":[],
    "scriptContent":base64.b64encode(content),
  }
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData
