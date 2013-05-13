stratum-mining
==============

Demo implementation of litecoin mining pool using Stratum mining protocol -- forked from Slush0
http://github.com/slush0/stratum-mining

Thanks go out to him for creating his version of the Stratum mining protocol and sample files that we
have been able to work through and adapt for litecoin mining.

For Stratum mining protocol specification, please visit http://mining.bitcoin.cz/stratum-mining.

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
