# Implement a 2 stage build here to build the react app and then copy it to the finished container in the /var/www/DjangoReactFlash/frontend/build folder

FROM ubuntu:22.04

RUN useradd -ms /bin/bash ubuntu

# only create group if it doesn't exist
RUN groupadd -r ubuntu ||true
# RUN usermod -aG mygroup myuser
RUN usermod -aG ubuntu ubuntu
RUN usermod -aG sudo ubuntu
# add ubuntu to sudo
RUN echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers


COPY . /var/www/DjangoReactFlash

RUN chmod -R 777 /var/www/

USER ubuntu
CMD ["bash"]
RUN sudo bash /var/www/DjangoReactFlash/deployment/setenv.sh
RUN sudo rm /var/www/DjangoReactFlash/deployment/setenv.sh
RUN sudo bash /var/www/DjangoReactFlash/deployment/deploy.sh