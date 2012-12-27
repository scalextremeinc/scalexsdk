import urllib
import urllib2
import json
#
import scalex
from scalex import userinfo

def getCompanies():
  '''
  '''
  assert userinfo.userid != '', 'you need login first'
  scalex.relogin()
  url = '%s/acl/usercompanies?rid=%s' % (userinfo.domain, userinfo.rid)
  value = {
    'userId':userinfo.userid
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData

def set(company):
  '''
  '''
  userinfo.companyid = company['companyId']
