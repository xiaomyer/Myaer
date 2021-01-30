#!/bin/sh
date=$(date +"%m-%d-%Y-%T")
cp /home/myer/Myaer/Myaer/data/guilds.json /home/myer/backup/guilds_config_backup_${date}.json
cp /home/myer/Myaer/Myaer/data/users.json /home/myer/backup/users_config_backup_${date}.json
# cp /home/myer/Myaer/Myaer/analytics.json /home/myer/backup/analytics_backup_${date}.json
