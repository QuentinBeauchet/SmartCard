/**
 * 
 */
package src;

import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.APDU;
import javacard.framework.Util;

/**
 * @author Robert
 *
 */
public class CustomApplet extends Applet {
	private final static byte[] PIN = { 0x73, 0x65, 0x63, 0x72, 0x65, 0x74 };
	private final static byte[] PIN_ANSWER = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
	private static byte valid_pin = 0x4F;

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
				insertPIN(apdu, buf);
				break;

			case (byte) 0xA1:
				connectPIN(apdu, buf);
				break;

			case (byte) 0xA2:
				disconnectPIN(apdu, buf);
				break;

			case (byte) 0xA3:
				changePIN(apdu, buf);
				break;

			default:
				// good practice: If you don't know the INStruction, say so:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
		}
	}

	private void isConnectedWithPIN() {
		if (valid_pin != 0x00) {
			ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
		}
	}

	private void insertPIN(APDU apdu, byte[] buf) {
		short bytesRead = apdu.setIncomingAndReceive();
		short answerOffset = (short) 0;

		while (bytesRead > 0) {
			Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN_ANSWER, answerOffset, bytesRead);
			answerOffset += bytesRead;
			bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
		}

		apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) PIN_ANSWER.length);
	}

	private void connectPIN(APDU apdu, byte[] buf) {
		valid_pin = Util.arrayCompare(PIN, (byte) 0, PIN_ANSWER, (byte) 0, (short) PIN_ANSWER.length);

		byte[] res = { valid_pin };

		Util.arrayCopy(res, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) 1);
		apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) 1);
	}

	private void disconnectPIN(APDU apdu, byte[] buf) {
		for (short i = 0; i < PIN_ANSWER.length; i++) {
			PIN_ANSWER[i] = 0x00;
		}

		connectPIN(apdu, buf);
	}

	private void changePIN(APDU apdu, byte[] buf) {
		short bytesRead = apdu.setIncomingAndReceive();
		short answerOffset = (short) 0;

		while (bytesRead > 0) {
			Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN, answerOffset, bytesRead);
			answerOffset += bytesRead;
			bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
		}

		apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) PIN.length);

		disconnectPIN(apdu, buf);
	}

	private void sendMessage(APDU apdu, byte[] buf, byte[] msg) {
		isConnectedWithPIN();
		Util.arrayCopy(msg, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) msg.length);
		apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) msg.length);
	}
}