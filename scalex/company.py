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
  assert userinfo.client_id != '' and userinfo.client_secret != '', 'you must set client_id and client_secret in userinfo.py first'
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
