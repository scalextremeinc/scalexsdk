'''
  @undocumented: __package__
  @undocumented: create
  
  @todo:
    - Add support for update/patch.
    - Add support for cancel job.
  
  @change:
    - Delete update/patch relative API.
    - Delete cancel()
'''

import urllib
import urllib2
import json
#
from scalex import userinfo
from scalex import script

def getJobs(type = 'script', object = {}):
  '''
    Get jobs of a given script
    
    @note: Currently support script jobs only.
    @todo: Add support for update/patch job
    
    @type   type: string
    @param  type: Job type, default is B{script}. Valid value is B{script}.
    
    @type   object: dict
    @param  object: If type is script, object is the script returned by scalex.script.getScripts()
    
    @rtype: list
    @return: List of jobs
    
    @change:
      - API usage changed.
      - Add parameter B{type}
      - Add parameter B{object}
  '''
#    FIXME, currently only support script jobs.
#    API : /jobs?type=<script, template etc,>&id=<id of script, id of template etc.,>
#    Method : GET
#    URL Structure: https://<servername>/v0/jobs?type=script&id=<script id>& access_token=<valid access token>
#    Input :
#    type (required), valid values are script, template, patch, update etc.,
#    id
#  '''
#  id = str(object['scriptId'])
  assert type in ['script', 'update', 'patch'], 'wrong type'
  path = '/jobs'
  query = {
    'type': type,
  }
  if type in ['script', 'update', 'patch']:
    assert object != {}, 'no script object'
    #FIXME, update and patch not support
    query['id'] = object['scriptId']
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _create_or_update_job(path, name, script, targets, arguments = [], type = 'script', serverGroups = [], 
                          scheduleType = 0, startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0):
  '''
    For Internal Use ONLY
  '''
#    For Internal Use ONLY
#    FIXME, what about VERSION??
#    API : /jobs
#    Method : POST
#    URL structure: https://<servername>/v0/jobs
#    Input param: Following json payload
#    {
#    "name":"Sample Job",
#    "scriptId":2446,
#    "targets":[140],
#    "scriptArgs":["Test1","Test2"],
#    "type":"script",
#    
#    "repeatCount":0,
#    "serverGroups":[],
#    "endTime":0,
#    "startTime":1339353250011,
#    "scheduleType":12,
#    "taskParameters":[],
#    "repeatInterval":0
#    }
#    scheduleType: 0, Run Once
#    1, Recurring
#  '''
  _schecule_type = [12, 14, 2]
  if scheduleType == 0:
    if startTime != 0:
      d = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H:%M")
      startTime = int(time.mktime(d.timetuple())*1000)
  elif scheduleType == 1:
    if repeatCount == 0 and endTime == 0:
      assert False, 'wrong schedule'
    if endTime != 0:
      d = datetime.datetime.strptime(endTime, "%Y-%m-%d-%H:%M")
      endTime = int(time.mktime(d.timetuple())*1000)
    pass
  else:
    assert False, 'wrong schedule type'
  scheduleType = _schecule_type[scheduleType]
  if not isinstance(targets, list):
    t = targets
    targets = []
    targets.append(t)
  agents = []
  for n in targets:
    agents.append(n['agentId'])
  payload = {
    "name":name,
    "scriptId":script['scriptId'],
    "targets":agents,
    "scriptArgs":arguments,
    "type":type,
    "repeatCount":repeatCount,
    "serverGroups":serverGroups,
    "endTime":endTime,
    "startTime":startTime,
    "scheduleType":scheduleType,
    "taskParameters":[],
    "repeatInterval":repeatInterval,
  }
  postData = json.dumps(payload)
  url = userinfo.geturl(path)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def create(name, script, targets, arguments = [], type = 'script', serverGroups = [], 
           scheduleType = 0, startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0):
  
  path = '/jobs'
  return _create_or_update_job(path, name, script, targets, arguments, type, serverGroups,
                               scheduleType, startTime, repeatInterval, endTime, repeatCount)


