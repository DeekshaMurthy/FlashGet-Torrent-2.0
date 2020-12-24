import sys
import selectors
import json
import io
import struct
import subprocess
from subprocess import Popen, PIPE
import socket


class Message:
    def __init__(self, selector, sock, addr, request):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None
        self.start = 0

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
            data = self.sock.recv(40960)
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
            #print(self._recv_buffer)
            self.read()
        if mask & selectors.EVENT_WRITE:
            #print(self._recv_buffer)
            self.write()


    def read(self):
        self._read()
        #print(self._recv_buffer,"plzzz")
        self.process_response()

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                self._set_selector_events_mask("r")

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
        except OSError as e:
            print(
                f"error: socket.close() exception for",
                f"{self.addr}: {repr(e)}",
            )
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def queue_request(self):
        #message = b'"{str(self.request.get(value))}"'

        message = self._json_encode(self.request, "utf-8")
        self._send_buffer += message
        self._request_queued = True

    def informserver(self,addr,output):


        for i in output:
            print("informing server", repr(i.split("\t")))
            if len(i.split("\t")) > 1:
                name = i.split("\t")[1]
                size = i.split("\t")[0]
                address = self._json_encode({"size" :size,"value":name[2:],"from":addr},"utf-8")
                try:
                    sent = self.sock.send(address)

                except BlockingIOError:
                    # Resource temporarily unavailable (errno EWOULDBLOCK)
                    pass


    def process_response(self):
        print ("Recieved RAW  data\n",self._recv_buffer)
        content1 = self._json_decode(self._recv_buffer,"utf-8")
        print ("Recieved data\n",repr(content1))
        if len(content1)>1 and type(content1)== list:
            content = content1[0]
        else :
            content = content1
        if content.get("action") == "search":
            arg = content.get("value")
            p = Popen(['./script.sh', str(arg)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate()
            rc = p.returncode
            #val = subprocess.check_call("./script.sh '%s'" % arg,   shell=True)
            #(output,err) = val.communicate()
            print("\nSearch request output: ",output.decode(),type(output))
            if not output.decode() == "0":
                self.informserver(content.get("from"),output.decode().split("\n"))
            self._recv_buffer=b""
        elif not content.get("list",0) == 0:
            f=open("IP_list.txt", "a+")
            f.write(str(content.get("list")[0])+"\t"+str(content.get("name"))+"\t"+str(content.get("size")))
            f.write("\n")
            f.close()
            self._recv_buffer=b""
