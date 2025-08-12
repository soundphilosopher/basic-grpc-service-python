# Basic gRPC Service written in Python

## Prerequisites
- Python 3.7 or higher
- pip

## Installation

```shell
~ mkcert -install
~ mkcert -cert-file ./certs/local.crt -key-file ./certs/local.key localhost 127.0.0.1 0.0.0.0 ::1
```

```shell
~ python -m pip install -e .
```

## Run server

```shell
~ python server.py
```

## Server calls

```shell
# list services
~ grpcurl 127.0.0.1:8443 list

# list methods of service
~ grpcurl 127.0.0.1:8443 list basic.v1.BasicService

# call hello
- grpcurl -d '{"message": "World"}' 127.0.0.1:8443 basic.v1.BasicService/Hello
```

## ToDo's

- [ ] Implement talk "chatbot"
- [ ] Implement background tasks
- [ ] Add all necessary information to README.md
- [ ] Add LICENSE.md file
