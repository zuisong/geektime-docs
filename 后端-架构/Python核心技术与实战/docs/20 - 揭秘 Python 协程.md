你好，我是景霄。

上一节课的最后，我们留下一个小小的悬念：生成器在 Python 2 中还扮演了一个重要角色，就是用来实现 Python 协程。

那么首先你要明白，什么是协程？

协程是实现并发编程的一种方式。一说并发，你肯定想到了多线程/多进程模型，没错，多线程/多进程，正是解决并发问题的经典模型之一。最初的互联网世界，多线程/多进程在服务器并发中，起到举足轻重的作用。

随着互联网的快速发展，你逐渐遇到了 C10K 瓶颈，也就是同时连接到服务器的客户达到了一万个。于是很多代码跑崩了，进程上下文切换占用了大量的资源，线程也顶不住如此巨大的压力，这时， NGINX 带着事件循环出来拯救世界了。

如果将多进程/多线程类比为起源于唐朝的藩镇割据，那么事件循环，就是宋朝加强的中央集权制。事件循环启动一个统一的调度器，让调度器来决定一个时刻去运行哪个任务，于是省却了多线程中启动线程、管理线程、同步锁等各种开销。同一时期的 NGINX，在高并发下能保持低资源低消耗高性能，相比 Apache 也支持更多的并发连接。

再到后来，出现了一个很有名的名词，叫做回调地狱（callback hell），手撸过 JavaScript 的朋友肯定知道我在说什么。我们大家惊喜地发现，这种工具完美地继承了事件循环的优越性，同时还能提供 async / await 语法糖，解决了执行性和可读性共存的难题。于是，协程逐渐被更多人发现并看好，也有越来越多的人尝试用 Node.js 做起了后端开发。（讲个笑话，JavaScript 是一门编程语言。）
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（45） 💬（0）<div>思考题答案：

在 python 3.7 及以上的版本中，我们对 task 对象调用 add_done_callback() 函数，即可绑定特定回调函数。回调函数接受一个 future 对象，可以通过 future.result() 来获取协程函数的返回值。

示例如下：

import asyncio

