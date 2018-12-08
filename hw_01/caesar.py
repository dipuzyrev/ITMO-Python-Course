def encrypt_caesar(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON", 2)
    'RAVJQP'
    >>> encrypt_caesar("python", 2)
    'ravjqp'
    >>> encrypt_caesar("Python3.6", 2)
    'Ravjqp3.6'
    >>> encrypt_caesar("", 2)
    ''
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

        newLetterCode = letterCode + shift
        if newLetterCode > codesRange[1]:
            newLetterCode = codesRange[0] + (newLetterCode - codesRange[1] - 1)

        ciphertext += chr(newLetterCode)
    return ciphertext


def decrypt_caesar(ciphertext, shift):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("RAVJQP", 2)
    'PYTHON'
    >>> decrypt_caesar("ravjqp", 2)
    'python'
    >>> decrypt_caesar("Ravjqp3.6", 2)
    'Python3.6'
    >>> decrypt_caesar("", 2)
    ''
    """
    bigAlphabetStart = ord('A')
    bigAlphabetEnd = ord('Z')
    smallAlphabetStart = ord('a')
    smallAlphabetEnd = ord('z')
    plaintext = ""

    for i in range(len(ciphertext)):
        letterCode = ord(ciphertext[i])
        if bigAlphabetStart <= letterCode <= bigAlphabetEnd:
            codesRange = [bigAlphabetStart, bigAlphabetEnd]
        elif smallAlphabetStart <= letterCode <= smallAlphabetEnd:
            codesRange = [smallAlphabetStart, smallAlphabetEnd]
        else:
            plaintext += ciphertext[i]
            continue

        newLetterCode = letterCode - shift
        if newLetterCode < codesRange[0]:
            newLetterCode = codesRange[1] - (codesRange[0] - newLetterCode - 1)

        plaintext += chr(newLetterCode)
    return plaintext
