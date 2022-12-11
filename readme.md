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

# CLI

```sh
$ help
Command List :
- login ... -> connect with a PIN to the card
- logout  -> disconnect the card
- changepin ...  -> change the PIN
- genkeys  -> generate a RSA key pair
- pubkey  -> get the public key from the card
- sign ...  -> get the signature of a message
- verify ...  -> check if the message in argument is matching
- info  -> get card infos
```

Examples :
```sh
$ login secret
Successfully connected using PIN
```
```sh
$ changepin secret
Successfully changed the PIN and disconnected
```
```sh
$ genkeys
Successfully generated a new RSA KeyPair
```
```sh
$ pubkey
-----BEGIN RSA PUBLIC KEY-----
MEgCQQClmsxmuMET0kBl5nMIoLuXoQPmwNxtLjOybeXH4XYXFo5d8DoBnFqKE30u
Fa0qN87UBsxLjGYsbjSOgmvjabQpAgMBAAE=
-----END RSA PUBLIC KEY-----
```
```sh
$ sign hello 
Received signature: ¤³@Ë]&§+ÄàºSð¨ªÂPþV"AgY[.»gCT'ÑK³`üzýå¼eàóâÑù­ÿ±»ou:V
```
```sh
$ verify hello
Signature is valid
```
```sh
$ info
Created by Quentin BEAUCHET and Yann FORNER
```


# Documentation

- [List of responses code](https://www.eftlab.com/knowledge-base/complete-list-of-apdu-responses)
- [APDU message protocol format](https://en.wikipedia.org/wiki/Smart_card_application_protocol_data_unit)
