#!/bin/sh
heroku create
heroku stack:set container
git push heroku master
heroku logs --tail
heroku apps:destroy