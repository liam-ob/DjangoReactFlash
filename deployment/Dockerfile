FROM ubuntu:22.04

COPY . /website

RUN chmod +x /website/deployment/deploy.sh
RUN /website/deployment/deploy.sh