你好，我是景霄。

上节课，我们一起学习了Python并发编程的一种实现——多线程。今天这节课，我们继续学习Python并发编程的另一种实现方式——Asyncio。不同于协程那章，这节课我们更注重原理的理解。

通过上节课的学习，我们知道，在处理I/O操作时，使用多线程与普通的单线程相比，效率得到了极大的提高。你可能会想，既然这样，为什么还需要Asyncio？

诚然，多线程有诸多优点且应用广泛，但也存在一定的局限性：

- 比如，多线程运行过程容易被打断，因此有可能出现race condition的情况；
- 再如，线程切换本身存在一定的损耗，线程数不能无限增加，因此，如果你的 I/O操作非常heavy，多线程很有可能满足不了高效率、高质量的需求。

正是为了解决这些问题，Asyncio应运而生。

## 什么是Asyncio

### Sync VS Async

我们首先来区分一下Sync（同步）和Async（异步）的概念。

- 所谓Sync，是指操作一个接一个地执行，下一个操作必须等上一个操作完成后才能执行。
- 而Async是指不同操作间可以相互交替执行，如果其中的某个操作被block了，程序并不会等待，而是会找出可执行的操作继续执行。

举个简单的例子，你的老板让你做一份这个季度的报表，并且邮件发给他。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（30） 💬（7）<div>思考题答案：
import multiprocessing
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


if __name__ == &quot;__main__&quot;:
    numbers = [10000000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f&quot;Duration {duration} seconds&quot;)</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（6） 💬（2）<div>上网查询资料后，初步了解了多进程的一些知识，按照资料中的方法简单改写了一下程序，由于多进程方式时，不知什么原因，cpu_bound函数不能实时输出，所以就把cpu_bound改为返回字符串形式的结果，等所有的数计算完成后，再一并输出结果 ，程序中常规执行和多进程两种方式都有，并作了对比后发现，常规执行用时约23秒，多进程用时约6秒，两者相差4倍，程序如下，不足处请老师指正：
#多进程演示
import multiprocessing
import time

def cpu_bound(number):
    return &#39;sum({}^2)={}&#39;.format(number,sum(i * i for i in range(number)))

