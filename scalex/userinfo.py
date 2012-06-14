import uuid
import scalex

#for Oauth
client_id = 'Set Your client_id Here'
client_secret = 'Set Your client_secret Here'
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