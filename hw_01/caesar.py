def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    shift = 3
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


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    return plaintext
