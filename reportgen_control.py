# reportgen.py
# simple script to generate cis scan report based on the ouptut from custom plugins
# output failed controls and hosts per control

import json
import sys
import os
import csv

raw_log_path='reports/raw'

def getRuns(reports_path):
  dates =  [f for f in os.listdir(reports_path) if os.path.isdir(os.path.join(raw_log_path, f))]
  return sorted(dates, reverse=True)


def getHosts (hostfile):
  with open(hostfile, 'r') as f:
    your_list = f.readlines()
  hosts=[]
  for line in your_list:
     h = line[1]
     if not line.startswith ('#'):
       hosts.append(line.strip())
  return hosts


# get overall status of a host
def getControls(datestamp):
  try:
    with open(raw_log_path+'/'+datestamp+'/summary_report_'+datestamp+'.csv', 'rb') as f:
      reader = csv.reader(f)
      thelist = list(reader)
  except IOError as err:
    print err
    thelist={}
  failed_controls=[]
  failed_hosts=''
  for line in thelist:
   if line != []:
     status=line[2].strip()
     control=line[0].strip()
     h = line[1].strip()
     if status.startswith('FAIL'):
       failed_controls.append(control)
   result=[]
  map(lambda x: not x in result and result.append(x), failed_controls)
  return result

def getHostsPerControl(datestamp,control):
  try:
    with open(raw_log_path+'/'+datestamp+'/summary_report_'+datestamp+'.csv', 'rb') as f:
      reader = csv.reader(f)
      thelist = list(reader)
  except IOError as err:
    print err
    thelist={}
  failed_hosts=[]
  for line in thelist:
   if line != []:
     thiscontrol = line[0].strip()
     status = line[2].strip()
     if thiscontrol.startswith(control):
       h = line[1].strip()
       if status.startswith('FAIL'):
         failed_hosts.append(h)
  return failed_hosts

print "<html>"
print "<head>"
print '  <meta name="viewport" content="width=device-width, initial-scale=1">'
print '  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">'
print '  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>'
print '  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>'
print '</head>'
print '<body>'
print '<center><h3> cis scan report</h3></center>' 

run_list=getRuns(raw_log_path)
host_list=getHosts('test-hosts')
reportcount=0
print '<div class="container">'
print 'Run dates:'
print '</div>'
for rundate in run_list:
  failcontrols = getControls(rundate)
  count=0
  reportcount= reportcount + 1
  print '<div class="container">'
  print '<button type="button" class="btn btn-danger" data-toggle="collapse" data-target="#report_'+str(count)+''+str(reportcount)+'">'+rundate+'</button>'
  print '<div id="report_'+str(count)+''+str(reportcount)+'" class="collapse">'
  for control in failcontrols:
    hosts=getHostsPerControl(rundate,control)
    hostcount=len(hosts)
    count = count + 1

    print '<div class="panel-group" role="tablist">'
    print '<div class="panel panel-default">'
    print '<div class="panel-heading" role="tab" id="collapseListGroupHeading'+str(count)+''+str(reportcount)+'">'
    print '<h4 class="panel-title">'
    print '<a class="collapsed" data-toggle="collapse" href="#collapseListGroup'+str(count)+''+str(reportcount)+'" aria-expanded="false" aria-controls="collapseListGroup'+str(count)+''+str(reportcount)+'">'+control+'</a>'
    print '<span class="badge">'+str(hostcount)
    print '</h4>'
    print '</div>'
    print '<div id="collapseListGroup'+str(count)+''+str(reportcount)+'" class="panel-collapse collapse" role="tabpane'+str(count)+''+str(reportcount)+'" aria-labelledby="collapseListGroupHeading'+str(count)+''+str(reportcount)+'">'
    print '<ul class="list-group">'
    for host in hosts:
      print '<li class="list-group-item">'+host+'</li>'
    print '</ul>'
    print '</div>'
    print '</div>'
    print '</div>'
  
  print "</div>"
  print "</div>"
print "</body>"
print "</html>"
