#!/bin/zsh

set -ex

HEROKU_APP=$1

# Start worker on heroku
heroku ps:scale worker=1 --app=${HEROKU_APP}
