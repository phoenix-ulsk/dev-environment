#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
HOME = os.environ["HOME"]

if "DOCKER_DEV_ENVIRONMENT_DIR" in os.environ.keys():
    DOCKER_DIR = os.environ["DOCKER_DEV_ENVIRONMENT_DIR"]
else:
    DOCKER_DIR = SCRIPT_DIR

def printHelp():
    print("""
List of available commands:

dock help
dock setup
dock build
dock run
dock start
dock stop
dock restart
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

doxk setup
    Setup directories and ass this script as `dock` command to your system

dock build
    Build containers

dock run
    Build and start containers

dock start
    Build images and start containers with docker compose

dock stop
    Stop running containers

dock restart
    Restart containers

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

def dockerSetup():
    print("You need to super user permissions in order to execute this command")

    try:
        # Set up hosts file
        hosts = open("/etc/hosts", "r");
        if "dev.local" not in hosts.read():
            os.system("""sudo echo "
127.0.0.1\tlocalunixsocket
127.0.0.1\tdev5.local
127.0.0.1\tdev.local" >> /etc/hosts""")

        # Set up this script as system executable
        if not os.path.exists("~/.dev-environment"):
            os.system("mkdir -p ~/.dev-environment")
            os.system("cp ./dock.py ~/.dev-environment")
            os.system("sudo ln -s %s/.dev-environment/dock.py /usr/local/bin/dock" % HOME)

        # Set up autocomplete script
        if not os.path.exists("/usr/local/etc/bash_completion.d/dock"):
            os.system("cp ./dock_autocomplete ~/.dev-environment")
            os.system("ln -s %s/.dev-environment/dock_autocomplete /usr/local/etc/bash_completion.d/dock" % HOME)

        # Create directories for web server
        if not os.path.exists("~/www"):
            os.system("mkdir -p ~/www")
            os.system("mkdir -p ~/www/html")
            os.system("mkdir -p ~/www/log")
            os.system("mkdir -p ~/www/log/nginx")
            os.system("mkdir -p ~/www/log/php")
            os.system("mkdir -p ~/www/log/mysql5")

        # Add repository dir to as environment variable for future use
        bash = open("%s/.bash_profile" % HOME, "r+");
        if "DOCKER_DEV_ENVIRONMENT_DIR" not in bash.read():
            bash.write("\nexport DOCKER_DEV_ENVIRONMENT_DIR=%s" % SCRIPT_DIR);
            os.system("source ~/.bash_profile")

    except IOError as e:
        # You need to have super user permissions to set up hosts settings
        print(e)
        print("You need to super user permissions in order to execute this command")
        sys.exit(1)

def dockerBuild():
    os.system("docker-compose -f %s/docker-compose.yml build" % DOCKER_DIR)

def dockerStart():
    os.system("docker-compose -f %s/docker-compose.yml up -d" % DOCKER_DIR)

def dockerStop():
    os.system("docker-compose -f %s/docker-compose.yml stop" % DOCKER_DIR)

if len(sys.argv) > 1:
    command = sys.argv[1]
else:
    command = "help"

if command == "help":
    if (len(sys.argv) == 3 and sys.argv[2] == "all"):
        printDetailedHelp()
    else:
        printHelp()

elif command == "setup":
    dockerSetup();

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
    os.system("docker network rm $(docker network ls -q)")

elif command == "list":
    if len(sys.argv) > 2:
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
