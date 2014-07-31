from socket import ( socket, AF_INET, SOCK_DGRAM,
                     IPPROTO_TCP, SOCK_STREAM,
                     SOL_SOCKET, SO_REUSEADDR)
from ssl import wrap_socket, CERT_NONE

TCP_DEFAULT_FRAME_SIZE = 1200

class Transport(object):
    def __init__(self, hostname, port):
        self.addr = (hostname, port)
        self.__connection = None

    def connect(self):
        raise Exception("Not Implemented Error")
        
    def close(self):
        raise Exception("Not Implemented Error")
    
        
class UDPTransport(Transport):
    def __init__(self, hostname, port):
        super(UDPTransport, self).__init__(hostname, port)
        self.__connection = socket(AF_INET, SOCK_DGRAM)

    def connect(self):
        self.__connection.connect(self.addr)
        
    def send(self, message):
        self.__connection.sendto(message, self.addr)

    def recv(self):
        return self.__connection.recv(4096)

    def close(self):
        self.__connection.close()
    
class TCPTransport(Transport):
    def __init__(self, hostname, port):
        super(TCPTransport, self).__init__(hostname, port)
        self.__connection = socket(AF_INET, SOCK_STREAM)
        self.__connection.setsockopt(SOL_SOCKET,
                                     SO_REUSEADDR,
                                     1)        
    def connect(self):
        self.__connection.connect(self.addr)
        
    def send(self, message):
        self.__connection.sendto(message, self.addr)

    def recv(self, frame_size=TCP_DEFAULT_FRAME_SIZE):
        return self.__connection.recv(frame_size)
    
    def close(self):
        self.__connection.close()


class TLS_TCPTransport(TCPTransport):
    #TODO: This should just be a wrapper 
    def __init__(self, hostname, port, timeout=10):
        super(TLS_TCPTransport, self).__init__(hostname, port)
        #TODO: Should do a better build up of ssl_socket
        self.__connection = wrap_socket(socket(AF_INET, SOCK_STREAM),
                                        cert_reqs=CERT_NONE,
                                        do_handshake_on_connect=False)
        self.__connection.setsockopt(SOL_SOCKET,
                                     SO_REUSEADDR,
                                     1)
        self.__connection.settimeout(timeout)
        
    def connect(self):
        try:
            self.__connection.connect(self.addr)
        finally:
            pass
        
    def send(self, message):
        self.__connection.write(message)

    def recv(self, n_of_bytes=TCP_DEFAULT_FRAME_SIZE):
        return self.__connection.read(n_of_bytes)

    def recv_all(self):
        data = self.recv(n_of_bytes=1000)
        while data:
            print "receiving", data
            recv_buffer = data
            data = self.recv(n_of_bytes=1000)
        return recv_buffer
    
    def close(self):
        self.__connection.close()




