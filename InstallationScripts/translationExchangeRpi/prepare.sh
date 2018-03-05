#!/bin/sh

COLOR='\033[0;35m'
NC='\033[0m'

gconftool --type bool --set /apps/gksu/sudo-mode true
sudo apt install -y curl
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
curl -fsSL get.docker.com -o /tmp/get-docker.sh
sudo sh /tmp/get-docker.sh
sudo apt install -y gdebi

echo -e "${COLOR}-------| Preparation complete. Now execute translationExchange.deb |-------${NC}"