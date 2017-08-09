#!/bin/bash
egrep -v "^\+" /etc/passwd | awk -F: '($1!="root" && $1!="sync" && $1!="shutdown" && $1!="halt" && $1!="pe-postgres" && $1!="puppet-dashboard" && $3<500 && $7!="/sbin/nologin") {print}'
