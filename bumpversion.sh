#!/usr/bin/env bash

version=$1

if [ -z "$version" ]
	then
		echo "You need to specify a version"
		exit
fi


sed -i.bak s/DOIT_VERSION.*/DOIT_VERSION\ \=\ \'${version}\'/ doit/settings/base.py
