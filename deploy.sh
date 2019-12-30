#!/bin/sh
heroku create
heroku stack:set container
heroku config:set URL=$1
git push heroku master
heroku logs --tail
heroku apps:destroy