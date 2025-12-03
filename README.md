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
helm -n naavre-containerizer-service upgrade --install --create-namespace naavre-containerizer-service ./helm/naavre-containerizer-service -f values-deploy-naavre-containerizer-service-minikube-github-secrets.yaml
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

```shell


### Test on GitHub

The secrets.CONFIG_FILE should have quotes escaped:

```commandline
{   \"vl_configurations\": [     {       \"name\": \"openlab\",       \"base_image_tags_url\": \"https://raw.githubusercontent.com/QCDIS/NaaVRE-conf/main/base_image_tags_latest.json\",       \"module_mapping_url\": \"https://raw.githubusercontent.com/QCDIS/NaaVRE-conf/main/module_mapping.json\",       \"cell_github_url\": \"https://github.com/NaaVRE/cells-vl-tests.git\",       \"cell_github_token\": \"TOKEN\",       \"registry_url\": \"ghcr.io/qcdis/naavre-cells-vl-tests\"     },     {       \"name\": \"virtual_lab_2\",       \"base_image_tags_url\": \"https://raw.githubusercontent.com/QCDIS/NaaVRE-conf/main/base_image_tags_latest.json\",       \"module_mapping_url\": \"https://raw.githubusercontent.com/QCDIS/NaaVRE-conf/main/module_mapping.json\",       \"cell_github_url\": \"\",       \"cell_github_token\": \"\",       \"registry_url\": \"https://registry.naavre.com\"     }   ] }
```

You can run the following command to generate the secrets.CONFIG_FILE:

```shell
tr -d '\n' < configuration.json | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'
```

