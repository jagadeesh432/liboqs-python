"""
Open Quantum Safe (OQS) Python Wrapper for liboqs

The liboqs project provides post-quantum public key cryptography algorithms:
https://github.com/open-quantum-safe/liboqs

This module provides a Python 3 interface to libOQS <oqs/rand.h> RNGs.
"""

import oqs


def randombytes(bytes_to_read):
    """
    Generates random bytes. This implementation uses either the default RNG algorithm ("system"), or whichever
    algorithm has been selected by random_bytes_switch_algorithm().

    :param bytes_to_read: the number of random bytes to generate.
    :return: random bytes.
    """
    result = oqs.ct.create_string_buffer(bytes_to_read)
    oqs.liboqs.OQS_randombytes(result, oqs.ct.c_int(bytes_to_read))
    return bytes(result)


def randombytes_switch_algorithm(alg_name):
    """
    Switches the core OQS_randombytes to use the specified algorithm. See <oqs/rand.h> liboqs headers for more details.

    :param alg_name: algorithm name, possible values are "system", "NIST-KAT", "OpenSSL".
    """
    if oqs.liboqs.OQS_randombytes_switch_algorithm(oqs.ct.create_string_buffer(alg_name.encode())) != oqs.OQS_SUCCESS:
        raise RuntimeError('Can not switch algorithm')


def randombytes_nist_kat_init(entropy_input, personalization_string=None):
    """
    Initializes the NIST DRBG with the an entropy seed.

    :param entropy_input: entropy input seed, must be exactly 48 bytes long.
    :param personalization_string: optional personalization string, which, if present, must be at least 48 bytes long.
    """
    if len(entropy_input) != 48:
        raise ValueError('The entropy source must be exactly 48 bytes long')

    if personalization_string is not None:
        if len(personalization_string) < 48:
            raise ValueError('The personalization string must be either empty or at least 48 bytes long')
        oqs.liboqs.OQS_randombytes_nist_kat_init(oqs.ct.create_string_buffer(entropy_input),
                                                 oqs.ct.create_string_buffer(personalization_string), 256)

    oqs.liboqs.OQS_randombytes_nist_kat_init(oqs.ct.create_string_buffer(entropy_input), 0, 256)

# def randombytes_in_place(random_array, bytes_to_read):
#     raise NotImplementedError

# def randombytes_custom_algorithm(fun):
#     raise NotImplementedError
