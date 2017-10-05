#!/bin/bash
# 9.1.13 Find SUID System Executables (Not Scored)
df --local -P | awk {'if (NR!=1) print $6'} | xargs -I '{}' find '{}' -xdev -type f -perm -4000 -print
