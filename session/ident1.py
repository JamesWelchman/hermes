

from .udp0 import get_udp_socket


class IdentSession:
    """
    IdentSession is responsible for proving user identity
    and proving the payloads don't get tampered with.

    We use sha512 hashing and an RSA private key to prove
    non-tampered. We use a chameleon hash based schema for
    to prove we own a given user_id.

    We implement a key exchange to get the other users RSA public
    key along with their user_id.

    We furthermore implement sequence numbers, retry logic
    and segmenting large message over different UDP packets.
    """

    def __init__(self, host, config):
        # A raw UDP socket. Hole punching
        # has completed succesfully.
        self._sock = get_udp_socket(host)
