import urllib
import urllib2
import json
#
import userinfo

def get():
  if userinfo.userid == '':
    print 'you need login first'
    return
  if userinfo.companyid == '':
    print 'you need setCompany first'
    return
  
  url = '%s/scalex/acl/userroles?rid=%s' % (userinfo.domain, userinfo.rid)
  value = {
    'user':userinfo.username,
    'companyId':userinfo.companyid
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData
