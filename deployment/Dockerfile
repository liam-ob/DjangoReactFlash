FROM ubuntu:22.04

COPY . /var/www/DjangoReactFlash

RUN chmod +x /var/www/DjangoReactFlash/deployment/deploy.sh
RUN chmod +x /var/www/DjangoReactFlash/deployment/setenv.sh
RUN /var/www/DjangoReactFlash/deployment/setenv.sh
RUN /var/www/DjangoReactFlash/deployment/deploy.sh