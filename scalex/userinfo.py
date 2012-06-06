import uuid
import scalex

domain = 'https://manage.scalextreme.com'
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