def update(job, name, script, targets, arguments = [], type = 'script', serverGroups = [], 
           scheduleType = 0, startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0):
  '''
    Update a job
    
    @todo: params and tags not implement
    
    @type   job: dict
    @param  job: Job returned by getJobs()
    
    @type   name: string
    @param  name: Job Name 
    
    @type   script: dict
    @param  script: Script returned by getScripts()
    
    @param  targets: Targets returned by scalex.node.getNodes() or a single node.
    
    @type   arguments: list
    @param  arguments: Arguments of the script, default is []
    
    @type   scheduleType: int
    @param  scheduleType: Schedule type of job, default is 0, valid values are:
      - B{0}, Run Once
      - B{1}, Recurring
    
    @param  startTime: Start time formatted like B{2012-12-12-00:00}, default is now, 
    
    @param  repeatInterval: Repeat interval of recurring schedule, default is 60 mins. 
    
    @param  endTime: End time of recurring schedule, formatted like B{2012-12-12-00:00}.
    You must specify this argument if you want to schedule a recurring job and with a repeat interval.
    
    @type   repeatCount: int
    @param  repeatCount: Repeat count of a recurring scheduled job.
    
    @rtype: dict
    @return: Job just updated
    
    @change:
      - Delete Cron Expression support
    
  '''
#    FIXME
#    scheduleType: 0, Run Once
#    1, Recurring
#    2, Cron Schedule (Advanced)
#    '''
  path = '/jobs/' + str(job['jobId'])
  return _create_or_update_job(path, name, script, targets, arguments, type, serverGroups,
                               scheduleType, startTime, repeatInterval, endTime, repeatCount)
#
#def _appliedUpdatesOrPatches(path):
#  '''
#  '''
#  value = {
#    'companyid':userinfo.companyid,
#    'user':userinfo.userid,
#    'role':userinfo.rolename,
#    'rid':userinfo.rid
#  }
#  query = urllib.urlencode(value)
#  url = '%s%s?%s' % (userinfo.domain, path, query)
#  payload = {
#    'companyId': userinfo.companyid,
#    'user': str(userinfo.userid),
#    'role': userinfo.rolename,
#    'scriptId': 0
#  }
#  postData = 'payload=' + json.dumps(payload)
#  request = urllib2.Request(url, postData)
#  request.add_header('cookie', userinfo.cookie)
#  response = urllib2.urlopen(request)
#  returnData = json.loads(response.read())
#  return returnData
#
#def getUpdateJobs():
#  '''
#  '''
#  updatesPath = '/managejob/appliedupdates'
#  return _appliedUpdatesOrPatches(updatesPath)
#
#def getPatchJobs():
#  '''
#  '''
#  patchesPath = '/managejob/appliedpatches'
#  return _appliedUpdatesOrPatches(patchesPath)
#
def getRuns(job):
  '''
    Get runs of a given job.
     
    @type   job: dict
    @param  job: Job returned by getJobs()

    @rtype: list
    @return: List of runs
    
    @change:
      - Not changed

  '''
#    NOTE, no runid
#    API: /jobs/{jobid}/runinfo
#    Method: GET
#    URL structure: https://<servername>/v0/jobs/{jobid}/runinfo?access_token=<valid access token>
#    Input: runid (optional), can specify runid
#    Output:
#    [{"jobId":1814,"taskPropertyBeans":[],"status":"complete","role":"Admin","companyId":40042,"projectId":69,"runId":65,"user":"10093","runTimestamp":1339099219184}]
#  '''
  path = '/jobs/%s/runinfo' % (job['jobId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData
  
def getOutputs(run):
  '''
    Get outputs of a given run.
    
    @type   run: dict
    @param  run: Run returned by getRuns()
    
    @rtype: list
    @return: List of outputs
    
    @change:
      - Not changed

  '''
#    API : /jobs/{jobid}/runoutput?runid=<valid runid>
#    Method : GET
#    URL structure: https://<servername>/v0/jobs/{jobid}/runoutput?runid=<validrunid>&access_token=<valid access token>
#    Input : runid(required)
#  '''
  path = '/jobs/%s/runoutput' % (str(run['jobId']))
  query = {
    'runid':run['runId']
  }
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData
#
#def cancel(job):
#  '''
#    //manage.scalextreme.com/managejob?rid=1&companyid=10274&user=10002&role=Admin&operation=canceljob
#  '''
#  userinfo.check()
#
#  payload = {
#    'companyId': userinfo.companyid,
#    'user': str(userinfo.userid),
#    'role': userinfo.rolename,
#    'jobId':job['jobId'],
#  }
#  postData = 'payload=' + json.dumps(payload)
#  url = userinfo.domain + '/managejob'
#  value = {
#    'companyid':userinfo.companyid,
#    'user':userinfo.userid,
#    'role':userinfo.rolename,
#    'operation':'canceljob',
#    'rid':userinfo.rid
#  }
#  query = urllib.urlencode(value)
#  url = url + '?' + query
#  request = urllib2.Request(url, postData)
#  request.add_header('cookie', userinfo.cookie)
#  response = urllib2.urlopen(request)
#  returnData = json.loads(response.read())
#  return returnData
#  









