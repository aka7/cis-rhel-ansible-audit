# reportgen.py
# simple script to generate cis scan report based on the ouptut from custom plugins
# output failed controls and hosts per control

import json
import sys
import os
import csv
from optparse import OptionParser

raw_log_path='reports/raw'
report_path = 'reports/html'


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
    print  err
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

# get control details
def getHostControlDetails(hostname,control_id,datestamp):
  try:
    with open(raw_log_path+'/'+datestamp+'/'+hostname+'_'+datestamp+'.json', 'rb') as f:
      data = f.readlines()
      for line in data:
        j = json.loads(line)
        for control, result in j.iteritems():
          if control.startswith(control_id):
            return control,result
  except IOError as err:
   return control_id,{}
  return control_id,{}

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

parser = OptionParser()
parser.add_option("-i", "--inventory", dest="inventoryfile",
                  help="inventory list of hostnames")

(options, args) = parser.parse_args()

if not options.inventoryfile:
	parser.print_help()
	sys.exit(1)

if not os.path.exists(report_path):
  os.mkdir(report_path)
htmlfile = open(report_path+'/cis_report_per_control.html','w') 

htmlfile.write( "<html>")
htmlfile.write( "<head>")
htmlfile.write( '  <meta name="viewport" content="width=device-width, initial-scale=1">')
htmlfile.write( '  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">')
htmlfile.write( '  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>')
htmlfile.write( '  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>')
htmlfile.write ( '<script> $(document).ready(function(){ $("[data-toggle=\'tooltip\']").tooltip(); }); </script>')
htmlfile.write( '</head>')
htmlfile.write( '<body>')
htmlfile.write( '<center><h3> CIS scan report</h3></center>' )

run_list=getRuns(raw_log_path)
host_list=getHosts(options.inventoryfile)

# count needed for uniq html collapse tartgets
reportcount=0

htmlfile.write( '<div class="container">')
htmlfile.write( 'Run dates:')
htmlfile.write( '</div>')
for rundate in run_list:
  failcontrols = getControls(rundate)
  count=0
  reportcount= reportcount + 1
  htmlfile.write( '<div class="container">')
  htmlfile.write( '<button type="button" class="btn btn-danger" data-toggle="collapse" data-target="#report_'+str(count)+''+str(reportcount)+'">'+rundate+'</button>')
  htmlfile.write( '<div id="report_'+str(count)+''+str(reportcount)+'" class="collapse">')
  for control in failcontrols:
    hosts=getHostsPerControl(rundate,control)
    hostcount=len(hosts)
    count = count + 1

    htmlfile.write( '<div class="panel-group" role="tablist">')
    htmlfile.write( '<div class="panel panel-default">')
    htmlfile.write( '<div class="panel-heading" role="tab" id="collapseListGroupHeading'+str(count)+''+str(reportcount)+'">')
    htmlfile.write( '<h4 class="panel-title">')
    htmlfile.write( '<a class="collapsed" data-toggle="collapse" href="#collapseListGroup'+str(count)+''+str(reportcount)+'" aria-expanded="false" aria-controls="collapseListGroup'+str(count)+''+str(reportcount)+'" data-toggle="tooltip" title="info on control">'+control+'</a>')
    htmlfile.write( '<span class="badge">'+str(hostcount))
    htmlfile.write( '</h4>')
    htmlfile.write( '</div>')
    htmlfile.write( '<div id="collapseListGroup'+str(count)+''+str(reportcount)+'" class="panel-collapse collapse" role="tabpane'+str(count)+''+str(reportcount)+'" aria-labelledby="collapseListGroupHeading'+str(count)+''+str(reportcount)+'">')
    htmlfile.write( '<ul class="list-group">')
    for host in hosts:
      ctlname,controlout = getHostControlDetails(host,control,rundate)
      cmd_out = controlout['output']
      htmlfile.write( '<li class="list-group-item"> <a href="#" data-toggle="tooltip" title="'+cmd_out+'">'+host+'</a>')
      htmlfile.write( '</li>')
    htmlfile.write( '</ul>')
    htmlfile.write( '</div>')
    htmlfile.write( '</div>')
    htmlfile.write( '</div>')
  
  htmlfile.write( "</div>")
  htmlfile.write( "</div>")
htmlfile.write( "</body>")
htmlfile.write( "</html>")

print 'Html report generated in'+report_path
