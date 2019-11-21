# MITMInjector

![screenshot](https://www.andreafortuna.org/wp-content/uploads/2019/11/MITMInject.jpg)


Simple MITM proxy with injection features.

Initially designed for debugging purposes, during the development has turned into a tool useful for penetration testing, user tracking and social engineering assessment.


## Usage

inject.py [-h] -u URL [-p PORT] [-P PAYLOAD || -W WEBWORKER] [-n] [-s]

URL: Url to clone

PAYLOAD: Js payload to inject into cloned page

WEBWORKER: Js webworker to inject into cloned page

-n: Export service using ngrok.com. In order to use this feature, you must register on ngrok.com, get your auth token from https://dashboard.ngrok.com/auth and save it into a file named ngroktoken.

-s: Mask ngrok url using TinyUrl

## Available payloads

- formgrabber: dumps all data written by target into page forms
- geocoding: track target position using browser geolocation
- ipgeolocation: track target position using IP geolocation

## Disclaimer

This software has been created purely for the purposes of academic research and for the development of effective defensive techniques, and is not intended to be used to attack systems except where explicitly authorized. Author is not responsible or liable for misuse of the software. 
Use responsibly.