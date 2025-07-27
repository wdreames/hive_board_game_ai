#!/bin/bash

[ ! -d data ] && mkdir data

python -m src.play_hive "$@"