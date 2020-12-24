import sys
import selectors
import json
import io
import struct
import socket

request_search = {
    "morpheus": "Follow the white rabbit. \U0001f430",
    "ring": "In the caves beneath the Misty Mountains. \U0001f48d",
    "\U0001f436": "\U0001f43e Playing ball! \U0001f3d0",
}


class Message:
    def __init__(self, selector, sock, addr, connection_list,sockets):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._forward_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False
        self.connection_list = connection_list
        self.sockets = sockets

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {repr(mode)}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            print("sending", repr(self._send_buffer), "to", self.addr)
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.


                    #self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self._write()

    def read(self):
        self._read()
        self.process_request()

    def close(self):
        print("closing connection to", self.addr)
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"error: selector.unregister() exception for",
                f"{self.addr}: {repr(e)}",
            )

        try:
            self.sock.close()
            self.connection_list.remove(self.addr)
            self.sockets.remove(self.sock)
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def informclient(self,content):
        for i in range(0,len(self.connection_list)):
            if list(self.connection_list[i]) == content.get("from"):
                self.sockets[i].send(self._json_encode([{"list":self.addr,"name":content.get("value"),"size":content.get("size")},{"done":"1"}],"utf-8"))
                break


    def forward_request(self,message):
        content = self._json_decode(message,"utf-8")
        if content.get("action","0") == "0" and content.get("alive","0") == "0":
            self.informclient(content)
            return

        content["from"] = self.addr
        message = self._json_encode(content,"utf-8")
        temp = []
        sent = []
        for j in range(0,len(self.sockets)):
            temp.append(message)
            sent.append(0)
        for i in range(0,len(self.sockets)):
            if temp[i] and not self.sockets[i] == self.sock:
                print("forwarding request ", repr(temp[i]), "to", self.connection_list[i])
                try:
                    # Should be ready to write
                    sent[i] = self.sockets[i].send(temp[i])
                except BlockingIOError:
                    # Resource temporarily unavailable (errno EWOULDBLOCK)
                    pass
                else:
                    temp[i] = temp[i][sent[i]:]
                    # Close when the buffer is drained. The response has been sent.
                    if self.check_if_done(temp,sent):
                        self._forward_buffer = b""
                        print("Done forwarding to all peers")

                        #self.close()
    def check_if_done(self,temp,sent):
        count = 0
        for i in range(0,len(temp)):
            if sent[i] and not temp[i]:
                count =count +1
        if count == len(temp):
            return True
    #def send_response(self):

    def process_request(self):
        data = self._recv_buffer
        #print("Message rec",data)
        self._set_selector_events_mask("rw")
        self.forward_request(data)
        self._recv_buffer= b""
