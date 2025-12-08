"""
GhostLink Connection Pooling Configuration
Optimizes database and external service connections
"""

import asyncio
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Optional imports with fallbacks
try:
    import aiomysql
    AIOMYSQL_AVAILABLE = True
except ImportError:
    aiomysql = None
    AIOMYSQL_AVAILABLE = False
    logger.warning("aiomysql not available, database pooling disabled")

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    aiohttp = None
    AIOHTTP_AVAILABLE = False
    logger.warning("aiohttp not available, HTTP pooling disabled")

try:
    import aioredis
    AIOREDIS_AVAILABLE = True
except ImportError:
    aioredis = None
    AIOREDIS_AVAILABLE = False
    logger.warning("aioredis not available, Redis pooling disabled")

class ConnectionPoolManager:
    """Manages connection pools for optimal performance"""

    def __init__(self):
        self.db_pool = None  # aiomysql.Pool if available
        self.http_session = None  # aiohttp.ClientSession if available
        self.redis_pool = None  # aioredis pool if available

    async def init_db_pool(self, host: str = 'localhost', port: int = 3306,
                          user: str = 'ghostlink', password: str = '',
                          db: str = 'ghostlink', minsize: int = 5, maxsize: int = 20):
        """Initialize database connection pool"""
        if not AIOMYSQL_AVAILABLE:
            logger.warning("aiomysql not available, database pooling disabled")
            return

        try:
            self.db_pool = await aiomysql.create_pool(
                host=host,
                port=port,
                user=user,
                password=password,
                db=db,
                minsize=minsize,
                maxsize=maxsize,
                autocommit=True,
                pool_recycle=3600  # Recycle connections every hour
            )
            logger.info(f"Database connection pool initialized (min: {minsize}, max: {maxsize})")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise

    async def init_http_session(self, connector=None):
        """Initialize HTTP client session with connection pooling"""
        if not AIOHTTP_AVAILABLE:
            logger.warning("aiohttp not available, HTTP session pooling disabled")
            return

        if connector is None:
            connector = aiohttp.TCPConnector(
                limit=100,  # Max concurrent connections
                limit_per_host=10,  # Max connections per host
                ttl_dns_cache=300,  # DNS cache TTL
                use_dns_cache=True,
                keepalive_timeout=60,
                enable_cleanup_closed=True
            )

        self.http_session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=30, connect=10)
        )
        logger.info("HTTP session with connection pooling initialized")

    async def init_redis_pool(self, host: str = 'localhost', port: int = 6379,
                             db: int = 0, minsize: int = 5, maxsize: int = 20):
        """Initialize Redis connection pool"""
        if not AIOREDIS_AVAILABLE:
            logger.warning("aioredis not available, Redis pooling disabled")
            return

        try:
            self.redis_pool = aioredis.ConnectionPool(
                host=host,
                port=port,
                db=db,
                minsize=minsize,
                maxsize=maxsize,
                retry_on_timeout=True
            )
            logger.info(f"Redis connection pool initialized (min: {minsize}, max: {maxsize})")
        except Exception as e:
            logger.error(f"Failed to initialize Redis pool: {e}")
            raise

    async def get_db_connection(self):
        """Get database connection from pool"""
        if not self.db_pool:
            raise RuntimeError("Database pool not initialized")
        return await self.db_pool.acquire()

    async def release_db_connection(self, conn):
        """Release database connection back to pool"""
        if self.db_pool:
            self.db_pool.release(conn)

    async def close_all(self):
        """Close all connection pools"""
        if self.db_pool:
            self.db_pool.close()
            await self.db_pool.wait_closed()

        if self.http_session:
            await self.http_session.close()

        if self.redis_pool:
            await self.redis_pool.disconnect()

        logger.info("All connection pools closed")

# Global connection pool manager instance
pool_manager = ConnectionPoolManager()

async def init_connection_pools():
    """Initialize all connection pools"""
    try:
        await pool_manager.init_db_pool()
    except Exception as e:
        logger.warning(f"Database pool initialization failed: {e}")

    try:
        await pool_manager.init_http_session()
    except Exception as e:
        logger.warning(f"HTTP session initialization failed: {e}")

    try:
        await pool_manager.init_redis_pool()
    except Exception as e:
        logger.warning(f"Redis pool initialization failed: {e}")

async def cleanup_connection_pools():
    """Cleanup all connection pools"""
    await pool_manager.close_all()

# Context manager for database connections
class DatabaseConnection:
    """Context manager for database connections"""

    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        self.conn = await pool_manager.get_db_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            await pool_manager.release_db_connection(self.conn)

# Optimized query execution with connection pooling
async def execute_query(query: str, params: tuple = None) -> list:
    """Execute database query using connection pool"""
    async with DatabaseConnection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchall()

async def execute_query_single(query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
    """Execute query and return single result"""
    async with DatabaseConnection() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, params or ())
            return await cursor.fetchone()
