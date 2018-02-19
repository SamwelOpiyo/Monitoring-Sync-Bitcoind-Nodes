# Monitoring-Sync-Bitcoind-Nodes

Monitoring Latest Block and the difference between Bitcoin Block Number and LatestBlock

## Installing Dependencies

### Bitcoin Core

Download bitcoin core binaries

`wget https://bitcoin.org/bin/bitcoin-core-0.16.0/test.rc3/bitcoin-0.16.0rc3-x86_64-linux-gnu.tar.gz`

Extract bitcoin core

`tar xzf bitcoin-0.16.0rc3-x86_64-linux-gnu.tar.gz`

Install bitcoin core

`sudo install -m 0755 -o root -g root -t /usr/local/bin bitcoin-0.16.0/bin/*`

Start bitcoin core

`bitcoind -daemon`

### Influxdb

Download InfluxDB

`wget https://dl.influxdata.com/influxdb/releases/influxdb_1.4.0_amd64.deb`

Install InfluxDB

`sudo dpkg -i influxdb_1.4.0_amd64.deb`

Start InfluxDB

`sudo systemctl start influxdb`

Verify that InfluxDB is Running

Using the SHOW DATABASES curl command, verify that InfluxDB is up and running:

`curl "http://localhost:8086/query?q=show+databases"`

If InfluxDB is running, you should see an object that contains the _internal database:

`{"results":[{"statement_id":0,"series":[{"name":"databases","columns":["name"],"values":[["_internal"]]}]}]}`


### Python Dependencies

- Install requirements: Run `pip install -r requirements.txt` on the working directory (you almost certainly want to do this in a virtualenv).

## Running the Program

From the working directory, run `python main.py`
