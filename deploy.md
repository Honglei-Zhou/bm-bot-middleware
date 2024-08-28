## Deploy Bot Middleware in AWS with HTTPS

### 1. Use Nginx + Gunicorn + Eventlet
```buildoutcfg
1. Install virtualenv
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install gunicorn
pip install eventlet

pip install -r requirements.txt

2. Run app in tmux
gunicorn --worker-class eventlet -w 1 -bind 0.0.0.0:5000 wsgi:app

3. Install nginx

sudo apt-get update
sudo apt-get install nginx

4. Config nginx config file

sudo vim /etc/nginx/sites-available/bot-middleware
// Check appendix 1

// make a soft link of config file
sudo ln -s /etc/nginx/sites-available/bot-middleware /etc/nginx/sites-enabled/bot-middleware

// Check config status
sudo nginx -t

// Restart nginx
sudo systemctl restart nginx

```

### 2. Create AWS ALB
```buildoutcfg
Create as tutorial below:
https://aws.amazon.com/blogs/aws/new-aws-application-load-balancer/
```

### 3. Get a domain and ACM certificate
```buildoutcfg
Check tutorals online
```

### 4. Bot middleware is available to use now

#### Appendix 1. Nginx configuration file
```buildoutcfg
server {

           listen 80;  #Custom listener port pointed to 8180 and not 80
           server_name middleware.bmhax.com;
           access_log /var/log/nginx/bm-bot-middleware.log;

           location / {
             # proxy_pass http://unix:/home/ubuntu/bm-bot-middleware/bm-bot-middleware.sock;
             proxy_pass http://127.0.0.1:5001;
             proxy_redirect off;
             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           }

           location /socket.io {
             proxy_pass http://127.0.0.1:5001/socket.io;
             # proxy_pass http://unix:/home/ubuntu/bm-bot-middleware/bm-bot-middleware.sock/socket.io;
             proxy_http_version 1.1;
             proxy_redirect off;
             proxy_buffering off;

             proxy_set_header Host $host;
             proxy_set_header X-Real-IP $remote_addr;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

             proxy_set_header Upgrade $http_upgrade;
             proxy_set_header Connection "Upgrade";
             proxy_set_header 'Access-Control-Allow-Origin' '*';
             # add_header 'Access-Control-Allow-Origin' '*';
           }

```