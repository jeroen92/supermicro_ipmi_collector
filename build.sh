#!/usr/bin/env bash

set -e

IMAGE=smipmi_collector
VERSION=0.0.1
SMCIPMITOOL_VERSION='SMCIPMITool_2.20.0_build.180525_bundleJRE_Linux_x64'
SMCIPMITOOL_SRC="ftp://ftp.supermicro.com/utility/SMCIPMItool/Linux/$SMCIPMITOOL_VERSION.tar.gz"

WORKDIR=`pwd`

if [ "$1" ]; then
    SMCIPMITOOL_PATH=$1
    mkdir ./smcipmitool
    cp -R $SMCIPMITOOL_PATH/* ./smcipmitool
    SMCIPMITOOL_PATH=./smcipmitool
    CLEANUP_DIR="./smcipmitool"
else
    curl ${SMCIPMITOOL_SRC} -o smcipmitool.tar.gz
    tar xf smcipmitool.tar.gz
    rm smcipmitool.tar.gz

    SMCIPMITOOL_PATH=$SMCIPMITOOL_VERSION
    CLEANUP_DIR=$SMCIPMITOOL_PATH
fi;

echo ${SMCIPMITOOL_PATH}
docker build . -t ${IMAGE}:${VERSION} --build-arg SMCIPMITOOL_PATH=${SMCIPMITOOL_PATH}

if [ -z "$1" ]; then
    echo rm -R ${CLEANUP_DIR}
fi;
