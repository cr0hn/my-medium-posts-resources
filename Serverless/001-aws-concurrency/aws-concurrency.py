import csv
import asyncio

from typing import List

import httpx

from collections import Counter

from httpcore import ConnectTimeout

URL = "https://oipdjld2b6dbqcmts3ar2qusim0vmyht.lambda-url.us-east-2.on.aws/"

async def do_request(client, sem: asyncio.Semaphore, count: Counter):

    try:
        async with sem:
            r = await client.get(URL)

            key = r.text

            count[key] += 1

    except Exception as e:
        print("Error: ", e)
        count["error"] += 1

    finally:
        sem.release()

def print_stadistics(concurrency, total_requests, statistics: Counter):

    print(f"Statistics. Concurrency: {concurrency} - Total requests: {total_requests} - Total instances - {len(statistics)} - Errors: {statistics['error']}")

    # for k, v in statistics.items():
    #     print(f"{k} - {v}")

def save_csv(data: List[tuple]):
    with open('concurrency_vs_requests.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(
            csvfile,
            delimiter=' ',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )
        spamwriter.writerow(["concurrency", "requests", "Errors", "Instances"])
        for d in data:
            spamwriter.writerow(d)

async def do_test(concurrency: int, total_requests: int):

    sem = asyncio.Semaphore(concurrency)
    count = Counter()

    coro = []
    async with httpx.AsyncClient() as client:
        for i in range(total_requests):
            t = asyncio.create_task(do_request(client, sem, count))
            coro.append(t)

        await asyncio.wait(coro)

    return count


async def concurrency_vs_requests():
    ret = []

    for concurrency in (10, 100, 1000):
        for requests in (10, 1000, 10_000):
            if concurrency > requests:
                continue

            print("Starting test. Concurrency: {concurrency} - Requests: {requests} => ".format(concurrency=concurrency, requests=requests), flush=True, end="")

            res = await do_test(concurrency, requests)

            print_stadistics(concurrency, requests, res)

            ret.append((concurrency, requests, res["error"], len(res)))

            await asyncio.sleep(5)

    save_csv(ret)

if __name__ == '__main__':
    asyncio.run(concurrency_vs_requests())
