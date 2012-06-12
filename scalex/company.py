import urllib
import urllib2
import json
#
import scalex
from scalex import userinfo

def getCompanies():
  '''
    curl -k 'https://cloudmanage.scalextreme.com/v0/companies?client_id='
  '''
#  assert userinfo.userid != '', 'you need login first'
#  scalex.relogin()
#  url = '%s/scalex/acl/usercompanies?rid=%s' % (userinfo.domain, userinfo.rid)
#  value = {
#    'userId':userinfo.userid
#  }
#  postData = urllib.urlencode(value)
#  response = urllib2.urlopen(url, postData)
#  returnData = json.loads(response.read())
#  return returnData
#  
  path = '/companies'
  query = {
    'client_id':userinfo.client_id,
    'company_id':userinfo.companyid,
  }
  url = '%s%s?%s' % (userinfo.baseurl, path, urllib.urlencode(query))
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def set(company):
  '''
  '''
  userinfo.companyid = str(company['companyId'])
