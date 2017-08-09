# Ansible + CIS Benchmarks + RHEL/CentOS 6

Ansible audit for CIS.

This is an ansible playbook for auditing a system running Red Hat Enterprise Linux 6 or CentOS 6  to see if it passes CIS Security Benchmarks.

Insipired by https://github.com/major/cis-rhel-ansible but instead of applying the changes, this will just report if a system passes or fails for each task.

# NOTE
this project is still in profject,  added following sections so far
- section1
- section2
- section3
- section4
- section5

### setup
add  hosts in your ansible file, i.e test-hosts

update vars/main.yml to suit your setup

### Example:
```
ansible-playbook -i test-hosts playbook.yml --extra-vars="nodes=all" --tags=level2 -K -k
```
## WARN
some tasks may take a long time to run, check the scripts in files/bin

# LOGS

Custom logs, if custom_reporter plugin is enabled, you can find logs in log dir if log dir doesn't exists, create it first

log/${hostname}.txt
log/summary_report.csv

Logs will always be apended, so if you want clean logs, rm log/* then run playbook.

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

# NOTES On Custom_reporter plugin

  - Logs only if a task has a name
  - Do not add any comma(,) in name. This is because of summary_report.csv , otherwise you will have more fields when you open the file in excel.


TODO:
  - add missing sections (6, 7 and 8)
  - work on custom_loger to output in json
  - create reports based on the output (html)

# Limitations
requires ansible > 2.1

Tested on ansible 2.1 only.
