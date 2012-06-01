#!/usr/bin/env python

import hashlib
import urllib
import urllib2
import uuid
import json
import base64

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
  
  def info(self):
    print 'user', self.user
    print 'company id', self.currentCompanyId
    print 'role', self.currentRole
    
  
  def login(self):
    '''
    '''
    url = 'https://manage.scalextreme.com/scalex/acl/authenticate?type=scalex&rid=%s' % (self.rid)
    value = {
        'user':self.user,
        'password':self.pwd
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData)
    self.cookie = response.headers.get('Set-Cookie')
    usrInfo = json.loads(response.read())
    self.userId = usrInfo['data']['userID']
#    print self.cookie

  def getCompanies(self):
    url = 'https://manage.scalextreme.com/scalex/acl/usercompanies?rid=%s' % (self.rid)
    value = {
        'userId':self.userId
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData).read()

    self.companies = json.loads(response)['data']

  def setCompany(self, companyId):
    self.currentCompanyId = companyId

  def getRoles(self):
    '''
    URL: https://manage.scalextreme.com/scalex/acl/userroles?rid=
    Post Data: companyId=11307&user=ol
    '''
    if self.currentCompanyId == '':
      print 'you need setCompany first'
      return
    
    url = 'https://manage.scalextreme.com/scalex/acl/userroles?rid=%s' % (self.rid)
    value = {
      'companyId':self.currentCompanyId,
      'user':self.user
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData).read()
    roleList = json.loads(response)['data']
    for i in roleList:
      self.roles.append(base64.b64decode(i))
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
    Requesting URL: https://manage.scalextreme.com/scalex/acl/nodelistbyrole?rid=4AC31284-CE1A-47DF-A771-E764C09EB555
    Post Data: companyId=11307&role=Admin&user=olivier.tarroux%40edifixio.com&
    '''
#    need set company and role first
#
    if not self.isReady():
      return
#
    url = 'https://manage.scalextreme.com/scalex/acl/nodelistbyrole?rid=%s' % (self.rid)
    value = {
      'companyId':self.currentCompanyId,
      'role':self.currentRole,
      'user':self.user
    }
    postData = urllib.urlencode(value)
    response = urllib2.urlopen(url, postData).read()
    self.nodes = json.loads(response)['data']
#    print self.nodes[0]['nodeName']

  def getMyScripts(self):
    '''
      this request need cookie
      https://manage.scalextreme.com/library?companyid=10476&user=10473&role=Admin&operation=userscripts&rid=7861539B-6EA3-4C0A-9FEA-EF961E44233E
      '''
    #    need set company and role first
    if not self.isReady():
      return
#    
    url = 'https://manage.scalextreme.com/library'
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
#    print self.myScripts
  
  def getOrgScripts(self):
    '''
      this request need cookie
      https://manage.scalextreme.com/library?rid=7861539B-6EA3-4C0A-9FEA-EF961E44233E&companyid=10476&user=10473&role=Admin&operation=orgscripts
      '''
    if not self.isReady():
      return
    #    

    url = 'https://manage.scalextreme.com/library'
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
    print self.orgScripts

  def getJobsForScript(self, scriptId):
    '''
    https://manage.scalextreme.com/managejob?rid=2794A488-BC90-43DD-B13B-292233803B91&companyid=10361&user=10002&role=Admin&operation=joblist
    '''
    payload = {
      "companyId": self.currentCompanyId,
      "scriptId": str(scriptId),
      "user": str(self.userId),
      "role": self.currentRole,
#      "scriptName": "Script With Variables",
#      "version": "3",
#      "scriptType": None,
#      "scriptPlatform": None,
#      "scriptTags": None,
#      "scriptDescription": "VGVzdA==",
#      "scriptContent": None,
#      "inputParams": None,
#      "scriptAttachments": [],
#      "status": None,
#      "sku": None,
#      "scriptLocation": None,
#      "viewableFlag": None,
#      "activeFlag": None,
#      "parentScriptId": 0,
#      "parentScriptVersion": None,
#      "parentCompanyId": 0,
#      "parentUser": None,
#      "purchasedFlag": None,
#      "sharedFlag": None,
#      "scriptInputParams": []
    }
    postData = 'payload=' + json.dumps(payload)
    url = 'https://manage.scalextreme.com/managejob'
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
    print self.jobs.keys()
    print self.jobs['7'][0].keys()
  
#      get runs for job
  def getRunsForJob(self, jobId):
    '''
    https://manage.scalextreme.com/managejob?rid=2794A488-BC90-43DD-B13B-292233803B91&companyid=10361&user=10002&role=Admin&operation=rundetail
    '''
    payload = {
      "companyId": self.currentCompanyId,
      "user": str(self.userId),
      "role": self.currentRole,
      "jobId": jobId,
    }
    postData = 'payload=' + json.dumps(payload)
    url = 'https://manage.scalextreme.com/managejob'
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

  def getOutputForRun(self, jobId, projectId, projectRunId):
    '''
      https://manage.scalextreme.com/managejob?rid=&companyid=10361&user=10002&role=Admin&operation=runoutput
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
    url = 'https://manage.scalextreme.com/managejob'
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
    output = base64.b64decode(json.loads(response)['data'][0]['output'])
    return output

  def runScript(self):
    '''
      this request need cookie
      https://manage.scalextreme.com/managescript?rid=22673add-18fa-4096-ae75-5030c32a3646
      # arguments
      scriptId
      scriptVersion
      targets [], nodeId
      schedule info
      '''
    print 'FIXME, this method not finished'
    payload = {
      "companyId": self.currentCompanyId,
      "user": self.userId,
      "role": self.currentRole,
      "scriptId": 7,
      "version": "3",
      "scriptArgs": [],
      "targets": [9],
      "destInstallDir": None,
      "scheduleType": 12,
      "startTime": 0,
      "endTime": 0,
      "repeatCount": 0,
      "repeatInterval": 0,
      "cronExpr": None,
      "timeZone": None,
      "name": "python test",
      "description": "python teset",
      "jobId": 0,
      "jobName": None,
      "scriptType": None
    }
    postData = 'operation=runscript&payload=' + json.dumps(payload)
    url = 'https://manage.scalextreme.com/managescript?rid='
    request = urllib2.Request(url, postData)
    request.add_header('cookie', self.cookie)
    response = urllib2.urlopen(request).read()
    print response


#if __name__ == '__main__':
#  sx = scaleXtreme('karthik@scalextreme.com', '123456')
#  sx.login()
#  sx.getCompanies()
#  sx.getRoles()
  
