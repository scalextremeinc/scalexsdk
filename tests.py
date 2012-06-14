import scalex

client_id = 'y5uvy4ySubypajanuRyzadu4yXezuqyt'
client_secret = 'eZymyXuPu4eJapa9aguZuReByJuWy2yq'
company_id = '40034'
rolename = 'Admin'


def setup():
  assert client_id != '' and client_secret != '', 'must SET Oauth key/secret'
  assert company_id != '' and rolename != ''
  
  scalex.setCliendId(client_id)
  scalex.setClientSecret(client_secret)
  coms = scalex.company.getCompanies()
  scalex.company.set({'companyId':company_id})
  roles = scalex.role.getRoles()
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
  # sleep for 10 seconds, wait for job running
  import time
  time.sleep(10)
  # get jobs of scripts
  jobs = scalex.job.getJobs(object = script)
  # get first job
  assert len(jobs) != 0, 'get no jobs'
  job = jobs[0]
  # update this job with a different name
  import uuid
  scalex.job.update(job, 'new-job-name' + str(uuid.uuid4()), script, nodes[0])
  # get runs for job
  runs = scalex.job.getRuns(job)
  # get ouputs for run
  scalex.job.getOutputs(runs[0])
  # delete this script
  scalex.script.delete(script)
  print 'all tests passed'

if __name__ == '__main__':
  setup()
  test()



