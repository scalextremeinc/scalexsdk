#!/usr/bin/env python

import cmd
import urllib
import urllib2
import uuid
import json
import base64
import sys
import scalex
import time
#
import scalex

class scalex_cmd(cmd.Cmd):
  companies = []
  roles = []
  myscripts = []
  orgscripts = []
  scripts = []
  process = []
  nodes = []
  jobs = []
  runs = []
  patches = []
  updates = []
  patchJobs = []
  updateJobs = []
  audits = []

  currentWindows = ''
  currentUnix = ''

  def __init__ ( self ):
    self.prompt = "scalex>>";
    cmd.Cmd.__init__(self);

  def emptyline(self):
    return;

  def do_help(self,s):
    s = s.strip();
#    if ( s == "login" ) :
#      self.help_login();
    if ( s == "get" ):
      self.help_get();
    elif ( s == "set" ):
      self.help_set()
    elif ( s == "script" ):
      self.help_script();
    elif ( s == "exit" ):
      self.help_exit();
    elif ( s == "job" ):
      self.help_job();
    elif ( s == "apply" ):
      self.help_apply();
    elif ( s == "exit" ):
      self.help_exit();
    else :
      print "Available Command:"
#      print "\t login"
      print "\t get"
      print "\t set"
      print "\t script"
      print "\t job"
      print "\t apply"
      print "\t exit"
      print "help COMMAND for more information on a specific command."
    return

#  def help_login(self):
#    print "login client_id client_secret"

  def help_job(self):
    print "job cancel INDEX"

  def help_get(self):
    print "get companies => get companies"
    print "get roles => get roles"
    print "get nodes  => get nodes"
    print "get node INDEX => get node info"
    print "get orgscripts => get org scripts"
    print "get myscripts => get my scripts"
    print "get arguments INDEX => get arguments for script"
    print "get jobs INDEX => get jobs for script"
    print "get runs INDEX => get runs for jobs"
    print "get output INDEX => get output for runs"
    print "get nodesforupdate INDEX_updates => get nodes which have the listed updates missing"
    print "get nodesforpatch INDEX_patches => get nodes which have the listed patches missing"
    print 'get updates INDEX => get missing updates for node'
    print 'get patches INDEX => get missing patches for a node'
    print 'get updatejobs => get all update jobs'
    print 'get patchjobs => get all patch jobs'

  def help_set(self):
    print 'set company INDEX'
    print 'set role INDEX'
    print 'set client_id CLIENT_ID'
    print 'set client_secret CLIENT_SECRET'

  def help_script(self):
    print 'script run job_name script_INDEX node_INDEX,node_INDEX startTime=2012-09-02-12:12 parameters=PARAM1,PARAM2'
    print 'nodes are comma separated example: 1,2'
    print 'for instance: run script 0 at node 0,1,2 at 2012-08-01-00:00, two parameters, install and -v'
    print '>>script run test_run 0 0,1,2 startTime=2012-08-01-00:00 parameters=install,-v'
    print 'run script 0 at node 0 now, two parameters, foo bar and -v'
    print '>>script run test_run_now 0 0 parameters=foo bar,-v'
    print "export script 7 into a directory called /tmp/scripts"
    print '>>>script export /tmp/scripts 7'
    print "import a single script from a directory called /tmp/scripts"
    print '>>>script importone /tmp/scripts'
    #print 'startTime 0 means run now, or schedule time format 2012-06-02-12:12'
    #print 'parameters are space separated example: argument1 argument2'

  def help_cancel(self):
    print 'cancel update/patch/job INDEX'

  def help_apply(self):
    print 'apply patches / updates to one or more machines'
    print 'apply update/patch node_Index1,node_Index2 patch_Index1,patch_Index2 jobname [startTime]'
    print 'startTime 0 means run now, or schedule time format 2012-06-02-12:12'
    print 'example: apply update 0,1 0,1,2,3 job_name 2012-01-01-01:01'

  def help_exit(self):
    print "exit --- exit this program"

