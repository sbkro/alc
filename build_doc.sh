#!/bin/sh

###########################################################
# build_app.sh
# @author sbkro
# @date 2014/07/30
###########################################################

pushd ./doc
PYTHONPATH=../src make clean
PYTHONPATH=../src make html
popd
