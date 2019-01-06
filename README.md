# KNBASE
Online Knowledge Base(someplace for storing unstructured personal notes)


# Ways to launch

##run locally

docker-compose up --build


##run in digitalocean droplet

docker-machine create \
    --driver=generic \
    --generic-ip-address=IP_ADDRESS \
    --generic-ssh-user=USERNAME \
    --generic-ssh-key=PATH_TO_SSH_KEY \
        MACHINE_NAME
        
eval "$(docker-machine env MACHINE_NAME)"

docker-compose build

docker-compose up -d



