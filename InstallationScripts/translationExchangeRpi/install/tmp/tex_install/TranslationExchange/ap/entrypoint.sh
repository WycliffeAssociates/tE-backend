#!/bin/bash

pid=0
echo "PID INIT: $pid"

# SIGTERM-handler
term_handler() {
  if [ $pid -ne 0 ]; then
    echo "Get SIGTERM"
    
    /etc/init.d/dnsmasq stop
    /etc/init.d/hostapd stop
    /etc/init.d/dbus stop

    iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
    iptables -D FORWARD -i eth0 -o $IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
    iptables -D FORWARD -i $IFACE -o eth0 -j ACCEPT

    kill -SIGTERM "$pid"
    wait "$pid"
  fi
  exit 143;
}

# config UUID
config_uuid() {
    UUID=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1)
    sed -i "s/ssid=.*/ssid=TranslationExchangeAP_$UUID/g" /etc/hostapd/hostapd.conf
    echo "1" > /config_done
}

IFACE=$(iw dev | awk '$1=="Interface"{print $2}')
echo "Device: $IFACE"

sed -i "s/interface=.*/interface=$IFACE/g" /etc/dnsmasq.conf
sed -i "s/interface=.*/interface=$IFACE/g" /etc/hostapd/hostapd.conf

if [ ! -f /config_done ]; then
    config_uuid
fi

ifconfig $IFACE 10.0.0.1/24

#echo 1 > /proc/sys/net/ipv4/ip_forward
sysctl -w net.ipv4.ip_forward=1
sysctl -p
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o $IFACE -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $IFACE -o eth0 -j ACCEPT

/etc/init.d/dbus start
/etc/init.d/hostapd start
/etc/init.d/dnsmasq start

# setup handlers
trap 'kill ${!}; term_handler' SIGTERM

sleep infinity &

pid="$!"
echo "PID: $pid"

wait ${!}
