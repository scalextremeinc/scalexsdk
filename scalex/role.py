'''
  @undocumented: __package__
'''
import urllib
import urllib2
import json
import base64
#
from scalex import userinfo
import scalex

def getRoles():
  '''
    Get list of roles

    @requires: Set company first
    
    @rtype: list
    @return: list of roles
  '''
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

def set(role):
  '''
    Set role
    
    @type   role: string
    @param  role: role returned by getRoles()
    
    @return: None
  '''

  assert role != '', 'wrong rolename'
  userinfo.rolename = role
#  get access token after set role
  scalex._auth()


