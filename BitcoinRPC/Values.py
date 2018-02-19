import requests

import json

from socket import error as socket_error

import subprocess

from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

import logging

# Logging Settings
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


# Use requests module to read text from webpage
def get_text(url):
    text = requests.get(url).text
    logger.debug("Scrapped: " + url)
    return text


# Change Json text to python dictionary
def dictify(json_text):
    dict_ = json.loads(json_text)
    logger.debug("Json converted successfully to Python Dict")
    return dict_


# Get dict item with key height
def get_height(latestblock):
    height_ = latestblock["height"]
    logger.debug("Height for latestblock-\
                 " + str(latestblock["block_index"]) + ": " + str(height_))
    return height_


# Find the difference between two items
def get_diff(height, latest_block):
    diff = height-latest_block
    logger.debug("Difference between Height and Latest Block: " + str(diff))
    return diff


# Get block count from bitcoin rpc
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
            # Use subprocess library to run bash command to get block count
            p = subprocess.Popen(["bitcoin-cli", "getblockcount"],
                                 stdout=subprocess.PIPE)
            output, err = p.communicate()
            block_count = int(output)
            logger.debug("Block Count: " + str(block_count))
            return block_count

        except Exception as err:
            logger.critical(err)
            quit()
