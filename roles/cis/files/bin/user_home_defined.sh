#!/bin/bash

defUsers="root bin daemon adm lp sync shutdown halt mail news uucp operator games gopher ftp nobody nscd vcsa rpc mailnull smmsp pcap ntp dbus avahi sshd rpcuser nfsnobody haldaemon avahi-autoipd distcache apache oprofile webalizer dovecot squid named xfs gdm sabayon saslauth"

# change to getent passwd to look at AD accounts
cat /etc/passwd |\
  /bin/awk -F: '{ print $1" "$6 }' |\
  while read user dir; do
    found=0
    for tUser in ${defUsers}
	do 
	  if [ "${user}" = "${tUser}" ]; then 
	    found=1
            break
	  fi
    done 
    if [ $found -eq 0 ]; then
      if [ ! -d "${dir}" ]; then
        echo "User $user has no home directory ($dir)."
      fi
    fi
  done
