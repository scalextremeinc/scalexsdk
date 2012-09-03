import sys
import scalex
import time

# getInfo()
def normalFunction():
  budgets = scalex.budget.getBudgets()
  scalex.budget.getInfo(budgets[0])

def CRUD():
  budgets = scalex.budget.getBudgets()
  #  
  budgetLevels = ['org', 'user', 'role']
  for a in budgetLevels:
    limits = scalex.budget.getLimitBean(a)
    for b in limits:
      b['softLimit'] = '2'
      b['hardLimit'] = '2'
    print limits
    budget = scalex.budget.create('budget-test-create', 'desc', budgetLevel = a, limits = limits)
    budget = scalex.budget.update(budget, 'budget-name-modified', description = 'desc-mod')
    #  delete
    scalex.budget.delete(budget)

def test():
  CRUD()
  normalFunction()

