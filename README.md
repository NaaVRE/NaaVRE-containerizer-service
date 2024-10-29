# NaaVRE-containerizer-service

## Running locally

Install dependencies:

```shell
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

For the rpy2 dependency, you need to install 'python3.11-dev':

```shell
sudo apt-get install python3.11-dev 
```


Run the dev server

```shell
fastapi dev app/main.py
```

## Build Docker image

```shell
docker build . -f docker/Dockerfile -t naavre-containerizer-service:dev
```

To run it:

```shell
docker run -p 127.0.0.1:8000:8000 naavre-containerizer-service:dev
```

and open http://127.0.0.1:8000/docs

## Deployment

We use Helm for the deployment:

```shell
helm -n naavre-containerizer-service upgrade --install --create-namespace naavre-containerizer-service ./helm/naavre-containerizer-service -f values.yaml
```

`values.yaml` should contain ingress, OAuth2, and other configuration (checkout [./helm/naavre-containerizer-service/values-example.yaml](./helm/naavre-containerizer-service/values-example.yaml)).
