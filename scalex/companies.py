import urllib
import urllib2
import json
#
import userinfo

def get():
  if userinfo.userid == '':
    print 'you need login first'
    return
  url = '%s/scalex/acl/usercompanies?rid=%s' % (userinfo.domain, userinfo.rid)
  value = {
    'userId':userinfo.userid
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData
