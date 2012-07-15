import sys
import scalex
import time

scripts = []
scriptName = 'script-test-delete'
jobName = 'script-test-jobName'

# getScripts()
def getScripts():
  scalex.script.getScripts('user')
  scalex.script.getScripts('org')
  scalex.script.getScripts('purchase')
  scalex.script.getScripts()
  
# create()
def create():
  script = scalex.script.create(scriptName, 'sh', 'pwd')

# getContent()
# getVersions()
# run()
# update()
# delete()
def CRUD():
  create()
  time.sleep(10)
  global scripts
  scripts = scalex.script.getScripts()
  scalex.script.getVersions(scripts[0])
  scalex.script.getContent(scripts[0])
#
  script = ''
  for i in scripts:
    if i['scriptName'] == scriptName:
      script = i
      break
  if script == '':
    sys.stderr.write('**ERROR: NO script\n')
    return
  scalex.script.update(script, type = 'updated')
# run
  nodes = scalex.node.getNodes()
  if nodes == []:
    sys.stderr.write('**ERROR: NO nodes\n')
    return
  print nodes[0]
  scalex.script.run(jobName, script, nodes[0])
# delete
  scalex.script.delete(script)
                    
def test():
  CRUD()
  getScripts()
  