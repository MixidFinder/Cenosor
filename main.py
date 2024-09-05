import asyncio

from bot import bot


async def main():
    await bot.main()
    # parser.price_parse()


if __name__ == "__main__":
    asyncio.run(main())
