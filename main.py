import os

from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from Influxdb.Db import connect_db, create_db, drop_db, add_data, query_data

from BitcoinRPC.Values import get_text, dictify, get_height, get_diff, get_latest_block

import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

logger = logging.getLogger('Monitoring Sync Bitcoind Nodes Program')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs/main.log')
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(fh)

def rpc_main(**kwargs):
    try:
        rpc_host = kwargs.get('RPC_HOST', os.environ["RPC_HOST"])
        rpc_port = kwargs.get('RPC_PORT', os.environ["RPC_PORT"])
        rpc_user = kwargs.get('RPC_USER', os.environ["RPC_USER"])
        rpc_password = kwargs.get('RPC_PASSWORD', os.environ["RPC_PASSWORD"])
        db_host = kwargs.get('INFLUXDB_HOST', os.environ["INFLUXDB_HOST"])
        db_port = kwargs.get('PORT', os.environ["PORT"])
        db_name = kwargs.get('DATABASE_NAME', os.environ["DATABASE_NAME"])
        
    except KeyError:
        rpc_host = "127.0.0.1"
        rpc_port = 8332
        rpc_user = None
        rpc_password = None
        db_name = "default"
        db_host = 'localhost'
        db_port = 8086

    new_connection = connect_db(db_name, db_host, db_port)
    create_db(new_connection, db_name)

    data = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "Block Count": "Bitcoin RPC",
                "Bitcoin block number": "https://blockchain.info/latestblock"
            },
            "time": str(datetime.now()),
            "fields": {}
        }
    ]

    text_ = get_text("https://blockchain.info/latestblock")
    dict_ = dictify(text_) 
    data[0]["fields"]["Bitcoin block number"] = get_height(dict_)

    data[0]["fields"]["Block Count"] = get_latest_block(rpc_host,
                                                        rpc_port,
                                                        rpc_user,
                                                        rpc_password)

    data[0]["fields"]["Difference"] = get_diff(data[0]["fields"]["Bitcoin block number"],
                                                    data[0]["fields"]["Block Count"])

    try:
        add_data(new_connection, db_name, data)
        logger.debug(data)
    except Exception as err:
        logger.critical(err)
        quit()
    return data      



if __name__ == '__main__':
    # execute only if run as the entry point into the program
    try:
        call_timeout = int(os.environ["CALL_TIMEOUT"])
    except KeyError:
        call_timeout = 600

    sched = BlockingScheduler()
    # Schedule job_function to be called every set time
    sched.add_job(rpc_main, 'interval', seconds=call_timeout)

    sched.start()
