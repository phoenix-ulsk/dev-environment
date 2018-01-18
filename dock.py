#!/usr/bin/env python3
import os
import sys
import subprocess

def checkRequirements():
    missing_requirements = []

    for packet, command in REQUIREMENTS.items():
        (code, res) = subprocess.getstatusoutput(command)

        if code > 0:
            missing_requirements.append(packet)

    if len(missing_requirements) > 0:
        for packet in missing_requirements:
            print("\33[1;31;40m{0} is required. Please install {0}.".format(packet))

        os.system("tput sgr0")
        sys.exit(1)

def checkoutSystemBranch():
    if sys.platform == "darwin":
        (code, res) = subprocess.getstatusoutput("git rev-parse --abbrev-ref HEAD")

        if res != "osx/php+mysql":
            os.system("git --git-dir={0}/.git checkout osx/php+mysql -q".format(DOCKER_DIR))

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
    print("You need to super user permissions in order to execute this command")

    try:
        # Set up hosts file
        hosts = open(HOSTS_FILE, "r");
        if "dev.local" not in hosts.read():
            HOSTS_LIST = """
127.0.0.1\tlocalunixsocket
{0}\tdev.local
{0}\tdev5.local
{0}\tphpmyadmin.local
{0}\tmailcatcher.local""".format(DOCKER_MACHINE_IP)
            os.system("echo \"{0}\" | sudo tee -a /etc/hosts > /dev/null".format(HOSTS_LIST))

        # Set up this script as system executable
        if not os.path.exists("~/.dev-environment"):
            os.system("mkdir -p ~/.dev-environment")
            os.system("cp {0}/dock.py ~/.dev-environment".format(DOCKER_DIR))
            os.system("sudo ln -s {0}/.dev-environment/dock.py {1}/dock".format(HOME, EXECUTABLE_DIR))

        # Set up autocomplete script
        if not os.path.exists("{0}/dock".format(AUTOCOMPLETE_DIR)):
            os.system("cp {0}/dock_autocomplete ~/.dev-environment".format(DOCKER_DIR))
            if sys.platform == "darwin":
                os.system("ln -s {0}/.dev-environment/dock_autocomplete {1}/dock".format(HOME, AUTOCOMPLETE_DIR))
            else:
                os.system("sudo cp {0}/.dev-environment/dock_autocomplete {1}/dock".format(HOME, AUTOCOMPLETE_DIR))

        # Create directories for web server
        if not os.path.exists("{0}/www".format(HOME)):
            os.system("mkdir -p {0}/www".format(HOME))
            os.system("mkdir -p {0}/www/html".format(HOME))
            os.system("mkdir -p {0}/www/log".format(HOME))
            os.system("mkdir -p {0}/www/log/nginx".format(HOME))
            os.system("mkdir -p {0}/www/log/php".format(HOME))
            os.system("mkdir -p {0}/www/log/mysql5".format(HOME))

        # Add repository dir to as environment variable for future use
        bash = open(BASH_PROFILE, "r+");
        if "DOCKER_DEV_ENVIRONMENT_DIR" not in bash.read():
            bash.write("\nexport DOCKER_DEV_ENVIRONMENT_DIR={0}".format(SCRIPT_DIR));
            os.system("source ~/.bash_profile")

    except IOError as e:
        # You need to have super user permissions to set up hosts settings
        print("You need to super user permissions in order to execute this command")
        sys.exit(1)

def dockerBuild():
    if sys.platform == "darwin":
        os.system("docker-sync start -c {0}/docker-sync.yml".format(DOCKER_DIR))

    os.system("docker-compose -f {0}/docker-compose.yml build".format(DOCKER_DIR))

def dockerStart():
    if sys.platform == "darwin":
        os.system("docker-sync start -c {0}/docker-sync.yml".format(DOCKER_DIR))

    os.system("docker-compose -f {0}/docker-compose.yml up -d".format(DOCKER_DIR))

def dockerStop():
    os.system("docker-compose -f {0}/docker-compose.yml stop".format(DOCKER_DIR))

    if sys.platform == "darwin":
        os.system("docker-sync stop -c {0}/docker-sync.yml".format(DOCKER_DIR))

def dockerBash(container):
    shells = ["/bin/bash", "/bin/sh"]

    for shell in shells:
        try:
            os.system("docker exec -it {0} {1}".format(container, shell))
            break
        except:
            pass

# Search for available docker machines named like default or dev
def getDockerMachinesList():
    mlist = []
    cmd_output = os.popen("docker-machine ls --filter name=de --format \"{{.Name}}\"")

    for line in cmd_output.readlines():
        mlist.append(line.strip())

    return mlist

def getDockerMachineIpByName(name):
    return os.popen("docker-machine ip {0}".format(name)).read().strip()

#### [START] Init application variables ####

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
HOME = os.environ["HOME"]

REQUIREMENTS = {
    "git": "git --version",
    "docker": "docker --version",
    "docker-compose": "docker-compose --version",
}

if "DOCKER_DEV_ENVIRONMENT_DIR" in os.environ.keys():
    DOCKER_DIR = os.environ["DOCKER_DEV_ENVIRONMENT_DIR"]
else:
    DOCKER_DIR = SCRIPT_DIR

machines_list = getDockerMachinesList()
DOCKER_MACHINE_IP = "127.0.0.1"

# Set system specific variables, required in the SCRIPT_DIR
if sys.platform == "darwin":
    HOSTS_FILE = "/etc/hosts"
    AUTOCOMPLETE_DIR = "/usr/local/etc/bash_completion.d"
    EXECUTABLE_DIR = "/usr/local/bin"
    BASH_PROFILE = "{0}/.bash_profile".format(HOME)
    REQUIREMENTS["docker-sync"] = "docker-sync --version"

    if len(machines_list) > 0:
        DOCKER_MACHINE_IP = getDockerMachineIpByName(machines_list[0])

elif sys.platform == "linux":
    HOSTS_FILE = "/etc/hosts"
    AUTOCOMPLETE_DIR = "/etc/bash_completion.d"
    EXECUTABLE_DIR = "/usr/local/bin"
    BASH_PROFILE = "{0}/.profile".format(HOME)

    if len(machines_list) > 0:
        DOCKER_MACHINE_IP = getDockerMachineIpByName(machines_list[0])

#### [END] Init application variables ####

checkRequirements()
checkoutSystemBranch()

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
    os.system("docker rm --force $(docker ps -aq)")
    os.system("docker container prune --force")
    os.system("docker network prune --force")
    os.system("docker images prune --force")

elif command == "purge":
    os.system("docker stop $(docker ps -aq)")
    os.system("docker rm --force $(docker ps -aq)")
    os.system("docker rmi --force $(docker images -aq)")
    os.system("docker network rm $(docker network ls -q)")

    if sys.platform == "darwin":
        os.system("docker-sync clean")

elif command == "list":
    if len(sys.argv) > 2:
        os.system("docker ps {0}".format(sys.argv[2]))
    else:
        os.system("docker ps")

elif command == "bash":
    if len(sys.argv) == 3:
        dockerBash(sys.argv[2])
    else:
        print("Please provide container name or ID")

elif command == "logs":
    if len(sys.argv) == 3:
        os.system("docker logs {0}".format(sys.argv[2]))
    else:
        print("Please provide container name or ID")
