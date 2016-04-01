########
Practice
########

**************************************
Running a bitcoin node in regtest mode
**************************************

.. code-block:: bash

    bitcoind -regtest

Bitcoin clients: bitcoin-cli & json rpc
=======================================

json rpc ref: https://en.bitcoin.it/wiki/API_reference_%28JSON-RPC%29

* via curl
* via python with python-bitcoinrpc
* via python with requests
* via transactions

curl
----

.. code-block:: bash

    $ curl --user user --data-binary  \
        '{"jsonrpc": "1.0", "id":"dummy", "method": "getinfo", "params": [] }'  \
        -H 'content-type: text/plain;' http://127.0.0.1:18332/


bitcoin json rpc revisited with docker
======================================
We can repeat the same as in the previous section, but this time with some
parts, and everything dockerized.

We add the twist that:

1. the bitcoin server is running in a container, meanwhile client calls are
   made from the docker host
2. the bitcoin server and client are running in separate containers

For 1. and 2. we connect to the bitcoin node:

* via curl
* via python with python-bitcoinrpc
* via python with requests
* via transactions


host - container
----------------
Running bitcoind in container and making rpc calls to it from the host machine,
(sender_ip)

given the following ``bitcoin.conf``:

.. code-block:: bash

    dnsseed=0
    rpcuser=a
    rpcallowip=<sender_ip>


.. code-block:: bash

    docker run --rm --name btc -v ~/.bitcoin-docker:/root/.bitcoin -p <sender_ip>:58332:18332 btc5 bitcoind -regtest -printtoconsole

.. code-block:: bash

    curl --user a:b --data-binary '{"jsonrpc": "1.0", "id":"", "method": "getinfo", "params": [] }' -H 'content-type: text/plain;' http://<sender_ip>:58332


container-container
-------------------
We can use docker-compose.

In one shell:

.. code-block:: bash

    $ docker-compose run --rm bitcoin


In another shell:

.. code-block:: bash

    $ docker ps

    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                            NAMES
    94787e1325a3        sbellem/bitcoin     "bitcoind -regtest -p"   5 seconds ago       Up 5 seconds        8332-8333/tcp, 18332-18333/tcp   transactions_bitcoin_run_1

Using the ``CONTAINER ID`` or ``NAME``:

.. code-block:: bash

    $ docker exec -it transactions_bitcoin_run_1 bash
    # bitcoin-cli -regtest getinfo

.. code-block:: bash

    root@94787e1325a3:/# curl --user a:b --data-binary \
        '{"jsonrpc": "1.0", "id":"", "method": "getinfo", "params": [] }' \
        -H 'content-type: text/plain;' http://localhost:18332 \
        | python -m json.tool

    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
    Dload  Upload   Total   Spent    Left  Speed
    100   386  100   323  100    63  57483  11211 --:--:-- --:--:-- --:--:-- 64600
    {
        "error": null,
        "id": "",
        "result": {
            "balance": 0.0,
            "blocks": 0,
            "connections": 0,
            "difficulty": 4.656542373906925e-10,
            "errors": "",
            "keypoololdest": 1459269071,
            "keypoolsize": 101,
            "paytxfee": 0.0,
            "protocolversion": 70012,
            "proxy": "",
            "relayfee": 1e-05,
            "testnet": false,
            "timeoffset": 0,
            "version": 120000,
            "walletversion": 60000
        }
    }
