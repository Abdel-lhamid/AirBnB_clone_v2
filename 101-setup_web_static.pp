# Puppet manifest to set up web servers for the deployment of web_static

# Step 1: Install Nginx
package { 'nginx':
  ensure => installed,
}

# Step 2: Create necessary directories if they don't exist
file { ['/data/web_static/releases/test', '/data/web_static/shared']:
  ensure => directory,
}

# Step 3: Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => file,
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
}

# Step 4: Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Step 5: Set ownership of the /data/ folder to ubuntu user and group recursively
file { '/data/':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Step 6: Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "server {
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
}",
}

# Step 7: Restart Nginx
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}

