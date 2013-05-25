stratum-mining
==============

<<<<<<< HEAD
Demo implementation of litecoin mining pool using Stratum mining protocol -- forked from Slush0
http://github.com/slush0/stratum-mining

Thanks go out to him for creating his version of the Stratum mining protocol and sample files that we
have been able to work through and adapt for litecoin mining.
=======
Basic implementation of bitcoin mining pool using Stratum mining protocol.
>>>>>>> 567b38a0d8172d04e3f73b4d3b37703115129bb2

This fork includes database optimisations for MySQL and password hashing using a salt.

<<<<<<< HEAD
This fork is still a work in progress - once complete, full details will be posted and a link will be shared.

If you wish to help improve/debug this, please feel free to contact me at the address below.


This fork should support all scrypt based coins including litecoin and feathercoin.

Install Instructions:
-------
sudo apt-get install python-twisted

sudo easy_install -U distribute

sudo easy_install stratum

sudo pip install python-memcached

git clone https://github.com/Tydus/litecoin_scrypt.git

cd litecoin_scrypt

sudo python setup.py install

Now rename the example config file (conf/config_sample.py) to config.py and make any changes as required.

Run with the following command:

twistd -ny launcher_demo.tac

Contact:
-------
This pool implementation is provided by http://www.viperausmedia.com.au. You can contact
me by email info(at)viperausmedia.com.au.

Donations:
----------
BTC - 1CWmoy4xTSXV8NmiFtz2aCHWfy1ikzaBTM

LTC - LVWjBYNgj9MFPMhm5bMq3tjRCKiKVzMeL1
=======
JSON API
--------

There is also a JSON API, currently just for users (db: pool_workers). Enabled if you set 
ADMIN_PORT to a valid port rather than None. Once enabled, you can perform 
the following on http://localhost:ADMIN_PORT/, provided you have a password set (see after commands).

GET /users - list all users
POST /users - create a user (JSON body: {"username": "username", "password": "password"}). Password will be encrypted using the salt.
                
GET /users/{id_or_username} - Get a JSON object of a specific user
DELETE /users/{id_or_username} - Remove a pool_worker. If using MySQL, any shares associated with that user will be associated with the global system account (ID: 0)
PUT /users/{id_or_username} - Update password for user, send as {"password": "password"}, as with POST /users, the password will be encrypted for you.

### Authentication

Access to the JSON API requires basic auth. The username does not matter; the password is the same as the ADMIN_PASSWORD_SHA256 password which 
can generated using scripts/generateAdminHash.sh .

I would strongly suggested locking down the port as well using iptables or similar.

The Rest
--------

Basic worker stats are provided (and updated)

See the INSTALL file for install instructions.

For more info on Stratum:
http://mining.bitcoin.cz/stratum-mining.

Original version by Slush
Modified version by GeneralFault

This version by Wade Womersley (Media Skunk Works) ( Tips Welcome: 1FxBTbWR15WZp8vnru8N6zVsVBwigPAcdN )
>>>>>>> 567b38a0d8172d04e3f73b4d3b37703115129bb2
