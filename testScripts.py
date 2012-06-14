
# use nosetests for test
# INSTALLATION 
# #easy_install nosetests
import scalex

script_name = 'testcase-name'
script_type = 'testcase-name'
script_content = 'testcase-name'

def script_getScripts():
  result = scalex.script.getScripts()
  print result
  return result

def script_create():
  result = scalex.script.create(script_name, script_type, script_content)
  print result
  return result

#def script_update():
#  result = scalex.script.update(script_name+'updated', script_type, script_content)
#  print result
#  return result

def script_getContent(script):
  result = scalex.script.getContent(script)
  print result
  return result

def script_getVersions(script):
  result = scalex.script.getVersions(script)
  print result
  return result

def script():
  script_create()
  scripts = script_getScripts()
  s = scripts[0]
  script_getContent(s)
  script_getVersions(s)
  
#test for node.py
def node_getNodes():
  scalex.node.getNodes()
  scalex.node.getNodes(platform='Windows')
  scalex.node.getNodes(status='online')

def node():
  node_getNodes()

# test for job.py
def job_getJobs(object):
  scalex.job.getJobs('script', object)
  #scalex.job.getJobs('patch')
  #scalex.job.getJobs('update')

def job_getRuns(job):
  scalex.job.getRuns(job)

def job_getOutputs(run):
  scalex.job.getOutputs(run)

def job():
  scripts = script_getScripts()
  s = scripts[0]
  job = job_getJobs(s)

#def job_create
  
def setup():
  coms = scalex.company.getCompanies()
  scalex.company.set(coms[0])
  roles = scalex.role.getRoles()
  role = roles[0]
  scalex.role.set(role)

def test():
  script()
  node()


