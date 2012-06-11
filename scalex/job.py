import urllib
import urllib2
import json
#
from scalex import userinfo
from scalex import script

def getJobs(script):
  '''arguments: type
    0 is myscripts
    1 is orgscripts
    default is 0
  '''
  userinfo.check()
  payload = {
    'companyId': userinfo.companyid,
    'scriptId': str(script['scriptId']),
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

def _appliedUpdatesOrPatches(path):
  '''
  '''
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.userid,
    'role':userinfo.rolename,
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = '%s%s?%s' % (userinfo.domain, path, query)
  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'scriptId': 0
  }
  postData = 'payload=' + json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getUpdateJobs():
  '''
  '''
  updatesPath = '/managejob/appliedupdates'
  return _appliedUpdatesOrPatches(updatesPath)

def getPatchJobs():
  '''
  '''
  patchesPath = '/managejob/appliedpatches'
  return _appliedUpdatesOrPatches(patchesPath)

def getRuns(job):
  '''
  '''
  userinfo.check()

  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'jobId': job['jobId'],
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

def getOutputs(run):
  '''
  '''
  userinfo.check()

  payload = {
  'companyId': userinfo.companyid,
  'user': str(userinfo.userid),
  'role': userinfo.rolename,
  'projectRunId': run['projectRunId'],
  'projectId': run['projectId'],
  'jobId': run['jobId'],
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
  response = urllib2.urlopen(request)
  data = json.loads(response.read())
  returnData = data
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
  
  return returnData

def update(name, script, job, targets, arguments = [], scheduleType = 0,
           startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0, cronExpr = None, timeZone = ''):
  '''
    FIXME
    scheduleType: 0, Run Once
    1, Recurring
    2, Cron Schedule (Advanced)
    '''
  # 
  userinfo.check()

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
#  if len(arguments) == 0:
#    #FIXME
#    params = json.loads(script.getContent(scriptid, version))['data']
#    for p in params['scriptInputParams']:
#      arguments.append(p['parameterDefaultValue'])
  
  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'scriptId': script['scriptId'],
    'version': str(script['version']),
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
    'jobId': job['jobId'],
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

def cancel(job):
  '''
    //manage.scalextreme.com/managejob?rid=1&companyid=10274&user=10002&role=Admin&operation=canceljob
  '''
  userinfo.check()

  payload = {
    'companyId': userinfo.companyid,
    'user': str(userinfo.userid),
    'role': userinfo.rolename,
    'jobId':job['jobId'],
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
  









