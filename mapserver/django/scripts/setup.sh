#!/usr/bin/env bash

# Install rabbitmq

sudo apt update -y; apt -y install curl gnupg
curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | sudo apt-key add -
sudo apt-get install apt-transport-https

RELEASE=`lsb_release -sc`

sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
## Installs the latest Erlang 23.x release.
## Change component to "erlang-22.x" to install the latest 22.x version.
## "bionic" as distribution name should work for any later Ubuntu or Debian release.
## See the release to distribution mapping table in RabbitMQ doc guides to learn more.
deb https://dl.bintray.com/rabbitmq-erlang/debian $RELEASE erlang
## Installs latest RabbitMQ release
deb https://dl.bintray.com/rabbitmq/debian $RELEASE main
EOF

sudo apt-get update -y; sudo apt-get install rabbitmq-server -y --fix-missing

sudo service rabbitmq-server start

rabbitmqctl add_user inasafe $RABBITMQ_PASSWORD
rabbitmqctl add_vhost inasafe
rabbitmqctl set_permissions -p inasafe inasafe ".*" ".*" ".*"


# Install celeryd
groupadd celery
useradd -M celery -g celery -s `which nologin`
