#!/bin/bash
datetime=`date +%Y-%m-%d" "%H":"%M`
email="neo.chan@live.com"
password=$(cat /dev/urandom | tr -cd [:alnum:] | fold -w30 | head -n 1)
echo $password | passwd www --stdin > /dev/null

for pts in $(w | awk -F' ' '{if ($1 == "www") print $2}')
do 
	pkill -9 -t $pts
done

#cat $password | mutt -s "$datetime new passwd" $email
echo $password
