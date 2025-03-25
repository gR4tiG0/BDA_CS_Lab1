# BDA
### Lab1
##### Build and start the containers in the background
`docker compose up -d`

##### Stop and remove containers, networks, etc.
`docker compose down`

##### Completely remove containers, images, volumes, and orphans
`docker compose down --rmi all -v --remove-orphans`