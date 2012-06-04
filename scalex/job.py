import urllib
import urllib2
import json
#
import userinfo
from scalex import script

def getJobsForScript(scriptid):
  '''arguments: type
    0 is myscripts
    1 is orgscripts
    default is 0
    '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  payload = {
    'companyId': userinfo.companyid,
    'scriptId': str(scriptid),
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'joblist',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getRuns(jobid):
  '''
  '''
  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'jobId': jobid,
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'rundetail',
    'rid':userinfo.rid,
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getOutputsForRun(jobId, projectId, projectRunId):
  '''
  '''
  payload = {
  'companyId': userinfo.companyid,
  'user': str(userinfo.userid),
  'role': userinfo.rolename,
  'projectRunId': projectRunId,
  'projectId': projectId,
  'jobId': jobId,
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'runoutput',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request).read()
  data = json.loads(response)['data'];
#  outputs = []
  
#  for index,item in enumerate(data):
#    o1 = base64.b64decode(item['output'])
#    truncated = 'N'
#    if len(o1) > 500:
#      truncated = 'Y'             
#    outputs.append({
#                        'target' : item['agentId'], 
#                        'outputStatus' : item['stepExitCode'], 
#                        'output': o1[0:500],
#                        'truncated' :  truncated 
#                        })
  
  return response

def update(name, scriptid, version, jobId, targets, arguments = [], scheduleType = 0,
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
      d = datetime.datetime.strptime(startTime, '%Y-%m-%d-%H:%M')
      startTime = int(time.mktime(d.timetuple())*1000)
  elif scheduleType == 1:
    if repeatCount == 0 and endTime == 0:
      #wrong
      pass
    if endTime != 0:
      d = datetime.datetime.strptime(endTime, '%Y-%m-%d-%H:%M')
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
    params = json.loads(script.getContent(scriptid, version))['data']
    for p in params['scriptInputParams']:
      arguments.append(p['parameterDefaultValue'])
  
  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'scriptId': scriptid,
    'version': str(version),
    'scriptArgs': arguments,
    'targets': targets,
    'destInstallDir': None,
    'scheduleType': type[scheduleType],
    'startTime': startTime,
    'endTime': endTime,
    'repeatCount': repeatCount,
    'repeatInterval': repeatInterval,
    'cronExpr': cronExpr,
    'timeZone': timeZone,
    'name': name,
    'description': name,
    'jobId': jobId,
    'jobName': None,
    'scriptType': None
  }
  postData = 'operation=editjobbyscript&payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob?rid=' + userinfo.rid
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def cancel(jobId):
  '''
  payload={"companyId":10274, "user":"10002", "role":"Admin", "jobId":638, "parentJobId":0, "jobName":"testRun (6)", "jobDescription":"This job is auto-created", "actionGroupId":639, "targetGroupId":639, "targetDetailBeans":[{"agentId":40, "companyId":10274, "user":"10002", "role":"Admin", "ipAddress":"10.211.31.18", "hostName":"domU-12-31-39-0A-1C-E4", "nodeMask":"", "nodeIf":"12:31:39:0a:1c:e4", "nodeMac":"eth0", "nodeHw":"i686", "nodeDesc":"", "osName":"Linux", "osVer":"2.6.35.14-97.44.amzn1.i686", "osCat":"#1 SMP Mon Oct 24 16:03:22 UTC 2011"}], "scheduleBeans":[{"companyId":0, "user":null, "role":null, "name":"trigger_testRun (6)", "scheduleId":8165, "jobName":"testRun (6)", "jobId":638, "scheduleType":2, "startTime":1338798839315, "endTime":86560732799315, "repeatCount":0, "repeatInterval":0, "cronExpr":"0 * * * 6 ?", "timeZone":"Australia/Perth", "calendarType":"no calendar", "nextFireTime":1338801120000, "prevFireTime":1338801060000, "timesTriggered":0}], "activeFlag":null, "status":"complete"}
    
    //manage.scalextreme.com/managejob?rid=1&companyid=10274&user=10002&role=Admin&operation=canceljob
  '''
  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'jobId':jobId,
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'operation':'canceljob',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData
  









