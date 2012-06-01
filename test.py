import scalex

s = scalex.scaleXtreme('karthik@scalextreme.com', '123456')
s.login()
s.getCompanies()
s.companies
s.setCompany(10361)
s.setRole('Admin')
s.getMyScripts()
s.myScripts
s.getJobsForScript('7')
s.getRunsForJob(s.jobs['7'][0]['jobId'])
print s.runs
s.getOutputForRun(s.jobs['7'][0]['jobId'], s.runs[s.jobs['7'][0]['jobId']][0]['projectId'], s.runs[s.jobs['7'][0]['jobId']][0]['projectRunId'])
