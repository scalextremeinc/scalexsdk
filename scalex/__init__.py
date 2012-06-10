'''
  scalextreme.com python sdk
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

__version__ = '0.5'

#function
def login(username, password):
  '''login with username and password
    '''
  assert username != '' and password != '', 'username/password is empty'
  userinfo.username = username
  userinfo.password = password
  pwd = hashlib.md5(password).hexdigest()
  url = '%s/scalex/acl/authenticate?type=scalex&rid=%s' % (userinfo.domain, userinfo.rid)
  value = {
    'user':username,
    'password':pwd
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  userinfo.cookie = response.headers.get('Set-Cookie')
  returnData = json.loads(response.read())
  if returnData['result'] == 'SUCCESS':
    userinfo.userid = returnData['data']['userID']
  return returnData

def relogin():
  return login(userinfo.username, userinfo.password)