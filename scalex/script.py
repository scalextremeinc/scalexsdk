'''
  @undocumented: __package__
'''

import urllib
import urllib2
import json
import time
import datetime
import base64
import os
#
from scalex import userinfo
import scalex

def getScripts(type = ''):
  '''
    Get scripts
    
    @type   type: string
    @param  type: Optional, valid values are B{user}, B{org} or B{purchase}
    
    @rtype: list
    @return: List of scripts
    
    @change:
      - Parameter type now changed. Used to be 0 or 1, now it can be one of B{user}, B{org} and B{purchase}
  '''
#    API : /scripts
#    Method : GET
#    URL structure : https://<servername>/v0/scripts?access_token=<valid access token>
#    Input params :
#    version (optional) parameter
#    type (optional) 
#    type=user     Return my scripts
#    type=org      Return org scripts
#    type=purchase Return purchase scripts

  assert type in ['', 'user', 'org', 'purchase'], "script type must be one of ['', 'user', 'org', 'purchase']"
  path = '/scripts'
  query = {}
  if type != '':
    query['type'] = type
#  elif script != '':
#    path = '/scripts/' + str(script['scriptId'])
#    if version != 0:
#      query['version'] = version
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getContent(script, version = -1):
  '''
    Get script content
    
    @type   script: dict
    @param  script: Script returned by getScripts()

    @type   version: int
    @param  version: Optional

    @rtype: dict
    @return: Content of script
    
    @change: 
      - Not changed
  '''
#    API : /scripts/{id}
#    Method : GET
#    URL structure : https://<servername>/v0/scripts?access_token=<valid access token>
#    Input params : version (optional) parameter
#  '''
  scriptid = script['scriptId']
  path = '/scripts/%s' % (str(scriptid))
  query = {
  }
  if version != -1:
    query['version'] = version
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getVersions(script):
  '''
    Get script content
    
    @type   script: dict
    @param  script: Script returned by getScripts()
    
    @rtype: list
    @return: Versions of specific script
    
    @change: 
      - Not changed
  '''
#    API : /scripts/versions?id=1234
#    Method : GET
#  '''
  path = '/scripts/%s/versions' % (str(script['scriptId']))
  query = {
  }
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def run(name, script, targets, arguments = [], type = 'script', version = -1, serverGroups = [], 
        scheduleType = 0, startTime = 0, repeatInterval = 60, endTime = 0, repeatCount = 0):
  '''
    Run script
    
    @todo: Version support
    
    @type   name: string
    @param  name: Job Name 
    
    @type   script: dict
    @param  script: Script returned by getScripts()
    
    @param  targets: Targets returned by scalex.node.getNodes() or a single node.
    
    @type   arguments: list
    @param  arguments: Arguments of the script, default is []
    
    @type   type: string
    @param  type: Job type, default is 'script'
    
    @type   version: int
    @param  version: Version of script
    
    @type   serverGroups: list
    @param  serverGroups: Server groups of node
    
    @type   scheduleType: int
    @param  scheduleType: Schedule type of job, default is 0, valid values are:
      - B{0}, Run Once
      - B{1}, Recurring
    
    @param  startTime: Start time formatted like B{2012-12-12-00:00}, default is now, 

    @param  repeatInterval: Repeat interval of recurring schedule, default is 60 mins. 

    @param  endTime: End time of recurring schedule, formatted like B{2012-12-12-00:00}. You must specify this argument if you want to schedule a recurring job and with a repeat interval.

    @type   repeatCount: int
    @param  repeatCount: Repeat count of a recurring scheduled job.
    
    @rtype: dict
    @return: Job just scheduled
    
    @change: 
      - Delete Cron Expression support

  '''
  return scalex.job.create(name, script, targets, arguments, type, version, serverGroups,
                           scheduleType, startTime, repeatInterval, endTime, repeatCount)

def create(name, type, content, description = '', params = [], tagList = []):
  '''
    Create a script
    
    @todo: params and tags not implement
    
    @type   name: string
    @param  name: Script Name 
    
    @type   type: string
    @param  type: Script type(filename extension)
    
    @type   content: string
    @param  content: Script content
    
    @type   description: string
    @param  description: Script description
    
    @rtype: dict
    @return: script just created
    
    @change:
      - Not changed
  '''
  
#FIXME, no script attachments, no tags, no params
#ttps://manage.scalextreme.com/library?rid=411C2ECD-BDD0-4F61-9F37-E3718F02E084
#    API : /scripts
#    Method : POST
#    URL Structure: https://<servername>/v0/scripts?access_token=<valid token generated by authentication>
#    Input : Json payload like 
#    {
#    "scriptName":"Test script",
#    "scriptType":"bat",
#    "scriptDescription":"",
#    "scriptInputParams":[],
#    "tagList":[],
#    "scriptAttachments":[],
#    "scriptContent":"bGluZTEKbGluZTIKbGluZTMKbGluZTQKbGluZTUKZWNobyAnSGknCg=="
#    }
#  '''
  
  path = '/scripts'
  url = userinfo.geturl(path)
  payload = {
    "scriptName":name,
    "scriptType":type,
    "scriptDescription":base64.b64encode(description),
    "scriptInputParams":params,
    "tagList":tagList,
    "scriptAttachments":[],
    "scriptContent":base64.b64encode(content),
  }
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def exportAll(pathPrefix, type = ""):
  '''
   Export all scripts of a certain type
    
   
   
   @type type: string
   @param type: my , org, purchased
   
  '''
  allScripts = getScripts(type)
  for script in allScripts:
    export(pathPrefix, script)
    time.sleep(2) 

