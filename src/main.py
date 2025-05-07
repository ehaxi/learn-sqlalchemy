import asyncio
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queries.core import SyncCore, AsyncCore
from queries.orm import SyncORM, AsyncORM

SyncORM.create_tables()
# SyncCore.create_tables()

SyncORM.insert_workers()
# SyncCore.insert_workers()

SyncCore.select_workers()