#!/bin/zsh

set -ex

HEROKU_APP=$1

# Deploy worker on heroku
heroku container:login
heroku container:push worker --app=${HEROKU_APP}
heroku container:release worker --app=${HEROKU_APP}
