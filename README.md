Requirements
--

What do you need to use this shit? You will need **python3** in your system and definitely some kind of Unix environment. Luckily Windows 10 users got the wonderful **Windows Subsystem for Linux** thing. If you have Windows 10 - use it! Makes real OS out of Windows 10. And you will obviously need a **Docker** in your environment.

The `dock.py` script has all the things you need to control the Docker containers. You will need to keep the repository though because the script will use docker images from this repository to do its stuff.

Installation
--

Run `./dock.py setup` inside the root directory of this repo. The script requires superuser privileges in order to set up your `/etc/hosts` file. After that, you should be able to use `dock` command from your console in order to manage this environment. The script is saved in `~/.dev-environment/` directory in your home dir.

Managing the Environment
--

Ever feeling lost? Run `dock help` or `dock help all` to see the light.

If you trying to set up the environment for the first time, run `dock build` to build Docker containers and then `dock start` to run them. Or you can just run `dock run` and do both with one command, how neet!

If you built these images you can just run `dock start`, it's faster. Run `dock stop` to stop all containers.

Run `dock list` to get the list of running containers.

If you want to get inside that container, run `dock bash [CONTAINER ID]`. For example, you can run `dock bash nginx` to get all close and personal with that Nginx container serving your shit.

If you wish to remove all containers and images in order to rebuild them from scratch, do `dock purge`.

Sometimes things go wrong. Run `dock logs [CONTAINER ID]` to get to the bottom of things. Logs don't lie.

Useful Docker Commands
--

Build an image: `docker build -t [name]`

Run container detached in background (indefinitely): `docker run -dt [image name]`

List all active docker containers: `docker ps -a`

Inspect the container (network address and all): `docker inspect [container id]`

SSH into container: `docker exec -it [container id] /bin/bash`
