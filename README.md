How to use this shit. You will need python3 by the way.

Q: How do I run this shit.
A: First you need to build the containers cause they not gonna build themselves. Use `./dock build` to do it.
Then run `./dock start` if you are on "UNIX" like system. Cry if you use Windows.

Q: Is there a way to get the list of all available commands?
A: Run `./dock help` and read that shit carefully.

Q: And how do I stop all this shit.
A: Run `./dock stop`, and if you can start this on Windows, sure you know how to stop this shit.

Q: How to "ssh" into the running container?
A: First run `./dock list` and find out [CONTAINER ID] of the running container that you want to get into.
Then run `./dock bash [CONTAINER ID]` to run `bash` in the context of the container.

Q: I played with my private parts and these scripts a little and now there are all kind of containers and
images all over my machine, what should I do?
A: Just run `./dock purge` and it will remove all your docker images and containers.

Useful Docker commands:
Build an image:
  docker build -t [name] .

Run container detached in background (indefinitely):
  docker run -dt [image name]

List all active docker containers:
  docker ps -a

Inspect the container (network address and all)
  docker inspect [container id]

SSH into container:
  docker exec -it [container id] /bin/bash
