import asyncio
import datetime
import json
import aiohttp


class CurrencyRates:

    def __init__(self, session: aiohttp.ClientSession):
        self._session = session
        self._base_url = "https://api.privatbank.ua/p24/exchange_rates"

    async def get_rates(self, days: int) -> dict:
        if days > 10:
            raise ValueError("Кількість днів не може перевищувати 10")

        now = datetime.datetime.now()
        start_date = now - datetime.timedelta(days=days)
        end_date = now

        response = await self._session.get(
            f"{self._base_url}?date={start_date.strftime('%d.%m.%Y')}&date_to={end_date.strftime('%d.%m.%Y')}"
        )

        if response.status == 200:
            data = json.loads(response.text)
            return data
        else:
            raise ValueError(f"Не вдалося отримати курси валют: {response.status}")


async def main(days: int):
    loop = asyncio.get_event_loop()
    session = aiohttp.ClientSession()
    rates = loop.run_until_complete(CurrencyRates(session).get_rates(days))

    print(rates)


if __name__ == "__main__":
    days = int(input("Кількість днів: "))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(days))
