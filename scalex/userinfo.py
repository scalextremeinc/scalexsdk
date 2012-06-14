import uuid
import scalex

#for Oauth
client_id = ''
client_secret = ''
access_token = ''

domain = 'https://cloudmanage.scalextreme.com'
baseurl = domain + '/v0'

rid = str(uuid.uuid4())
cookie = ''
username = ''
password = ''
userid = ''
companyid = ''
rolename = ''

def geturl(path, query = {}):
  assert path != ''
  import urllib
  query['access_token'] = access_token
  query = urllib.urlencode(query)
  url = baseurl + path + '?' + query
  return url