async def crawl_page(url):
    print(&#39;crawling {}&#39;.format(url))
    sleep_time = int(url.split(&#39;_&#39;)[-1])
    await asyncio.sleep(sleep_time)
    return &#39;OK {}&#39;.format(url)

async def main(urls):
    tasks = [asyncio.create_task(crawl_page(url)) for url in urls]
    for task in tasks:
        task.add_done_callback(lambda future: print(&#39;result: &#39;, future.result()))
    await asyncio.gather(*tasks)

%time asyncio.run(main([&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;]))

输出：

crawling url_1
crawling url_2
crawling url_3
crawling url_4
result:  OK url_1
result:  OK url_2
result:  OK url_3
result:  OK url_4
Wall time: 4 s</div>2019-07-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJOlibibPFEWOib8ib7RtfAtxND5FUqCxxoeTuLAbBI9ic23xuwdXT4IyiaWq3Fic9RgEAYI0lBTbEp2rcg/132" width="30px"><span>Jingxiao</span> 👍（77） 💬（10）<div>发现评论区好多朋友说无法运行，在这里统一解释下：
1. %time 是 jupyter notebook 自带的语法糖，用来统计一行命令的运行时间；如果你的运行时是纯粹的命令行 python，或者 pycharm，那么请把 %time 删掉，自己用传统的时间戳方法来记录时间也可以；或者使用 jupyter notebook
2. 我的本地解释器是 Anaconda Python 3.7.3，亲测 windows &#47; ubuntu 均可正常运行，如无法执行可以试试 pip install nest-asyncio，依然无法解决请尝试安装 Anaconda Python
3. 这次代码因为使用了较新的 API，所以需要较新的版本号，但是朋友们依然出现了一些运行时问题，这里先表示下歉意；同时也想说明的是，在提问之前自己经过充分搜索，尝试后解决问题，带来的快感，和能力的提升，相应也是很大的，一门工程最需要的是 hands on dirty work（动手做脏活），才能让自己的能力得到本质的提升，加油！</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/92/fb/4c06bcef.jpg" width="30px"><span>Airnm.毁</span> 👍（8） 💬（3）<div>豆瓣那个发现requests.get(url).content&#47;text返回都为空，然后打了下status_code发现是418，网上找418的解释，一般是网站反爬虫基础机制，需要加请求头模仿浏览器就可跳过，改为下面的样子就可通过：url = &quot;https:&#47;&#47;movie.douban.com&#47;cinema&#47;later&#47;beijing&#47;&quot;
head={
    &#39;User-Agent&#39;:&#39;Mozilla&#47;5.0 (Windows NT 6.1; Win64; x64) AppleWebKit&#47;537.36 (KHTML, like Gecko) Chrome&#47;81.0.4044.113 Safari&#47;537.36&#39;,
    &#39;Referer&#39;:&#39;https:&#47;&#47;time.geekbang.org&#47;column&#47;article&#47;101855&#39;,
    &#39;Connection&#39;:&#39;keep-alive&#39;}
res = requests.get(url,headers=head)</div>2020-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/37/8775d714.jpg" width="30px"><span>jackstraw</span> 👍（4） 💬（2）<div>有点没明白，前面说任务创建后立马就开始执行了么？怎么后面在解密底层运行过程的时候，说任务创建后等待执行？到底是哪一个呀？</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/c4/6f97daea.jpg" width="30px"><span>长期规划</span> 👍（2） 💬（1）<div>老师，在最后那个协程例子中为何没用requests库呢？是因为它不支持协程吗</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f3/b3/0ba7a760.jpg" width="30px"><span>一凡</span> 👍（1） 💬（1）<div>协程是单线程怎么理解？所有的协程都是吗</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e2/c4/25acaa38.jpg" width="30px"><span>苹果</span> 👍（1） 💬（1）<div>asyncio.run() cannot be called from a running event loop
这个问题是如何解决，
</div>2020-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/78/2828195b.jpg" width="30px"><span>隰有荷</span> 👍（1） 💬（1）<div>老师，在如下代码中：
async def worker_2():
    print(&#39;worker_2 start&#39;)
    await asyncio.sleep(2)
    print(&#39;worker_2 done&#39;)

其中的await asyncio.sleep(2)是否可以理解为在切出当前程序，2秒后再继续执行print(&#39;worker_2 done&#39;)代码？
那么如果我有个耗时任务 def xxx(): ...，那么该如何用await asyncio来让这个xxx函数运行并切出当前程序呢？</div>2019-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（1） 💬（1）<div>请问下有木有相关的书籍，来进行这块的学习呢！有些原理性的东西还是没办法深入理解，谢谢。</div>2019-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/41/19/30504ae1.jpg" width="30px"><span>cotter</span> 👍（1） 💬（3）<div>受教了，第一次听说这个高级功能！
我在工作中遇到一个需要并发的问题，用python在后台并发执行shell ,并发数量用时间范围控制，要不停的改时间分多次串行，方法比较笨拙。协程可以简化我的代码。
老师，并发很多事件应该也是需要消耗很多资源，协程改如何控制并发数量？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/93/8c/cf41cf2b.jpg" width="30px"><span>SUN</span> 👍（0） 💬（2）<div>Jupyter 中运行 %time asyncio.run(main([&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;])) 会报错：
RuntimeError: asyncio.run() cannot be called from a running event loop
Python、Anaconda、Jupyter都安装了。
话说：Jupyter不就是为了消除个人本地开发环境差异性而诞生的吗？这个结果有点反讽。
各位学员的留言都看了，没人解决了此问题……
</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b3/b6/ac302d89.jpg" width="30px"><span>36度道</span> 👍（0） 💬（1）<div>老师，课程的代码是基于py3的吗？</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（72） 💬（7）<div>说一下我对await的理解：
开发者要提前知道一个任务的哪个环节会造成I&#47;O阻塞，然后把这个环节的代码异步化处理，并且通过await来标识在任务的该环节中断该任务执行，从而去执行下一个事件循环任务。这样可以充分利用CPU资源，避免CPU等待I&#47;O造成CPU资源白白浪费。当之前任务的那个环节的I&#47;O完成后，线程可以从await获取返回值，然后继续执行没有完成的剩余代码。
由上面分析可知，如果一个任务不涉及到网络或磁盘I&#47;O这种耗时的操作，而只有CPU计算和内存I&#47;O的操作时，协程并发的性能还不如单线程loop循环的性能高。</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/07/78441c2b.jpg" width="30px"><span>大侠110</span> 👍（45） 💬（1）<div>感觉还是有很多人看不懂，我试着用通俗的语句讲一下：协成里面重要的是一个关键字await的理解，async表示其修饰的是协程任务即task，await表示的是当线程执行到这一句，此时该task在此处挂起，然后调度器去执行其他的task，当这个挂起的部分处理完，会调用回掉函数告诉调度器我已经执行完了，那么调度器就返回来处理这个task的余下语句。
      </div>2019-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/77/da/54c663f3.jpg" width="30px"><span>Wing·三金</span> 👍（36） 💬（1）<div>思考题：简单的理解是每个新建的协程对象都会自动调用 add_done_callback() 函数来添加一个回调函数，当协程对象的 Future 状态启动时就会调用该回调函数，从而实现回调。

综合下前面的留言和个人的学习，总结下 py 3.6 版本下 asyncio 的主要不同：
1、没有 run(), create_task()，可以用 asyncio.get_even_loop().run_until_complete() 来代替 run()，用 ensure_future() 来代替 create_task()；
2、可能会出现 RuntimeError: This event loop is already running，解决方案一：pip install nest_asyncio; import nest_asyncio; nest_asyncio.apply()；解决方案二：有些友人说是 tornado 5.x 起的版本才有此问题，可考虑将其版本降至 4.x（不推荐）；
3、%time 与 %%time 的主要区别：%time func()（必须是同一行）；%%time 必须放在单元格的开头，强烈建议单独一行 + 不要与 import、def 相关的语句放在同个单元格；
4、爬虫中的 aiohttp.ClientSession(headers=header, connector=aiohttp.TCPConnector(ssl=False)) 提及未声明的 header，要么将 headers=header 部分去掉使用默认参数，要么用诸如 header={&quot;User-Agent&quot;: &quot;Mozilla&#47;5.0 (Windows NT 6.1; Win64; x64) AppleWebKit&#47;537.36 (KHTML, like Gecko) Chrome&#47;74.0.3729.157 Safari&#47;537.36&quot;} 来显式声明；
5、tasks = [asyncio.create_task(crawl_page(url)) for url in urls]; await asyncio.gather(*tasks); 
约等于
tasks = [crawl_page(url) for url in urls]; asyncio.get_even_loop().run_until_complete(asyncio.wait(tasks));
或
tasks = [asyncio.ensure_future(crawl_page(url)) for url in urls]; await asyncio.gather(*tasks);</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f6/4e/0066303c.jpg" width="30px"><span>cuikt</span> 👍（20） 💬（1）<div>在代码async with aiohttp.ClientSession(headers=header, connector=aiohttp.TCPConnector(ssl=False)) as session:中的headers=header需要定义header为一个字典可以像下面这样，否则会报错。
header={&quot;User-Agent&quot;: &quot;Mozilla&#47;5.0 (Windows NT 6.1; Win64; x64) AppleWebKit&#47;537.36 (KHTML, like Gecko) Chrome&#47;74.0.3729.157 Safari&#47;537.36&quot;}</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/78/e8/b79240e8.jpg" width="30px"><span>rogerr</span> 👍（16） 💬（8）<div>目前看到进阶篇就很痛苦了，对于小白来说，基础篇还好理解，到这儿就对深层次的知识无法深入理解和实践，感觉渐行渐远，不知道如何深入下去</div>2019-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（10） 💬（2）<div>学习笔记:异步和阻塞。

阻塞主要是同步编程中的概念:执行一个系统调用，如果暂时没有返回结果，这个调用就不会返回，那这个系统调用后面的应用代码也不会执行，整个应用被“阻塞”了。

同步编程也可以有非阻塞的方式，在系统调用没有完成时直接返回一个错误码。

异步调用是系统调用完成后返回应用一个消息，应用响应消息，获取结果。

上面说的系统调用 对应Python中的异步函数——一个需要执行较长时间的任务。响应消息应该对应回调函数，但我觉得await异步函数返回本身就相当于系统告知应用系统调用完成了，后面的代码起码可以完成部分回调函数做的事情。

阻塞和异步必须配合才能完成异步编程。

1、await异步函数会造成阻塞;
2、await一个task不会造成阻塞，但是task对应的异步函数中必定几乎await一个异步函数，这个异步函数会阻塞这个task的执行，这样其余task才能被事件调度器的调度从而获取执行机会。</div>2019-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/d4/bdd3ed27.jpg" width="30px"><span>converse✪</span> 👍（9） 💬（0）<div>#coding:utf-8
import asyncio
import time

async def corou1():
    print(&quot;corou 1, {}&quot;.format(time.perf_counter()))
    await asyncio.sleep(2) 
    print(&quot;corou 1, {}&quot;.format(time.perf_counter()))
    
async def corou2():
    print(&quot;corou 2, {}&quot;.format(time.perf_counter()))
    # await asyncio.sleep(2)
    time.sleep(5) 
    print(&quot;corou 2, {}&quot;.format(time.perf_counter()))

async def corou3():
    print(&quot;corou 3, {}&quot;.format(time.perf_counter()))
    await asyncio.sleep(2) 
    print(&quot;corou 3, {}&quot;.format(time.perf_counter()))

async def main():
    tasks = [asyncio.create_task(corou())for corou in [corou1,corou2,corou3] ]
    await asyncio.gather(*tasks)

if __name__ == &quot;__main__&quot;:
    asyncio.run(main())
###########执行结果############
func 1, 0.3864962
func 2, 0.3866095
func 2, 5.386688
func 3, 5.387335
func 1, 5.3877248
func 3, 7.3883411

通过上述例子可以看出，协程corou1，corou2，corou3的执行顺序按照加入循环事件的顺序。协程corou1 通过 await asyncio.sleep(2) 让出控制权，协程corou2由于没有await让出控制权所以一直在执行。当corou2结束后，很显然corou1也已经执行完，但还是先执行协程corou3，等协程corou3通过await让出控制权后，协程corou1才执行。

从上可以看出：
- 协程是按照事件循环顺序执行。即使交出控制权的协程执行完毕任务后等待再次获取控制权完成剩余任务，也必须等到循环到该协程才能获得CPU控制权。不会由于该协程已经完成await的任务而直接给它。这就是解释，协程corou2执行完会继续执行协程corou3，而并非继续执行协程corou1。
- await是交出协程控制权的地方
- 从上述代码可以看出，协程中当执行耗时IO操作时，应及时释放控制权，否则其他协程即便完成任务也由于没有CPU控制权而无法继续执行任务。</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7c/8a/bdeb76ac.jpg" width="30px"><span>Fergus</span> 👍（7） 💬（2）<div># -*- encoding: utf-8 -*-
&#39;&#39;&#39;
aiohttp + aysncio爬取电豆瓣电影
py 3.6
sublime text3
&#39;&#39;&#39;


import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup

now = lambda: time.perf_counter()

async def fetchHtmlText(url):
    async with aiohttp.ClientSession(
        headers={&#39;users-agent&#39;:&#39;Mozilla&#47;5.0&#39;}, 
        connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    url = &quot;https:&#47;&#47;movie.douban.com&#47;cinema&#47;later&#47;beijing&#47;&quot;
    html = await fetchHtmlText(url)
    soup = BeautifulSoup(html, &quot;html.parser&quot;)

    divs = soup.find_all(&#39;div&#39;, class_=&#39;item mod&#39;)
    urls = list(map(lambda x: x.a.img[&#39;src&#39;], divs))
    names = list(map(lambda x: x.h3.a.string, divs))
    dats = list(map(lambda x: x.ul.li.string, divs))

    lis = zip(names, dats, urls)
    for i in lis:
        print(&quot;{0:{3}^25} \t {1:{3}^10} \t {2:{3}^}&quot;.format(i[0], i[1], i[2],chr(12288)))


start = now()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
print(&quot;Wall time: {}&quot;.format(now() - start))


# 九龙不败　　　　　　　　　　　　　　　　　　　　　    　　07月02日　　      https:&#47;&#47;img3.doubanio.com&#47;view&#47;photo&#47;s_ratio_poster&#47;public&#47;p2560169035.jpg
# 别岁　　　　　　　　　　　　　　　　　　　　　　　    　　07月02日　　      https:&#47;&#47;img3.doubanio.com&#47;view&#47;photo&#47;s_ratio_poster&#47;public&#47;p2558138041.jpg
...
# 刀背藏身　　　　　　　　　　　　　　　　　　　　　    　　07月19日　　      https:&#47;&#47;img1.doubanio.com&#47;view&#47;photo&#47;s_ratio_poster&#47;public&#47;p2557644589.jpg
# Wall time: 1.994356926937086
# [Finished in 3.7s]
</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ee/4d/5d021e4c.jpg" width="30px"><span>向左看齐</span> 👍（5） 💬（3）<div>    for each_movie in all_movies.find_all(&#39;div&#39;, class_=&quot;item&quot;):

AttributeError: &#39;NoneType&#39; object has no attribute &#39;find_all&#39;
执行报错，有没有人和我一样的问题？请指教</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/cb/7c004188.jpg" width="30px"><span>和你一起搬砖的胡大爷</span> 👍（4） 💬（0）<div>对于熟悉线程模型的程序员来讲，如果不把时间循环解释清楚，协程确实很难理解。
我的理解协程在编程语言层面实现aio，只有io等待才切换上下文而不像线程按scheduler分片cpu在没必要的时候也切换上下文。不知道我理解的对不对。</div>2019-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7c/8a/bdeb76ac.jpg" width="30px"><span>Fergus</span> 👍（4） 💬（1）<div># -*- coding:utf-8 -*-
&#39;&#39;&#39;
sublime
py -3.6
asyncio.gather(*args) 并发
&#39;&#39;&#39;


import time
import asyncio

async def crawl_page(url):
    print(&#39;crawling {}&#39;.format(url))
    sleep_time = int(url.split(&#39;_&#39;)[-1])
    await asyncio.sleep(sleep_time)
    print(&#39;OK {}&#39;.format(url))
    
star = time.perf_counter()
loop = asyncio.get_event_loop()
tasks = (crawl_page(url) for url in [&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;])
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

print(&#39;Wall time: {:.2f}&#39;.format(time.perf_counter() - star))


crawling url_4
crawling url_1
crawling url_2
crawling url_3
OK url_1
OK url_2
OK url_3
OK url_4
Wall time: 4.00
[Finished in 4.5s]</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/42/cd/09b568fc.jpg" width="30px"><span>JabariH</span> 👍（3） 💬（0）<div>对“解密协程运行时”那部分下的程序执行做一个解释，欢迎大家指正：
1. asyncio.run(main())程序进入main函数，**事件循环**[main --&gt; task1 --&gt; task2 --&gt;tas3 --&gt; main]开启；
2. task_1、task_2、task_3任务被创建，并进入事件循环等待运行；
3. 主程序运行到await asyncio.sleep(2)，await 导致主程序被阻塞2s，此时事件调度器将控制权从主任务交给task_1(asyncio是根据任务创建顺序来赋予任务控制权的，相当于一个queue，先进先出)，并记录主程序运行到的位置；
4. 进入task1，输出“asyncio in task1”，后运行到asyncio.sleep(1)，程序被阻塞，事件调度器将控制权从task1交给task2，并记录task1程序运行到的位置；
5. 同样，task2输出“asyncio in task2”后运行到await asyncio.sleep(2)，被阻塞，记录task2程序运行到的位置，事件调度器开始调度task3；
6. 同理，task3输出“asyncio in task3”后运行到await asyncio.sleep(3)，被阻塞，记录程序阻塞的位置，事件调度器控制权又交回给主程序；
7. 此时，主程序还在被阻塞当中，事件调度器又按顺序开始调度task1；
8. 当时间接近1s的时候，task1开始接着上次运行到的位置往下运行，返回1，task1从事件循环中退出；
9. 当时间接近2s的时候，task2开始接着上次运行到的位置往下运行，返回2，task2从事件循环中退出；
10. 当时间接近3s的时候，由于主程序比task3早开始阻塞，所以主程序比task3先一步解除阻塞，事件调度器将控制权交给主程序，主程序从上次运行到的位置开始往下运行，取消task3任务，task3将不会有返回值，主程序从事件循环中退出，此时程序执行完毕。</div>2021-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/f9/3e/0d5f27c4.jpg" width="30px"><span>肥猫不开心</span> 👍（3） 💬（0）<div>网页改了，最新同步爬虫
import requests
from bs4 import BeautifulSoup

def main():
    url = &quot;https:&#47;&#47;movie.douban.com&#47;cinema&#47;later&#47;beijing&#47;&quot;
    headers = {&#39;User-Agent&#39;: r&#39;Mozilla&#47;5.0 (Windows NT 10.0; WOW64) AppleWebKit&#47;537.36 (KHTML, like Gecko) Chrome&#47;91.0.4472.164 Safari&#47;537.36&#39;}
    init_page = requests.get(url, headers=headers).content
    init_soup = BeautifulSoup(init_page, &#39;lxml&#39;)
    all_movies = init_soup.find(&#39;div&#39;, id=&quot;showing-soon&quot;)
    for each_movie in all_movies.find_all(&#39;div&#39;, class_=&quot;intro&quot;):
        all_a_tag = each_movie.find_all(&#39;a&#39;)
        all_li_tag = each_movie.find_all(&#39;li&#39;)

        movie_name = all_a_tag[0].text
        url_to_fetch = all_a_tag[0][&#39;href&#39;]
        movie_date = all_li_tag[0].text

        response_item = requests.get(url_to_fetch, headers=headers).content
        soup_item = BeautifulSoup(response_item, &#39;lxml&#39;)
        img_tag = soup_item.find(&#39;div&#39;, id=&#39;mainpic&#39;).find(&#39;img&#39;)

        print(&#39;{} {} {}&#39;.format(movie_name, movie_date, img_tag[&#39;src&#39;]))

main()</div>2021-08-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/gKnIR8mga02s9xdQoxyJBibmuxHGhfQ8WZicia3Ie4wBQKg4Zc1oVoS03mvaCD46je9xCza25qXc3w6KMckpS0BqQ/132" width="30px"><span>supakito</span> 👍（3） 💬（3）<div>对于这段代码：

import asyncio

async def worker_1():
    print(&#39;worker_1 start&#39;)
    await asyncio.sleep(1)
    print(&#39;worker_1 done&#39;)

async def worker_2():
    print(&#39;worker_2 start&#39;)
    await asyncio.sleep(2)
    print(&#39;worker_2 done&#39;)

async def main():
    task1 = asyncio.create_task(worker_1())
    task2 = asyncio.create_task(worker_2())
    print(&#39;before await&#39;)
    await task1
    print(&#39;awaited worker_1&#39;)
    await task2
    print(&#39;awaited worker_2&#39;)

%time asyncio.run(main())

########## 输出 ##########

before await
worker_1 start
worker_2 start
worker_1 done
awaited worker_1
worker_2 done
awaited worker_2
Wall time: 2.01 s

我对老师的解释有些疑问，不知道是不是只要创建了任务以后，不用执行await，就会运行worker_1和worker_2中的代码，因为我注释掉了await语句后，发现仍然会输出worker_1 done和worker_2 done。所有老师的第三步应该不是调度worker_1，而是等待worker_1执行完成？</div>2019-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/de/4c/a51ece16.jpg" width="30px"><span>刘润森</span> 👍（3） 💬（1）<div> asyncio.run() cannot be called from a running event loop</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/03/c0fe1dbf.jpg" width="30px"><span>考休</span> 👍（3） 💬（0）<div>翻阅评论，发现大家也有相似的问题，就是在老师的第二个代码块中，代码：
%time asyncio.run(main([&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;]))
这行代码因为前面有%time语法糖，所以大家想当然就在jupyter中执行了，但是很多人都遇到了：
RuntimeError: asyncio.run() cannot be called from a running event loop 
查阅Stack Overflow的解释jupyter已经一个event loop（https:&#47;&#47;stackoverflow.com&#47;questions&#47;55409641&#47;asyncio-run-cannot-be-called-from-a-running-event-loop），因此需要将代码改成：
await main([&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;])，而且不能在await前面加%time，否则会报错：
SyntaxError: &#39;await&#39; outside function
新手学习协程感觉各种懵（苦笑脸）</div>2019-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/f8/3c0a6854.jpg" width="30px"><span>xavier</span> 👍（3） 💬（1）<div>老师你好，请教个问题。如下：

文中代码：

async def main():
    task1 = asyncio.create_task(worker_1())
    task2 = asyncio.create_task(worker_2())
    print(&#39;before await&#39;)
    await task1
    print(&#39;awaited worker_1&#39;)
    await task2
    print(&#39;awaited worker_2&#39;)

请问调度器从何时开始启动调度？是一有任务创建就执行调度还是执行await task1时？老师这里说的是执行await task1，事件调度器开始调度 worker_1。但后面的生产者消费者模型，没有await操作，任务已开始运行。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7c/8a/bdeb76ac.jpg" width="30px"><span>Fergus</span> 👍（3） 💬（0）<div># 例1   3.7以前的版本实现
import time
import asyncio

# &lt; py 3.7
async def crawl_page(url):
    print(&#39;crawling {}&#39;.format(url))
    sleep_time = int(url.split(&#39;_&#39;)[-1])
    r = await asyncio.sleep(sleep_time)
    print(&#39;OK {}&#39;.format(url))

async def main(urls):
    for url in urls:
        await crawl_page(url)
        
star = time.perf_counter()
loop = asyncio.get_event_loop()
loop.run_until_complete(main([&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;]))
loop.close()
# await main([&#39;url_1&#39;, &#39;url_2&#39;, &#39;url_3&#39;, &#39;url_4&#39;])
print(time.perf_counter() - star)


crawling url_1
OK url_1
crawling url_2
OK url_2
crawling url_3
OK url_3
crawling url_4
OK url_4
10.003888006104894</div>2019-06-26</li><br/>
</ul>