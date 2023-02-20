#!/bin/bash

apt install git
cd /opt
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd /opt/rpi-rgb-led-matrix
make -C examples-api-use
