import logging.handlers
import socketserver
import struct
import logging
import pickle

class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            chunk=self.connection.recv(4)
            if len(chunk)<4:
                break
            slen=struct.unpack(">L",chunk)[0]
            chunk=self.connection.recv(slen)
            while len(chunk)<slen:
                chunk=chunk+self.connection.recv(slen-len(chunk))
            obj=self.unPickle(chunk)
            record=logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle(self,data):
        return pickle.loads(data)

    def handleLogRecord(self,record):
        if self.server.logname is not None:
            name=self.server.logname
        else:
            name=record.name
        logger=logging.getLogger(name)
        logger.handle(record)

class LogRecordSocketReceiver(socketserver.ThreadingTCPServer):
    allow_reuse_address=True
    def __init__(self,host="localhost",port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,handler=LogRecordStreamHandler):
        socketserver.ThreadingTCPServer.__init__(self,(host,port),handler)
        self.abort=0
        self.timeout=1
        self.logname=None
        
    def serve_until_stopped(self):
        import select
        abort=0
        while not abort:
            rd,wr,ex=select.select([self.socket.fileno()],[],[],self.timeout)
            if rd:
                self.handle_request()
            abort=self.abort

def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(name)s [%(funcName)s(%(module)s:%(lineno)s)] %(message)s'

    )
    tcpserver=LogRecordSocketReceiver()
    print("about to starp tcp server.......")
    tcpserver.serve_until_stopped()

if __name__=="__main__":
    main()

