#!/bin/bash

source ~/.bashrc

# Configure QGIS paths
QGIS_PREFIX_PATH=/usr
if [ -n "$1" ]; then
    DEBUG=$1
fi

if [ -n "$2" ]; then
    VALUE=$2
fi

# Create log dir if not existing
mkdir -p ~/.iquaview/log/

# Execute main and save output to log file
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 -u ${CURR_DIR}/iquaview/src/__main__.py ${DEBUG} ${VALUE} |& tee -a ~/.iquaview/log/"$(date +"%Y_%m_%d_%I_%M_%S")_iquaview.log"

echo "Usage:"
echo "./run.sh /your/optional/qgis/install/path"

