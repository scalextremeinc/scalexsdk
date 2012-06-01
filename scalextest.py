#!/usr/bin/env python

import scalex

sx = scalex.scaleXtreme('karthik@scalextreme.com', '123456')
sx.login()
print sx.getCompanies()
sx.setCompany(10361)
print sx.getRoles()
sx.setRole('Admin')
print sx.getNodes()
print sx.getMyScripts()
print sx.getJobsForScript(7)
print sx.getRunsForJob(20)
print sx.getOutputForRun(20, 24, 145)
sx.runScript(['7', '3', '9,18', '0'])
