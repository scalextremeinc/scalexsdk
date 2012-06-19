import scalex

####################################################################################
# These are dummy ids - please change this if you plan to use this to run tests     
# This test picks up the first aviaalble company and create a script, runs it on
# the first available machine in that company / role and deletes the script
###################################################################################
client_id = 'pa2yJyBamaVyLa7y6ujuZere9aRyMeDy'
client_secret = '4ymypeZy5yDyseZemuraJuqyXuZaNyDe'
rolename = 'Admin'


def setup():
  assert client_id != '' and client_secret != '', 'must SET Oauth key/secret'
  
  scalex.setClientId(client_id)
  scalex.setClientSecret(client_secret)
  coms = scalex.company.getCompanies()
  # login with first company
  scalex.company.set(coms[0])
  roles = scalex.role.getRoles()
  # set Admin for role
  scalex.role.set(rolename)

def test():
  scriptName = 'name-script-test'
  # get nodes
  nodes = scalex.node.getNodes()
  # create a script
  scalex.script.create(scriptName,'txt','ls','desc')
  # get all script
  scripts = scalex.script.getScripts()
  # get script we created
  script = ''
  for s in scripts:
    if scriptName in s['scriptName']:
      script = s
      break
  # update this script
  scalex.script.update(script, scriptName,'sh','content changed')
  # get content of this script
  scalex.script.getContent(script)
  # get versions of this script
  scalex.script.getVersions(script)
  # run this script, same as scalex.job.create()
  scalex.script.run('jobname-test', script, nodes[0])
  # get jobs of scripts
  jobs = scalex.job.getJobs(object = script)
  import time
  # sleep until job running
  while len(jobs) == 0:
    time.sleep(5)
    jobs = scalex.job.getJobs(object = script)
  # get first job
  assert len(jobs) != 0, 'get no jobs'
  job = jobs[0]
  # update this job with a different name
  import uuid
  scalex.job.update(job, 'new-job-name' + str(uuid.uuid4()), script, nodes[0])
  # get runs for job
  runs = scalex.job.getRuns(job)
  while len(runs) == 0:
    time.sleep(5)
    runs = scalex.job.getRuns(job)
  # get ouputs for run
  scalex.job.getOutputs(runs[0])
  # delete this script
  #scalex.script.delete(script)
  print 'all tests passed'

if __name__ == '__main__':
  import sys
  if len(sys.argv) == 3:
    client_id = sys.argv[1]
    client_secret = sys.argv[2]
  setup()
  test()



