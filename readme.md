# Add JC211_KIT to PATH

```sh
export JC_HOME_TOOLS=jc211_kit
export JAVA_HOME=/usr/lib/jvm/zulu-8-amd64/
export PATH=$JAVA_HOME/bin:$JC_HOME_TOOLS/bin:$PATH
```

# Add GPSHELL to PATH

```sh
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

# Compile java:

```sh
javac -source 1.2 -target 1.1 -g -cp jc211_kit/bin/api.jar helloworld/Helloworld.java
```

# Convert to CAP:

```sh
java -classpath $JC_HOME_TOOLS/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath $JC_HOME_TOOLS/api_export_files:helloworld -classdir . -applet 0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2 Helloworld helloworld 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0
```

# Start PCSCD Service

```sh
sudo service pcscd start
```