#  def do_login(self, s):
#    l = s.split()
#    if len(l)!=2:
#      self.help_login();
#      return
#    appkey = l[0].strip();
#    appsecret = l[1].strip();
#    sx = None;
#    try :
##      scalex.login( username , password )
#      scalex.setClientId(appkey)
#      scalex.setClientSecret(appsecret)
##      if ret['result'] == 'SUCCESS':
##        print "Login Successfully"
##      else :
##        print "Login Failed: " + ret
#    except Exception,e :
#      print "Login Failed:"
#      print e

  def do_set(self, s):
    l = s.split()
    if len(l)!=2:
      self.help_set();
      return
    try :
      s = s.strip()
      param = s.split();
      if ( param[0] == "company" ):
        scalex.company.set(self.companies[int(param[1])]);
        print 'set company ok'
      elif ( param[0] == "role" ):
        scalex.role.set(self.roles[int(param[1])]);
        print 'set role ok'
      elif param[0] == 'client_id':
        scalex.setClientId(param[1])
      elif param[0] == 'client_secret':
        scalex.setClientSecret(param[1])
      else :
        self.help_set();
    except Exception,e:
      print "Unknown Error:" , e

  def do_get(self,s):
    try :
      s = s.strip()
      param = s.split()
      if len(param) == 0:
          self.help_get()
          return

      param[0] = param[0].lower()
      if ( param[0] == "companies" ):
        coms = scalex.company.getCompanies();
        self.companies = coms
        for c in coms:
          print 'index: [%d] %s companyId:%d' % (coms.index(c), c['name'], c['companyId'])
      elif ( param[0] == "roles" ):
        roles = scalex.role.getRoles();
        self.roles = roles
        for i in roles:
          print 'index: [%d] %s' % (roles.index(i), i)
      elif (param[0] == "accesstoken" ):
          print scalex.userinfo.access_token
      elif ( param[0] == "myscripts" ):
        scripts = scalex.script.getScripts(type='user');
        self.scripts = scripts
        for i in scripts:
          print 'index: [%d] name: %s' % (scripts.index(i), i['scriptName'])
      elif ( param[0] == "orgscripts" ):
        scripts = scalex.script.getScripts(type='org');
        self.scripts = scripts
        for i in scripts:
          print 'index: [%d] name: %s' % (scripts.index(i), i['scriptName'])

      elif (param[0] == "process"):
          process = scalex.process.getProcess()
          self.process = process
          for i in process:
            print 'index: [%d] name: %s' % (process.index(i), i['name'])

      elif ( param[0] == "jobs" ):
        if len(param) < 2:
          self.help_get()
        i = int(param[1])
        script = self.scripts[i]
        jobs = scalex.job.getJobs(object=script);
        self.jobs = jobs
        for i in jobs:
          print 'index: [%d] name: %s' % (jobs.index(i), i['jobName'])

      elif ( param[0] == "runs" ):
        if len(param) < 2:
          self.help_get()
        i = int(param[1])
        job = self.jobs[i]
        self.runs = scalex.job.getRuns(job);
        for i in self.runs:
          print 'index: [%d] status: %s task name: %s' % (self.runs.index(i), i['status'], job['jobName'])

      elif param[0] == 'arguments':
        if len(param) < 2:
          self.help_get()
        index = int(param[1])
        script = self.scripts[index]
        content = scalex.script.getContent(script)
        print 'script: %s' % (content['scriptName'])
        for arg in content['scriptInputParams']:
          print 'argu: %s\ttype: %s\tdefault value: %s' % (arg['parameterKey'],arg['parameterDataType'],arg['parameterDefaultValue'])

      elif ( param[0] == "output" ):
        if len(param) < 2:
          self.help_get()
        i = int(param[1])
        run = self.runs[i]
        data  = scalex.job.getOutputs(run)
        outputs = []
        for index,item in enumerate(data):
            o1 = base64.b64decode(item['output'])
            truncated = 'N'
            if len(o1) > 500:
                truncated = 'Y'
            outputs.append({
                   'target' : item['agentId'],
                   'outputStatus' : item['stepExitCode'],
                   'output': o1[0:500],
                   'truncated' :  truncated
            })
