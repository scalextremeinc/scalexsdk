import scalex

groups = []

def setup():
  global groups
  groups = scalex.group.getGroups()

def CRUD():
  pass

def test_getNodesOfGroup():
  scalex.group.getNodesOfGroup(groups[0])

