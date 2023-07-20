#!/bin/bash

cd /home/joost/Pi/python/pump
date > pump.started
screen -dmS pump bash -c "python3 ./pump.py"

