'''
  scalextreme.com python sdk
  
  @undocumented: userinfo
  @undocumented: __package__
  
  @change:
    - Delete login()
    - Add setClientId()
    - Add setClientSecret()
    - API return data directly, old style API return data like scalex.role.getRoles()['data'], with new API you just need scalex.role.getRoles()
    - API error handling changed, all errors return as http status codes and B{will raise urllib2.HTTPError}. Below list explains each error  
      - 400  Bad input parameters or error messages. To fix this issue, API consumer need to pay attention to input parameters
      - 401  Bad credentials or expired token. To fix this need to authenticate with valid credentials
      - 500  Internal server error. This should happen only if we are not handling errors on server side.
'''

import hashlib
import urllib
import urllib2
import json
#
import company
import role
import node
import job
import script
import userinfo

__version__ = '0.6'

def setClientId(id):
  '''
    Set client_id for Oauth
    
    @type   id: string
    @param  id: client_id for Oauth
    
    @return: None
  '''
  assert id != '', 'empty client id'
  userinfo.client_id = id

def setClientSecret(secret):
  '''
    Set client_secret for Oauth
    
    @type   secret: string
    @param  secret: client_secret for Oauth
    
    @return: None
  '''
 
  assert secret != '', 'empty client secret'
  userinfo.client_secret = secret

#auth after set role, automatically
def _auth():
  assert userinfo.companyid != '' and userinfo.rolename != '', 'no companyid or rolename'
  
  path = '/oauth/token'
  scope = userinfo.rolename + ',' + userinfo.companyid
  query = {
    'grant_type':'client_credentials',
    'scope':scope
  }
  url = '%s%s?%s' % (userinfo.baseurl, path, urllib.urlencode(query))
  request = urllib2.Request(url, '')
  import base64
  authorization = 'Basic ' + base64.b64encode(userinfo.client_id + ':' + userinfo.client_secret)
  request.add_header('Authorization', authorization)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  userinfo.access_token = returnData['value']
#  print userinfo.access_token
  return returnData

#function
#def login(username, password):
#  '''login with username and password
#    '''
#  assert username != '' and password != '', 'username/password is empty'
#  userinfo.username = username
#  userinfo.password = password
#  pwd = hashlib.md5(password).hexdigest()
#  url = '%s/scalex/acl/authenticate?type=scalex&rid=%s' % (userinfo.domain, userinfo.rid)
#  value = {
#    'user':username,
#    'password':pwd
#  }
#  postData = urllib.urlencode(value)
#  response = urllib2.urlopen(url, postData)
#  userinfo.cookie = response.headers.get('Set-Cookie')
#  returnData = json.loads(response.read())
#  if returnData['result'] == 'SUCCESS':
#    userinfo.userid = returnData['data']['userID']
#  return returnData
#
#def relogin():
#  return login(userinfo.username, userinfo.password)
