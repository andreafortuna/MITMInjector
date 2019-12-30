#!/bin/sh
heroku create
heroku stack:set container
heroku config:set BASE_URL=$(heroku info -s | grep web_url | cut -d= -f2)
heroku config:set URL=$1
git push heroku master
heroku logs --tail
heroku apps:destroy