'''
  @undocumented: __package__
  
  
  '''

import urllib
import urllib2
import json
import base64
#
from scalex import userinfo
from scalex import script

def getTemplates():
  '''
    Get list of templates
    
    @rtype: list
    @return: list of templates
  '''
  
  path = '/templates'
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getInfo(template):
  '''
    Get template info
    
    @type   template: dict
    @param  template: template object returned by getTemplates()

    @rtype: dict
  '''
  
  path = '/templates/' + str(template['processId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getParameters(template):
  '''
    Get template parameters
    
    @type   template: dict
    @param  template: template object returned by getTemplates()

    @rtype: list
  '''
  
  info = getInfo(template)
  params = []
  for a in info['tasks']:
    scriptObject = {'scriptId': a['parentTaskId']}
    scriptContent = script.getContent(scriptObject)
    scriptParams = scriptContent['scriptInputParams']
    for b in scriptParams:
      b['parameterValue'] = b['parameterDefaultValue']
    paramInfo = {
      'scriptId': a['parentTaskId'],
      'taskName': scriptContent['scriptName'],
      'taskParameters': scriptParams
    }
    params.append(paramInfo)
  return params

def launch(template, targets = [], parameter = []):
  '''
    Launch a template
    
    @type   template: dict
    @param  template: template object returned by getTemplates()
    
    @type   targets: list
    @param  targets: target node list, node returned by node.getNodes()
    
    @type   parameter: list
    @param  parameter: parameters of template
    
    @rtype: dict
  '''
  #  HTTP Method: GET when launch without any script parameters
  #  HTTP Method: POST when launch with any script parameters
  path = '/templates/%s/launch' % (str(template['processId']))
  url = userinfo.geturl(path)
  #  
  postData = None
  info = getInfo(template)
#  targets
  if not isinstance(targets, list):
    t = targets
    targets = []
    targets.append(t)
  agents = []
  for n in targets:
    agents.append(n['nodeId'])
  info['targets'] = list(set(info['targets'] + agents))
#  parameter
  if parameter != []:
    for a in parameter:
      for b in info['tasks']:
        if a['scriptId'] == b['parentTaskId']:
          b['taskParameters'] = a['taskParameters']
          break
#    
  postData = json.dumps(info)
#
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _getTasks(scripts):
  '''
    convert scripts to tasks format
  '''
  tasks = []
  for task in scripts:
    taskinfo = {
      "taskName": task['scriptName'],
      "type": "SCRIPT",
      "parentTaskId": task['scriptId'],
      "taskProperties": [{
                         "propertyKey": "version",
                         "propertyValue": task['version'],
                         "sequenceNumber": 0
                         }],
      "taskParameters": []
    }
    tasks.append(taskinfo)
  return tasks

def create(name = '', targets = [], description = '', scripts = []):
  '''
    Create a template
    
    @type   name: string
    @param  name: Template name
    
    @type   targets: list
    @param  targets: Target node list
    
    @type   description: string
    @param  description: Template description
    
    @type   scripts: list
    @param  scripts: Scripts of template, returned by scalex.script.getScripts()
    
    @rtype: dict
    @return: Template just created
  '''
#  
  path = '/templates'
  url = userinfo.geturl(path)
#  
  if not isinstance(targets, list):
    t = targets
    targets = []
    targets.append(t)
  agents = []
  for n in targets:
    agents.append(n['nodeId'])
#
  template = {
    'processName': name,
    'description': base64.b64encode(description),
    'targets': agents,
    'tags': '',
    'templateFlag': 'Y',

    'excludeTargets': [],
    'parentProcessId': 0,
    'serverGroups': [],
    'tagList': [],
    "tasks": _getTasks(scripts),
    'processParameters': []
  }    
  postData = json.dumps(template)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def update(template, name = '', targets = [], description = '', scripts = []):
  '''
    Update a template
    
    @type   template: dict
    @param  template: The template you want to update
    
    @type   name: string
    @param  name: Template name
    
    @type   targets: list
    @param  targets: Target node list
    
    @type   description: string
    @param  description: Template description
    
    @type   scripts: list
    @param  scripts: Scripts of template, returned by scalex.script.getScripts()
    
    @rtype: dict
    @return: Template just updated

  '''
  template = getInfo(template)
#  
  path = '/templates/' + str(template['processId'])
  url = userinfo.geturl(path)
  #  
  if not isinstance(targets, list):
    t = targets
    targets = []
    targets.append(t)
  agents = []
  for n in targets:
    agents.append(n['nodeId'])
# name
  if name != '':
    template['processName'] = name
# targets
  if agents != []:
    template['targets'] = agents
# description
  if description != '':
    template['description'] = base64.b64encode(description)
# scripts
  if scripts != []:
    template['tasks'] = _getTasks(scripts)
  #
  postData = json.dumps(template)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def delete(template):
  '''
    Delete a template
    
    @param template: The template you want to delete
  '''
  path = '/templates'
  path = path + '/' + str(template['processId'])
  #
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  request.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData
