
from queue import Queue
from threading import Thread, Condition
from os import urandom

from .ident1 import IdentSession


def new_session(host, config, cond=None):
    cond = cond or Condition

    (inq, outq, errq) = (Queue(), Queue(), Queue())

    thread = Thread(target=Session,
                    args=(cond, host, config, inq, outq, errq))
    thread.run()

    return (inq, outq, errq)


class Session:
    """
    Our Session layer is responsible for.
        - Diffie-Helman key exchange
        - Ratchet functions / msg encyrption
        - Heartbeats

    We don't know anything about msg contents.
    The inq and outq are just _bytes_ which we
    encrypt and send via the ident1 layer.
    """

    def __init__(self, cond, host, config, inq, outq, errq):
        self._config = config
        self._inq = inq
        self._outq = outq
        self._errq = errq

        self._session_id = urandom(16).hex()

        # NOTE: We never return from this function
        # as long as the connection is alive.

        # Create an IdentSession
        # self._ident_session = IdentSession(host, config)

        # Wake up the caller
        with cond:
            cond.notify()

        while True:
            # run session forever (or until None is received,
            # on the inputQ)
            from time import sleep
            sleep(1)
