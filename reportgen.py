# reportgen.py
# simple script to generate cis scan report based on the ouptut from custom plugins
# output all controls, grouped together with PASS, FAIL, VERIFY

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
def getHostStatus(datestamp):
  try:
    with open(raw_log_path+'/'+datestamp+'/summary_report_'+datestamp+'.csv', 'rb') as f:
      reader = csv.reader(f)
      thelist = list(reader)
  except:
    thelist={}
  hosts={}
  for line in thelist:
   if line != []:
     status=line[2].strip()
     h = line[1].strip()
     if status == 'FAIL':
       hosts[h] = status
       break 
     hosts[h]=status
  return hosts

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
count=1
for host in host_list:
  hostname=host.strip()
  reportcount=1
  reportstatus=''
  print '<div class="container">'
  print '<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#host'+str(count)+'">'+hostname,reportstatus+'</button>'
  print '<div id="host'+str(count)+'" class="collapse">'
  for rundate in run_list:
      runstatus = getHostStatus(rundate)
      btn_class = 'btn-info'
      try:
        if runstatus[hostname].startswith ('FAIL'):
          btn_class='btn-danger'
        elif runstatus[hostname].startswith('VERIFY'):
          btn_class='btn-warn'
        elif runstatus[hostname].startswith('PASS'):
          btn_class='btn-success'
      except KeyError as err:
          btn_class='btn-disabled'
      print '<div class="container">'
      print '<button type="button" class="btn '+btn_class+'" data-toggle="collapse" data-target="#report_'+str(count)+''+str(reportcount)+'">'+rundate+'</button>'
      print '<div id="report_'+str(count)+''+str(reportcount)+'" class="collapse">'
      print '<div class="container">'
      print '<button type="button" class="btn btn-danger" data-toggle="collapse" data-target="#reportfailed_'+str(count)+''+str(reportcount)+'">FAILED</button>'
      print '<div id="reportfailed_'+str(count)+''+str(reportcount)+'" class="collapse">'
      print '<div class="table-responsive">'
      print "<table class='table'>"
      print "<tr><td>Date of run: "+rundate+"</td>"
      print "<tr bgcolor=grey><th> control</th> <th> status </th> <th>command</th> <th>output</th></tr>"
      try:
        with open(raw_log_path+'/'+rundate+'/'+hostname+'_'+rundate+'.json','r') as f:
          data = f.readlines()
          for line in data:
	    j = json.loads(line)
            for control, result in j.iteritems():
              colour='lightgreen'
              if result['status'] == 'FAIL':
                colour='red'
                print "<tr bgcolor="+colour+"><td>",control,"</td>", "<td>",result['status'],"</td>"
                print "<td>",result['cmd'],"</td>"
                print "<td>",result['output'],"</td></tr>"
      except IOError as err:
              print "<tr><td>no run for this date</td> <td>",err,"</td> </tr>"
      print "</table>"
      print '</div>'
      print '</div>'
      print '</div>'

      print '<div class="container">'
      print '<button type="button" class="btn btn-success" data-toggle="collapse" data-target="#reportpass_'+str(count)+''+str(reportcount)+'">PASS</button>'
      print '<div id="reportpass_'+str(count)+''+str(reportcount)+'" class="collapse">'
      print '<div class="table-responsive">'
      print "<table class='table'>"
      print "<tr><td>Date of run: "+rundate+"</td>"
      print "<tr bgcolor=grey><th> control</th> <th> status </th> <th>command</th> <th>output</th></tr>"
      try:
        with open(raw_log_path+'/'+rundate+'/'+hostname+'_'+rundate+'.json','r') as f:
          data = f.readlines()
          for line in data:
	    j = json.loads(line)
            for control, result in j.iteritems():
              colour='lightgreen'
              if result['status'] == 'PASS':
                colour='green'
                print "<tr bgcolor="+colour+"><td>",control,"</td>", "<td>",result['status'],"</td>"
                print "<td>",result['cmd'],"</td>"
                print "<td>",result['output'],"</td></tr>"
      except IOError as err:
              print "<tr><td>no run for this date</td> <td>",err,"</td> </tr>"
      print "</table>"
      print '</div>'
      print '</div>'
      print '</div>'

      print '<div class="container">'
      print '<button type="button" class="btn btn-warning" data-toggle="collapse" data-target="#reportverify_'+str(count)+''+str(reportcount)+'">VERIFY</button>'
      print '<div id="reportverify_'+str(count)+''+str(reportcount)+'" class="collapse">'
      print '<div class="table-responsive">'
      print "<table class='table'>"
      print "<tr><td>Date of run: "+rundate+"</td>"
      print "<tr bgcolor=grey><th> control</th> <th> status </th> <th>command</th> <th>output</th></tr>"
      try:
        with open(raw_log_path+'/'+rundate+'/'+hostname+'_'+rundate+'.json','r') as f:
          data = f.readlines()
          for line in data:
	    j = json.loads(line)
            for control, result in j.iteritems():
              colour='lightgreen'
              if result['status'] == 'VERIFY' or result['status'] == 'UNKNOWN':
                colour='orange'
                print "<tr bgcolor="+colour+"><td>",control,"</td>", "<td>",result['status'],"</td>"
                print "<td>",result['cmd'],"</td>"
                print "<td>",result['output'],"</td></tr>"
      except IOError as err:
              print "<tr><td>no run for this date</td> <td>",err,"</td> </tr>"
      print "</table>"
      print '</div>'
      print '</div>'

      print '</div>'
      print '</div>'
      print '</div>'
      reportcount =  reportcount + 1
  print '</div>'
  print '</div>'
  count =  count + 1
print "</body>"
print "</html>"
