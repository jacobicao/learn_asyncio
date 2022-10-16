import random
import asyncio


def generate_counter():
    cnt = [0]

    def add_one():
        cnt[0] = cnt[0] + 1
        return cnt[0]

    return add_one


class Potato:
    def __init__(self, i):
        self._id = i

    def __str__(self):
        return '{}<{}>'.format('土豆', self._id)


class Tomato:
    def __init__(self, i):
        self._id = i

    def __str__(self):
        return '{}<{}>'.format('西红柿', self._id)


class Store:
    def __init__(self, potato_batch=10, tomato_batch=10):
        self.potato_series = generate_counter()
        self.tomato_series = generate_counter()
        self.potato = asyncio.Queue()
        self.tomato = asyncio.Queue()
        self.potato_batch = potato_batch
        self.tomato_batch = tomato_batch
        self.potato_sem = asyncio.Lock()
        self.tomato_sem = asyncio.Lock()

    async def get_potato(self):
        async with self.potato_sem:
            return await self.potato.get()

    async def get_tomato(self):
        async with self.tomato_sem:
            return await self.tomato.get()

    async def supply_potato(self):
        async with self.potato_sem:
            if not self.potato.empty():
                print('土豆还有的')
                return
            print('土豆准备中...')
            await asyncio.sleep(random.randint(1, 2))
            potatoes = [Potato(self.potato_series()) for i in range(self.potato_batch)]
            for potato in potatoes:
                await self.potato.put(potato)
            print('土豆准备好了!')

    async def supply_tomato(self):
        async with self.tomato_sem:
            if not self.tomato.empty():
                print('西红柿还有的')
                return
            print('西红柿准备中...')
            await asyncio.sleep(random.randint(1, 2))
            batch = [Tomato(self.tomato_series()) for i in range(self.tomato_batch)]
            for item in batch:
                await self.tomato.put(item)
            print('西红柿准备好了!')


class Customer:
    def __init__(self, name, store, potato_num, tomato_num):
        self.name = name
        self.potato_num = potato_num
        self.tomato_num = tomato_num
        self.store = store
        self.bucket = []
        self.lock = asyncio.Lock()

    def __str__(self):
        return '{}<{}>'.format(self.__class__.__name__, self.name)

    async def take_potato(self, num):
        cnt = 0
        while True:
            if self.store.potato.empty():
                print('{}: 没土豆了,快补货啊!'.format(self))
                await self.store.supply_potato()
            item = await self.store.get_potato()
            yield item
            cnt += 1
            if cnt == num:
                break

    async def put_potato(self):
        async for item in self.take_potato(self.potato_num):
            print('{} get {}'.format(self, item))
            async with self.lock:
                await asyncio.sleep(random.randint(2, 5) * 0.1)
                self.bucket.append(item)

    async def take_tomato(self, num):
        cnt = 0
        while True:
            if self.store.tomato.empty():
                print('{}: 没西红柿了,快补货啊!'.format(self))
                await self.store.supply_tomato()
            item = await self.store.get_tomato()
            self.store.tomato.task_done()
            yield item
            cnt += 1
            if cnt == num:
                break

    async def puy_tomato(self):
        async for item in self.take_tomato(self.tomato_num):
            print('{} get {}'.format(self, item))
            async with self.lock:
                await asyncio.sleep(random.randint(5, 9) * 0.1)
                self.bucket.append(item)

    async def buy(self):
        await asyncio.gather(self.put_potato(), self.puy_tomato())


if __name__ == '__main__':
    cust_id = generate_counter()
    market = Store(potato_batch=5, tomato_batch=5)
    c1 = Customer(cust_id(), market, potato_num=3, tomato_num=5)
    c2 = Customer(cust_id(), market, potato_num=5, tomato_num=3)
    tasks = asyncio.wait([c1.buy(), c2.buy()])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    print('土豆剩余:{}'.format(market.potato.qsize()))
    print('西红柿剩余:{}'.format(market.tomato.qsize()))
