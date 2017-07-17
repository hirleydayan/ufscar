# Set the base image to node
# docker build -t freeboard -f Dockerfile .
FROM debian:jessie

# File Author / Maintainer
MAINTAINER Hirley Dayan

# Update the sources list and install requirements
RUN apt-get -y update
RUN apt-get install -y wget\
  vim\
  git\
  gnupg\
  curl\
  apache2

# Install NodeJS
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get install -y nodejs

# Install Grunt
RUN npm install -g grunt-cli

# FreeBoard
RUN git clone https://github.com/Freeboard/freeboard.git
RUN cd /freeboard && npm install --prefix /freeboard

# Run grunt
RUN cd /freeboard && grunt

# Apache2 settings for FreeBoard
RUN rm -Rf /var/www/html
RUN ln -s /freeboard /var/www/html

# Install FreeBoard plugins
# AWS plugin
RUN npm install -S --prefix /freeboard freeboard-aws-iot-ws-mqtt
RUN sed -i 's/.*head.js("js\/freeboard_plugins.min.js",/& "plugins\/freeboard-aws-iot-ws-mqtt\/index.js",/' /freeboard/index.html

# Fix missing library
RUN ln -s /freeboard/node_modules/crypto-js/core.js \
  /freeboard/plugins/freeboard-aws-iot-ws-mqtt/
RUN ln -s /freeboard/node_modules/crypto-js/hmac.js \
  /freeboard/plugins/freeboard-aws-iot-ws-mqtt/
RUN ln -s /freeboard/node_modules/moment/min/moment.min.js \
  /freeboard/plugins/freeboard-aws-iot-ws-mqtt/
RUN ln -s /freeboard/node_modules/crypto-js/sha256.js \
  /freeboard/plugins/freeboard-aws-iot-ws-mqtt/
RUN ln -s /freeboard/node_modules/paho-mqtt/mqttws31-min.js \
  /freeboard/plugins/freeboard-aws-iot-ws-mqtt/

# Cleanup
RUN apt-get clean

# Adjust auto start services
CMD service apache2 start && /bin/bash
