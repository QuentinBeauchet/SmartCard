# Architecture
Instruction | Usage
--- | --- |
```0x00``` | Returns the informations about the card stored in a byte[].
```0xA0``` | Read the PIN from the command data and compare it with the PIN stored in memory, returns ```69 82``` if the PIN does not match. Also to make your life easier we limited the PIN to a length of 6 bytes.
```0xA1``` | Disconnected the PIN meaning that the next time the user want to send a command to the JavaCard he will need to reconnect.
```0xA2``` | Allow the user to change the PIN stored in memory. It reads the new PIN from the command data, disconnect the PIN and returns ```69 83``` if the PIN was successfully changed.
```0xB0``` | Generate a 512 RSA Keys pair and store it in memory.
```0xB1``` | Returns the exponent and the modulus of the public key as ```len(exp) exp len(mod) mod``` (without spaces).
```0xB2``` | Read a message from the command data and signs it using the private key. The signature it stored in memory.
```0xB3``` | Returns the signature.

>Each commands with the exception of ```0xA0``` and ```0xA1``` needs to be connected using the PIN or they will return ```69 82``` before running.

>To test everything you can uncomment the last two lines from APDU.py and run it with ```python APDU.py```

# Requirements

- You need to clone the repo [pyscard](https://github.com/LudovicRousseau/pyscard) and run the setup.py script.
- You might also need to do ```pip install rsa``` to install the rsa module for python.
- To send the Applet to the JavaCard we use [gpshell](https://github.com/kaoh/globalplatform) but you can use what you want.

# Send the Applet to the JavaCard

We made a script named ```compile.sh``` and you need to run it each time you make changes to the Applet for it to update the JavaCard. Below are some of the things the script do.

### Add JC211_KIT to PATH

```sh
export JC_HOME_TOOLS=jc211_kit
export JAVA_HOME=/usr/lib/jvm/zulu-8-amd64/
export PATH=$JAVA_HOME/bin:$JC_HOME_TOOLS/bin:$PATH
```

### Add GPSHELL to PATH

```sh
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
```

### Compile java:

```sh
javac -source 1.2 -target 1.1 -g -cp jc211_kit/bin/api.jar helloworld/Helloworld.java
```

### Convert to CAP:

```sh
java -classpath $JC_HOME_TOOLS/bin/converter.jar:. com.sun.javacard.converter.Converter -verbose -exportpath $JC_HOME_TOOLS/api_export_files:helloworld -classdir . -applet 0xa0:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1:0x2 Helloworld helloworld 0x0a:0x0:0x0:0x0:0x62:0x3:0x1:0xc:0x6:0x1 1.0
```

### Start PCSCD Service

```sh
sudo service pcscd start
```

# CLI

To start the CLI simply run
```sh
python cli.py
```
Commands :

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
```sh
$ login secret
Successfully connected using PIN
```
```sh
$ logout secret
Successfully disconnected the PIN
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
