#!/usr/bin/env python

import urllib
import urllib2
import uuid
import json
import base64
import datetime
import time
import sys
import hashlib

class scaleXtreme():
  '''
    get companies
    set company
    get roles
    set role
    get my scripts
    get org scripts
    get nodesforrole
    run script
    get jobs for script
    get runs for job
    get output for run
  '''
  rid = str(uuid.uuid4())
  
  def __init__(self, usr, pwd):

    if sys.version_info < (2, 5):
      raise 'you must use python 2.5 or greater'

    self.cookie = ''
#
    self.user = usr
    self.pwd = hashlib.md5(pwd).hexdigest()
    self.userId = ''
    self.companies = []
    self.currentCompanyId = ''
    self.roles = []
    self.currentRole = ''
    self.nodes = []
    self.myScripts = []
    self.orgScripts = []
    self.jobs = {}
    self.runs = {}
    self.outputs = []
    self.arguments = {}
    self.domain = 'https://manage.scalextreme.com'
  
  def login(self):
    '''
    '''
    url = self.domain + '/scalex/acl/authenticate?type=scalex&rid=%s' % (self.rid)
    value = {
      'user':self.user,
      'password':self.pwd
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData)
    self.cookie = response.headers.get('Set-Cookie')
    usrInfo = json.loads(response.read())
    if ( usrInfo['result'] == 'FAILURE' ):
      return False, usrInfo['data']
    self.userId = usrInfo['data']['userID']
    return True,self.userId
#    print self.cookie

  def getCompanies(self):
    url = self.domain + '/scalex/acl/usercompanies?rid=%s' % (self.rid)
    value = {
        'userId':self.userId
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData).read()

    self.companies = json.loads(response)['data']
    return response
  
  def setCompany(self, companyId):
    self.currentCompanyId = companyId

  def getRoles(self):
    '''
    URL: <DOMAIN>/scalex/acl/userroles?rid=
    Post Data: companyId=11307&user=ol
    '''
    if self.currentCompanyId == '':
      print 'you need setCompany first'
      return
    
    url = self.domain + '/scalex/acl/userroles?rid=%s' % (self.rid)
    value = {
      'companyId':self.currentCompanyId,
      'user':self.user
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData).read()
    roleList = json.loads(response)['data']
    self.roles = []
    for i in roleList:
      self.roles.append(base64.b64decode(i))
    return response
#    self.currentRole = self.roles[0]
#    print postData, response

  def setRole(self, roleName):
    self.currentRole = roleName

  def isReady(self):
    if self.currentCompanyId == '':
      print 'you need setCompany and setRole first'
      return False
    if self.currentRole == '':
      print 'you need setRole first'
      return False
    return True

  def getNodes(self):
    '''
    Requesting URL: <DOMAIN>/scalex/acl/nodelistbyrole?rid=4AC31284-CE1A-47DF-A771-E764C09EB555
    Post Data: companyId=11307&role=Admin&user=olivier.tarroux%40edifixio.com&
    '''
#    need set company and role first
#
    if not self.isReady():
      return
#
    url = self.domain + '/scalex/acl/nodelistbyrole?rid=%s' % (self.rid)
    value = {
      'companyId':self.currentCompanyId,
      'role':self.currentRole,
      'user':self.user
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData).read()
    self.nodes = json.loads(response)['data']
    return response
#    print self.nodes[0]['nodeName']

  def getMyScripts(self):
    '''
      this request need cookie
      <DOMAIN>/library?companyid=10476&user=10473&role=Admin&operation=userscripts&rid=7861539B-6EA3-4C0A-9FEA-EF961E44233E
      '''
    #    need set company and role first
    if not self.isReady():
      return
#    
    url = self.domain + '/library'
    value = {
      'companyid':self.currentCompanyId,
      'user':self.userId,
      'role':self.currentRole,
      'operation':'userscripts',
      'rid':self.rid
    }
    query = urllib.urlencode(value)
    url = url + '?' + query
    request = urllib2.Request(url, '')
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    self.myScripts = json.loads(response)['data']
    return response
  
  def getOrgScripts(self):
    '''
      this request need cookie
      <DOMAIN>/library?rid=7861539B-6EA3-4C0A-9FEA-EF961E44233E&companyid=10476&user=10473&role=Admin&operation=orgscripts
      '''
    if not self.isReady():
      return
    #    
    url = self.domain + '/library'
    value = {
      'companyid':self.currentCompanyId,
      'user':self.userId,
      'role':self.currentRole,
      'operation':'orgscripts',
      'rid':self.rid
    }
    query = urllib.urlencode(value)
    url = url + '?' + query
    request = urllib2.Request(url, '')
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    self.orgScripts = json.loads(response)['data']
    return response

  def getJobsForScript(self, scriptId):
    '''
    <DOMAIN>/managejob?rid=2794A488-BC90-43DD-B13B-292233803B91&companyid=10361&user=10002&role=Admin&operation=joblist
    '''
    payload = {
      "companyId": self.currentCompanyId,
      "scriptId": str(scriptId),
      "user": str(self.userId),
      "role": self.currentRole,
    }
    postData = 'payload=' + json.dumps(payload)
    url = self.domain + '/managejob'
    value = {
      'companyid':self.currentCompanyId,
      'user':self.userId,
      'role':self.currentRole,
      'operation':'joblist',
      'rid':self.rid
    }
    query = urllib.urlencode(value)
    url = url + '?' + query
    request = urllib2.Request(url, postData)
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    self.jobs[scriptId] = json.loads(response)['data']
    return response

