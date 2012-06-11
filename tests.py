import scalex
import unittest
import random

USERNAME = ''
PASSWORD = ''

assert USERNAME != '' and PASSWORD != '', 'you must setup username and password in test code'

class ScriptCRUDTest(unittest.TestCase):
  def loginAndSetup(self):
    #login and set company and role, REQUIRED
    #make sure do these before any other API call
    scalex.login(USERNAME, PASSWORD)
    coms = scalex.company.getCompanies()['data']
    scalex.company.set(coms[0])
    #roles = scalex.role.getRoles()['data']
    scalex.role.set('Admin')

  def setUp(self):
    self.loginAndSetup()
    self.name = 'python_sdk_testcase_scriptname_' + str(int(random.random()*1000000))
    self.type = 'sh'
    self.content = 'pwd'
    self.desc = 'description'
    self.params = [
                {"parameterKey":"first int key", "parameterDefaultValue":"1", "parameterDataType":"int", "description":"desc", "requiredFlag":"Y"},
                {"parameterKey":"second str key", "parameterDefaultValue":"string2",  "parameterDataType":"string", "description":"desc", "requiredFlag":"Y"},
                ]

    self.tags = []

  def test_create(self):
    '''create a script'''
    result = scalex.script.create(self.name, self.type, self.content, description = self.desc, params = self.params, tags = self.tags)
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')
    #script name exists
    result = scalex.script.create(self.name, self.type, self.content, description = self.desc, params = self.params, tags = self.tags)
    self.assertTrue(result == None)

  def test_read(self):
    '''get a script'''
    scripts = scalex.script.getScripts()['data']
    result = scalex.script.getContent(scripts[0])
    self.assertTrue(result['result'], 'SUCCESS')

  def test_update(self):
    name = self.name + 'update'
    scalex.script.create(name, self.type, self.content)
    scripts = scalex.script.getScripts()['data']
    script = None
    for s in scripts:
      if s['scriptName'] == name:
        script = s
        break
    self.assertTrue(script != None)
    result = scalex.script.update(script, type = 'updated')
    self.assertTrue(result['result'], 'SUCCESS')

  def test_delete(self):
    name = self.name + 'delete'
    scalex.script.create(name, self.type, self.content)
    scripts = scalex.script.getScripts()['data']
    script = None
    for s in scripts:
      if s['scriptName'] == name:
        script = s
        break
    self.assertTrue(script != None)
    result = scalex.script.delete(script)
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')

  def test_runScript(self):
    name = self.name + 'run'
    jobname = 'testrun'
    time = '2014-01-01-00:00'
    scalex.script.create(name, self.type, self.content)
    scripts = scalex.script.getScripts()['data']
    script = None
    for s in scripts:
      if s['scriptName'] == name:
        script = s
        break
    self.assertTrue(script != None)
    node = scalex.node.getNodes()['data'][0]
    self.assertTrue(node != None)
    # run now
    result = scalex.script.run(jobname, script, node)
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')
    # run at a scheduled time
    result = scalex.script.run(jobname, script, node, startTime = time)
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')
    # recurring schedule
    # start now, repeat every 60 mins, end after 3 occurences
    result = scalex.script.run(jobname, script, node, scheduleType=1, repeatInterval = 60, repeatCount=3)
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')
    # start at future, repeat every 60 mins, end by '2014-02-01-00:00'
    result = scalex.script.run(jobname, script, node, startTime = time, scheduleType=1, repeatInterval = 60, endTime='2014-02-01-00:00')
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')
    # cron schedule(Advanced)
    result = scalex.script.run(jobname, script, node, scheduleType=2, cronExpr='0 0 0 * 6 ?')
    self.assertTrue(isinstance(result, dict))
    self.assertTrue(result['result'] == 'SUCCESS')

   

if __name__ == '__main__':
  unittest.main()

