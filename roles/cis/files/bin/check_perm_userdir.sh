#!/bin/bash
# check Permissions on User Home Directories
#
for dir in `/bin/cat /etc/passwd  | /bin/egrep -v '(root|halt|sync|shutdown)' |\
/bin/awk -F: '($8 == "PS" && $7 != "/sbin/nologin") { print $6 }'`; do
    dirperm=`/bin/ls -ld $dir | /bin/cut -f1 -d" "`
    if [ `echo $dirperm | /bin/cut -c6 ` != "-" ]; then
        echo "Group Write permission set on directory $dir"
    fi
    if [ `echo $dirperm | /bin/cut -c8 ` != "-" ]; then
        echo "Other Read permission set on directory $dir"
    fi
    if [ `echo $dirperm | /bin/cut -c9 ` != "-" ]; then
        echo "Other Write permission set on directory $dir"
    fi
    if [ `echo $dirperm | /bin/cut -c10 ` != "-" ]; then
        echo "Other Execute permission set on directory $dir"
    fi
done
