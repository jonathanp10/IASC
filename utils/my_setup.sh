# !/usr/bin/tcsh
setenv EN_ID 1
setenv IASC_dir_name iasc
setenv IASC_PATH /home/pi/Desktop/$IASC_dir_name
setenv EN_PATH $IASC_PATH/code/en
setenv GW_PATH $IASC_PATH/code/gw
if (!  -e ~/.vim/backup) then
   mkdir ~/.vim/backup
   endif
if (!  -e ~/.vim/tmp) then
   mkdir ~/.vim/tmp
   endif
source ~/.alias
