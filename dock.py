#!/usr/bin/env python3

def printHelp():
    print("""
List of available commands:

dock help
dock build
dock start
dock stop
dock clean
dock purge
dock list [OPTIONS]
dock bash [CONTAINER IDENTIFIER]
dock logs [CONTAINER IDENTIFIER]

Run "dock help all" to get a detailed explanation on functions
    """);

def printDetailedHelp():
    print("""
Available commands explained:

dock help
    Display this info

dock build
    Build containers

dock start
    Build images and start containers with docker compose

dock stop
    Stop running containers

dock clean
    Clean all compiled containers.

dock purge
    Purge all docker related data from your system

dock list [OPTIONS]
    List all active containers. Also accepts options of "docker ps" command

dock bash [CONTAINER IDENTIFIER]
    BASH into running container

dock logs [CONTAINER IDENTIFIER]
    Get container logs
    """);

def dockerPrepare():
    os.system("mkdir ~/www")
    os.system("mkdir ~/www/html")
    os.system("mkdir ~/www/mysql5")
    os.system("mkdir ~/www/log")
    os.system("mkdir ~/www/log/nginx")
    os.system("mkdir ~/www/log/php")

def dockerBuild():
    dockerPrepare()
    os.system("docker-compose build")

def dockerStart():
    os.system("docker-compose up -d")

def dockerStop():
    os.system("docker-compose stop")

import os
import sys

command = sys.argv[1]

if command == "help":
    if (len(sys.argv) == 3 and sys.argv[2] == "all"):
        printDetailedHelp()
    else:
        printHelp()

elif command == "build":
    dockerBuild()

elif command == "run":
    dockerBuild()
    dockerStart()

elif command == "start":
    dockerStart()

elif command == "stop":
    dockerStop()

elif command == "restart":
    dockerStop()
    dockerStart()

elif command == "clean":
    os.system("docker stop $(docker ps -aq)")
    os.system("docker container prune --force")
    os.system("docker network prune --force")
    os.system("docker images prune --force")

elif command == "purge":
    os.system("docker stop $(docker ps -aq)")
    os.system("docker rm --force $(docker ps -aq)")
    os.system("docker rmi --force $(docker images -aq)")
    os.system("docker network rm $(docker network ls -aq)")

elif command == "list":
    if len(sys.argv) > 3:
        os.system("docker ps %s" % sys.argv[2])
    else:
        os.system("docker ps")

elif command == "bash":
    if len(sys.argv) == 3:
        os.system("docker exec -it %s bash" % sys.argv[2])
    else:
        print("Please provide container name or ID")

elif command == "logs":
    if len(sys.argv) == 3:
        os.system("docker logs %s" % sys.argv[2])
    else:
        print("Please provide container name or ID")
