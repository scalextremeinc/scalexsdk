import urllib
import urllib2
import json
import base64
#
from scalex import userinfo
import scalex

def getRoles():
  assert userinfo.companyid != '', 'you need set company first'
#  scalex.relogin()
#  url = '%s/scalex/acl/userroles?rid=%s' % (userinfo.domain, userinfo.rid)
#  value = {
#    'user':userinfo.username,
#    'companyId':userinfo.companyid
#  }
#  postData = urllib.urlencode(value)
#  response = urllib2.urlopen(url, postData)
#  returnData = json.loads(response.read())
#  if returnData['result'] == 'SUCCESS' and len(returnData['data']) > 0:
#    for i in range(0, len(returnData['data'])):
#      returnData['data'][i] = base64.b64decode(returnData['data'][i])
#  return returnData
  path = '/roles'
  query = {
    'client_id':userinfo.client_id,
    'company_id':userinfo.companyid,
  }
  url = '%s%s?%s' % (userinfo.baseurl, path, urllib.urlencode(query))
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def set(rolename):
  assert rolename != '', 'wrong rolename'
  userinfo.rolename = rolename
#  Authorization after set role
  scalex.auth()


