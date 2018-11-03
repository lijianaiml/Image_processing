#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#

import threading
import socketserver
import json
import time

import pore_detection_server as pore_detection
from logutils import logger


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        # 返回客户端连接成功消息
        msg = {"result": "ready"}
        jmsg = json.dumps(msg)
        self.request.sendall(jmsg.encode())

    def handle(self):
        #
        data = self.request.recv(1024).decode()
        if data:
            jdata = json.loads(data)
            # print("Receive data from '%r'" % (data))
            logger.info("Receive data : '%r'" % (data))
            image_path = jdata['image']
            # imageT_path = jdata['imageT']
            imageT_path = image_path
            dic_json = pore_detection.detect(image_path, imageT_path)

            # jresp = json.dumps(response)
            self.request.sendall(dic_json.encode())
            logger.info('Send data :%s', dic_json)
            # rec_cmd = "proccess " + dic + " -o " + dic
            # print("CMD '%r'" % (rec_cmd))
            # os.system(rec_cmd)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "0.0.0.0", 50001

    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.allow_reuse_address = True

    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    # print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    logger.info("Server loop running in thread: %s" % (server_thread.name))

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
