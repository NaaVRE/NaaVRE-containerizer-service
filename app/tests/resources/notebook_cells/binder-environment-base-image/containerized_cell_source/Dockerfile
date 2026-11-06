FROM ghcr.io/naavre/binder-builds/naavre-2dvl-2dopenlab-d7acf3:8fcfe566848b077419e0743a6eb2b00b50ec1e40
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yaml .
RUN micromamba install -y -n notebook -f environment.yaml