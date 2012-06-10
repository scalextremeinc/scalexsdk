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
  nodes = []
  jobs = []
  runs = []
  patches = []
  updates = []
  patchJobs = []
  updateJobs = []
  audits = []
  
  def __init__ ( self ):
    self.prompt = "scalex>>";
    cmd.Cmd.__init__(self);
  
  def emptyline(self):
    return;
  
  def do_help(self,s):
    s = s.strip();
    if ( s == "login" ) :
      self.help_login();
    elif ( s == "get" ):
      self.help_get();
    elif ( s == "set" ):
      self.help_set();
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
      print "\t login"
      print "\t get"
      print "\t set"
      print "\t script"
      print "\t exit"
      print "\t job"
      print "\t apply"
      print "help COMMAND for more information on a specific command."
    return 
  
  def help_login(self):
    print "login username password"

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
    print "get otheragents INDEX_node INDEX_updates/INDEX_patches"
    print 'get updatejobs => get update jobs'
    print 'get patchjobs => get patch jobs'
  
  def help_set(self):
    print 'set company INDEX'
    print 'set role INDEX'
  
  def help_script(self):
    print 'script run script_INDEX node_INDEX,node_INDEX job_name'
    print 'targets are comma separated example: 1,2'
    #print 'startTime 0 means run now, or schedule time format 2012-06-02-12:12'
    #print 'parameters are space separated example: argument1 argument2'
  
  def help_cancel(self):
    print 'cancel update/patch/job INDEX'
  
  def help_apply(self):
    print 'apply update/patch node_Index1,node_Index2 patch_Index,patch_Index name [time]'
    print 'example: apply update 0,1 0,1,2,3 job_name 2012-01-01-01:01'
  
  def help_exit(self):
    print "exit --- exit this program"
  
  def do_login(self, s): 
    l = s.split()
    if len(l)!=2:
      self.help_login();
      return 
    username = l[0].strip();
    password = l[1].strip();
    sx = None;
    try :
      ret = scalex.login( username , password )
      if ret['result'] == 'SUCCESS':
        print "Login Successfully"
      else :
        print "Login Failed: " + ret['data']
    except Exception,e :
      print "Login Failed:"
      print e
  
  def do_set(self, s):
    l = s.split()
    if len(l)!=2:
      self.help_set();
      return 
    try :
      s = s.strip()
      param = s.split();
      index = int(param[1])
      if ( param[0] == "company" ):
        scalex.company.set(self.companies[index]);
        print 'set company ok'
      elif ( param[0] == "role" ):
        scalex.role.set(self.roles[index]);
        print 'set role ok'
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
        coms = scalex.company.getCompanies()['data'];
        self.companies = coms
        for c in coms:
          print 'index: [%d] %s' % (coms.index(c), c['name'])
      elif ( param[0] == "roles" ):
        roles = scalex.role.getRoles()['data'];
        self.roles = roles
        for i in roles:
          print 'index: [%d] %s' % (roles.index(i), i)
      elif ( param[0] == "myscripts" ):
        scripts = scalex.script.getScripts()['data'];
        self.scripts = scripts
        for i in scripts:
          print 'index: [%d] name: %s' % (scripts.index(i), i['scriptName'])
      elif ( param[0] == "orgscripts" ):
        scripts = scalex.script.getScripts(1)['data'];
        self.scripts = scripts
        for i in scripts:
          print 'index: [%d] name: %s' % (scripts.index(i), i['scriptName'])
      
      elif ( param[0] == "jobs" ):
        if len(param) < 2:
          self.help_get() 
        i = int(param[1])
        script = self.scripts[i]
        jobs = scalex.job.getJobs(script)['data'];
        self.jobs = jobs
        for i in jobs:
          print 'index: [%d] name: %s' % (jobs.index(i), i['jobName'])
      
      elif ( param[0] == "runs" ):
        if len(param) < 2:
          self.help_get()
        i = int(param[1])
        job = self.jobs[i]
        self.runs = scalex.job.getRuns(job)['data'];
        for i in self.runs:
          print 'index: [%d] status: %s task name: %s' % (self.runs.index(i), i['status'], i[u'stepRunLogBeans'][0]['taskName'])
      
      elif param[0] == 'arguments':
        if len(param) < 2:
          self.help_get()
        index = int(param[1])
        script = self.scripts[index]
        content = scalex.script.getContent(script)['data']
        print 'script: %s' % (content['scriptName'])
        for arg in content['scriptInputParams']:
          print 'argu: %s\ttype: %s\tdefault value: %s' % (arg['parameterKey'],arg['parameterDataType'],arg['parameterDefaultValue'])
      
      elif ( param[0] == "output" ):
        if len(param) < 2:
          self.help_get()
        i = int(param[1])
        run = self.runs[i]
        outputs  = scalex.job.getOutputs(run)['data']
        
        for r in outputs:
          print 'jobname:', run['stepRunLogBeans'][0]['taskName']
          print 'status: ', r['status']
          print 'output: ', base64.b64decode(r['output'])
          print 'run at: ', time.ctime(int(run['runTimestamp'])/1000)
      #        print '-----------------'  
      #        for output in self.outputs:
      #            print 'target:', output['target']
      #            print 'outputStatus:', output['outputStatus']
      #            if output['truncated'] == 'Y' :
      #                print 'output (truncated - more than 500 chars):'
      #            else: 
      #                print 'output:'
      #            print output['output'] 
      #            print '-----------------'
      
      elif ( param[0] == "nodes" ):
        self.nodes = scalex.node.getNodes()['data']
        for n in self.nodes:
          print 'index:[%d] nodeName: %s' % (self.nodes.index(n), n['nodeName'])
      elif ( param[0] == "node" ):
          if len(param) != 2 :
              self.help_get()
              return
          self.nodes = scalex.node.getNodes()['data']
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
        if scalex.node.isUnix(node):
          print 'this is not a windows mechine'
          return
        self.patches = scalex.node.getPatches(node)['data']
        if self.patches == []:
          print 'node is up to date'
          return
        for n in self.patches:
          print 'index:[%d] name: %s\tcategory: %s' % (self.patches.index(n), n['name'], n['classification'])
      elif ( param[0] == "updates" ):
        node = self.nodes[int(param[1])]
        if not scalex.node.isUnix(node):
          print 'this is not a unix mechine'
          return

        self.updates = scalex.node.getUpdates(node)['data']
        if self.updates == []:
          print 'node is up to date'
          return
        for n in self.updates:
          print 'index:[%d] name: %s\tversion: %s\trelease:%s' % (self.patches.index(n), n['name'], n['updateversion'], n['updaterelease'])
      elif param[0] == 'otheragents':
        if len(param) < 3:
          self.help_get()
          return
        nodeIndex = int(param[1])
        node = self.nodes[nodeIndex]
        patches = []
        if scalex.node.isWindows(node):
          for i in param[2].split(','):
            patches.append(self.patches[int(i)])
        else:
          for i in param[2].split(','):
            patches.append(self.updates[int(i)])
        others = scalex.node.getOtherAgentsWithPatch(node, patches)['data']
        for agent in others:
          for n in self.nodes:
            if n['agentId'] == agent:
              print 'index: [%d] nodeName: %s' % (self.nodes.index(n), n['nodeName'])
        
        pass
      elif param[0] == 'updatejobs':
        self.updateJobs = scalex.job.getUpdateJobs()['data']
        for i in self.updateJobs:
          print 'index:[%d] jobname: %s' % (self.updateJobs.index(i), i['jobName'])
      elif param[0] == 'patchjobs':
        self.patchJobs = scalex.job.getPatchJobs()['data']
        for i in self.updateJobs:
          print 'index:[%d] jobname: %s' % (self.updateJobs.index(i), i['jobName'])
      elif param[0] == 'audits':
        node = self.nodes[int(param[1])]
        overview = scalex.node.getOverviewOfAudits(node)
        if overview != {} and overview['data'] != {}:
          overview = overview['data']
          print 'You have %d warnings and %d failures' % (overview['auditWarningCount'], overview['auditFailCount'])
          import time
          print 'Last check done at: ' + time.ctime(overview['auditWarningCount']/1000)
          self.audits = scalex.node.getAudits(node)['data']
          for audit in self.audits:
            print 'status: %s\t message: %s' % (audit['auditLevel'], audit['auditDesc'])
    
    except Exception,e:
      print "Unknown Error:" , e
  
  def do_script(self,s):
    try :
      param = s.split()
      if len(param) < 4:
        self.help_script()
        return
      if ( param[0] == "run" ):
        script = self.scripts[int(param[1])]
        targets = []
        for i in param[2].split(','):
          targets.append(self.nodes[int(i)])
        name = param[3]
        arguments = []
        try:
          arguments = param[4].split(',')
        except:
          pass
        #        scheduleType = int(param[5])
        #        #schedule type should be one of 0 1 2
        #        startTime = param[6]
        result = scalex.script.run(name, script, targets)
        print result['result']
    except Exception,e:
      print "Unknown Error:" , e
  
  def do_job(self,s):
    try:
      param = s.split()
      
      if param[0] != 'cancel' and param[1] not in ['update', 'patch', 'job']:
        self.help_job()
        return
      index = int(param[1])
      jobs = {'update': self.updateJobs, 'patch':self.patchJobs, 'script':self.jobs}
      job = jobs[param[1]][index]
      result = scalex.job.cancel(job)
      print result['result']
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
      if scalex.node.isUnix(targets[0]):
        result = scalex.node.applyUpdates(name, targets, updates, startTime = time)
      else:
        result = scalex.node.applyPatches(name, targets, updates, startTime = time)
      print  result['result']
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
