#!/bin/bash
# script to list all files that is world writable
DIRS="/usr /etc /bin /boot /var"
for dir in ${DIRS}
do
 find  ${dir} -xdev -type f -perm -0002 -print
done
