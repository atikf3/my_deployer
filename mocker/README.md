# 2. A microservice of your choice
The other microservice's features are yours to decide, however they must remain relevant (for example: do not implement a "hello world" microservice).

## Docker
```bash
d build . -t dockerhub.labs.ikf3.com/etna.my_deployer.mocker:latest --build-arg https_proxy
d run -p 8000:8000 dockerhub.labs.ikf3.com/etna.my_deployer.mocker:latest
```

## Additional Data
**Contributors:**
[talamo_a](//www.talamona.com)

**License:**
MIT