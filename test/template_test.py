import sys
import scalex
import time

# getTemplate()
# getInfo()
# launch()
def normalFunction():
  templates = scalex.template.getTemplates()
  scalex.template.getInfo(templates[0])
#  scalex.template.launch(templates[0])

# getContent()
# getVersions()
# run()
# update()
# delete()
def CRUD():
  scripts = scalex.script.getScripts()
#  
  template = scalex.template.create('template-test-create', [], 'desc', scripts)
  template = scalex.template.update(template, 'template-name-modified', description = 'desc-mod')
#  delete
  scalex.template.delete(template)

def test():
  CRUD()
  normalFunction()

