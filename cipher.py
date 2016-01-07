from __future__ import print_function
import random
from optparse import OptionParser

import optparse


def encrypt(k, verbose):
    plaintext = raw_input('Enter plain text message: ')
    cipher = ''
    for each in plaintext:
        c = (ord(each) + k) % 126
        if c < 32:
            c += 31
        if verbose:
            print("char is: %s ordchar %s Cchar %s ordCchar %s" % (each, ord(each), c, chr(c)))
        cipher += chr(c)

    print('Your encrypted message is: ' + cipher)


def decrypt(k, verbose):
    cipher = raw_input('Enter encrypted message: ')
    plaintext = ''
    for each in cipher:
        p = (ord(each) - k) % 126

        if p < 32:
            p += 95
        if verbose:
            print("Cchar is: %s ordCchar %s Plain %s ord_plain %s " % (each, ord(each), p, chr(p)))
        plaintext += chr(p)
        plaintext.encode("utf-8")

    print('Your plain text message is: ' + plaintext)


def gen_key():
    master_key = random.randint(99, 1000)
    while master_key % 126 == 0:
        master_key = random.randint(99, 1000)
    return master_key


def main():
    parser = OptionParser()
    parser = optparse.OptionParser("usage: %prog [options] <string> or -h for help")
    parser.add_option("-d", "--decrypt",
                      action="store_true",
                      dest="cstring",
                      default=False,
                      help="decrypt a previous string cipher with this script")
    parser.add_option("-e", "--encrypt",
                      action="store_true",
                      dest="plain_string",
                      default=False,
                      help="encrypt a previous string cipher with this script")
    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="verbose",
                      default=False,
                      help="more verbose process")

    (options, args) = parser.parse_args()

    if not options.cstring:
        if not options.plain_string:
            if not options.verbose:
                print("invalid number of argument")
            elif options.verbose:
                print("alone verbose options is not valid")

    if options.plain_string:
        master_key = gen_key()
        print("Your Key is: %s" % master_key)
        print("store in a safety place is not recoverable")
        encrypt(master_key, options.verbose)
    if options.cstring:
        key = input("Enter your Key: ")
        decrypt(key,options.verbose)


if __name__ == "__main__":
    main()
