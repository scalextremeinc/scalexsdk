import urllib
import urllib2
import json
#
import userinfo

def get():
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  
  url = self.domain + '/scalex/acl/nodelistbyrole?rid=%s' % (self.rid)
  value = {
    'companyId':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.username
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData).read()
  return response
