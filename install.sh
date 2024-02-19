#!/bin/bash

light_blue='\033[1;36m'
light_red='\033[1;91m'
nc='\033[0m'

echo "discord" > requirements.txt
echo "requests" >> requirements.txt

if pip install -r requirements.txt; then
	echo -e "${light_blue}Installation done!${nc}"
	echo -e "${light_blue}Done! Use ./run.sh to run bot.${nc}"
else
	echo -e "${light_red}Error in installation!${nc}"
	exit 1
fi


