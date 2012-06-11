import scalex

'''
each API call return a dict like this
    {
        'result':'SUCCESS',
        'data':DATA
    }
    result may be 'SUCCESS' or 'FAILURE'
    data may be list/dict/string 
'''
USERNAME = ''
PASSWORD = ''

assert USERNAME != '' and PASSWORD != '', 'you must setup username and password in %s' % (__file__)

def loginAndSetupSample():
  #login and set company and role, REQUIRED
  #make sure do these before any other API call
  scalex.login(USERNAME, PASSWORD)
  coms = scalex.company.getCompanies()['data']
  scalex.company.set(coms[0])
  roles = scalex.role.getRoles()['data']
  scalex.role.set(roles[0])

def nodeSample():
  #get all nodes
  nodes = scalex.node.getNodes()['data']
  node = nodes[0]
  if scalex.node.isUnix(node):
    #get updates of a given node(unix)
    updates = scalex.node.getUpdates(node)['data']
#    update = updates[0]
#    scalex.node.applyUpdates('update_now_job', node, updates)  #run job now and apply more updates at once
#    scalex.node.applyUpdates('schedule_update_job', node, update, startTime = '2014-01-01-00:00')
    # get Tiger Audit Checks
    audits = scalex.node.getAudits(node)['data']
  else:
    #get patches of a given node(windows)
    patches = scalex.node.getPatches(node)['data']
    patch = patches[0]
#    scalex.node.applyPatches('patch_now_job', node, patch) #run job now
#    scalex.node.applyPatches('schedule_patch_job', node, patch, startTime = '2014-01-01-00:00')
  
def scriptAndJobSample():
  #CRUD operation
  #create a script
  params = [
            {"parameterKey":"first int key", "parameterDefaultValue":"1", "parameterDataType":"int", "description":"desc", "requiredFlag":"Y"},
            {"parameterKey":"second str key", "parameterDefaultValue":"string2",  "parameterDataType":"string", "description":"desc", "requiredFlag":"Y"},
            ]
  
  scalex.script.create('sample_name', #script name
                       'sh',          #script type
                       'echo foo',    #script content
                       description = 'desc',
                       params = params
                       )
                       
  #get all my scripts
  scripts = scalex.script.getScripts()['data']
#  scripts = scalex.script.getScripts(type = 1)['data'] #get all org scripts
  script = scripts[0]
  #get versions of a script
  versions = scalex.script.getVersions(script)['data']
  #get content of a script
  content = scalex.script.getContent(script)['data']
#  content = scalex.script.getContent(script, version = versions[0]['version']) #with a different version
  
  #run a script at a given node
  nodes = scalex.node.getNodes()['data']
  node = nodes[0]
  
  scalex.script.run('python_sdk_test_run', script, node)  #run now
#  scalex.script.run('python_sdk_test_run', script, node, scheduleType=1, repeatInterval = 60, repeatCount=2) #recurring schedule, start now, repeat every 60 mins, end after 2 occurences
#  scalex.script.run('python_sdk_test_run', script, node, scheduleType=1, repeatInterval = 60, endTime='2014-06-04-16:30') #recurring schedule, start now, repeat every 60 mins, end by 2014-06-04-16:30
#  scalex.script.run('python_sdk_test_run', script, node, scheduleType=2, cronExpr='0 0 0 * 6 ?') #cron schedule

  # get jobs for a script
  jobs = scalex.job.getJobs(script)['data']
  if len(jobs) > 0:
    job = jobs[0]
    # get runs for a job
    runs = scalex.job.getRuns(job)['data']
    if len(runs) > 0:
      run = runs[0]
      # get outputs for a run
      outputs  = scalex.job.getOutputs(run)['data']


if __name__ == '__main__':
  loginAndSetupSample()
  nodeSample()
  scriptAndJobSample()

