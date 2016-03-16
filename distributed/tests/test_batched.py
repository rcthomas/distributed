
import pytest
from tornado import gen
from tornado.tcpserver import TCPServer
from tornado.tcpclient import TCPClient
from tornado.iostream import StreamClosedError

from distributed.utils_test import gen_test
from distributed.batched import BatchedStream


class MyServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        batched = BatchedStream(stream, interval=10)
        while True:
            msg = yield batched.recv()
            batched.send(msg)
            batched.send(msg)


@gen_test(timeout=10)
def test_BatchedStream():
    port = 3434
    server = MyServer()
    server.listen(port)

    client = TCPClient()
    stream = yield client.connect('127.0.0.1', port)
    b = BatchedStream(stream, interval=20)

    b.send('hello')
    b.send('world')

    result = yield b.recv(); assert result == 'hello'
    result = yield b.recv(); assert result == 'hello'
    result = yield b.recv(); assert result == 'world'
    result = yield b.recv(); assert result == 'world'

    b.close()

@gen_test(timeout=10)
def test_BatchedStream_raises():
    port = 3435
    server = MyServer()
    server.listen(port)

    client = TCPClient()
    stream = yield client.connect('127.0.0.1', port)
    b = BatchedStream(stream, interval=20)

    stream.close()

    with pytest.raises(StreamClosedError):
        yield b.recv()

    with pytest.raises(StreamClosedError):
        yield b.send('123')
