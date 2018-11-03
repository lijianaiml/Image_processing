# -*- coding:utf-8 -*-
import logging


LOG_FORMAT = ("%(asctime)s %(filename)s:%(lineno)d] %(message)s")
logging.basicConfig(filename='pore_detection_server.log',
                    level=logging.DEBUG,
                    format=LOG_FORMAT)

logger = logging.getLogger()
