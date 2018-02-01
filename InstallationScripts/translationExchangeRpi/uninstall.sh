#!/bin/sh

COLOR='\033[0;35m'
NC='\033[0m'

echo -e "${COLOR}----------| Stopping Docker containers... |----------${NC}"
sudo docker stop ap01
sudo docker stop ng01
sudo docker stop dg01

echo -e "${COLOR}----------| Deleting Docker containers... |----------${NC}"
sudo docker system prune -f
sudo rm -R ~/TranslationExchange
sudo rm ~/tex_autorun.sh

echo -e "${COLOR}----------| Deleting installed packages... |----------${NC}"
sudo apt purge -y docker-ce nodejs
sudo rm /etc/apt/sources.list.d/nodesource.list
sudo rm /etc/apt/sources.list.d/docker.list
sudo pip uninstall -y docker docker-pycreds docker-compose dockerpty
