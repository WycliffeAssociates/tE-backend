# translation Exchange server installation scripts
A set of installation scripts to deploy TranslationExchange server on RaspberryPi or virtual machine

## System Requirements
* Linux OS (Debian 8, 9, Ubuntu)
* Hard Drive or SD Card - **8Gb or more** (for RPi)
* Local Area Netork Connection
   - *Wireless Router - for tablet connectivity*
   - *Wired*
* Localized in English

## VM installation
1. Make all the scripts executable `chmod +x *.*`
2. Execute prepare (`./prepare`)
3. Execute software (`./software`)
4. Execute install (`./install`)

To remove server from machine execute uninstall (`./uninstall`)

## RPi deb package build
In terminal you have to be in the same level with 'install' folder.
1. Set proper chmod `chmod -R 755 install/`
2. Execute `dpkg-deb --build install/`

## RPi installation
1. Make all the scripts executable `chmod +x *.*`
2. Execute prepare.sh (double click) 
3. Execute install.deb (double click)

To remove server from machine execute uninstall (double click or `./uninstall.sh`)

### Hardware 
* [Rasberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

## Contributors
This project was made by the *8WoC 2017* intern group.
