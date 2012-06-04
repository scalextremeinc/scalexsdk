import urllib
import urllib2
import json
#
import userinfo

def getNodes():
  if userinfo.companyid == '' or userinfo.rolename == '':
    #print 'you need setCompany and setRole first'
    return
  
  url = userinfo.domain + '/scalex/acl/nodelistbyrole?rid=%s' % (userinfo.rid)
  value = {
    'companyId':userinfo.companyid,
    'role':userinfo.rolename,
    'user':userinfo.username
  }
  postData = urllib.urlencode(value)
  response = urllib2.urlopen(url, postData)
  returnData = json.loads(response.read())
  return returnData
