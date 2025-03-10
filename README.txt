Launch clamav container with clamd in the foreground:

docker run -d --rm --env 'CLAMAV_NO_FRESHCLAMD=true' --publish 3310:3310 --name clamav clamav/clamav clamd --foreground

When programmatically shutting down clamd through the networksocket, the container will stop, which is what we want


Build docker image: 
docker build -t localhost:5000/sre/clamav_scanner .
docker push localhost:5000/sre/clamav_scanner


Accessing the Kubernetes API from inside a pod:
https://kubernetes.io/docs/tasks/run-application/access-api-from-pod/