#!/bin/bash
USERDIRS=`getent passwd | /bin/egrep -v '(root|halt|sync|shutdown)' | /bin/awk -F: '($7 != "/sbin/nologin") { print $6 }'`

for dir in $USERDIRS; do 
  for file in $dir/.netrc; do 
    if [ ! -h "$file" -a -f "$file" ]; then
      echo ".netrc file in $dir"
    fi
  done
done
