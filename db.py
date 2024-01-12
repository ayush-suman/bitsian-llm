from motor.motor_asyncio import AsyncIOMotorClient

import config
import sys
from datetime import datetime

mongodb_client = AsyncIOMotorClient(config.MONGODB_URL)
db = mongodb_client['bistian_ai_db']


async def backup_day_summary(day_summary: str, today: datetime):
    data = {"date": today.strftime("%B %d, %Y"), "summary": day_summary}
    inserted_id = await db['day_summaries'].insert_one(data)
    print("Inserted day summary with id: ", inserted_id, file=sys.stdout)
