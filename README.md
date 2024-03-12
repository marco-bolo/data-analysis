# Marco-Bolo data analysis

(note: this project makes use of local docker files, originally developped in a LifeWatch user-analysis context, these will be removed with updates)

## using this project

Steps:

1. retrieve the source code from github

2. to build the services simply run 

```bash
.$ cp dotenv-example .env             # make sure you have an .env file
.$ cd docker && docker-compose build  # use docker to build the services 
```

3. to start up the services simply run 

```bash
.$ cd docker && docker-compose up     # use docker to run the services 
```

4. open the jupyter notebook

```bash
.$ xdg-open $(docker/jupyter_url.sh)  # this gets the url for the service and opens a browser to it
```

5. open the graphdb browser ui

```bash
.$ xdg-open http://localhost:7200     # opens the web ui in a browser
```

6. run a test-ingest
   
This introduces forcefully at least the data/project.ttl into the triple store
This should not be needed when the ingest runs automatically

```bash
.$ docker exec -it lwua_ingest /bin/bash            # interactively gets you into the ingest env
root@f226b253fbd4:/lwua-py# python -m lwua.ingest   # run the ingest 
```
