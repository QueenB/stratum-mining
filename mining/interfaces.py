'''This module contains classes used by pool core to interact with the rest of the pool.
   Default implementation do almost nothing, you probably want to override these classes
   and customize references to interface instances in your launcher.
   (see launcher_demo.tac for an example).
''' 
import MySQLdb as mdb
import sys
import time
from twisted.internet import reactor, defer
from lib.util import b58encode
import MySQLdb.cursors
import stratum.logger
import memcache
from stratum import settings
log = stratum.logger.get_logger('interfaces')

import lib.notify_email

import DBInterface
dbi = DBInterface.DBInterface()
dbi.init_main()

class WorkerManagerInterface(object):
    def __init__(self):
        return
        
    def authorize(self, worker_name, worker_password):
        isauth = False
        mc = memcache.Client([settings.MEMCACHE_HOST], debug=1)
        cachedauth = False
	
        try:
            memkey = "%s-%s" % (str(worker_name), str(worker_password))
            cachedauth = mc.get(memkey)
        except:
            log.info("memcache set exception for %s" % (worker_name))

        if cachedauth == True:
            isauth = True
        else:
            con = mdb.connect(settings.DATABASE_HOST, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_DBNAME);
            cur = con.cursor()
            try:
                numrows = cur.execute("SELECT * FROM pool_worker WHERE username = %s AND password = %s", (worker_name, worker_password))
                if numrows > 0:
                    isauth = True
            except:
                log.info("mysql exception on select for %s" % (worker_name))
            cur.close()
            con.close()

        try:
            memkey = "%s-%s" % (str(worker_name), str(worker_password))
            mc.set(memkey, isauth, settings.MEMC_AUTH_TIMEOUT)
        except:
            log.info("memcache set exception for %s" % (worker_name))

        return isauth
        # Important NOTE: This is called on EVERY submitted share. So you'll need caching!!!
        return dbi.check_password(worker_name, worker_password)


class ShareLimiterInterface(object):
    '''Implement difficulty adjustments here'''
    
    def submit(self, connection_ref, job_id, current_difficulty, timestamp, worker_name):
        '''connection - weak reference to Protocol instance
           current_difficulty - difficulty of the connection
           timestamp - submission time of current share
           
           - raise SubmitException for stop processing this request
           - call mining.set_difficulty on connection to adjust the difficulty'''
        return dbi.update_worker_diff(worker_name, settings.POOL_TARGET)
 
class ShareManagerInterface(object):
    def __init__(self):
        self.block_height = 0
        self.prev_hash = 0
    
        # Send out the e-mail saying we are starting.
        notify_email = lib.notify_email.NOTIFY_EMAIL()
        notify_email.notify_start()

    def on_network_block(self, prevhash, block_height):
        '''Prints when there's new block coming from the network (possibly new round)'''
        self.block_height = block_height        
        self.prev_hash = b58encode(int(prevhash, 16))
        pass
    
    def on_submit_share(self, worker_name, block_header, block_hash, shares, timestamp, is_valid):
        log.info("%s %s %s" % (block_hash, 'valid' if is_valid else 'INVALID', worker_name))
        con = mdb.connect(settings.DATABASE_HOST, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_DBNAME);
        cur = con.cursor()
        try:
            cur.execute("""INSERT INTO shares (username, our_result, rem_host, solution) VALUES ("%s","%s", "", "%s")""" % (worker_name, 'Y' if is_valid else 'N', block_hash))
            con.commit()
        except:
            log.info("mysql exception %s" % (worker_name))
            con.rollback()
        cur.close()
        con.close()
    
    def on_submit_block(self, is_accepted, worker_name, block_header, block_hash, timestamp):
        log.info("Block %s %s" % (block_hash, 'ACCEPTED' if is_accepted else 'REJECTED'))
        con = mdb.connect(settings.DATABASE_HOST, settings.DATABASE_USER, settings.DATABASE_PASSWORD, settings.DATABASE_DBNAME);
        cur = con.cursor()
        try:
            cur.execute("""UPDATE shares SET upstream_result = "%s" WHERE solution = "%s" """ % ('Y' if is_accepted else 'N', block_hash))
            con.commit()
        except:
            con.rollback()
        cur.close()
        con.close()

    def on_submit_share(self, worker_name, block_header, block_hash, difficulty, timestamp, is_valid, ip, invalid_reason, share_diff):
        log.info("%s (%s) %s %s" % (block_hash, share_diff, 'valid' if is_valid else 'INVALID', worker_name))
        dbi.queue_share([worker_name, block_header, block_hash, difficulty, timestamp, is_valid, ip, self.block_height, self.prev_hash,
                invalid_reason, share_diff ])
 
    def on_submit_block(self, is_accepted, worker_name, block_header, block_hash, timestamp, ip, share_diff):
        log.info("Block %s %s" % (block_hash, 'ACCEPTED' if is_accepted else 'REJECTED'))
        dbi.found_block([worker_name, block_header, block_hash, -1, timestamp, is_accepted, ip, self.block_height, self.prev_hash, share_diff ])
        
        # Send out the e-mail saying we found a block.
        if is_accepted:
            notify_email = lib.notify_email.NOTIFY_EMAIL()
            notify_email.notify_found_block(worker_name)
    
class TimestamperInterface(object):
    '''This is the only source for current time in the application.
    Override this for generating unix timestamp in different way.'''
    def time(self):
        return time.time()

class PredictableTimestamperInterface(TimestamperInterface):
    '''Predictable timestamper may be useful for unit testing.'''
    start_time = 1345678900  # Some day in year 2012
    delta = 0
    
    def time(self):
        self.delta += 1
        return self.start_time + self.delta

class Interfaces(object):
    worker_manager = None
    share_manager = None
    share_limiter = None
    timestamper = None
    template_registry = None
    
    @classmethod
    def set_worker_manager(cls, manager):
        cls.worker_manager = manager    
    
    @classmethod        
    def set_share_manager(cls, manager):
        cls.share_manager = manager

    @classmethod        
    def set_share_limiter(cls, limiter):
        cls.share_limiter = limiter
    
    @classmethod
    def set_timestamper(cls, manager):
        cls.timestamper = manager
        
    @classmethod
    def set_template_registry(cls, registry):
        dbi.set_bitcoinrpc(registry.bitcoin_rpc)
        cls.template_registry = registry
