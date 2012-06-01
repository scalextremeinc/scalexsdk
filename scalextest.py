#!/usr/bin/env python

import scalex

sx = scalex.scaleXtreme('karthik@scalextreme.com', '123456')
print sx.login()
print sx.getCompanies()
print sx.setCompany(10274)
print sx.getRoles()
print sx.setRole('Admin')
print sx.getNodes()
print sx.getMyScripts()
print sx.getJobsForScript(1080)
print sx.getRunsForJob(629)
print sx.getOutputForRun(629, 734, 1676)
#sx.runScript(['7', '3', '9,18', '0'])
