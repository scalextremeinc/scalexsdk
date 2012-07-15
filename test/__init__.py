'''
  scalex python SDK tests
  
  please add Oauth client_id and client_secret before test
'''

import scalex

holder = 'REPLACE ME'
client_id = holder
client_secret = holder

assert client_id != holder or client_secret != holder, 'Please add client_id and client_secret in __init__.py before test'
scalex.setClientId(client_id)
scalex.setClientSecret(client_secret)

coms = scalex.company.getCompanies()
scalex.company.set(coms[0])
scalex.role.set('Admin')  # set role as Admin
