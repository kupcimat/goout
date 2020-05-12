#!/bin/zsh

set -ex

HEROKU_APP=$1

# Stop worker on heroku
heroku ps:scale worker=0 --app=${HEROKU_APP}
