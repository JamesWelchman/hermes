"""
session implements hermes chat protocol.
"""

from threading import Condition

from .session2 import new_session


__all__ = ['start_session']


def start_session(host, config):
    """
    start_session will begin a session with another party.
    Args:
        - host: a (ip, port) tuple
        - config: The hermes config dict
    Returns:
        - (inputQ, outputQ, errorQ)

    This function will block until a connection is established
    or raise an exception if we fail for some reason.

    inputQ:
        - the user may write bytes objects or None to the
          inputQ. If None is written then the connection is closed.
    outputQ:
        - the user may receive bytes objects or None on the
          outputQ. If None is received then the other party
          closed the connection.
    errorQ:
        - the user may receive exceptions on the errorQ.
          NOTE: This does not nessercarily mean the connection
          is over. The outputQ is used for this purpose.
    """
    cond = Condition()
    (inq, outq, errq) = new_session(host, config, cond=cond)

    # Wait for the server to be connected + ready
    with cond:
        cond.wait()

    if not errq.is_empty():
        raise errq.get()

    return (inq, outq, errq)
