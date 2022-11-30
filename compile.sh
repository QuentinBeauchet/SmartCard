#!/bin/bash
set -e

sudo service pcscd start

export JC_HOME_TOOLS=jc211_kit
export JAVA_HOME=/usr/lib/jvm/zulu-8-amd64/
export PATH=$JAVA_HOME/bin:$JC_HOME_TOOLS/bin:$PATH

javac -source 1.2 -target 1.1 -g -cp jc211_kit/bin/api.jar src/CustomApplet.java

java -classpath $JC_HOME_TOOLS/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath $JC_HOME_TOOLS/api_export_files:src -classdir . -applet 0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2 CustomApplet src 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0

eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"

gpshell ./scripts/deleteApplet >/dev/null
gpshell ./scripts/uploadApplet >/dev/null

echo "Deployement done you can now use python init.py"