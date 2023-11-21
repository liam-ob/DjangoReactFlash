
#!/bin/bash
export PROJECT="/website"

# Update the system
apt-get -q update

# Install Python 3.11
apt-get -q install python3.11 -y

# Install npm
apt-get -q install npm -y

# Install curl
apt-get -q install curl -y

#install poetry
curl -sSL https://install.python-poetry.org | python3.11 -
export PATH="/root/.local/bin:$PATH"
poetry config virtualenvs.create false

# Install nginx
apt-get install nginx -y

# Install Node.js
curl -sL https://deb.nodesource.com/setup_14.x | -E bash -
apt-get -q install nodejs -y

source ~/.bashrc

# Install Python dependencies without a virtual environment
echo "Installing Python dependencies..."
until cd $PROJECT; do
  echo "Waiting for volume to mount..."
  sleep 2
done
cd $PROJECT
poetry install

# Run the Django migrations
cd $PROJECT/backend
python3.11 manage.py makemigrations
python3.11 manage.py migrate

# Collect static files
python3.11 manage.py collectstatic --noinput

# Define where gunicorn is as an environment variable and refresh bashrc
export GUNICORN_PATH=$(which gunicorn)
source ~/.bashrc

# Install and build npm dependencies
cd $PROJECT/frontend
npm ci --silent
npm run build

# link nginx config file
ln -s $PROJECT/deployment/nginx.conf /etc/nginx/sites-enabled/website

# Start gunicorn
cp $PROJECT/deployment/gunicorn.service /etc/systemd/system/gunicorn.service
systemctl start gunicorn
systemctl enable gunicorn
systemctl status gunicorn
systemctl daemon-reload
systemctl restart gunicorn

# start nginx
nginx -t