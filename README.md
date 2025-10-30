# NaaVRE-containerizer-service

## Running locally

Create conda environment:

```shell
conda env create -f environment.yaml
```

Activate the environment:

```shell
conda activate naavre-containerizer-service
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

`values.yaml` should contain ingress, OAuth2, and other configuration (
checkout [./helm/naavre-containerizer-service/values-example.yaml](./helm/naavre-containerizer-service/values-example.yaml)).

## Configuration

### Generate JWT

To test the service, you need to generate a test JWT token. To do this, follow these [instructions](https://github.com/NaaVRE/NaaVRE-architecture/blob/main/overview.md#fake-authentication-mode-development-and-testing).
Then, add the token you created to the `Authorization` header to your HTTP requests:

```http
Authorization: Bearer eyJ0eXAi...
```
