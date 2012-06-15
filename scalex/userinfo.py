import scalex

#for Oauth
client_id = ''
client_secret = ''
access_token = ''

domain = 'https://manage.scalextreme.com'
baseurl = domain + '/v0'

companyid = ''
rolename = ''

def geturl(path, query = {}):
  assert path != ''
  import urllib
  query['access_token'] = access_token
  query = urllib.urlencode(query)
  url = baseurl + path + '?' + query
  return url