#{u'status': u'running', u'stepId': 4315, u'projectRunId': 8046, u'stepTag': u'metaphas-1339649867010', u'companyId': 40034, u'stepTagLocation': u'C:/Program Files (x86)/ScaleXtreme/mitos/proc', u'stepType': u'step', u'stepExitCode': u'0', u'stepRunId': 27935, u'role': u'Admin', u'user': u'7r@gmail.com', u'stepOutputType': 1, u'taskPropertyBeans': [], u'output': u'SW4gcHJvZ3Jlc3M=', u'agentId': 278}
# NOTE, output format has changed, as shown above, so I have to comment this line
#        print 'jobname:', run['stepRunLogBeans'][0]['taskName']
        print 'run status:', run['status']
        from time import ctime
        print 'run time: ', ctime(int(run['runTimestamp'])/1000)
        print '-----------------'
        for output in outputs:
            print 'target:', output['target']
            print 'outputStatus:', output['outputStatus']
            if output['truncated'] == 'Y' :
                print 'output (truncated - more than 500 chars):'
            else:
                print 'output:'
            print output['output']
            print '-----------------'

      elif ( param[0] == "nodes" ):
        self.nodes = scalex.node.getNodes()
        for n in self.nodes:
          print 'index:[%d] nodeName: %s' % (self.nodes.index(n), n['nodeName'])
      elif ( param[0] == "node" ):
          if len(param) != 2 :
              self.help_get()
              return
          self.nodes = scalex.node.getNodes()
          index = int(param[1])
          if len(self.nodes) > index:
              node = self.nodes[index]
              print 'index:[%d] nodeName: %s nodeId: %d ' % (index, node['nodeName'], node['nodeId'])
              print 'Properties:'
              attributeList = sorted(node['nodeAttrList'], key = lambda k: k['attributeName'])
              for x in attributeList:
                  print "%s : %s" % (x['attributeName'], x['attributeValue'])
          else:
              print 'invalid index '+index
      elif ( param[0] == "patches" ):
        node = self.nodes[int(param[1])]
        if 'Windows' not in str(node):
          print 'this is not a windows node'
          return
        self.currentWindows = node
        patches = scalex.node.getPatches(node)
        if patches == []:
          print 'node is up to date'
          return
        if not isinstance(patches, list):
          u = patches
          patches = []
          patches.append(u)
        self.patches = patches
        for n in self.patches:
          print 'index:[%d] name: %s\tcategory: %s' % (self.patches.index(n), n['name'], n['classification'])
      elif ( param[0] == "updates" ):
        node = self.nodes[int(param[1])]
        if 'Linux' not in str(node):
          print 'this is not a unix node'
          return
        self.currentUnix = node
        updates = scalex.node.getUpdates(node)
        if updates == []:
          print 'node is up to date'
          return
        if not isinstance(updates, list):
          u = updates
          updates = []
          updates.append(u)
        self.updates = updates
        for n in self.updates:
          print 'index:[%d] version:%s\trelease:%s\tname: %s' % (self.updates.index(n), n['updateversion'], n['updaterelease'], n['name'])

      elif param[0] == 'nodesforpatch':
        if len(param) < 2:
          self.help_get()
          return
        node = self.currentWindows
        patches = []
        if 'Windows' in str(node):
          for i in param[1].split(','):
            patches.append(self.patches[int(i)])
        else:
          for i in param[1].split(','):
            patches.append(self.updates[int(i)])
        others = scalex.node.getAllAgentsWithPatch(patches)
        for agent in others:
          for n in self.nodes:
            if n['agentId'] == agent:
              print 'index: [%d] nodeName: %s' % (self.nodes.index(n), n['nodeName'])

      elif param[0] == 'nodesforupdate':
        if len(param) < 2:
          self.help_get()
          return
        node = self.currentUnix
        patches = []
        if 'Windows' in str(node):
          for i in param[1].split(','):
            patches.append(self.patches[int(i)])
        else:
          for i in param[1].split(','):
            patches.append(self.updates[int(i)])
        others = scalex.node.getAllAgentsWithPatch(patches)
        for agent in others:
          for n in self.nodes:
            if n['agentId'] == agent:
              print 'index: [%d] nodeName: %s' % (self.nodes.index(n), n['nodeName'])
        print 'index: [%d] nodeName: %s' % (self.nodes.index(node), node['nodeName'])

      elif param[0] == 'updatejobs':
        self.updateJobs = scalex.job.getJobs('update')
        for i in self.updateJobs:
          print 'index:[%d] jobname: %s' % (self.updateJobs.index(i), i['jobName'])
      elif param[0] == 'patchjobs':
        self.patchJobs = scalex.job.getPatchJobs('patchjobs')
        for i in self.updateJobs:
          print 'index:[%d] jobname: %s' % (self.updateJobs.index(i), i['jobName'])
      elif param[0] == 'audits':
        node = self.nodes[int(param[1])]
        self.audits = scalex.node.getAudits(node)
        for audit in self.audits:
          print 'name: ', audit['name']
      else:
        self.help_get()
    except Exception,e:
      print "Unknown Error:" , e

  def do_script(self,s):
    try :
      param = s.split()
      if ( param[0] == "run" ):
        if len(param) < 4:
          self.help_script()
          return
        script = self.scripts[int(param[2])]
        targets = []
        for i in param[3].split(','):
          targets.append(self.nodes[int(i)])
        name = param[1]
        arguments = []
        startTime = 0
        try:
          for p in param[4:]:
            kv = p.split('=')
            paramName = kv[0]
            paramValue = kv[1]
            if paramName == 'startTime' and paramValue != 'now':
              startTime = paramValue
            elif paramName == 'parameters':
              i = param.index(p)
              arguments = s.split('parameters=')[1].split(',')
        except:
          pass
        #        scheduleType = int(param[5])
        #        #schedule type should be one of 0 1 2
        #        startTime = param[6]
        result = scalex.script.run(name, script, targets, arguments = arguments, startTime = startTime)
        print result
      elif ( param[0] == "export" ):
          script = self.scripts[int(param[1])]
          dname = param[2]
          result = scalex.script.export(dname, script)
          print result
      elif ( param[0] == "importone" ):
          dname = param[1]
          result = scalex.script.importOne(dname)
          print result
    except Exception,e:
      print "Unknown Error:" , e

  def do_job(self,s):
    try:
      param = s.split()
