'''
  @undocumented: __package__
  
'''

import urllib
import urllib2
import json
import base64
import time
import datetime
#
from scalex import userinfo

def getBudgets():
  '''
    Get list of budgets
    
    @rtype: list
    @return: list of all budgets for a Role and User
  '''
  
  path = '/budgets'
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getInfo(budget):
  '''
    Gets budget information for a particular budget
    
    @type   budget: dict
    @param  budget: budget object returned by getBudgets()
    
    @rtype: dict
    @return: budget information for the budget
    '''
  
  path = '/budgets/' + str(budget['budgetId'])
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _getUsers():
  '''
    returns:
    [{"authtype":0,"userID":10093,"companyId":0,"user":"org40042@gmail.com"}]
  '''
  path = '/budgets/users'
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def _getRoles():
  '''
    {u 'roleName': u 'Admin'}
  '''
  path = '/budgets/roles'
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def getLimitBean(budgetLevel):
  '''
    Get limit bean for the given budgetLevel
    
    @type   budgetLevel: string
    @param  budgetLevel: Budget Level, default value is B{org}. Valid values are:
      - B{org}, Organization
      - B{user}, User
      - B{role}, Role
    
    @rtype: list
    @return: Limit bean
  '''
  limits = []
  #  
  if budgetLevel.lower() == 'org':
    from scalex import company
    coms = company.getCompanies()
    for a in coms:
      limit = {
#        "budgetId": 0,
        "orgName": a['name'],
        "budgetedOrganizationId": a['companyId'],
#        "budgetedRole": None,
#        "budgetedUserId": 0,
        "softLimit": "0",
        "hardLimit": "0"
      }
      limits.append(limit)
  #  
  if budgetLevel.lower() == 'user':
    for a in _getUsers():
      limit = {
#        "budgetId": 0,
#        "budgetedOrganizationId": 0,
#        "budgetedRole": None,
        "userName": a['user'],
        "budgetedUserId": a['userID'],
        "softLimit": "0",
        "hardLimit": "0"
      }
      limits.append(limit)
  #        
  if budgetLevel.lower() == 'role':
    for a in _getRoles():
      limit = {
#        "budgetId": 0,
#        "budgetedOrganizationId": 0,
        "budgetedRole": a['roleName'],
#        "budgetedUserId": 0,
        "softLimit": "0",
        "softLimit": "0"
      }
      limits.append(limit)
  #  
  return limits

def create(name = '', description = '', providerAccountId = -999, periodType = 'monthly', budgetLevel = 'org', startTime = 0, endTime = 0, limits = {}):
  '''
    Create a budget
    
    @todo: Support provider account

    @type   name: string
    @param  name: Budget name
    
    @type   description: string
    @param  description: Budget description
    
    @type   periodType: string
    @param  periodType: Period Type of budget, default value is B{monthly}. Valid values are:
      - B{monthly}
      - B{weekly}
    
    @type   budgetLevel: string
    @param  budgetLevel: Budget Level, default value is B{org}. Valid values are:
      - B{org}, Organization
      - B{user}, User
      - B{role}, Role
    
    @param  startTime: Start time formatted like B{2012-12-12-00:00}, default is now

    @param  endTime: End time formatted like B{2012-12-12-00:00}, default is one year later
    
    @type   limits: list
    @param  limits: Soft and Hard Limits in your local currency. Default is 0, get limits use scalex.budget.getLimitBean(budgetLevel), change it's softLimit and hardLimit.
    
    @rtype: dict
    @return: Budget just created
    '''
  #  
  path = '/budgets'
  url = userinfo.geturl(path)
  #  
  if startTime != 0:
    d = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H:%M")
    startTime = int(time.mktime(d.timetuple())*1000)
  else:
    startTime = int(time.time()*1000)
  if endTime != 0:
    d = datetime.datetime.strptime(endTime, "%Y-%m-%d-%H:%M")
    endTime = int(time.mktime(d.timetuple())*1000)
  else:
    timeOfOneYear = 365*24*60*60*1000
    endTime = endTime + timeOfOneYear
# period type
  assert periodType.lower() in ['monthly', 'weekly'], 'Wrong periodType'
# budget level and limits
  assert budgetLevel.lower() in ['org', 'user', 'role'], 'Wrong budgetLevel'
  if limits == {}:
    limits = getLimitBean(budgetLevel)
  else:
    for a in limits:
      a['softLimit'] = str(a['softLimit'])
      a['hardLimit'] = str(a['hardLimit'])

  if budgetLevel == 'org':
    budgetLevel = 'ORGANIZATION'
  budgetBean = {
#    'budgetId': 0,
    'budgetName': name,
    'description': description,
    'budgetLevel': budgetLevel.upper(),
    'budgetBy': 'BY_PROVIDER_ACCOUNT',
    'providerAccountId': providerAccountId,  #this is provider account, -999 means all provider account
    'tag': None,
    'effectiveStartTimestamp': startTime,
    'effectiveEndTimestamp': endTime,
    'periodType': periodType.upper(),
    'budgetDetails': limits
  }    
  postData = json.dumps(budgetBean)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def update(budget, name = '', description = '', startTime = 0, endTime = 0, limits = {}):
  '''
    Update a budget
    Provider Account, Period Type and Budget Level can't be updated
    
    @param  budget: The budget you want to update
    
    @type   name: string
    @param  name: Budget name
    
    @type   description: string
    @param  description: Budget description

    @param  startTime: Start time formatted like B{2012-12-12-00:00}, default is now
    
    @param  endTime: End time formatted like B{2012-12-12-00:00}, default is one year later
    
    @rtype: dict
    @return: budget just updated
  '''
  path = '/budgets/' + str(budget['budgetId'])
  url = userinfo.geturl(path)
#  
  budgetBean = getInfo(budget)
#  
  if name != '':
    budgetBean['budgetName'] = name
  if description != '':
    budgetBean['description'] = description
  if startTime != 0:
    d = datetime.datetime.strptime(startTime, "%Y-%m-%d-%H:%M")
    budgetBean['effectiveStartTimestamp'] = int(time.mktime(d.timetuple())*1000)
  if endTime != 0:
    d = datetime.datetime.strptime(endTime, "%Y-%m-%d-%H:%M")
    budgetBean['effectiveEndTimestamp'] = int(time.mktime(d.timetuple())*1000)
#
  postData = json.dumps(budgetBean)
  request = urllib2.Request(url, postData)
  request.add_header('Content-Type', 'application/json')
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData

def delete(budget):
  '''
    Delete a budget
    
    @param budget: The budget you want to delete
  '''
  path = '/budgets/' + str(budget['budgetId'])
  #
  url = userinfo.geturl(path)
  request = urllib2.Request(url)
  request.get_method = lambda: 'DELETE'
  response = urllib2.urlopen(request)
  returnData = json.loads(response.read())
  return returnData
