# Groupme chatbot

## Introduction

The purpose of this bot is ultimately to provide a resource to (my) students.  Once functional, it will provide answers to common questions about the syllabus, important dates, and assignments.  

Presently the chatbot answers WolframAlpha queries

*Important note* My development is based primarily on a Raspberry Pi and I am a chemist, not a programmer.  Don't expect great things out of this code, and in fact, expect cringeworthy constructs.  

## Installation

The groupy and wolframclient modules need to be installed

```
pip3 install groupy
pip3 install wolframclient
```

More information about the Wolfram Client Library for Python can be found [here](https://blog.wolfram.com/2019/05/16/announcing-the-wolfram-client-library-for-python/).  The groupy GroupMe API wrapper documentation can be found [here](https://groupy.readthedocs.io/en/master/)

Recent Raspbian OS distributions do not come with the wolfram language installed by default.  It is still available via `sudo apt install wolfram-engine`.

## Usage

First, log in to your GroupMe account and create a group where you want the chatbot to reside.  Remember the name.

After cloning this repository to your Raspberry Pi, rename the `secrets.py.template` file to `secrets.py` and put the correct information into the dictionary.  You can obtain your GroupMe token by logging in with a GroupMe account at https://dev.groupme.com.  Create your Bot under the *Bots* tab and you will be provided with the Bot ID and Group ID needed for the remaining entries in secrets.py.

Run `python3 listener.py` to start the bot.  Chat messages beginning with ">" will be read by the bot as WolframAlpha queries.  

## Status

Presently, the chatbot is capable of returning numeric, string and images.  I have not tried an exhaustive array of WolframAlpha queries.


