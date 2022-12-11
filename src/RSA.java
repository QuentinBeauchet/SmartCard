package src;

import javacard.framework.APDU;
import javacard.framework.Util;
import javacard.framework.ISO7816;

import javacard.security.KeyPair;
import javacard.security.KeyBuilder;
import javacard.security.RSAPublicKey;
import javacard.security.Signature;

public class RSA {
    private static KeyPair keyPair;
    private static byte[] signature = new byte[64];

    public static void generateKeyPair() {
        keyPair = new KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_512);
        keyPair.genKeyPair();
    }

    public static void sendPublicKey(APDU apdu, byte[] buf) {
        RSAPublicKey publicKey = (RSAPublicKey) keyPair.getPublic();

        short offset = ISO7816.OFFSET_CDATA;

        short expLen = publicKey.getExponent(buf, (short) (offset + 2));
        offset = Util.setShort(buf, offset, expLen);
        offset += expLen;

        short modLen = publicKey.getModulus(buf, (short) (offset + 2));
        offset = Util.setShort(buf, (short) offset, modLen);
        offset += modLen;

        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (short) (offset - ISO7816.OFFSET_CDATA));
    }

    public static void signMessage(APDU apdu, byte[] buf) {
        short bytesRead = apdu.setIncomingAndReceive();
        short answerOffset = (short) 0;
        byte[] message = new byte[127];

        while (bytesRead > 0) {
            Util.arrayCopy(buf, ISO7816.OFFSET_CDATA, message, answerOffset, bytesRead);
            answerOffset += bytesRead;
            bytesRead = apdu.receiveBytes(ISO7816.OFFSET_CDATA);
        }

        Signature privSign = Signature.getInstance(Signature.ALG_RSA_SHA_PKCS1, false);
        privSign.init(keyPair.getPrivate(), Signature.MODE_SIGN);
        short len = privSign.sign(message, (short) 0, (short) message.length, signature, (short) 0);

        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) len);
    }

    public static void sendSignature(APDU apdu, byte[] buf) {
        Util.arrayCopy(signature, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) signature.length);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) signature.length);
    }
}