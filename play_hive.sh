#!/bin/bash

[ ! -d data ] && mkdir data

python3 -m src.play_hive "$@"