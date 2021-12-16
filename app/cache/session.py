# from redis import Sentinel, Redis
from redis import Redis
from redis.sentinel import Sentinel

from app.core.config import settings
import app.core.logging


sentinel = Sentinel([(settings.REDIS_SENTINEL_SERVER, settings.REDIS_SENTINEL_PORT)], socket_timeout=0.1)

masters = sentinel.discover_master('mymaster')
slaves = sentinel.discover_slaves('mymaster')

master = sentinel.master_for('mymaster', socket_timeout=0.1, password=settings.REDIS_PASSWORD, db=settings.REDIS_DATABASE)
slave = sentinel.slave_for('mymaster', socket_timeout=0.1, password=settings.REDIS_PASSWORD, db=settings.REDIS_DATABASE)

print("master", master)
print("slave", slave)

# keys = slave.keys("*")
# print(keys)
# for key in keys:
#     master.delete(key)
# keys = slave.keys("*")
# print(keys)

# print("flushdb()")
# master.flushdb()
