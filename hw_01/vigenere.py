def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    bigAlphabetStart = ord('A')
    bigAlphabetEnd = ord('Z')
    smallAlphabetStart = ord('a')
    smallAlphabetEnd = ord('z')
    ciphertext = ""

    for i in range(len(plaintext)):
        letterCode = ord(plaintext[i])
        if bigAlphabetStart <= letterCode <= bigAlphabetEnd:
            codesRange = [bigAlphabetStart, bigAlphabetEnd]
        elif smallAlphabetStart <= letterCode <= smallAlphabetEnd:
            codesRange = [smallAlphabetStart, smallAlphabetEnd]
        else:
            ciphertext += plaintext[i]
            continue

        keyLetterCode = ord(keyword[i % len(keyword)])
        if bigAlphabetStart <= keyLetterCode <= bigAlphabetEnd:
            shift = keyLetterCode - bigAlphabetStart
        elif smallAlphabetStart <= keyLetterCode <= smallAlphabetEnd:
            shift = keyLetterCode - smallAlphabetStart
        else:
            shift = 0

        newLetterCode = letterCode + shift
        if newLetterCode > codesRange[1]:
            newLetterCode = codesRange[0] + (newLetterCode - codesRange[1] - 1)

        ciphertext += chr(newLetterCode)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    return plaintext
