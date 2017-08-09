#Ansible + CIS Benchmarks + RHEL/CentOS 6

Ansible audit for CIS.

This is an ansible playbook for auditing a system running Red Hat Enterprise Linux 6 or CentOS 6  to see if it passes CIS Security Benchmarks.

Insipired by https://github.com/major/cis-rhel-ansible but instead of applying the changes, this will just report if a system passes or fails for each task.

Example:
add  hosts in test-hosts
```
ansible-playbook -i test-hosts playbook.yml --extra-vars="nodes=all" --tags=level2 -K -k
```

# LOGS

Custom logs, if custom_reporter plugin is enabled, you can find logs in log dir if log dir doesn't exists, create it first

log/${hostname}.txt
log/summary_report.csv

Logs will always be apended, so if you want clean logs, rm log/* then run playbook.

# NOTES On Custom_reporter plugin

  - Logs only if a task has a name
  - Do not add any comma(,) in name. This is because of summary_report.csv , otherwise you will have more fields when you open the file in excel.


TODO:
  - add missing sections
  - work on custom_loger to output in json
  - create reports based on the output (html)

# Limitations
requires ansible > 2.1
Tested on ansible 2.1 only.
