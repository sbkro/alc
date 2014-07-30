#!/bin/sh

###########################################################
# build_app.sh
# @author sbkro
# @date 2014/07/30
###########################################################

BUILD_DIR=./_build
SRC_DIR=./src

APP_FILE=alc.alfredworkflow

mkdir $BUILD_DIR
cp -r $SRC_DIR/alc            $BUILD_DIR
cp    $SRC_DIR/etc/info.plist $BUILD_DIR
pushd $BUILD_DIR
zip $APP_FILE ./alc/*.py ./info.plist
mv  $APP_FILE ..
popd
rm -fr $BUILD_DIR
