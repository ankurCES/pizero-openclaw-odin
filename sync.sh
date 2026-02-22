#!/bin/bash

rsync -avz --delete ./ pi@pizero.local:/home/pi/pizero-openclaw/ &&
ssh pi@pizero.local "cd pizero-openclaw && python3 main.py"