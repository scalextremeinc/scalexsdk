'''
  FIXME, add doc string
  '''

import hashlib
import urllib
import urllib2
import json
#
import userinfo

__version__ = '0.5'

#_domain = 'https://manage.scalextreme.com'
#_rid = str(uuid.uuid4())
#_cookie = ''
#_user = ''
#_userid = ''
#_companyid = ''
#_rolename = ''
#

def login(username, password):
  '''login with username and password
    '''
  userinfo.username = username
  pwd = hashlib.md5(password).hexdigest()
  url = '%s/scalex/acl/authenticate?type=scalex&rid=%s' % (userinfo.domain, userinfo.rid)
  value = {
    'user':username,
    'password':pwd
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  userinfo.cookie = response.headers.get('Set-Cookie')
  returnData = response.read()
  userinfo.userid = json.loads(returnData)['data']['userID']
  return returnData