#      get runs for job
  def getRunsForJob(self, jobId):
    '''
    <DOMAIN>/managejob?rid=2794A488-BC90-43DD-B13B-292233803B91&companyid=10361&user=10002&role=Admin&operation=rundetail
    '''
    payload = {
      "companyId": self.currentCompanyId,
      "user": str(self.userId),
      "role": self.currentRole,
      "jobId": jobId,
    }
    postData = 'payload=' + json.dumps(payload)
    url = self.domain + '/managejob'
    value = {
      'companyid':self.currentCompanyId,
      'user':self.userId,
      'role':self.currentRole,
      'operation':'rundetail',
      'rid':self.rid
    }
    query = urllib.urlencode(value)
    url = url + '?' + query
    request = urllib2.Request(url, postData)
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    self.runs[jobId] = json.loads(response)['data']
    return response

  def getOutputForRun(self, jobId, projectId, projectRunId):
    '''
      <DOMAIN>/managejob?rid=&companyid=10361&user=10002&role=Admin&operation=runoutput
      '''
    payload = {
      "companyId": self.currentCompanyId,
      "user": str(self.userId),
      "role": self.currentRole,
      "projectRunId": projectRunId,
      "projectId": projectId,
      "jobId": jobId,
#      "runTimestamp": 1338473760049,
#      "status": "failed",
#      "jobName": None,
#      "jobRunOutputBeans": []
    }
    postData = 'payload=' + json.dumps(payload)
    url = self.domain + '/managejob'
    value = {
      'companyid':self.currentCompanyId,
      'user':self.userId,
      'role':self.currentRole,
      'operation':'runoutput',
      'rid':self.rid
    }
    query = urllib.urlencode(value)
    url = url + '?' + query
    request = urllib2.Request(url, postData)
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    data = json.loads(response)['data'];
    self.outputs = []
    
    for index,item in enumerate(data):
        o1 = base64.b64decode(item['output'])
        truncated = 'N'
        if len(o1) > 500:
            truncated = 'Y'             
        self.outputs.append({
            'target' : item['agentId'], 
            'outputStatus' : item['stepExitCode'], 
            'output': o1[0:500],
            'truncated' :  truncated 
        })

    return response
  
  def getParamsOfScript(self, scriptId, version):
    '''
    <DOMAIN>/library?rid=&companyid=10361&user=10002&role=Admin&operation=scriptcontent
    '''
    payload = {
      'scriptid':scriptId,
      'version':version
    }
    url = self.domain + '/library'
    value = {
      'companyid':self.currentCompanyId,
      'user':self.userId,
      'role':self.currentRole,
      'operation':'scriptcontent',
      'rid':self.rid
    }
    query = urllib.urlencode(value)
    url = url + '?' + query
    request = urllib2.Request(url, urllib.urlencode(payload))
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    returnData = json.loads(response)['data']
    self.arguments[scriptId] = returnData
    return response

  def runScript(self, params):
    '''
      this request need cookie
      <DOMAIN>/managescript?rid=22673add-18fa-4096-ae75-5030c32a3646
      '''
#    startTime 0 means run now
#    scriptId, version, targets, startTime
    name = params[0]
    scriptId = params[1]
    version = params[2]
    targets = params[3].split(',')
    startTime = params[4]
    if startTime != '0':
      d = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H:%M")
      startTime = int(time.mktime(d.timetuple())*1000)
    arguments = []
    self.getParamsOfScript(scriptId, version)
    for a in self.arguments[scriptId]['scriptInputParams']:
      arguments.append(a['parameterDefaultValue'])
    i = 0
    if len(params) > 6:  
      for argu in params[5:]:
        arguments[i] = argu
        i += 1

    payload = {
      "companyId": self.currentCompanyId,
      "user": self.userId,
      "role": self.currentRole,
      "scriptId": scriptId,
      "version": version,
      "scriptArgs": arguments,
      "targets": targets,
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
      "scriptType": None
    }
    postData = 'operation=runscript&payload=' + json.dumps(payload)
    url = self.domain +'/managescript?rid='
    request = urllib2.Request(url, postData)
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    returnData = json.loads(response)
    print 'runScript %s' % (returnData['result'])

#if __name__ == '__main__':
#  sx = scaleXtreme('karthik@scalextreme.com', '123456')
#  sx.login()
#  sx.getCompanies()
#  sx.getRoles()
  
