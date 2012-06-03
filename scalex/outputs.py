import urllib
import urllib2
import json
#
import userinfo

def get(jobid, projectid, projectrunid):
  '''arguments: jobid, projectid, projectrunid
    '''
  if userinfo.companyid == '' or userinfo.rolename == '':
    print 'you need setCompany and setRole first'
    return
  payload = {
    "companyId": userinfo.companyid,
    "jobId": str(jobid),
    "user": str(userinfo.userid),
    "role": userinfo.rolename,
    "projectRunId": projectrunid,
    "projectId": projectid,
    "jobId": jobid
  }
  postData = 'payload=' + json.dumps(payload)
  url = userinfo.domain + '/managejob'
  value = {
    'companyid':userinfo.companyid,
    'user':userinfo.username,
    'role':userinfo.rolename,
    'operation':'runoutput',
    'rid':userinfo.rid
  }
  query = urllib.urlencode(value)
  url = url + '?' + query
  request = urllib2.Request(url, postData)
  request.add_header('cookie', userinfo.cookie)
  response = urllib2.urlopen(request).read()
  return response
