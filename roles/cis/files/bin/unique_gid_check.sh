#!/bin/bash
/bin/cat /etc/group | /bin/cut -f3 -d":" | /bin/sort -n | /usr/bin/uniq -c |\
  while read x ; do 
    [ -z "${x}" ] && break
    set - $x 
    if [ $1 -gt 1 ]; then
      grps=`/bin/gawk -F: '($3 == n) { print $1 }' n=$2\
        /etc/group | /usr/bin/xargs`
      echo "Duplicate GID ($2): ${grps}"
    fi
done
