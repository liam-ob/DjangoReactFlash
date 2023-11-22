
#!/bin/bash
export PROJECT="/home/ubuntu/DjangoReactFlash"

# Update the system
sudo apt-get update

# Install Python 3.11
sudo apt-get install python3.11 -y

# Install npm
sudo apt-get install npm -y

# Install curl
sudo apt-get install curl -y

#install poetry
curl -sSL https://install.python-poetry.org | sudo python3.11 -
sudo /usr/local/bin/poetry config virtualenvs.create false

# Install nginx
sudo apt-get install nginx -y

# Install Node.js
sudo apt-get install nodejs -y

source ~/.bashrc

# Install Python dependencies without a virtual environment
echo "Installing Python dependencies..."
until cd $PROJECT; do
  echo "Waiting for volume to mount..."
  sleep 2
done
cd $PROJECT
sudo /usr/local/bin/poetry install

# Run the Django migrations
cd $PROJECT/backend
python3.11 manage.py makemigrations
python3.11 manage.py migrate

# Collect static files
python3.11 manage.py collectstatic --noinput

# Define where gunicorn is as an environment variable and refresh bashrc
export GUNICORN_PATH=$(which gunicorn)
source ~/.bashrc

# update node
sudo npm install -g n
sudo n stable

# Install and build npm dependencies
cd $PROJECT/frontend
sudo npm ci --silent
sudo npm run build

# Start gunicorn
cp $PROJECT/deployment/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
sudo systemctl daemon-reload

# start nginx
sudo ln -s $PROJECT/deployment/nginx.conf /etc/nginx/sites-enabled/DjangoReactFlash
cp $PROJECT/deployment/nginx.service /etc/systemd/system/nginx.service
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
sudo systemctl daemon-reload

# restart both the services
sudo systemctl restart nginx
sudo systemctl restart gunicorn