def calculate_sums(numbers):
    
    results = []

    print(&#39;-&#39;*10+&#39;串行执行开始：&#39;+&#39;-&#39;*10)

    for number in numbers:
        results.append(cpu_bound(number))

    print(&#39;-&#39;*10+&#39;串行执行结束，结果如下：&#39;+&#39;-&#39;*10)
    for res in results:
        print(res)

def multicalculate_sums(numbers):

    #创建有4个进程的进程池
    pool = multiprocessing.Pool(processes=4)

    results = []

    print(&#39;-&#39;*10+&#39;多进程执行开始：&#39;+&#39;-&#39;*10)

    #为每一个需要计算的元素创建一个进程
    for number in numbers:
        results.append(pool.apply_async(cpu_bound, (number,)))

    pool.close() #关闭进程池，不能往进程池添加进程
    pool.join()  #等待进程池中的所有进程执行完毕

    print(&#39;-&#39;*10+&#39;多进程执行结束，结果如下：&#39;+&#39;-&#39;*10)
    for res in results:
        print(res.get())
    
def main():

    numbers = [10000000 + x for x in range(20)]

    #串行执行方式
    start_time = time.perf_counter()  
    calculate_sums(numbers)
    end_time = time.perf_counter()
    print(&#39;串行执行用时：Calculation takes {} seconds&#39;.format(end_time - start_time))

    #多进程执行方式
    start_time = time.perf_counter()  
    multicalculate_sums(numbers)
    end_time = time.perf_counter()
    print(&#39;多进程执行用时：Calculation takes {} seconds&#39;.format(end_time - start_time))
    
if __name__ == &#39;__main__&#39;:
    main()
</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5a/2a/5ab880b0.jpg" width="30px"><span>szc</span> 👍（1） 💬（1）<div>能否举一些例子，哪些场景是IO密集型中的IOheavy， 那些是IO很快</div>2019-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/99/27/47aa9dea.jpg" width="30px"><span>阿卡牛</span> 👍（0） 💬（2）<div>常听到阻塞，同步是不是就是阻塞地意思</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（60） 💬（3）<div>总结多线程和协程之间的共同点和区别：
共同点：
都是并发操作，多线程同一时间点只能有一个线程在执行，协程同一时间点只能有一个任务在执行；
不同点：
多线程，是在I&#47;O阻塞时通过切换线程来达到并发的效果，在什么情况下做线程切换是由操作系统来决定的，开发者不用操心，但会造成race condition；
协程，只有一个线程，在I&#47;O阻塞时通过在线程内切换任务来达到并发的效果，在什么情况下做任务切换是开发者决定的，不会有race condition的情况；
多线程的线程切换比协程的任务切换开销更大；
对于开发者而言，多线程并发的代码比协程并发的更容易书写。
一般情况下协程并发的处理效率比多线程并发更高。</div>2019-06-28</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（30） 💬（4）<div>1、单进程，老师的原程序，运行时间
     Calculation takes 15.305913339 seconds
2、CPU并行方式，运行时间：
     Calculation takes 3.457259904 seconds
      def calculate_sums(numbers):    
             with concurrent.futures.ProcessPoolExecutor() as executor:
             executor.map(cpu_bound,numbers)
3、多线程，cocurrent.futures，运行时间
      Calculation takes 15.331446270999999 seconds
      def calculate_sums(numbers):
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                executor.map(cpu_bound,numbers)
4、异步方式，asyncio
      Calculation takes 16.019983702999998 seconds
      async def cpu_bound(number):
            print(sum(i * i for i in range(number)))
      async def calculate_sums(numbers):
           tasks=[asyncio.create_task(cpu_bound(number)) for number in numbers]
           await asyncio.gather(*tasks)</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/11/5d113d5c.jpg" width="30px"><span>天凉好个秋</span> 👍（8） 💬（2）<div>如果完成，则将其放到预备状态的列表；
如果未完成，则继续放在等待状态的列表。
这里是不是写的有问题？
PS:想问一下，完成之后为什么还要放队列里？难道不应该从队列里移除吗？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/de/7d/61d76ae0.jpg" width="30px"><span>transformation</span> 👍（8） 💬（5）<div>import time
from concurrent import futures


def cpu_bound(number):
    return sum(i * i for i in range(number))


def calculate_sums(numbers):
    for number in numbers:
        print(cpu_bound(number))


def main():
    start_time = time.perf_counter()
    numbers = [10000000 + x for x in range(20)]
    calculate_sums(numbers)
    end_time = time.perf_counter()
    print(&#39;Calculation takes {} seconds&#39;.format(end_time - start_time))


def main_process():
    start_time = time.perf_counter()
    numbers = [10000000 + x for x in range(20)]
    with futures.ProcessPoolExecutor() as pe:
        result = pe.map(cpu_bound, numbers)
        print(f&quot;result: {list(result)}&quot;)
    end_time = time.perf_counter()
    print(&#39;multiprocessing Calculation takes {} seconds&#39;.format(end_time - start_time))


if __name__ == &#39;__main__&#39;:
    main()
    main_process()
————————
输出：
333333283333335000000
333333383333335000000
333333483333355000001
333333583333395000005
333333683333455000014
333333783333535000030
333333883333635000055
333333983333755000091
333334083333895000140
333334183334055000204
333334283334235000285
333334383334435000385
333334483334655000506
333334583334895000650
333334683335155000819
333334783335435001015
333334883335735001240
333334983336055001496
333335083336395001785
333335183336755002109
Calculation takes 15.771127400000001 seconds
result: [333333283333335000000, 333333383333335000000, 333333483333355000001, 333333583333395000005, 333333683333455000014, 333333783333535000030, 333333883333635000055, 333333983333755000091, 333334083333895000140, 333334183334055000204, 333334283334235000285, 333334383334435000385, 333334483334655000506, 333334583334895000650, 333334683335155000819, 333334783335435001015, 333334883335735001240, 333334983336055001496, 333335083336395001785, 333335183336755002109]
multiprocessing Calculation takes 4.7333084 seconds
</div>2019-06-28</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（4） 💬（0）<div>sync是线性前后执行。
async是穿插执行，之所以要穿插，代码需要的资源不同，有的代码需要CPU，有的代码需要IO（例如网络）,穿插以后，同时需要CPU和网络的代码可以同时执行，充分利用硬件。

具体到关键字 async 是表示函数是异步的，也就是来回穿插的起点（进入预备队列），await是表示调用需要IO，也就是进入等待队列的入口（函数开始调用）和出口（函数调用结束，重新进入预备队列）。</div>2019-11-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKokKnHQKrAupdgYJ8mHPbZbeDxKR229qLYkaJt4pwvd1ZcdicgjTdqPKuJlO09ibtZSOvsSLAAnWJQ/132" width="30px"><span>唐哥</span> 👍（3） 💬（2）<div>老师好，对于 Asyncio 来说，它的任务在运行时不会被外部的一些因素打断。不被打断是如何保证的？还有event loop是每次取出一个任务运行，当这个任务运行期间它就是只等待任务结束吗？不干其他事了吗？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/19/37/e0a9bf99.jpg" width="30px"><span>Geek_59f23e</span> 👍（3） 💬（0）<div>import time
from multiprocessing import Pool


def square(number):
    return sum(i * i for i in range(number))


def single_process(numbers):
    res = []
    for number in numbers:
        res.append(square(number))
    return res


def multi_process(numbers):
    with Pool() as pool:
        res = pool.map(square, numbers)
    return res


if __name__ == &#39;__main__&#39;:
    numbers = [10000000 + x for x in range(20)]
    start1 = time.perf_counter()
    single_process(numbers)
    print(&#39;单进程用时：%f 秒&#39; % (time.perf_counter() - start1))
    start2 = time.perf_counter()
    multi_process(numbers)
    print(&#39;多进程用时：%f 秒&#39; % (time.perf_counter() - start2))

————————
输出：
单进程用时：29.382878 秒
多进程用时：10.354565 秒

[333333283333335000000, 333333383333335000000, 333333483333355000001, 333333583333395000005, 333333683333455000014, 333333783333535000030, 333333883333635000055, 333333983333755000091, 333334083333895000140, 333334183334055000204, 333334283334235000285, 333334383334435000385, 333334483334655000506, 333334583334895000650, 333334683335155000819, 333334783335435001015, 333334883335735001240, 333334983336055001496, 333335083336395001785, 333335183336755002109]
</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/53/79/327ef30e.jpg" width="30px"><span>sugar</span> 👍（2） 💬（0）<div>asyncio是不是跟IO多路复用一个道理啊</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（2） 💬（2）<div>race condition 是什么？</div>2019-06-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ib3Rzem884S7icAGXsBzGKyricapL0sfax7wL7T4n1W1ZPZ0h7XNtGd5aqLlZQgZ3bZTPBmC4xa7ia8iaR0XBKMAuIQ/132" width="30px"><span>Geek_63ad86</span> 👍（1） 💬（0）<div>李金甲到此一游</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/4a/35/66caeed9.jpg" width="30px"><span>完美坚持</span> 👍（1） 💬（1）<div>我在jupyter notebook中用下面的多进程地并行多次尝试只需要0.2-0.9s间，但是老师给的普通程序需要30多s，而且老师在留言中给出的答案代码，不知道哪里不对，运行不出结果，没有报错但是一直出不来结果
import concurrent.futures
import time
def cpu_bound(number):
    return sum(i * i for i in range(number))

def calculate_sums(numbers):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(cpu_bound, numbers)

def main():
    start_time = time.perf_counter()  
    numbers = [10000000 + x for x in range(20)]
    calculate_sums(numbers)
    end_time = time.perf_counter()
    print(&#39;Calculation takes {} seconds&#39;.format(end_time - start_time))
    
if __name__ == &#39;__main__&#39;:
    main()</div>2020-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5b/13/6db9ba58.jpg" width="30px"><span>Kevin</span> 👍（1） 💬（0）<div>使用resp.content_length 得到的None

通过text = await resp.text()
len(text)可以拿到资源大小但是很耗时</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（1） 💬（2）<div>看了很多提问都没有被回答，我也对asyncio有个很大的疑问，那就是我越来越感觉asyncio是一个很糟糕的名字，从内容上看只是解决并发问题，我没有看到针对io的描述，而且我目前的知识体系认为:Linux上解决高并发大多是用的io多路复用和非阻塞，至于异步io很少使用，而且Linux仅仅实现了磁盘读写的异步io，而网络io没有实现异步。所以我就自然对Python这个asyncio有疑问了？它和操作系统io是同一个层次概念么？至少我觉得这是个很糟糕的命名，我不知道初学者遇到异步io的概念时花大力气搞清楚阻塞非阻塞异步和同步之后，面对Linux上异步io支持以及应用有限的事实之后会作何感想！盼复！</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（1） 💬（2）<div>运行文章中出现的代码时出现‘aiohttp.client_exceptions.ClientConnectorCertificateError’的这个报错，我讲代码第7行更改成‘async with session.get(url, ssl=False) as resp’后运行成功，是否还有其他的解决方案？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3d/e7/e4b4afcc.jpg" width="30px"><span>方向</span> 👍（1） 💬（3）<div>如果完成，则放到预备状态列表，这句话不理解。这样一来，预备状态列表同时拥有两种形式的任务啊</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第22讲打卡</div>2024-06-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/icLAWkJCK7qiaw4FroNGVLu9zxH65tnIQBhgd7giah1U7oL3tDAXliaZpve9JPfUbjXicy6Y29w4SUS8Oia265dTpiaFw/132" width="30px"><span>Geek_581965</span> 👍（0） 💬（0）<div>想问一下老师，我将接口提供给下游，多人调用我的接口，对于这个接口来说，是多进程还是多线程啊～？</div>2023-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e2/81/2cbb88b1.jpg" width="30px"><span>这只鸟不会飞</span> 👍（0） 💬（0）<div>我使用了多线程和Asyncio为啥感觉和上面串行执行的相差不大，这是为啥？ 代码如下：



import asyncio
import time
import concurrent.futures

####################################  使用 Asyncio 方式 ， 耗时：24s ##########################################


async def cpu_bound_as(number):
    print(sum(i * i for i in range(number)))


async def cal_sums_as(numbers):
    print(&#39;numbers : {}&#39;.format(numbers))
    tasks = [asyncio.create_task(cpu_bound_as(number)) for number in numbers]
    await asyncio.gather(*tasks)


###############################  使用 多线程方式, 耗时：24s #############################################################


def cpu_bound_future(number):
    print(sum(i * i for i in range(number)))


def cal_sums_future(numbers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(cpu_bound_future, numbers)

########################### 使用并行方式, 耗时: 7s #######################################################################


def cal_sum_process(numbers):
    &quot;&quot;&quot;并行实现数据处理&quot;&quot;&quot;
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(cpu_bound_future, numbers)


########################### 使用普通方式, 耗时: 27s #######################################################################

def cpu_bound_usual(number):
    result = sum(i * i for i in range(number))
    print(result)
    return result


def cal_sums_usual(numers):
    &quot;&quot;&quot;串行执行&quot;&quot;&quot;
    results = [cpu_bound_usual(number) for number in numers]
    print(results)


def main():
    time_start = time.perf_counter()
    numbers = [10000000 + x for x in range(20)]
    # cal_sums_usual(numbers)
    cal_sums_future(numbers)
    # asyncio.run(cal_sums_as(numbers))
    # cal_sum_process(numbers)
    time_end = time.perf_counter()
    print(&#39;Wall time {}s&#39;.format(time_end - time_start))</div>2023-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（0）<div>老师，cpu密集型，用多进程，可以给个例子吗？</div>2022-11-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLAdqqPjPWlIibwqDydskjPMfv4V0dibs3p7DoeEziaJVSKoib1siaMHw7xYvk5KwiafCdGRWtUw6eeoyvg/132" width="30px"><span>陈雁南</span> 👍（0） 💬（0）<div>使用 asyncio.get_event_loop().run_until_complete(download_all(sites)) 替换asyncio.run(download_all(sites))</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/bf/52/59304c42.jpg" width="30px"><span>默默且听风</span> 👍（0） 💬（0）<div>class WeiXinWeb:
# set(name, value, ex=None
    def __init__(self,appid,secret) -&gt; None:
        
        self.base_url = &quot;https:&#47;&#47;api.weixin.qq.com&#47;&quot;
        self.appid = appid
        self.secret = secret

    async def access_token(self) -&gt;str:
        &quot;&quot;&quot;获取基础access_token&quot;&quot;&quot;
        # 判断redis中的基础token
        if not await redis_conn.get(&quot;access_token&quot;) :
            # 拼接基础token请求字符串
            url:str = f&quot;{self.base_url}cgi-bin&#47;token?grant_type=client_credential&amp;appid={self.appid}&amp;secret={self.secret}&quot;
            # 异步请求基础token
            async with ClientSession() as sess:
                async with sess.get(url) as r:
                    # 获取到的基础token存入redis中
                    res = await r.text()
                    await redis_conn.set(&quot;access_token&quot;, json.loads(res).get(&quot;access_token&quot;,&quot;&quot;), ex=3600)
        token = await redis_conn.get(&quot;access_token&quot;)
        return str(token,&quot;utf-8&quot;)

appid = &quot;&quot;
secret = &quot;&quot;</div>2022-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/c4/86/0658e993.jpg" width="30px"><span>涼白开</span> 👍（0） 💬（0）<div>import multiprocessing
import time


def cpu_bound(number):
    return sum(i * i for i in range(number))


def find_sums(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)


if __name__ == &quot;__main__&quot;:
    numbers = [10000000 + x for x in range(20)]

    start_time = time.time()
    find_sums(numbers)
    duration = time.time() - start_time
    print(f&quot;Duration {duration} seconds&quot;)</div>2021-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/f9/3e/0d5f27c4.jpg" width="30px"><span>肥猫不开心</span> 👍（0） 💬（0）<div>怎样把一个普通的同步方法封装成异步呢</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/28/85/3ae5efed.jpg" width="30px"><span>Silence°</span> 👍（0） 💬（0）<div>请问下这两种方式我在我电脑上运行时间差不多，哪个是多进程的？我看老师讲过的这两个都是呀。。
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(cpu_bound, numbers)
另一个是：
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)
第二个是老师给的答案，求大佬指教！</div>2021-08-15</li><br/><li><img src="" width="30px"><span>陈先跑</span> 👍（0） 💬（0）<div>多线程和 Asyncio的选择上，怎么才算IO慢？能给点具体的场景吗？</div>2021-08-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/OwZuBRbVUkziazePs2xTKskNpZachRtCBZLHlv4dAUgaBC5qHI292xaxvg3atGnHlDwjIOXPKEbc7zOrtMyicSNg/132" width="30px"><span>罗辑</span> 👍（0） 💬（0）<div>思考题对于计算密集型，采用和电脑CPU核数匹配的多进程是最快的。多线程核协程都无法100%使用CPU，多进程可以。望老师指点。
import asyncio
import aiohttp
import concurrent.futures
import threading
import time

def cpu_bound(number):
    print(sum(i * i for i in range(number)))

def calculate_sums(numbers):
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        executor.map(cpu_bound,numbers)

def main():
    start_time = time.perf_counter()
    numbers = [10000000 + x for x in range(20)]
    calculate_sums(numbers)
    end_time = time.perf_counter()
    print(&#39;Calculation takes {} seconds&#39;.format(end_time - start_time))


if __name__ == &#39;__main__&#39;:
    main()</div>2021-07-05</li><br/>
</ul>