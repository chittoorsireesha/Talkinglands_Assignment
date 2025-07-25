#!/bin/bash
apt-get update -y
apt-get install nginx -y
echo "Deployed via Terraform." > /var/www/html/index.html
systemctl enable nginx
systemctl start nginx
