from socket import ( socket, AF_INET, SOCK_DGRAM,
                     IPPROTO_TCP, SOCK_STREAM,
                     SOL_SOCKET, SO_REUSEADDR)
from ssl import wrap_socket

# From default protocol connection 
class Connection(object):
    def __init__(self, url, port=None):
        self.url = url
        self.port = port
        self.addr = (self.url, self.port)
        self.__connection = None

    def connect(self):
        pass
        
    def close(self):
        pass
    
        
class UDPConnection(Connection):
    def __init__(self, url, port=None):
        super(UDPConnection, self).__init__(url, port)
        self.__connection = socket(AF_INET, SOCK_DGRAM)

    def connect(self):
        self.__connection.connect(self.addr)
        
    def send(self, message):
        self.__connection.sendto(message, self.addr)

    def recv(self):
        return self.__connection.recv(2048)

    def close(self):
        self.__connection.close()
    
class TCPConnection(Connection):
    def __init__(self, url, port=None):
        super(TCPConnection, self).__init__(url, port)
        self.__connection = socket(AF_INET, SOCK_STREAM)
        self.__connection.setsockopt(SOL_SOCKET,
                                     SO_REUSEADDR,
                                     1)        
    def connect(self):
        self.__connection.connect(self.addr)

        
    def send(self, message):
        self.__connection.sendto(message, self.addr)

    def recv(self):
        return self.__connection.recv(2048)

    def close(self):
        self.__connection.close()


class TLS_TCPConnection(TCPConnection):
    def __init__(self, url, port=None):
        super(TLS_TCPConnection, self).__init__(url, port)
        self.__connection = wrap_socket(socket(AF_INET, SOCK_STREAM))
        self.__connection.setsockopt(SOL_SOCKET,
                                     SO_REUSEADDR,
                                     1)        
    def connect(self):
        self.__connection.connect(self.addr)
        
    def send(self, message):
        self.__connection.write(message)

    def recv(self):
        return self.__connection.read()

    def close(self):
        self.__connection.close()




