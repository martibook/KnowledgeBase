# KnBase
Online Knowledge Base(someplace for storing unstructured personal notes)

![ index ](https://github.com/MartiBook/knbase/raw/master/previews/index.gif)


# What Could Be Done With KnBase

# create a piece of note
![ create a piece of note ](https://github.com/MartiBook/knbase/raw/master/previews/create.gif)

# view notes you've created
![ view notes you've created ](https://github.com/MartiBook/knbase/raw/master/previews/detail.gif)

# search for notes by keywords
![ search for notes by keywords ](https://github.com/MartiBook/knbase/raw/master/previews/search.gif)

# get all notes related to the keywords
![ get all notes related to the keywords ](https://github.com/MartiBook/knbase/raw/master/previews/result.gif)


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



