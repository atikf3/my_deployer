# 1. The checker microservice

The first and mandatory microservice will expose an HTTP service to retrieve information about the Docker containers on the host.

It will have 2 routes:

*   `GET - /containers/{id}`, returns the following information about the container whose hash or name matches `id`:  
      - name  
      - short hash  
      - image (name and tag)  
      - uptime  
      - published ports  
      - volumes
*   `GET - /containers/`  
     - Returns all containers (even stopped ones) if the `all` query parameter is set to true  
     - Returns a list of containers currently running on the host otherwise.

Its directory hierarchy is as follows:
```bash
    $ ls checker/
    Dockerfile requirements.txt app.py
```

### Accessing docker from inside a container
> As stated in the instructions above, the `checker` microservice will need to access information about containers. Therefore, you will need to be able to reach the hosts Docker daemon from inside the microservice's container. That can be achieved by mounting `/var/run/docker.sock` as a volume.

## Docker
```bash
# cp .env.example .env
d build . -t dockerhub.labs.ikf3.com/etna.my_deployer.checker:latest --build-arg https_proxy
d run --rm -p 5000:5000 --env-file .env --name checker -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd)/:/app  dockerhub.labs.ikf3.com/etna.my_deployer.checker:latest
# or 
d run --rm -p 5000:5000 --env-file .env -e DOCKER_URL=tcp://host:2376 --name checker -v $(pwd)/:/app  dockerhub.labs.ikf3.com/etna.my_deployer.checker:latest
```

## Additional Data
**Contributors:**
[talamo_a](//www.talamona.com)

**License:**
[MIT](./LICENSE)