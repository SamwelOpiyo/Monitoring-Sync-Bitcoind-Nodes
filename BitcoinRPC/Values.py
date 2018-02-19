import requests

import json

from socket import error as socket_error

import subprocess

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

logger = logging.getLogger('BitcoinRPC and Blockchain.info get Values')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs/bitcoinrpc.log')
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(fh)


def get_text(url):
    text = requests.get(url).text
    logger.debug("Scrapped: " + url)
    return text


def dictify(json_text):
    dict_ = json.loads(json_text)
    logger.debug("Json converted successfully to Python Dict")
    return dict_


def get_height(latestblock):
    height_ = latestblock["height"]
    logger.debug("Height for latestblock-\
                 " + str(latestblock["block_index"]) + ": " + str(height_))
    return height_


def get_diff(height, latest_block):
    diff = height-latest_block
    logger.debug("Difference between Height and Latest Block: " + str(diff))
    return diff


def get_latest_block(host, port, user, password):
    try:
        rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s" % (user,
                                                                  password,
                                                                  host,
                                                                  port))
        block_count = rpc_connection.getblockcount()
        logger.debug("Block Count: " + block_count)
        return block_count
    except socket_error:
        logger.critical("Connection Refused!! \
                         Confirm the status of bitcoin RPC service.")
        quit()
    except JSONRPCException:
        try:
            p = subprocess.Popen(["bitcoin-cli", "getblockcount"],
                                 stdout=subprocess.PIPE)
            output, err = p.communicate()
            block_count = int(output)
            logger.debug("Block Count: " + str(block_count))
            return block_count

        except Exception as err:
            logger.critical(err)
            quit()
