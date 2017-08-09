#!/bin/bash
# Groups defined in the /etc/passwd file but not in the /etc/group file pose a threat to system security since group permissions are not properly managed.
# Analyze the output of the Audit step above and perform the appropriate action to correct any discrepancies found.

defUsers="root bin daemon adm lp sync shutdown halt mail news uucp operator games gopher ftp nobody nscd vcsa rpc mailnull smmsp pcap ntp dbus avahi sshd rpcuser nfsnobody haldaemon avahi-autoipd distcache apache oprofile webalizer dovecot squid named xfs gdm sabayon"

userlist=$(/bin/cat /etc/passwd)
grouplist=$(/bin/cat /etc/group)
for x in ${userlist}
do
  if [ "$x" = "" ] 
  then
    break 
  fi
  userid=`echo "$x" | cut -f1 -d':'`
  found=0
  for n in $defUsers 
  do 
    if [ $userid = "$n" ]
    then 
	  found=1
	  break
	fi 
  done
  if [ $found -eq 1 ]
  then 
    continue
  fi 
  groupid=`echo "$x" | /bin/cut -f4 -d':'` 
  for g in ${grouplist}
  do
	if [ "$g" = "" ] 
	then 
	  echo "Groupid $groupid does not exist in /etc/group, but is used by $userid"
	  break
	fi
	y=`echo $g | cut -f3 -d":"`
	if [ "$y" = "$groupid" ]
	then
  	  break
	fi
  done
done
