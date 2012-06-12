import uuid
import scalex

#for Oauth
client_id = 'y5uvy4ySubypajanuRyzadu4yXezuqyt'
client_secret = 'eZymyXuPu4eJapa9aguZuReByJuWy2yq'
access_token = 'u18j6344ag98w9t5zshgom8ji'

domain = 'https://cloudmanage.scalextreme.com'
baseurl = 'https://cloudmanage.scalextreme.com/v0'

rid = str(uuid.uuid4())
cookie = ''
username = ''
password = ''
userid = ''
companyid = ''
rolename = ''

def check():
  assert userid != '', 'you need login first'
  assert companyid != '','you need setCompany first'
  assert rolename != '', 'you need setRole first'
  scalex.relogin()

def geturl(path, query = {}):
  assert path != ''
  import urllib
  query['access_token'] = access_token
  query = urllib.urlencode(query)
  url = baseurl + path + '?' + query
  return url