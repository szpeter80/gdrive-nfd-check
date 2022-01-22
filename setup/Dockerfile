FROM docker.io/library/alpine:3.15

# ARG is gone after build
# ENV will be in the image

ENV INSTALL_DIR="/srv/gdrive-nfd-check"
ENV DATA_DIR="/mnt/gdrive-nfd-check"
ENV NFD_CHECKER__GCP_CLIENT_ID="dummy-clientid"
ENV NFD_CHECKER__GCP_CLIENT_SECRET="dummy-clientsecret"

ARG GIT_BRANCH="main"
ARG GIT_TAG="1.0.0"

ARG RUNTIME_PKGS="tini \
            bash \
            nano \
            tzdata \
            python3 \
            python3-dev \
            py3-pip"

ARG BUILD_PKGS="gcc \
            musl-dev \
            libffi-dev \
            git \
            python3-dev"

# Build and cleanup needs to stay in the same RUN
# otherwise cleanup will run in a separate layer and wont reduce the image size
RUN set -eux && \
    apk update &&\
    apk add \
        --no-cache \
        --clean-protected \
        ${RUNTIME_PKGS} && \
    apk add \
        --no-cache \
        --clean-protected \
        ${BUILD_PKGS} && \
    mkdir -p ${DATA_DIR} && \
    mkdir -p ${INSTALL_DIR} && \
    cd ${INSTALL_DIR} && \
    git clone -b ${GIT_BRANCH} --single-branch https://github.com/szpeter80/gdrive-nfd-check . && \
    git checkout ${GIT_TAG} && \
    rm -rf ./.git && \
    ln -s ${DATA_DIR}/reports reports && \
    ln -s ${DATA_DIR}/settings.yaml settings.yaml && \
    python3 -m venv project-venv && \
    . ./project-venv/bin/activate && \
    pip install -r ${INSTALL_DIR}/setup/requirements.txt && \
    echo "Docker build RUN success" && \
    apk del \
            --no-cache \
            --clean-protected \
        ${BUILD_PKGS} && \
    rm -rf /var/cache/apk/* && \
    rm -rf /root/.cache && \
    echo "Docker cleanup RUN success"

RUN set -eux && \
    echo -e "#!/bin/bash\n\ncd ${INSTALL_DIR} && ./run-unattended.sh" \
        >> /etc/periodic/15min/nfd-checker && \
        chmod +x /etc/periodic/15min/nfd-checker && \
    echo "Docker crontab setup RUN success"

COPY docker-entrypoint.sh /docker-entrypoint.sh

VOLUME [ "${DATA_DIR}" ]
# CMD can be overridden in "docker run", ENTRYPOINT can't be
ENTRYPOINT ["/sbin/tini", "--", "/docker-entrypoint.sh"] 
