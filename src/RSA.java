package src;

import javacard.framework.APDU;
import javacard.framework.Util;
import javacard.framework.ISO7816;
import javacard.framework.ISOException;

import javacard.security.KeyPair;
import javacard.security.KeyBuilder;
import javacard.security.RSAPrivateKey;
import javacard.security.RSAPublicKey;
import javacard.security.Signature;

import javacardx.crypto.Cipher;

public class RSA {

    private static Cipher cipher;
    private static RSAPublicKey publicKey;
    private static RSAPrivateKey privateKey;
    private static Signature signer;

    private static byte[] signature = new byte[512];
    private static short signature_len = 0;

    public static void generateKeys(APDU apdu, byte[] buf) {
        // Generate a new RSA key pair using KeyBuilder
        KeyPair keyPair = new KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_512);
        keyPair.genKeyPair();

        byte[] buffer = apdu.getBuffer();
        short offset = ISO7816.OFFSET_CDATA;

        publicKey = (RSAPublicKey) keyPair.getPublic();
        privateKey = (RSAPrivateKey) keyPair.getPrivate();

        signer = Signature.getInstance(Signature.ALG_RSA_SHA_PKCS1, false);

        signer.init(privateKey, Signature.MODE_SIGN);

        short expLen = publicKey.getExponent(buffer, (short) (offset + 2));
        Util.setShort(buffer, offset, expLen);
        short modLen = publicKey.getModulus(buffer, (short) (offset + 4 + expLen));
        Util.setShort(buffer, (short) (offset + 2 + expLen), modLen);
        apdu.setOutgoingAndSend(offset, (short) (4 + expLen + modLen));
    }

    public static void signMessage(APDU apdu, byte[] buf) {

        short bytesRead = apdu.setIncomingAndReceive();
        signature_len = signer.sign(buf, ISO7816.OFFSET_CDATA, bytesRead, signature, (short) 0);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) signature_len);
    }

    public static void getSignature(APDU apdu, byte[] buf) {
        Util.arrayCopy(signature, (byte) 0, buf, ISO7816.OFFSET_CDATA, (byte) signature_len);
        apdu.setOutgoingAndSend(ISO7816.OFFSET_CDATA, (byte) signature_len);
    }
}
