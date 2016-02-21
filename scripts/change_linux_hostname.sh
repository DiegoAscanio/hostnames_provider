#!/bin/bash
url='hostnameprovider'
final_hostname=`curl $url`
current_hostname=`hostname`
if [ $current_hostname != $final_hostname ]; then
    echo $final_hostname > /etc/hostname
    sed -i '/$current_hostname/c\127.0.1.1\t$final_hostname' /etc/hosts
    reboot
fi;
