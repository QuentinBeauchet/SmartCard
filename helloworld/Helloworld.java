/**
 * 
 */
package helloworld;

import javacard.framework.Applet;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.APDU;
import javacard.framework.Util;

/**
 * @author Robert
 *
 */
public class Helloworld extends Applet {

	private final static byte[] hello = { 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x20, 0x72, 0x6f, 0x62, 0x65, 0x72, 0x74 };
	private final static byte[] salut = { 0x73, 0x61, 0x6c, 0x75, 0x74 };
	private final static byte[] PIN = { 0x73, 0x65, 0x63, 0x72, 0x65, 0x74 };
	private final static byte[] PIN_ANSWER = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

	private final static boolean valid_pin = false;

	public static void install(byte[] buffer, short offset, byte length)

	{
		// GP-compliant JavaCard applet registration
		new Helloworld().register();
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
				Util.arrayCopy(salut, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) salut.length);
				apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) salut.length);
				break;
			case (byte) 0xA0:
				short bytesRead = apdu.setIncomingAndReceive();
				short answerOffset = (short) 0;

				while (bytesRead > 0) {
					Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN_ANSWER, answerOffset, bytesRead);
					answerOffset += bytesRead;
					bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
				}

				apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) PIN_ANSWER.length);
				break;

			case (byte) 0xA1:
				byte[] valid_pin = {
						Util.arrayCompare(PIN, (byte) 0, PIN_ANSWER, (byte) 0, (short) PIN_ANSWER.length) };

				Util.arrayCopy(valid_pin, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) 1);
				apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) 1);
				break;

			default:
				// good practice: If you don't know the INStruction, say so:
				ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
		}
	}
}