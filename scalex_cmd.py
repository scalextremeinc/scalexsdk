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

class scalex_cmd(cmd.Cmd):
  
  scalex_instance = None;
  
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
    elif ( s == "script" ):
      self.help_script();
    elif ( s == "exit" ):
      self.help_exit();
    else :
      print "Available Command:"
      print "\tlogin"
      print "\tget"
      print "\tset"
      print "\tscript"
      print "\texit"
      print "help COMMAND for more information on a specific command."
    return 
  
  def help_login(self):
    print "login username password"
  
  def help_get(self):
    print "get json [companies/roles/myScripts/orgScripts]=> get json format data"
    print "get companies => get companies"
    print "get roles => get roles"
    print "get nodes [nodename] => get nodes info, if nodename is provided, show the detail of this node"
    print "get myScripts => get myScripts"
    print "get orgScripts => get orgScripts"
    print "get jobs [scriptId] => get jobs for script"
    print "get runs [jobId] => get runs for jobs"
    print "get arguments [scriptId] [script version] => get runs for jobs"
    print "get output [jobId, projectId, projectRunId] => get output for runs"

  def help_set(self):
    print 'set company [companyId]'
    print 'set role [companyId]'

  def help_script(self):
    print "script run [job name] [scriptId] [version] [targetIds] [startTime] [parameters]"
    print 'targets are comma separated example: 101,102'
    print 'startTime 0 means run now, or schedule time format 2012-06-02-12:12'
    print 'parameters are space separated example: argument1 argument2'
  
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
      sx = scalex.scaleXtreme( username , password )
      ret,value = sx.login();
      if ( ret ):
        sx.getCompanies()
#        sx.getRoles()
        self.scalex_instance = sx
        print "Login Successfully"
      else :
        print "Login Failed:" + value
    except Exception,e :
      print "Login Failed:"
      print e
  
  def do_set(self, s):
    if ( self.scalex_instance == None ):
      print "Please Login first"
      return 
    l = s.split()
    if len(l)!=2:
      self.help_set();
      return 
    try :
      s = s.strip()
      param = s.split();
      if ( param[0] == "company" ):
        self.scalex_instance.setCompany(param[1]);
        print 'set company ok'
      elif ( param[0] == "role" ):
        self.scalex_instance.setRole(param[1]);
        print 'set role ok'
      else :
        self.help_set();
    except Exception,e:
      print "Unknown Error:" , e
        
  def do_get(self,s):
    
    if ( self.scalex_instance == None ):
      print "Please Login first"
      return 
    try :
      s = s.strip()
      param = s.split();
      if param[0] == 'json':
        if len(param) != 2:
          self.help_get()
        elif param[1] == 'companies':
          print json.dumps(self.scalex_instance.companies)
        elif param[1] == 'roles':
          print json.dumps(self.scalex_instance.roles)
        elif param[1] == 'myScripts':
          print json.dumps(self.scalex_instance.myScripts)
        elif param[1] == 'orgScripts':
          print json.dumps(self.scalex_instance.orgScripts)
        else:
          self.help_get()
            
      if ( param[0] == "companies" ):
        self.scalex_instance.getCompanies();
#        print self.scalex_instance.companies;
        for com in self.scalex_instance.companies:
          print 'name: %s \t\t companyId: ' % (com['name']), com['companyId']

      elif ( param[0] == "roles" ):
        self.scalex_instance.getRoles();
        print self.scalex_instance.roles;

      elif ( param[0] == "myScripts" ):
        print 'get my scripts'
        self.scalex_instance.getMyScripts();
        for s in self.scalex_instance.myScripts:
          print 'id: %s\tversion: %s\tname: %s' % (s['scriptId'], s['version'], s['scriptName'])

      elif ( param[0] == "orgScripts" ):
        self.scalex_instance.getOrgScripts();
        for s in self.scalex_instance.myScripts:
          print 'id: %s\tversion: %s\tname: %s' % (s['scriptId'], s['version'], s['scriptName'])

      elif ( param[0] == "jobs" ):
        if len(param) < 2:
          self.help_get() 
        self.scalex_instance.getJobsForScript(param[1]);
        for j in self.scalex_instance.jobs[param[1]]:
          print 'jobId: %s\tstatus: %s\t\tjobName: %s' % (j['jobId'], j['status'], j['jobName'])

      elif ( param[0] == "runs" ):
        if len(param) < 2:
          self.help_get()
        jobId = param[1]
        self.scalex_instance.getRunsForJob(jobId);
        for r in self.scalex_instance.runs[jobId]:
          print 'jobId: %s\tprojectId: %s\tprojectRunId: %s\tstatus: %s\t' % (r['jobId'], r['projectId'], r['projectRunId'], r['status'])

      elif param[0] == 'arguments':
        if len(param) < 3:
          self.help_get()
        scriptId = param[1]
        version = param[2]
        self.scalex_instance.getParamsOfScript(scriptId, version)
        print 'script: %s, scriptId: %s' % (self.scalex_instance.arguments[scriptId]['scriptName'], self.scalex_instance.arguments[scriptId]['scriptId'])
        for arg in self.scalex_instance.arguments[scriptId]['scriptInputParams']:
          print 'argu: %s\ttype: %s\tdefault value: %s' % (arg['parameterKey'],arg['parameterDataType'],arg['parameterDefaultValue'])
 
      elif ( param[0] == "output" ):
        if len(param) != 4:
          self.help_get()
        jobId = param[1]
        projectId = param[2]
        projectRunId = param[3]
        self.scalex_instance.getOutputForRun(jobId, projectId, projectRunId)
        
        for r in self.scalex_instance.runs[jobId]:
          print 'jobname:', r['stepRunLogBeans'][0]['taskName']
          print 'status: ', r['status']
          print 'run at: ', time.ctime(int(r['runTimestamp'])/1000)
        
        print '-----------------'  
        for output in self.scalex_instance.outputs:
            print 'target:', output['target']
            print 'outputStatus:', output['outputStatus']
            if output['truncated'] == 'Y' :
                print 'output (truncated - more than 500 chars):'
            else: 
                print 'output:'
            print output['output'] 
            print '-----------------'
          
      elif ( param[0] == "nodes" ):
        self.scalex_instance.getNodes()
        for n in self.scalex_instance.nodes:
          print 'nodeId: %d\tnodeName: %s' % (n['nodeId'], n['nodeName'])
          
    except Exception,e:
      print "Unknown Error:" , e
  
  def do_script(self,s):
    
    if ( self.scalex_instance == None ):
      print "Please Login first"
      return 
    try :
      param = s.split()
      if len(param) < 6:
        self.help_script()
        return
      if ( param[0] == "run" ):
        del param[0]
        self.scalex_instance.runScript(param);
    except Exception,e:
      print "Unknown Error:" , e
  
  def do_EOF(self, line): 
    print ""
    return True
  
  def do_exit(self,s):
    sys.exit(0);

if __name__ == '__main__':
  
  scalex_cmd().cmdloop();
  
  sys.exit(0);
