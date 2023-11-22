
#!/bin/bash
export PROJECT="/home/ubuntu/DjangoReactFlash"

# Update the system
echo "Updating apt-get"
sudo apt-get -qq update

# Install Python 3.11
echo "Installing Python 3.11..."
sudo apt-get -qq install python3.11 -y

# Install npm
echo "Installing npm..."
sudo apt-get -qq install npm -y

# Install curl
echo "Installing curl..."
sudo apt-get -qq install curl -y

#install poetry
echo "Installing poetry..."
curl -s -sSL https://install.python-poetry.org | sudo python3.11 -
sudo /usr/local/bin/poetry config virtualenvs.create false

# Install nginx
echo "Installing nginx..."
sudo apt-get -qq install nginx -y

# Install Node.js
echo "Installing Node.js..."
sudo apt-get -qq install nodejs -y

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
echo "Running Django migrations..."
cd $PROJECT/backend
python3.11 manage.py makemigrations
python3.11 manage.py migrate

# Collect static files
echo "Collecting static files..."
python3.11 manage.py collectstatic --noinput

# update node
echo "Updating node..."
sudo npm cache clean -f
sudo npm install -g n
sudo n stable

# Install and build npm dependencies
echo "Installing and building npm dependencies..."
cd $PROJECT/frontend
sudo npm ci --silent
sudo npm run build
sudo chmod -R 755 $PROJECT/frontend/build

# Start gunicorn
echo "Starting gunicorn..."
cp $PROJECT/deployment/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
sudo systemctl daemon-reload

# start nginx
# TODO: Should nginx be run in its own user?
echo "Starting nginx..."
sudo ln -s $PROJECT/deployment/nginx.conf /etc/nginx/sites-enabled/DjangoReactFlash
cp $PROJECT/deployment/nginx.service /etc/systemd/system/nginx.service
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
sudo systemctl daemon-reload

# restart both the services
echo "Restarting both the services..."
sudo systemctl restart nginx
sudo systemctl restart gunicorn


echo "Deployment complete"