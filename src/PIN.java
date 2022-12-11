package src;

import javacard.framework.ISO7816;
import javacard.framework.ISOException;
import javacard.framework.APDU;
import javacard.framework.Util;

public class PIN {
    private final static byte[] PIN = { 0x73, 0x65, 0x63, 0x72, 0x65, 0x74 };
    private final static byte[] PIN_ANSWER = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };

    public static void isConnectedWithPIN() {
        if (Util.arrayCompare(PIN, (byte) 0, PIN_ANSWER, (byte) 0, (short) PIN_ANSWER.length) != 0x00) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
    }

    public static void connectPIN(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN_ANSWER, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        isConnectedWithPIN();
    }

    public static void disconnectPIN() {
        resetPIN();
        isConnectedWithPIN();
    }

    public static void changePIN(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, PIN, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        resetPIN();
        ISOException.throwIt((short) 0x6983);
    }

    public static void resetPIN() {
        for (short i = 0; i < PIN_ANSWER.length; i++) {
            PIN_ANSWER[i] = 0x00;
        }
    }
}
