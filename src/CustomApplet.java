/**
 * 
 */
package src;

import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.APDU;
import javacard.framework.Util;

import javacard.security.Key;
import javacard.security.KeyBuilder;
import javacard.security.RSAPublicKey;

public class CustomApplet extends Applet {
	private final static byte[] hello = { 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x72, 0x6f, 0x62, 0x65, 0x72, 0x74 };
	private final static byte[] salut = { 0x73, 0x61, 0x6c, 0x75, 0x74 };

	public static void install(byte[] buffer, short offset, byte length)

	{
		// GP-compliant JavaCard applet registration
		new CustomApplet().register();
	}

	public void process(APDU apdu) {
		// Good practice: Return 9000 on SELECT
		if (selectingApplet()) {
			return;
		}

		byte[] buf = apdu.getBuffer();
		switch (buf[ISO7816.OFFSET_INS]) {
			case (byte) 0x00:
				Util.arrayCopy(hello, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) 12);
				apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) 12);
				break;

			case (byte) 0xCA:
				sendMessage(apdu, buf, salut);
				break;

			case (byte) 0xA0:
				PIN.insertPIN(apdu, buf);
				break;

			case (byte) 0xA1:
				PIN.connectPIN(apdu, buf);
				break;

			case (byte) 0xA2:
				PIN.disconnectPIN(apdu, buf);
				break;

			case (byte) 0xA3:
				PIN.changePIN(apdu, buf);
				break;

			case (byte) 0xB0:
				Key pubKey = (RSAPublicKey) KeyBuilder.buildKey(KeyBuilder.TYPE_RSA_PUBLIC, KeyBuilder.LENGTH_RSA_512,
						false);
				break;
			default:
				// good practice: If you don't know the INStruction, say so:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
		}
	}

	private void sendMessage(APDU apdu, byte[] buf, byte[] msg) {
		PIN.isConnectedWithPIN();
		Util.arrayCopy(msg, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) msg.length);
		apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) msg.length);
	}
}