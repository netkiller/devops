#!/bin/bash
datetime=`date +%Y-%m-%d" "%H":"%M`
email="neo.chan@live.com"
#password=$(cat /dev/urandom | tr -cd [:alnum:] | fold -w30 | head -n 1)
string=$(date -u "+%Y$1%m$2%d$3%H$4%M")
password=$(echo $string | md5sum | cut -c 2-9 | base64 | tr -d "=" | cut -c 1-32)
echo $string
echo $password > ~/.lastpasswd
exit
echo $password | passwd www --stdin > /dev/null

#for pts in $(w | awk -F' ' '{if ($1 == "www") print $2}')
#do 
#	pkill -9 -t $pts
#done

#cat $password | mutt -s "$datetime new passwd" $email
