import asyncio
import traceback

from news_bot.News import News, AlarmConfig

async def test_in_try_except():
    try:
        c = AlarmConfig("soru-cevap", 16, 30)
        await News.sendNews(None, c)
    except Exception as ex:
        traceback.print_exception(type(ex), ex, ex.__traceback__)

def test_timeout():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_in_try_except())