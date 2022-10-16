# learn_asyncio

```
if __name__ == '__main__':
    market = Store(potato_batch=5, tomato_batch=5)
    c1 = Customer(1, market, potato_num=3, tomato_num=5)
    c2 = Customer(2, market, potato_num=5, tomato_num=3)
    tasks = asyncio.wait([c1.buy(), c2.buy()])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

    print('土豆剩余:{}'.format(market.potato.qsize()))
    print('西红柿剩余:{}'.format(market.tomato.qsize()))
```

>python async_market.py
```
Customer<2>: 没土豆了,快补货啊!
土豆准备中...
Customer<2>: 没西红柿了,快补货啊!
西红柿准备中...
Customer<1>: 没土豆了,快补货啊!
Customer<1>: 没西红柿了,快补货啊!
土豆准备好了!
西红柿准备好了!
土豆还有的
西红柿还有的
Customer<2> get 土豆<1>
Customer<2> get 西红柿<1>
Customer<1> get 土豆<2>
Customer<1> get 西红柿<2>
Customer<1> get 土豆<3>
Customer<2> get 土豆<4>
Customer<2> get 西红柿<3>
Customer<1> get 西红柿<4>
Customer<2> get 土豆<5>
Customer<1>: 没土豆了,快补货啊!
土豆准备中...
Customer<2> get 西红柿<5>
Customer<2>: 没土豆了,快补货啊!
Customer<1>: 没西红柿了,快补货啊!
西红柿准备中...
西红柿准备好了!
Customer<1> get 西红柿<6>
土豆准备好了!
土豆还有的
Customer<1> get 土豆<6>
Customer<2> get 土豆<7>
Customer<1> get 西红柿<7>
Customer<2> get 土豆<8>
Customer<1> get 西红柿<8>
土豆剩余:2
西红柿剩余:2
```