#      FIXME, cancel runs, not jobs
      if param[0] != 'cancel' and param[1] not in ['update', 'patch', 'job']:
        self.help_job()
        return
      index = int(param[1])
      jobs = {'update': self.updateJobs, 'patch':self.patchJobs, 'script':self.jobs}
      job = jobs[param[1]][index]
      result = scalex.job.cancel(job)
      print result
    except:
      pass
  def do_apply(self,s):
    try:
      param = s.split()
      #apply update 1,2 1,2,3 name time
      #update/patch nodes patches name [time]
      if param[0] != 'update' and param[0] != 'patch':
        self.help_apply()
        return
      targets = []
      for i in param[1].split(','):
        targets.append(self.nodes[int(i)])
      updates = []
      if param[0] == 'update':
        updateList = self.updates
      else:
        updateList = self.patches
      for i in param[2].split(','):
        updates.append(updateList[int(i)])
      name = param[3]
      time = 0
      try:
        time = param[4]
      except:
        pass
      if 'Linux' in str(targets[0]):
        result = scalex.node.applyUpdates(name, targets, updates, startTime = time)
      else:
        result = scalex.node.applyPatches(name, targets, updates, startTime = time)
      print  result
    except Exception, e:
      print "Unknown Error:" , e

  def do_EOF(self, line):
    print ""
    return True

  def do_exit(self,s):
    sys.exit(0);

if __name__ == '__main__':
  scalex_cmd().cmdloop();
  sys.exit(0);
