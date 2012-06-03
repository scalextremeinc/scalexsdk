import urllib
import urllib2
import json
#
import userinfo

def getScripts(type = 0):
  '''arguments: type
    0 is myscripts
    1 is orgscripts
    default is 0
    '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  operation = ['userscripts', 'orgscripts']
  if type < 0 or type > len(operation) - 1:
    return
  url = userinfo.domain + '/library'
  value = {
    'companyid':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.username,
    'rid':userinfo.rid,
    'operation':operation[type]
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, '')
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request).read()
  return response


def getContent(scriptid, version):
  '''arguments: scriptid, version
  '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  payload = {
    'scriptid': scriptid,
    'version': version,
  }
  url = userinfo.domain + '/library'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.username,
    'role':userinfo.rolename,
    'operation':'scriptcontent',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, urllib.urlencode(payload))
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request).read()
  return response
