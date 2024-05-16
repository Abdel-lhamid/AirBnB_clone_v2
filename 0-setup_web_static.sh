#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static
# 1. Install Nginx
apt-get update
apt-get install -y nginx
# 2. Create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test /data/web_static/shared
# 3. Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

# 4. Create or recreate the symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# 5. Set ownership of the /data/ folder to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# 6. Update Nginx configuration
config_block="
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
    add_header X-Served-By $HOSTNAME;
}"
echo "$config_block" > /etc/nginx/sites-available/default
# Restart Nginx
service nginx restart
