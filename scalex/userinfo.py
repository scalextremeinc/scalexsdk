import uuid
import scalex

#for Oauth
client_id = 'y5uvy4ySubypajanuRyzadu4yXezuqyt'
client_secret = 'eZymyXuPu4eJapa9aguZuReByJuWy2yq'
access_token = ''

domain = 'https://cloudmanage.scalextreme.com'
baseurl = 'https://cloudmanage.scalextreme.com/v0'

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