import urllib
import urllib2
import json
import base64
#
from scalex import userinfo
import scalex

def getRoles():
  assert userinfo.companyid != '', 'you need set company first'

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
#  get access token after set role
  scalex.auth()


