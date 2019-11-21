# MITMInjector

Simple MITM proxy with injection features
Initially developed for debugging purposes, 


## Usage

inject.py [-h] -u URL [-p PORT] [-P PAYLOAD || -W WEBWORKER] [-n] [-s]

URL: Url to clone

PAYLOAD: Js payload to inject into cloned page

WEBWORKER: Js webworker to inject into cloned page

-n: Export service using ngrok.com. In order to use this feature, you must register on ngrok.com, get your auth token from https://dashboard.ngrok.com/auth and save it into a file named ngroktoken.

-s: Mask ngrok url using TinyUrl

