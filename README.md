# faiss-api
Simple faiss API for index search with flask and docker

# About Faiss
Faiss is a tool created by the Facebook Research team to efficiently get vector similarities, more info on https://github.com/facebookresearch/faiss/

# How to use

* Export your faiss index to .index file like:

```
import faiss
index = ... #your index logic
index.train(data)
index.add(data)
faiss.write_index(index, "latest.index")
#optional - save the sequencial list of keys
import numpy as np
np.save('keys.npy', np.array(keys_list)) 
```

* clone this repository
* add the `latest.index` in the app root path
* add the `keys.npy` in the app root path (optional)

# Run local with Docker

* Build docker image (in the app root path)
> docker build -t samuelhei/faiss-api:latest .

* Run Image
> docker run -e LD_LIBRARY_PATH='/usr/local/lib' -p 5000:5000 samuelhei/faiss-api:latest

* Open a new terminal and get the docker IP

> $ docker ps
> $ docker inspect <container id> | grep "IPAddress"

Change the `<container id>` part with the id returned on the `docker ps` command, the returned IP address will be your host, using the port `5000` like http://127.0.0.2:5000

# Deploy on AWS beanstalk

* Install the AWS client (if not installed)

> $ pip install awscli
> $ pip install awsebcli

* Set your preferences of the region and set Docker as Environment
> $ eb init 
* Create and Deploy application (This will use t2.micro as default)
> $ eb create  -d --envvars LD_LIBRARY_PATH=/usr/local/lib 
* When you update your application then you can redeploy
> $ eb deploy

# Test the endpoint
* Open in your browser `<host>/ping`, if everything is ok it will be returned the following result:  `{"ping":"pong"}`

# Getting search results from the index

* Send a POST method to `<host>/get_similarities` with the following parms:
    * `vector` as text like 0.10359007865190506,0.25027135014533997,0.6511507034301758,0.501607358455658,0.39755818247795105,0.007388297468423843,0.33636972308158875,0.1718718260526657,0.1494559347629547,0.23654937744140625,0.39706116914749146 
    * `n` as the number of itens to return (default value 5)
    
