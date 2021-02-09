#!/bin/bash

current_ip=$(curl ifconfig.co)
public_ip=51.68.213.59

if [[ $current_ip == $public_ip ]]; then
        echo "VPN Is Running.."
        echo "Current Public IP is: " $current_ip
elif [[ $current_ip != $public_ip ]]; then
        echo "VPN IS NOT Running, Trying to Reconnect"
        sleep 3
        /usr/sbin/openvpn /root/*.ovpn &
        sleep 5
        current_ip=$(curl ifconfig.co)
        echo "Your Public IP Is: " $current_ip

fi
