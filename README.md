# Drunkar/hubot-alpine
This docker image is heavily relies on https://github.com/HearstAT/docker-alpinehubot.

# Build Info
## NODE
- NodeJS: 6.3.1
- NPM: 3

## Default Scripts
- [hubot-diagnostics]()
- [hubot-help]()
- [hubot-google-images]()
- [hubot-pugme]()
- [hubot-maps]()
- [hubot-redis-brain](https://github.com/github/hubot-scripts/blob/master/src/scripts/redis-brain.coffee)
- [hubot-rules]()
- [hubot-shipit](https://github.com/github/hubot-scripts/blob/master/src/scripts/shipit.coffee)
- [hubot-reload-scripts](https://github.com/vinta/hubot-reload-scripts)

## Installed Packages
- bash
- supervisor
- nodejs
- redis
- build-base
- gc
- g++
- gcc-objc
- libtool
- libc6-compat
- make
- expat
- expat-dev
- python
- wget
- gnupg
- tar
- git
- zip
- curl
- wget

## Suggested Mounts
Mount the redis directory to avoid data reset on container replacement
- /var/lib/redis

Mount the config directory to manage credentials/settings outside of container
- /opt/hubot/config

Mount the scripts directory to manage any non-npm installs/simple scripts
- /opt/hubot/scripts

Mount the external-scripts for control
- /opt/hubot/external-scripts-for-npm.json

# Usage
You have a few options in how to utilize this container

## Basic Start

```
docker run -d drunkar/docker-alpinehubot
```

## Configuration File Start

```
docker run -v /path/to/hubot.conf:/opt/hubot/config/hubot.conf -d drunkar/docker-alpinehubot
```

## Full Feature Start

```
docker run -v /path/to/hubot.conf:/opt/hubot/config/hubot.conf \
-v /path/to/redis/save:/var/lib/redis \
-v /path/to/external-scripts-for-npm.json:/opt/hubot/external-scripts-for-npm.json \
-d drunkar/docker-alpinehubot
```
## Dev Mode Start
I've setup this bot to be able to switch back and forth from Hipchat to Shell via startup commands. This is how to get into "Dev Mode" or enable the shell adapter.
```
docker run -d drunkar/docker-alpinehubot /usr/bin/devmode
```
then just do the following to connect to the container at the shell level
```
docker exec -it $container_name bash
```
then once in run the following
```
./bin/hubot
```
Then you can interact with hubot at the shell level

## Node-Inspector

Run:

    docker run -d -p 8123:8123 -p 5858:5858 --name=devbot drunkar/docker-alpinehubot devmode
    docker exec -it devbot bash
    coffee --nodejs --debug $(which hubot)

In Chrome navigatate to http://<docker IP>:8123/?ws=<docker IP>:8123&port=5858
For Mac users "docker IP" can be found in Kitematic.
Example: http://192.168.99.100:8123/?ws=192.168.99.100:8123&port=5858

NOTE: You should end up in a hubot REPL, if you end up in a coffee REPL you did something wrong.  To exit:

    coffee> process.exit()

NOTE: node-inspector currently only works in Chrome.

To set a breakpoint in coffeescript you will want to open the code in the /opt/hubot/node_modules/ directory and add at the appropriate line:

    debugger

You may want to mount a directory locally so you can use your local editor.  For Mac this will need to be in your /Users/<username> dir  To do this consider:

    mkdir -p ~/node_modules
    docker run -d -p 8123:8123 -p 5858:5858 -v /Users/<username>/node_modules:/opt/hubot/node_modules --name=devbot drunkar/docker-alpinehubot devmode

## Prod Mode Start
To switch back to hipchat or "Prod Mode" do the following
```
docker exec $container_name /usr/bin/prodmode
```
or just run a new container

# Run Time Help
Since this container comes with a bot reload option, edit the external-scripts-for-npm.json as needed and run the following

```
docker exec $container_name python script-install.py
```
Note: you can just restart the container, it will re-run the same script before loading the bot.

Then in chat tell hubot to reload (my default is thebot)

```
@hubot reload
```

# Building
To build the image, do the following

```
docker build github.com/Drunkar/docker-alpinehubot
```


# Template files
## Hubot.Conf
Lives at /opt/hubot/config and is sourced at run time.

Add all environment variables needed to conf file. See script repos for specific settings available.

The baseline config file in container only has ADAPTER/HUBOT_NAME set.

```
## Bot Settings
export HUBOT_NAME='hubot'

## Slack adapter settings
# slack setting
export HUBOT_SLACK_TOKEN=<YOUR_TOKEN>
```

## external-scripts-for-npm.json
The embedded script-install.py utilizes the external-scripts-for-npm.json for it's install items, I did this to simplify the process. You already have to add everything to the file regardless, so use it to install from.

```
[
  "hubot-diagnostics",
  "hubot-help",
  "hubot-google-images",
  "hubot-pugme",
  "hubot-maps",
  "hubot-redis-brain",
  "hubot-rules",
  "hubot-shipit",
  "hubot-reload-scripts",
  "bouzuya/hubot-lgtm"
]
```
