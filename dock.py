#!/usr/bin/env python3
import os
import sys
import subprocess

def scriptPrint(string):
    if config["verbose"] == 1:
        print(string)

def checkRequirements():
    missing_requirements = []

    for packet, command in config["requirements"].items():
        (code, res) = subprocess.getstatusoutput(command)

        if code > 0:
            missing_requirements.append(packet)

    if len(missing_requirements) > 0:
        for packet in missing_requirements:
            scriptPrint("\33[1;31;40m{0} is required. Please install {0}.".format(packet))

        os.system("tput sgr0")
        sys.exit(1)

# Parse script arguments
def parseArguments():
    if len(sys.argv) > 1:
        i = 0
        for arg in sys.argv:
            # Is silent
            if arg == "-s":
                config["verbose"] = 0

            if any(arg == cmd for cmd in config["known_commands"]):
                config["command"] = arg
                config["args"] = sys.argv[i+1:len(sys.argv)]

            i += 1

# Gather system specific data
def gatherFacts():
    if config["platform"] == SYS_MACOS:
        config["system"]["hosts"] = "/etc/hosts"
        config["system"]["autocomplete_dir"] = "/usr/local/etc/bash_completion.d"
        config["system"]["executable_dir"] = "/usr/local/bin"
        config["system"]["src_dir"] = "/usr/local/lib/dev-environment"
        config["system"]["bash_profile"] = "/etc/profile.d/dock.sh"
        config["system"]["www_dir"] = "/var/www"
        config["system"]["requirements"]["docker-sync"] = "docker-sync --version"

    elif config["platform"] == SYS_LINUX:
        config["system"]["hosts"] = "/etc/hosts"
        config["system"]["autocomplete_dir"] = "/etc/bash_completion.d"
        config["system"]["executable_dir"] = "/usr/local/bin"
        config["system"]["src_dir"] = "/usr/local/src/dev-environment"
        config["system"]["bash_profile"] = "/etc/profile.d/dock.sh"
        config["system"]["www_dir"] = "/var/www"

def printHelp():
    scriptPrint("""
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
    scriptPrint("""
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
    Clean all compiled containers and their networks

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
    try:
        # Set up hosts file
        hosts = open(config["system"]["hosts"], "r");
        if "dev.local" not in hosts.read():
            hosts_list = """
{0}\tdev.local
{0}\tdev5.local
{0}\tdev70.local
{0}\tdev71.local
{0}\tdev72.local
{0}\tphpmyadmin.local
{0}\tmailcatcher.local""".format(config["docker"]["ip"])
            os.system("echo \"{0}\" | sudo tee -a {1} > /dev/null".format(hosts_list, config["system"]["hosts"]))

        # Set up this script as system executable
        if not os.path.exists(config["system"]["src_dir"]):
            os.system("sudo mkdir {0}".format(config["system"]["src_dir"]))
            os.system("sudo cp -R {0}/* {1}".format(config["script_dir"], config["system"]["src_dir"]))
            os.system("sudo ln -s {0}/dock.py {1}/dock".format(config["system"]["src_dir"], config["system"]["executable_dir"]))

        # Set up autocomplete script
        if not os.path.exists("{0}/dock".format(config["system"]["autocomplete_dir"])):
            if sys.platform == "darwin":
                os.system("ln -s {0}/dock_autocomplete {1}/dock".format(config["system"]["src_dir"], config["system"]["autocomplete_dir"]))
            else:
                os.system("sudo cp {0}/dock_autocomplete {1}/dock".format(config["system"]["src_dir"], config["system"]["autocomplete_dir"]))

        # Create directories for web server
        if not os.path.exists(config["system"]["www_dir"]):
            os.system("sudo mkdir -p {0}".format(config["system"]["www_dir"]))
            os.system("sudo mkdir -p {0}/html".format(config["system"]["www_dir"]))
            os.system("sudo chmod 0777 {0}/html".format(config["system"]["www_dir"]))
            os.system("sudo mkdir -p {0}/log".format(config["system"]["www_dir"]))
            os.system("sudo mkdir -p {0}/log/nginx".format(config["system"]["www_dir"]))
            os.system("sudo mkdir -p {0}/log/php".format(config["system"]["www_dir"]))

        # Add repository dir to as environment variable for future use
        if not os.path.exists(config["system"]["bash_profile"]):
            os.system("echo \"export DOCKER_DEV_ENVIRONMENT_DIR={0}\" | sudo tee -a {1} > /dev/null"
                .format(config["system"]["src_dir"], config["system"]["bash_profile"]))
            os.system("source {0}".format(config["system"]["bash_profile"]))

    except IOError as e:
        # You need to have super user permissions to set up hosts settings
        scriptPrint("You need to super user permissions in order to execute this command")
        sys.exit(1)

def dockerBuild():
    os.system("docker-compose -f {0}/docker-compose.yml build".format(config["script_dir"]))

def dockerStart():
    os.system("docker-compose -f {0}/docker-compose.yml up -d".format(config["script_dir"]))

def dockerStop():
    os.system("docker-compose -f {0}/docker-compose.yml stop".format(config["script_dir"]))

def dockerClean():
    os.system("docker stop $(docker ps -aq)")
    os.system("docker rm --force $(docker ps -aq)")
    os.system("docker container prune --force")
    os.system("docker network prune --force")

def dockerPurge():
    os.system("docker stop $(docker ps -aq)")
    os.system("docker rm --force $(docker ps -aq)")
    os.system("docker rmi --force $(docker images -aq)")
    os.system("docker network rm $(docker network ls -q)")
    os.system("docker volume prune --force")

def dockerList(args = ""):
    os.system("docker ps {0}".format(args))

def dockerBash(container):
    shells = ["/bin/bash", "/bin/sh"]

    for shell in shells:
        try:
            os.system("docker exec -it {0} {1}".format(container, shell))
            break
        except:
            pass

def dockerLogs(container):
    os.system("docker logs {0}".format(container))

#### Init application [START] ####

SYS_MACOS = "darwin";
SYS_LINUX = "linux";

config = {
    "platform": sys.platform,
    "script_dir": os.path.dirname(os.path.realpath(__file__)),
    "requirements": {
        "git": "git --version",
        "docker": "docker --version",
        "docker-compose": "docker-compose --version",
    },
    "verbose": 1,
    "known_commands": (
        "help", "setup", "build", "run", "start", "stop", "restart", "sync", "clean",
        "purge", "list", "bash", "logs",
    ),
    "command": "help",
    "args": [],
    "docker": {
        "ip": "127.0.0.1",
    },
    "system": {},
}

if "DOCKER_DEV_ENVIRONMENT_DIR" in os.environ.keys():
    config["script_dir"] = os.environ["DOCKER_DEV_ENVIRONMENT_DIR"]

gatherFacts()
checkRequirements()
parseArguments()

#### Init application [END] ####

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
    dockerClean()

elif command == "purge":
    dockerPurge()

elif command == "list":
    if len(sys.argv) > 2:
        dockerList(sys.argv[2])
    else:
        dockerList()

elif command == "bash":
    if len(sys.argv) == 3:
        dockerBash(sys.argv[2])
    else:
        scriptPrint("Please provide container name or ID")
        sys.exit(1)

elif command == "logs":
    if len(sys.argv) == 3:
        dockerLogs(sys.argv[2])
    else:
        scriptPrint("Please provide container name or ID")
        sys.exit(1)
