#!/bin/bash

defWorldpayUsers="saslauth postfix tcpdump pe-puppet pe-puppetdb pe-postgres exim puppet-dashboard pe-auth pe-memcached pe-console-services pe-apache"

defUsers="root bin daemon adm lp sync shutdown halt mail news uucp operator games gopher ftp nobody nscd vcsa rpc mailnull smmsp pcap ntp dbus avahi sshd rpcuser nfsnobody haldaemon avahi-autoipd distcache apache oprofile webalizer dovecot squid named xfs gdm sabayon $defWorldpayUsers"

/bin/cat /etc/passwd |\
  /bin/awk -F: '($3 < 500) { print $1" "$3 }' |\
  while read user uid; do
    found=0
    for tUser in ${defUsers}
	do 
	  if [ ${user} = ${tUser} ]; then 
	    found=1
            break
	  fi
    done 
    if [ $found -eq 0 ]; then
      echo "User $user has a reserved UID ($uid)."
    fi
  done
