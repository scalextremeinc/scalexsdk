'''
  @undocumented: __package__
'''
import urllib
import urllib2
import json
#
import scalex
from scalex import userinfo

def getCompanies():
  '''
    Get list of companies, you need to set Oauth client id and client secret before call this function
    
    @requires: Set Oauth client id and client secret first
    
    @rtype: list
    @return: List of companies
  '''
  assert userinfo.client_id != '' and userinfo.client_secret != '', 'you must set client_id and client_secret in userinfo.py first'
  path = '/companies'
  query = {
    'client_id':userinfo.client_id,
  }
  url = '%s%s?%s' % (userinfo.baseurl, path, urllib.urlencode(query))
  response = urllib2.urlopen(url)
  returnData = json.loads(response.read())
  return returnData

def set(company):
  '''
    Set company
    
    @type   company: dict
    @param  company: Company returned by getCompanies()
    
    @return: None
  '''
  userinfo.companyid = str(company['companyId'])
