#!/usr/bin/env python

import readline
import cmd
import urllib
import urllib2
import uuid
import json
import base64
import sys
import scalex

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
    print "get companies => get companies"
    print "get roles => get roles"
    print "get nodes [nodename] => get nodes info, if nodename is provided, show the detail of this node"
    print "get myScripts => get myScripts"
    print "get orgScripts => get orgScripts"
    print "get jobs [scriptId] => get jobs for script"
    print "get runs [jobId] => get runs for jobs"
    print "get output [jobId, projectId, projectRunId] => get output for runs"

  def help_set(self):
    print 'set company [companyId]'
    print 'set role [companyId]'

  def help_script(self):
    print "script runtest"
  
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
          print 'id: %s\tverion: %s\tname: %s' % (s['scriptId'], s['version'], s['scriptName'])
      elif ( param[0] == "orgScripts" ):
        self.scalex_instance.getOrgScripts();
        for s in self.scalex_instance.myScripts:
          print 'id: %s\tverion: %s\tname: %s' % (s['scriptId'], s['version'], s['scriptName'])
      elif ( param[0] == "jobs" ):
        if len(param) < 2:
          self.help_get() 
        self.scalex_instance.getJobsForScript(param[1]);
        for j in self.scalex_instance.jobs[param[1]]:
          print 'jobId: %s\tstatus: %s\tjobName: %s' % (j['jobId'], j['status'], j['jobName'])
      elif ( param[0] == "runs" ):
        if len(param) < 2:
          self.help_get()
        jobId = param[1]
        self.scalex_instance.getRunsForJob(jobId);
        for r in self.scalex_instance.runs[jobId]:
          print 'jobId: %s\tprojectId: %s\tprojectRunId: %s\tstatus: %s\t' % (r['jobId'], r['projectId'], r['projectRunId'], r['status'])
      elif ( param[0] == "output" ):
        if len(param) != 4:
          self.help_get()
        jobId = param[1]
        projectId = param[2]
        projectRunId = param[3]
        print 'output: ', self.scalex_instance.getOutputForRun(jobId, projectId, projectRunId);

      elif ( param[0] == "nodes" ):
        if ( len(param) == 2 ):
          self.scalex_instance.getNodes(param[1]);
          print self.scalex_instance.nodes
        elif ( len(param) == 1 ): 
          self.scalex_instance.getNodes(param[1]);
          print self.scalex_instance.nodes
        else:
          self.help_get();
      else :
        self.help_get();
    except Exception,e:
      print "Unknown Error:" , e
  
  def do_script(self,s):
    
    if ( self.scalex_instance == None ):
      print "Please Login first"
      return 
    try :
      param = s.strip()
      if ( s == "runtest" ):
        print self.scalex_instance.runScript();
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
