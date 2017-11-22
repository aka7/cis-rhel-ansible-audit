# Ansible + CIS Benchmarks + RHEL/CentOS 6

Ansible audit for CIS.

This is an ansible playbook for auditing a system running Red Hat Enterprise Linux 6 or CentOS 6  to see if it passes CIS Security Benchmarks.

Insipired by https://github.com/major/cis-rhel-ansible but instead of applying the changes, this will just report if a system passes or fails for each task.

If you want to remedy the failed tasks, I recommend you use https://github.com/major/cis-rhel-ansible

### setup
provide your inventory file.  Example uses hosts set in test-hosts

update vars/main.yml to suit your organisation settings, such as ntp server, mailconfig, syslog_dest. Update if conditions where ansible_domain check is used, i.e  syslog_dest, puppet_server replace the domain with your domain names per environment.

The shells scripts in files/bin are taken from cis report.  These checks are disbaled by default, some find commands can take a while to run.  This is entirely upto you if like to to enable it.

To enable these checks, set vars `verify_find` and `run_shell_scripts` to  yes, in vars/mail.yml

```
verify_find: no
run_shell_scripts: no
```

section10 is added to allow any company specific controls, which are not requirement of CIS, such as checking for puppet.

enable plugins/custom_reporter.py in ansible.cfg (set by default)

```
callback_plugins = plugins
```
This is enabled by the default in ansible.cfg file provided.

Make sure this is in the current directory.

### Warn 
Check the scripts in files/bin and enable them as mentioned.  These checks are disabled by default, just so you can review them before running.

It is safe to run all the checks on this playbook. Some tasks could take a while to run depending on your infrastructure.  I would recommand you run this on a test server first before running against multiple servers. No changes are made on the system.

### Example:
```
ansible-playbook -i test-hosts playbook.yml --extra-vars="nodes=all" --tags=section1 -K -k

```

Generate reports (if customer_reporter.py plugin is enabled)

```
python reportgen.py -i test-hosts 
python reportgen_control.py -i test-hosts

```
open file cis_report.html in browser to see the result.

open file cis_report_per_control.html in browser to see result per control.

you can also view the .csv file 

reports/raw/${date}/summary_report_${date}.csv


# LOGS and REPORTS

Custom logs, if custom_reporter plugin is enabled, you can find logs in reports/raw dir.  if dir doesn't exists, it will create it. These logs are generated so we can then run scripts to generate fancy report. .csv can be opened in excel to view at a glance on which controls failed.

```
reports/raw/${date}/${hostname}-${date}.json
reports/raw/${date}/summary_report_${date}.csv
```

Logs will always have date and time of run.

example output, for summary_report.csv, will look like his

```
TASK: cis : 1.1.18 Disable Mounting of cramfs Filesystems (Not Scored), alif.aka47.local, FAIL'
TASK: cis : 1.1.19 Disable Mounting of freevxfs Filesystems (Not Scored), alif.aka47.local, PASS'
TASK: cis : 1.1.20 Disable Mounting of jffs2 Filesystems (Not Scored), alif.aka47.local, FAIL'
TASK: cis : 1.1.21 Disable Mounting of hfs Filesystems (Not Scored), alif.aka47.local, PASS'
TASK: cis : 1.1.22 Disable Mounting of hfsplus Filesystems (Not Scored), alif.aka47.local, PASS'
TASK: cis : 1.1.23 Disable Mounting of squashfs Filesystems (Not Scored), alif.aka47.local, FAIL'
TASK: cis : 1.1.24 Disable Mounting of udf Filesystems (Not Scored), alif.aka47.local, FAIL'
TASK: cis : 1.2.4 Disable the rhnsd Daemon (Not Scored), alif.aka47.local, PASS'
TASK: cis : 1.3.1 Install AIDE (Scored), alif.aka47.local, FAIL'
TASK: cis : 1.3.2 Implement Periodic Execution of File Integrity (Scored), alif.aka47.local, FAIL'
TASK: cis : 1.4.1 Enable SELinux in /etc/grub.conf (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.1 Enable SELinux in /etc/grub.conf (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.2 Set the SELinux State (set in file) (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.2 Set the SELinux State (sestatus) (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.3 Set the SELinux Policy (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.4 Remove SETroubleshoot (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.5 Remove MCS Translation Service (mcstrans) (Scored), alif.aka47.local, PASS'
TASK: cis : 1.4.6 Check for unconfined daemons (Scored), alif.aka47.local, PASS'
TASK: cis : 2.1.11 - Check if xinetd is installed (Scored), alif.aka47.local, PASS'
TASK: cis : 4.2.3 Disable Secure ICMP Redirect Acceptance (Scored), alif.aka47.local, FAIL'
TASK: cis : 4.2.7 Enable RFC-recommended Source Route Validation (Scored), alif.aka47.local, FAIL'
TASK: cis : 5.2.1.1 Configure Audit Log Storage Size (Not Scored), alif.aka47.local, PASS'
TASK: cis : 5.2.1.2 Disable System on Audit Log Full (Not Scored), alif.aka47.local, PASS'
TASK: cis : 5.2.1.2 Disable System on Audit Log Full (Not Scored), alif.aka47.local, PASS'
TASK: cis : 5.2.1.2 Disable System on Audit Log Full (Not Scored), alif.aka47.local, PASS'
TASK: cis : 5.2.1.3 Keep All Auditing Information (Scored), alif.aka47.local, FAIL'
TASK: cis : 5.2.2 Enable auditd Service (Scored), alif.aka47.local, FAIL'
TASK: cis : 5.2.3 Enable Auditing for Processes That Start Prior to auditd (Scored), alif.aka47.local, FAIL'
TASK: cis : command, alif.aka47.local, FAIL'
TASK: cis : 5.2.4 - 5.2.17  Configure auditd Rules (Scored), alif.aka47.local, FAIL'
TASK: cis : 5.2.18 Make the Audit Configuration Immutable (Scored), alif.aka47.local, FAIL'

```

# REPORTS

To generate nice html report, there are two python scripts.  The scripts read the summary csv and the host.json files to generate html output.


```
python reportgen.py -i test-hosts 

```
reportgen.py will output file called  reports/html/cisreport.html

This will generate report of all the runs found in reports/raw dir, for all hosts given in test-hosts inventory file.


To output html report per failed control, with collapse list of host listed, run reportgen_per_control.py

```
python reportgen_per_control.py -i test-hosts 

```
reportgen_control.py will output file called  reports/html/cis_report_per_control.html

This will generate report of all the runs found in reports/raw dir, list only the failed controls and which hosts failed. For all hosts given in test-hosts inventory file.

open file in browser, or place in www dir on a webserver to view. This is a static file.


These reports scripts are in progress  and has been created for a quick html view of the reports generated.

All the scripts needs to run from current dir of where playbook.yml is located.


# NOTES On Custom_reporter plugin

  - Logs only if a task has a name, this is so we can managed logging and only log the tasks we like to report on by giving a name.
  - Do not add any comma(,) in name. This is because of summary_report.csv , otherwise you will have more fields when you open the file in excel.


TODO:
  - improve reporting, html out, csv output
  - show remedy options for each failed control
  - rhel7/centos7 support

# Limitations
requires ansible > 2.1
tested only againnst ansible 2.1

Tested on ansible 2.1 only.
