# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Inspired from: https://gist.github.com/cliffano/9868180
#
# Made changes to it suites what we trying achieve for this pci audit
# change to write the output to file.
# summary of each task, pass or fail, or verify. 
# writes output of each server in own file, log/${hostname}.txt and summary of all tasks in summary.csv
# TODO: better gui type reporting based on the csv output, so can be shared with security team for review

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
try:
    import simplejson as json
except ImportError:
    import json
import time

# to record taskname per server
taskid=''

class CallbackModule(CallbackBase):
    def custom_reporter(self, data, host):
        perhost_file = open('log/'+host+'.txt', 'a')
        summary = open('log/summary_report.csv', 'a')
        #print (json.dumps(data,indent=4))
        try:
             module_name=data['invocation']["module_name"]
        except:
             module_name=None

        if module_name == 'setup':
             # this is only availble in setup task, so you use to wirte host details, whcih will be at the start
             datetime=time.strftime("%Y-%m-%d %H:%M")
             try:
                ip=data['ansible_facts']['facter_ipaddress']
             except:
                ip='facter_ipaddress not found'

             try:
                fqdn=data['ansible_facts']['facter_fqdn']
             except:
                fqdn='facter_fqdn not found'

             try:
                osrel=data['ansible_facts']['facter_operatingsystemrelease']
             except:
                osrel='facter_operatingsystemrelease not found'
             
             try:
               os=data['ansible_facts']['facter_operatingsystem']
             except:
               os='facter_operatingsystem not found'

             perhost_file.write("\nDATE: {0}\nHost: {1}\nIP: {2}\nOS: {3} {4}\n============\n".format(datetime,fqdn,ip,os,osrel))
        else:
          if type(data) == dict:
            status='UNKNOWN'
            output=''
            keyfound=False
            # get fields we are interested in 
            if 'stdout' in data.keys():
              stdout=self._format_output(data['stdout'],'stdout')
            else:
              stdout=""
            if 'stderr' in data.keys():
              stderr=self._format_output(data['stderr'],'stderr')
            else:
              stderr=""
            if 'msg' in data.keys():
              msg=self._format_output(data['msg'],'msg')
            else:
              msg=""
            if 'rc' in data.keys():
              rc=self._format_output(data['rc'],'rc')
            else:
              rc=""

            # if we find 'failed' then it's simple as setting it pass or fail.
            if 'failed' in data.keys():
                if data['failed'] == True:
                  status='FAIL'
                  keyfound=True
                  if type(msg) == list:
                    msg=str(msg)
                  if stdout == '' and  stderr == '':
                    output=msg
                else:
                  status='PASS'
                  keyfound=True
                  if type(msg) == list:
                    msg=str(msg)
                  if stdout == '' and stderr == '':
                    if msg != []:
                      output=msg
            else:
               keyfound=False

            # else we look at if its msg is a item data
            if not keyfound:
		output,status=self.itemOutput(msg)
                keyfound=True
		if status == '':
                  keyfound=False
            # at this stage, its not with_items or doesn't have 'failed' failed, so let check rc
            if not keyfound:
                if rc == 0:
                    status='PASS'
                    keyfound=True

            if not keyfound:
                 status='UNKNOWN'
                # TODO: ADD ANY OTHER USE CASES. IF reach here, then haven't captured this yet
                # not all ansibe tasks has bene used, so look into other use cases, if needed

            #print("\n{0}: {1}, {2}".format(field, output.replace("\\n","\n"), status))
            output = output+'\n'+stdout +'\n' + stderr
            if self.taskid != '':
              #print("\n{0}, {1}".format(host,status))
              perhost_file.write("\n{0}, {1}\n {2}".format(self.taskid,status,output))
              summary.write("\n{0}, {1}, {2}'".format(self.taskid,host,status))

    def _format_output(self, output, field):
        # Strip unicode
        if type(output) == unicode:
            output = output.encode('ascii', 'replace')

        # If output is a dict
        if type(output) == dict:
            return json.dumps(output, indent=2)

        if type(output) == list and output == []:
	    return ''

        # If output is a list of dicts
        if type(output) == list and type(output[0]) == dict:
            # This gets a little complicated because it potentially means
            # nested results, usually because of with_items.
            real_output = list()
            for index, item in enumerate(output):
                copy = item
                if type(item) == dict:
                     if field in item.keys():
                        copy[field] = self._format_output(item[field],field)
                real_output.append(copy)
            return real_output

        # If output is a list of strings
        if type(output) == list and type(output[0]) != dict:
            # Strip newline characters
            real_output = list()
            for item in output:
                if "\n" in item:
                    for string in item.split("\n"):
                        real_output.append(string)
                else:
                    real_output.append(item)

            # Reformat lists with line breaks only if the total length is
            # >75 chars
            if len("".join(real_output)) > 75:
                return "\n" + "\n".join(real_output)
            else:
                return " ".join(real_output)

        # Otherwise it's a string, just return it
        return output

    def setTaskID(self,taskname,iscon):
      self.taskid = taskname

    def itemOutput(self,msg):
    # def for iterating through with_items output, to get fail ro pass details per item
                if  type(msg) == list:
                  # this is  when item.results is printed out
                  all_item_output = ""
                  item_failed=False
                  for index, item in enumerate(msg):
                      if type(item) == dict:
                        if 'failed' in item.keys():
                          if item['failed']:
                            item_status='FAIL'
                            item_stdout = item['stderr']+' '+item['stdout']
                            item_failed=True
                          else:
                            item_status='PASS'
                            item_stdout = item['stdout']
                        else:
                          if item['rc'] == 0:
                            item_status='PASS'
                            item_stdout = item['stdout']
                          else:
                            item_status='FAIL'
                            item_stdout = item['stderr']+' '+item['stdout']
                            item_failed=True
                        all_item_output= all_item_output+"\nItem: "+item['item'] +', '+item_status+'\n'+ item_stdout
                      # if it's not a dict, just log the items
                      if (type(item)) != dict:
		        all_item_output = all_item_output +'\n'+item
		       
		  if item_failed:
                    status='FAIL'
                  else:
                    status='PASS'

                  return all_item_output,status
                else:
                  if msg == 'All items completed':
                    status='PASS'
                    stdout = msg
                  elif msg == 'One or more items failed':
                    status='FAIL'
                    stdout = msg
                  elif msg != '':
                    # else it could be just a debug msg, so just display debug msg
                    # N/A on any task which is not applicable
                    if msg == "N/A":
  		      status = 'N/A'
                    else:
  		      status = 'VERIFY'
                    stdout = msg
                  else:
                    status=''
                    stdout=''
                  return stdout,status

    def on_any(self, *args, **kwargs):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.custom_reporter(res,host)

    def runner_on_ok(self, host, res):
        self.custom_reporter(res,host)


    def runner_on_error(self, host, msg):
        pass

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        self.custom_reporter(res,host)

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        self.custom_reporter(res,host)

    def runner_on_async_ok(self, host, res, jid):
        self.custom_reporter(res,host)

    def runner_on_async_failed(self, host, res, jid):
        self.custom_reporter(res,host)

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        self.setTaskID(name,is_conditional) 

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None,
                                encrypt=None, confirm=False, salt_size=None,
                                salt=None, default=None):
        pass

    def playbook_on_setup(self):
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        pass

    def playbook_on_not_import_for_host(self, host, missing_file):
        pass

    def playbook_on_play_start(self, pattern):
        pass

    def playbook_on_stats(self, stats):
        pass
