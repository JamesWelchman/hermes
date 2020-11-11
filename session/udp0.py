from socket import socket, AF_INET, SOCK_DGRAM


def get_udp_socket(host):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.connect(host)

    # TODO: UDP hole punch
    return sock
