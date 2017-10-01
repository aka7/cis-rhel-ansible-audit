#!/bin/bash
# 9.2.10 Check for Presence of User .rhosts Files
USERDIRS=`getent passwd | /bin/egrep -v '(root|halt|sync|shutdown)' | /bin/awk -F: '($7 != "/sbin/nologin") { print $6 }'`

for dir in $USERDIRS; do 
  for file in $dir/.rhosts; do 
    if [ ! -h "$file" -a -f "$file" ]; then
      echo ".rhosts file in $dir"
    fi
  done
done
