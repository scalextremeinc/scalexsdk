'''
  scalex python SDK tests
  
  please add Oauth client_id and client_secret before test
'''

import scalex

client_id = 'y5uvy4ySubypajanuRyzadu4yXezuqyt'
client_secret = 'eZymyXuPu4eJapa9aguZuReByJuWy2yq'

scalex.setClientId(client_id)
scalex.setClientSecret(client_secret)

coms = scalex.company.getCompanies()
scalex.company.set(coms[0])
scalex.role.set('Admin')  # set role as Admin
