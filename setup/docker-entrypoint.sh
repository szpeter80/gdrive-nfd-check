#!/bin/bash

cp "${INSTALL_DIR}/setup/settings.yaml.example" "${DATA_DIR}/settings.yaml"

sed -i "s/your-client-id\.apps\.googleusercontent\.com/$NFD_CHECKER__GCP_CLIENT_ID/g"  "${DATA_DIR}/settings.yaml"
sed -i "s/tell no-one this/$NFD_CHECKER__GCP_CLIENT_SECRET/g"  "${DATA_DIR}/settings.yaml"

### # crond --help                                                                                                                       
### BusyBox v1.32.1 () multi-call binary.                                                                                                                       
###                                                                                                                                                             
### Usage: crond -fbS -l N -d N -L LOGFILE -c DIR                                                                                                               
###                                                                                                                                                             
###         -f      Foreground                                                                                                                                  
###         -b      Background (default)                                                                                                                        
###         -S      Log to syslog (default)                                                                                                                     
###         -l N    Set log level. Most verbose 0, default 8                                                                                                    
###         -d N    Set log level, log to stderr                                                                                                                
###         -L FILE Log to FILE                                                                                                                                 
###         -c DIR  Cron dir. Default:/var/spool/cron/crontabs

crond -f -l 8 -d 8 -L /dev/stdout