import sys
import scalex
import time

updateJobs = []
patchJobs = []

# getJobs()
def getJobs_test():
  global updateJobs
  global patchJobs
  updateJobs = scalex.job.getJobs(type = 'update')
  patchJobs  = scalex.job.getJobs(type = 'patch')

# update()
# getRuns()
# getOutputs()
def test():
  nodes = scalex.node.getNodes()
  scripts = scalex.script.getScripts()
  scalex.script.run('job-test-run', scripts[0], nodes[0])
  scriptJobs = scalex.job.getJobs(object = scripts[0])
  if scriptJobs == []:
    sys.stderr.write('**ERROR: NO script jobs\n')
    return
#  getruns and getoutputs
  time.sleep(10)
  runs = scalex.job.getRuns(scriptJobs[0])
  if runs != []:
    scalex.job.getOutputs(runs[0])
# update
  import uuid
  scalex.job.update(scriptJobs[0], 'name-updated'+str(uuid.uuid4()), scripts[0], nodes[0], startTime = '2013-12-12-00:00')
# cancel()
# delete()
  jobs = scalex.job.getJobs(object = scripts[0])
  runs = scalex.job.getRuns(jobs[0])
  if runs != []:
    scalex.job.cancel(runs[0])
  scalex.job.delete(jobs[0])

#nodes = scalex.node.getNodes()
#if nodes == []:
#  sys.stderr.write('**ERROR: NO nodes\n')
#  return
#print nodes[0]
#scalex.script.run(jobName, script, nodes[0])
