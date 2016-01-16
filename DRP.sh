#!/bin/bash
# DO NOT MODIFY THIS FILE

CONFDIR=/etc/ovirtdrp
CONFFILE=config.yml
CONFLIST=${CONFDIR}/*Fail*

function set_config() {
ln -sf $1 ${CONFDIR}/${CONFFILE}
}

function config_menu() {
CONFs=""

NUM=0
for CONF in ${CONFLIST}
do
NUM=$[NUM+1]
CONFs="$CONFs $CONF $(basename -s .yml $CONF) "
done
OPTION=$(whiptail --title "Menu DRP - Ministerio Hacienda" --menu "Choose your option" 15 60 4 \
$CONFs 3>&1 1>&2 2>&3)

exitstatus=$?
if [ $exitstatus = 0 ]; then
clear
set_config $OPTION
echo "Your using $(basename -s .yml $CONF) "
echo ""
~/ovirtdrp/drp_ovirt.py

else
exit 1
fi

}

config_menu