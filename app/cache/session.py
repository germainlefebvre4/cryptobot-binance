from redis import Sentinel, Redis

from app.core.config import settings


sentinel = Sentinel([("localhost", 26379)], socket_timeout=0.1)

masters = sentinel.discover_master('mymaster')
slaves = sentinel.discover_slaves('mymaster')

# master = sentinel.master_for('mymaster', socket_timeout=0.1, password=settings.REDIS_PASSWORD, sentinel_kwargs={"password": settings.REDIS_PASSWORD})
# slave = sentinel.slave_for('mymaster', socket_timeout=0.1, password=settings.REDIS_PASSWORD, sentinel_kwargs={"password": settings.REDIS_PASSWORD})
master = sentinel.master_for('mymaster', socket_timeout=0.1, password=settings.REDIS_PASSWORD)
slave = sentinel.slave_for('mymaster', socket_timeout=0.1, password=settings.REDIS_PASSWORD)

# keys = slave.keys("*")
# print(keys)
# for key in keys:
#     master.delete(key)
# keys = slave.keys("*")
# print(keys)
