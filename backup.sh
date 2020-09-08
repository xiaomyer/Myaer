#!/bin/sh
date=`date +"%m-%d-%Y-%T"`
cp /home/myerfire/Myaer/Myaer/core/config/guilds.json /home/myerfire/backup/guilds_config_backup_${date}.json
cp /home/myerfire/Myaer/Myaer/core/config/users.json /home/myerfire/backup/users_config_backup_${date}.json
cp /home/myerfire/Myaer/Myaer/analytics.json /home/myerfire/backup/analytics_backup_${date}.json
