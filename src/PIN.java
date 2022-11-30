package src;

import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.APDU;
import javacard.framework.Util;

public class PIN {
    private final static byte[] PIN = { 0x73, 0x65, 0x63, 0x72, 0x65, 0x74 };
    private final static byte[] PIN_ANSWER = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
    private static byte valid_pin = 0x4F;

    public static void isConnectedWithPIN() {
        if (valid_pin != 0x00) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    public static void insertPIN(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN_ANSWER, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) PIN_ANSWER.length);
    }

    public static void connectPIN(APDU apdu, byte[] buf) {
        valid_pin = Util.arrayCompare(PIN, (byte) 0, PIN_ANSWER, (byte) 0, (short) PIN_ANSWER.length);

        byte[] res = { valid_pin };

        Util.arrayCopy(res, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) 1);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) 1);
    }

    public static void disconnectPIN(APDU apdu, byte[] buf) {
        for (short i = 0; i < PIN_ANSWER.length; i++) {
            PIN_ANSWER[i] = 0x00;
        }

        connectPIN(apdu, buf);
    }

    public static void changePIN(APDU apdu, byte[] buf) {
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
}