def export(pathprefix = "./", script = '', version = -1):
  '''
    Exports a script
    @type pathprefix: string
    @param pathprefix: valid directory where the script should be placed
     
    @type script: dict
    @param script: Script returned by getScripts()

    @type version: string
    @param version: version of the script or current version if nothing is passed in
  '''
  #this gets the full object with content as base 64 encoded string and attachments and other things..
  fullScript = getContent(script, version)
  SEPARATOR = '.'
  scriptName = fullScript['scriptName'] + SEPARATOR + fullScript['scriptType'].replace('.', '')
  scriptDir  = pathprefix + "/" + scriptName
  version = scriptDir + "/version-" + fullScript['version']
  try: 
    #create a dir with the script name
    os.mkdir(scriptDir)
    # create a dir for the version
    os.mkdir(version)
    #create script and meta data
    __createFile(version + "/" + scriptName, fullScript['scriptContent'])
    __createFile(version + "/" + "metadata.json", 
        json.dumps(__getMeta(fullScript)), False)
  except:
    raise 

def importAll(pathPrefix):
    for subdir, dirs, files in os.walk(pathPrefix):
        for dir in dirs:
            importOne(os.path.join(subdir, dir))
        

def importOne(scriptDir):

    versionDir = __findCurrentVersion(scriptDir)

    if versionDir == False:
        return


    scriptDirBasename = os.path.basename(scriptDir)
    name, type = os.path.splitext(scriptDirBasename)

    scriptName = scriptDirBasename;
    with open(versionDir + "/" + scriptName) as f: content = f.read()

    params = []
    with open(versionDir + "/" + "metadata.json") as f: meta = json.loads(f.read())
    params = meta["scriptInputParams"]
    tags = meta["tagList"];
    description = meta["description"];
    type=type[1:]

    create(name, type, content, description, params, tags)

def __findCurrentVersion(scriptDir):
    for subdir, dirs, files in os.walk(scriptDir):
        for dir in dirs:
            if "version-" not in dir:
                continue

            return os.path.join(subdir, dir)

    return False



def delete(script = '', type = ''):
  '''
    Delete a script or a group of scripts
    
    @todo: Add return info about this API
    
    @type   script: dict
    @param  script: Script returned by getScripts()
    
    @type   type: string
    @param  type: Valid values are B{user}, B{org} or B{purchase}
    
    @change:
      - Add parameter B{type}, you can delete a group of scripts now.
  '''

#    API : /scripts/1234
#    Method : DELETE
#    /scripts?type=user      Delete user scripts
#    /scripts?type=org       Delete org scripts
#    /scripts?type=purchase  Delete purchase scripts
  
  path = '/scripts'
  query = {}
  if script != '':
    path = path + '/' + str(script['scriptId'])
  else:
    assert type in ['user', 'org', 'purchase'], 'wrong script type'
    query['type'] = type
  url = userinfo.geturl(path, query)
  request = urllib2.Request(url)
  request.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def update(script, name = '', type = '', content = '', description = '', params = [], tagList = []):
  '''
    Update a script
    
    @todo: params and tags not implement
    
    @type   script: dict
    @param  script: Script will be updated
    
    @type   name: string
    @param  name: Script Name 
    
    @type   type: string
    @param  type: Script type(filename extension)
    
    @type   content: string
    @param  content: Script content
    
    @type   description: string
    @param  description: Script description
    
    @rtype: dict
    @return: script just created
    
    @change:
      - Not changed
  '''
    
#    API : /scripts/1234
#    Method : POST
#    URL Structure: https://<servername>/v0/scripts?access_token=<valid token generated by authentication>
#    Input : Json payload like 
#    {
#    "scriptName":"Test script",
#    "scriptType":"bat",
#    "scriptDescription":"",
#    "scriptInputParams":[],
#    "tagList":[],
#    "scriptAttachments":[],
#    "scriptContent":"bGluZTEKbGluZTIKbGluZTMKbGluZTQKbGluZTUKZWNobyAnSGknCg=="
#    }
#  '''def update(script, name = '', type = '', content = '', description = '', params = [], tags = [] ):
#  FIXME, no script attachments, incomplete params/tags/attachments
  path = '/scripts/' + str(script['scriptId'])
  parameters = []
  url = userinfo.geturl(path)
  script = getContent(script)
  # script contents
  if name == '':
    name = script['scriptName']
  if type == '':
    type = script['scriptType']
  if content == '':
    content = script['scriptContent']
  else:
    content = base64.b64encode(content)
  payload = {
    "scriptName":name,
    "version":script['version'],
    "scriptType":type,
    "scriptDescription":base64.b64encode(description),
    "scriptInputParams":params,
    "tagList": tagList,
    "scriptAttachments":[],
    "scriptContent":content,
  }
  postData = json.dumps(payload)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def __getMeta(script):
    return {
        "scriptInputParams" : script['scriptInputParams'],
        "tagList" : script['tagList'],
        "description" : base64.decodestring(script['scriptDescription'])
    }

def __createFile(filename, content, decode=True):
    try:
        scriptFile = open(filename, "wb")
        if decode:
            scriptFile.write(base64.decodestring(content))
        else:
            scriptFile.write(content)
        scriptFile.close()
    except:
        raise 
    
