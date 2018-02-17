#!/bin/sh

inotifywait -m . -e create -e moved_to |
  while read path action file; do
    pipenv run python main.py $path/$file
  done
