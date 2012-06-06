import urllib
import urllib2
import json
#
from scalex import userinfo
import scalex

def getRoles():
  assert userinfo.companyid != '', 'you need set company first'
  scalex.relogin()
  url = '%s/scalex/acl/userroles?rid=%s' % (userinfo.domain, userinfo.rid)
  value = {
    'user':userinfo.username,
    'companyId':userinfo.companyid
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData

def set(rolename):
  assert rolename != '', 'wrong rolename'
  userinfo.rolename = rolename

