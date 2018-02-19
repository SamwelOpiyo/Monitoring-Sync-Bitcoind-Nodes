# -*- coding: utf-8 -*-

import os

from influxdb import InfluxDBClient

import logging
logger = logging.getLogger('Influx Database')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('logs/influxdb.log')
fh.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - \
                               %(name)s - \
                               %(levelname)s - \
                               %(message)s')

fh.setFormatter(formatter)

# add the handlers to logger
logger.addHandler(fh)


def connect_db(dbname, host='localhost', port=8086):
    user = 'root'
    password = 'root'
    client = InfluxDBClient(host, port, user, password, dbname)
    logger.debug("Connection Successfully.")
    return client


def create_db(db_instance, dbname):
    db_instance.create_database(dbname)
    logger.debug("Database created Successfully.")
    return


def drop_db(db_instance, dbname):
    db_instance.drop_database(dbname)
    logger.debug("Database dropped Successfully.")
    return


def add_data(db_instance, dbname, data):
    db_instance.write_points(data)
    logger.debug("Data added Successfully.")
    return


def query_data(db_instance, dbname, search_string):
    db_instance.query(search_string)
    return


def db_main(**kwargs):
    try:
        db_host = kwargs.get('INFLUXDB_HOST', os.environ["INFLUXDB_HOST"])
        db_port = kwargs.get('PORT', os.environ["PORT"])
        db_name = kwargs.get('DATABASE_NAME', os.environ["DATABASE_NAME"])

    except KeyError:
        db_host = 'localhost'
        db_port = 8086
        db_name = "default"

    new_connection = connect_db(db_name, db_host, db_port)
    create_db(new_connection, db_name)
    logger.debug("Database " + db_name + " created.")
    return


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    db_main()
