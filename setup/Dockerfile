FROM alpine:3.15.0

# ARG is gone after build
# ENV will be in the image

ENV INSTALL_DIR="/srv/gdrive-nfd-check"
ENV DATA_DIR="/mnt/gdrive-nfd-check"
ENV NFD_CHECKER__GCP_CLIENT_ID="dummy-clientid"
ENV NFD_CHECKER__GCP_CLIENT_SECRET="dummy-clientsecret"

RUN set -eux && \
    INSTALL_PKGS="bash \
            nano \
            gcc \
            tzdata \
            musl-dev \
            libffi-dev \
            git \
            python3 \
            python3-dev \
            py3-pip" && \
    apk update &&\
    apk add \
            --no-cache \
            --clean-protected \
        ${INSTALL_PKGS} && \
    mkdir -p ${DATA_DIR} && \
    mkdir -p ${INSTALL_DIR} && \
    cd ${INSTALL_DIR} && \
    git clone https://github.com/szpeter80/gdrive-nfd-check . && \
    ln -s ${DATA_DIR}/reports reports && \
    ln -s ${DATA_DIR}/settings.yaml settings.yaml && \
    python3 -m venv project-venv && \
    . ./project-venv/bin/activate && \
    pip install -r ${INSTALL_DIR}/setup/requirements.txt && \
    echo "Docker RUN success"


COPY docker-entrypoint.sh /docker-entrypoint.sh
CMD /docker-entrypoint.sh