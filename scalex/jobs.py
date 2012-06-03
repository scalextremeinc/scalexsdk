import urllib
import urllib2
import json
#
import userinfo

def get(scriptid):
  '''arguments: type
    0 is myscripts
    1 is orgscripts
    default is 0
    '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  payload = {
    "companyId": userinfo.companyid,
    "scriptId": str(scriptid),
    "user": str(userinfo.userid),
    "role": userinfo.rolename,
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.username,
    'role':userinfo.rolename,
    'operation':'joblist',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request).read()
  return response
