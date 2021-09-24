
#set -euxo pipefail

#DOCKER_REGISTRY=${DOCKER_REGISTRY:hub.docker.com}
#PREFIX=${PREFIX:-agent-}
VERSION=${VERSION:-latest}

# TODO check $1 and DOCKER_REGISTRY
#if [ -z $1 ]; then
#    echo "no image name provided."
#    exit 1
#fi


for agent in $(ls -1)
do
	echo $agent
	echo "cat $agent/Dockerfile | docker build -t $agent:$VERSION -f - $agent/"
	#echo cat $agent/Dockerfile | docker build -t $DOCKER_REGISTRY/$agent:$VERSION -f - $agent/

if [ -n $DOCKER_REGISTRY ]; then
    echo "docker push $DOCKER_REGISTRY$agent:$VERSION"
fi


done
