# Local development environment setup

I added the support for dockerised testing environment allowing easy getting started development.

What you need is docker or some other container platform and docker-compose

### Prerequisites

- docker
- docker-compose

# How to use

Setup .env and .db-secrets files as per example

Do not set FIXIE_URL, rather set: DEV_ENV='yes' to the file, to enable development mode 

Run: 
```bash
docker-compose up 
```

Your application should be available for you to see bad data, but that's so you have some data immediately so you can start developing. 


