############################################
# Author: netkiller<netkiller@msn.com>
# Homepage: http://www.netkiller.cn
############################################

GROUP=$1
BRANCH=$2
PROJECT=$3

DEPLOYLOG=/var/tmp/deploy-$GROUP.$PROJECT.$BRANCH.$(date '+%Y-%m-%d.%H:%M:%S').log
PROJECT_DIR=/www/$GROUP/$PROJECT/$BRANCH
TMPFILE=$(mktemp)

echo $PROJECT_DIR > $DEPLOYLOG
echo "--------------------------------------------------" >> $DEPLOYLOG

if [ -d $PROJECT_DIR ]; then
	cd $PROJECT_DIR
	ant pull | tail -n +2 > $TMPFILE
	cat $TMPFILE >> $DEPLOYLOG
	ant deploy >> $DEPLOYLOG

	if egrep -q "(\.java|\.xml|\.jar|\.properties)" $TMPFILE; then
		echo "--------------------------------------------------" >> $DEPLOYLOG
		ant restart >> $DEPLOYLOG
		echo "--------------------------------------------------" >> $DEPLOYLOG
	fi	
	
	rm -rf $TMPFILE
fi