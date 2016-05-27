#!/usr/bin/python

import hashlib
from base64 import urlsafe_b64encode as encode
from base64 import urlsafe_b64decode as decode
import crypt, getpass
import getpass
import fileinput
import argparse
import sys
import os
import platform

parser = argparse.ArgumentParser()

parser.add_argument('--action', type=str, choices=['create_env', 'rebuild_env', 'destroy_env'])
parser.add_argument('--bitbucket_username', type=str, required = True)
parser.add_argument('--linux_username', type=str, required = True)

args = parser.parse_args()

platform = platform.dist()

if platform[1] == "14.04" or platform[1] == "14.10":
	deb = "deb https://apt.dockerproject.org/repo ubuntu-trusty main"

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


def makeSecret(password):
    salt = os.urandom(4)
    h = hashlib.sha1(password)
    h.update(salt)
    return "{SSHA}" + encode(h.digest() + salt)

if args.tools == 'create_env':
        proc = subprocess.Popen('sudo apt-get update; sudo apt-get install -y virtualbox apt-transport-https ca-certificates python-pip', shell=True, stdin=None, stdout=open(os.devnull,"wb"), stderr=STDOUT, executable="/bin/bash")
	os.system("sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D")
	os.system("sudo touch /etc/apt/sources.list.d/docker.list; sudo chmod 777 /etc/apt/sources.list.d/docker.list;  echo "deb https://apt.dockerproject.org/repo ubuntu-trusty main" > /etc/apt/sources.list.d/docker.list")


