/**
 * 
 */
package src;

import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.APDU;
import javacard.framework.Util;

public class CustomApplet extends Applet {
	private final static byte[] informations = { 67, 114, 101, 97, 116, 101, 100, 32, 98, 121, 32, 81, 117, 101, 110,
			116, 105,
			110, 32, 66, 69, 65, 85, 67, 72, 69, 84, 32, 97, 110, 100, 32, 89, 97, 110, 110, 32, 70, 79, 82, 78, 69,
			82 };

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
				PIN.isConnectedWithPIN();
				Util.arrayCopy(informations, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) informations.length);
				apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) informations.length);
				break;

			case (byte) 0xA0:
				PIN.connectPIN(apdu, buf);
				break;

			case (byte) 0xA1:
				PIN.disconnectPIN();
				break;

			case (byte) 0xA2:
				PIN.isConnectedWithPIN();
				PIN.changePIN(apdu, buf);
				break;

			case (byte) 0xB0:
				PIN.isConnectedWithPIN();
				RSA.generateKeyPair();
				break;

			case (byte) 0xB1:
				PIN.isConnectedWithPIN();
				RSA.sendPublicKey(apdu, buf);
				break;

			case (byte) 0xB2:
				PIN.isConnectedWithPIN();
				RSA.signMessage(apdu, buf);
				break;

			case (byte) 0xB3:
				PIN.isConnectedWithPIN();
				RSA.sendSignature(apdu, buf);
				break;

			default:
				// good practice: If you don't know the INStruction, say so:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
		}
	}
}