FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        docker-cli \
        python3 \
        git \
        curl && \
    rm -rf /var/lib/apt/lists/*

USER jenkins

RUN jenkins-plugin-cli --plugins \
    git \
    github \
    workflow-aggregator \
    htmlpublisher \
    credentials-binding