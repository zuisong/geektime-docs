你好，我是景霄。

无论对于哪门语言，并发编程都是一项很常用很重要的技巧。比如我们上节课所讲的很常见的爬虫，就被广泛应用在工业界的各个领域。我们每天在各个网站、各个App上获取的新闻信息，很大一部分便是通过并发编程版的爬虫获得。

正确合理地使用并发编程，无疑会给我们的程序带来极大的性能提升。今天这节课，我就带你一起来学习理解、运用Python中的并发编程——Futures。

## 区分并发和并行

在我们学习并发编程时，常常同时听到并发（Concurrency）和并行（Parallelism）这两个术语，这两者经常一起使用，导致很多人以为它们是一个意思，其实不然。

首先你要辨别一个误区，在Python中，并发并不是指同一时刻有多个操作（thread、task）同时进行。相反，某个特定的时刻，它只允许有一个操作发生，只不过线程/任务之间会互相切换，直到完成。我们来看下面这张图：

![](https://static001.geekbang.org/resource/image/37/3f/37cbce0eb67909990d83f21642fb863f.png?wh=1620%2A524)

图中出现了thread和task两种切换顺序的不同方式，分别对应Python中并发的两种形式——threading和asyncio。

对于threading，操作系统知道每个线程的所有信息，因此它会做主在适当的时候做线程切换。很显然，这样的好处是代码容易书写，因为程序员不需要做任何切换操作的处理；但是切换线程的操作，也有可能出现在一个语句执行的过程中（比如 x += 1），这样就容易出现race condition的情况。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（73） 💬（4）<div>思考题：
1. request.get 会触发：ConnectionError, TimeOut, HTTPError等，所有显示抛出的异常都是继承requests.exceptions.RequestException 
2. executor.map(download_one, urls) 会触发concurrent.futures.TimeoutError
3. result() 会触发Timeout，CancelledError
4. as_completed() 会触发TimeOutError</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/84/7d21bd9e.jpg" width="30px"><span>Goal</span> 👍（11） 💬（1）<div>学习到的知识点：
1. 并发和并行的区别，大佬通俗易懂的方式让我更深刻的体会到了程序到底是如何跑在多核机器上的
2. python中 Futures 特性，第一次接触到这个模块，待后续继续加深了解；
3. Python 中之所以同一时刻只允许一个线程运行，大佬解释了这是因为全局解释器锁的存在，而全局解释器锁又是为了解决 race condition而引入的，这个也从另一方面验证了我之前学习到的，python中多线程是无法利用多核的； 
但是多线程无法利用多核也并不是一无是处，就像大佬在文中聊到的，多线程主要的适用场景就是 有IO延迟的场景，因为一个线程遇到IO延迟，它占用的全局解释器锁就会释放，而另一个线程即可以拿到锁开始执行； 这种在IO延迟场景中的并发，高效也是显而易见的；</div>2020-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/03/370ebbc8.jpg" width="30px"><span>Steve</span> 👍（7） 💬（1）<div>老师，我有一个很类似的场景。之前我用单线程去下载所有页面。然后在每个页面解析出需要的内容放入一个集合里。如果改成并发的实现，多线程写一个集合(写文件也类似)，是不是有线程安全的问题。有没有小例子可以学习一下~</div>2020-05-15</li><br/><li><img src="" width="30px"><span>Geek_5bb182</span> 👍（7） 💬（1）<div>老师你好，concurrent.futures 和 asyncio 中的Future 的区别是什么，在携程编程中</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/96/7d/c7e8cd34.jpg" width="30px"><span>干布球</span> 👍（4） 💬（3）<div>请问老师，future任务是调用submit后就开始执行，还是在调用as_completed之后才开始执行呢？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3f/6a/9dba4488.jpg" width="30px"><span>简传宝</span> 👍（3） 💬（1）<div>老师好，请问是否可以理解为计算密集型任务用多进程，io密集型用多线程</div>2019-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（3） 💬（3）<div>总结下并发和并行的概念：

并发，是指遇到I&#47;O阻塞时（一般是网络I&#47;O或磁盘I&#47;O），通过多个线程之间切换执行多个任务（多线程）或单线程内多个任务之间切换执行的方式来最大化利用CPU时间，但同一时刻，只允许有一个线程或任务执行。适合I&#47;O阻塞频繁的业务场景。

并行，是指多个进程完全同步同时的执行。适合CPU密集型业务场景。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（3） 💬（4）<div>老师好，请问一下在python存在GIL的情况下，多进程是不是还是无法并发运行？谢谢老师</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/91/65ff3154.jpg" width="30px"><span>_stuView</span> 👍（2） 💬（1）<div>老师，请问什么是线程安全，什么是race condition呢？</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/fc/c26b6207.jpg" width="30px"><span>MarDino</span> 👍（1） 💬（1）<div>想问下老师，该怎么向executor.map中的函数，传入多个参数？</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5a/65/cbe70852.jpg" width="30px"><span>BotterZhang</span> 👍（47） 💬（4）<div>关于concurrent写过一篇学习笔记：
https:&#47;&#47;www.zhangqibot.com&#47;post&#47;python-concurrent-futures&#47;
Python实现多线程&#47;多进程，大家常常会用到标准库中的threading和multiprocessing模块。
但从Python3.2开始，标准库为我们提供了concurrent.futures模块，它提供了ThreadPoolExecutor和ProcessPoolExecutor两个类，实现了对threading和multiprocessing的进一步抽象，使得开发者只需编写少量代码即可让程序实现并行计算。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（30） 💬（0）<div>future之与中文理解起来其实挺微妙，不过这与生活中大家熟知的期物在底层逻辑上是一致的，future英文词义中就有期货的意思，都是封存一个东西，平常你该干嘛就干嘛，可以不用去理会，在未来的某个时候去看结果就行，只是python中那个物是对象而已。而关键词是延迟，异步。
思考题：添加异常处理
def download_all(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        to_do = {}
        for site in sites:
            future = executor.submit(download_one, site)    
            to_do[future]=site
            
        for future in concurrent.futures.as_completed(to_do):
            try：
                res=future.result()
            except request.exceptions.HTTPError as e:
                e_msg=‘HTTP erro’
            except request.exceptions.ConnectionError as e:
                e_msg=‘Connection erro’
            else:
                e_msg=&#39;&#39;
            if  e_msg:
                site=to_do[future]
                Print(‘Error is {} from {}’.format(e_msg,site))
</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/f9/caf27bd3.jpg" width="30px"><span>大王叫我来巡山</span> 👍（14） 💬（8）<div>老师，我感觉您对并发和并行的理解是有问题的，并发是针对最初的单核CPU的，并行是针对现代的多核CPU，并且所有的调度行为都是基于线程的，一个进程中至少有一个线程，资源的分配是基与进程的，并不是只有多进程模型才可以同时在多个核心上运行的。</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7c/8a/bdeb76ac.jpg" width="30px"><span>Fergus</span> 👍（7） 💬（3）<div>需要加异常的应该就只有一个地方：requests.get()发送网页请求的时候。其它地方不涉及IO。也不涉及数据类型变化，不用做数据类型判断。
由于不能访问wiki，所以网页改了成了国内的。
-- ps: 和0.2s比起来太慢了。

# -*- encoding -*-
&#39;&#39;&#39;
py 3.6
sulime
&#39;&#39;&#39;
import concurrent.futures
import threading
import requests
import time

now = lambda: time.perf_counter()

def download_one(url):
    try:
        req = requests.get(url)
        req.raise_for_status()
        print(&#39;Read {} from {}&#39;.format(len(req.content), url))
    except:
        print(&#39;404&#39;)

def download_all(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_one, sites)

def main():
    sites = [
            &#39;https:&#47;&#47;www.baidu.com&#47;&#39;,
            &#39;https:&#47;&#47;pypi.org&#47;&#39;,
            &#39;https:&#47;&#47;www.sina.com.cn&#47;&#39;,
            &#39;https:&#47;&#47;www.163.com&#47;&#39;,
            &#39;https:&#47;&#47;news.qq.com&#47;&#39;,
            &#39;http:&#47;&#47;www.ifeng.com&#47;&#39;,
            &#39;http:&#47;&#47;www.ce.cn&#47;&#39;,
            &#39;https:&#47;&#47;news.baidu.com&#47;&#39;,
            &#39;http:&#47;&#47;www.people.com.cn&#47;&#39;,
            &#39;http:&#47;&#47;www.ce.cn&#47;&#39;,
            &#39;https:&#47;&#47;news.163.com&#47;&#39;,
            &#39;http:&#47;&#47;news.sohu.com&#47;&#39;
            ]
    start = now()
    download_all(sites)
    print(&#39;Download {} sites in {} s&#39;.format(len(sites), now() - start))

if __name__ == &#39;__main__&#39;:
    main()

# Read 2443 from https:&#47;&#47;www.baidu.com&#47;
# Read 6216 from https:&#47;&#47;news.qq.com&#47;
# Read 699004 from https:&#47;&#47;www.163.com&#47;
# Read 250164 from http:&#47;&#47;www.ifeng.com&#47;
# Read 579572 from https:&#47;&#47;www.sina.com.cn&#47;
# Read 107530 from http:&#47;&#47;www.ce.cn&#47;
# Read 165901 from http:&#47;&#47;www.people.com.cn&#47;
# Read 107530 from http:&#47;&#47;www.ce.cn&#47;
# Read 210816 from https:&#47;&#47;news.163.com&#47;
# Read 74060 from https:&#47;&#47;news.baidu.com&#47;
# Read 174553 from http:&#47;&#47;news.sohu.com&#47;
# Read 19492 from https:&#47;&#47;pypi.org&#47;
# Download 12 sites in 2.8500169346527673 s
# [Finished in 3.6s]</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（4） 💬（1）<div>from multiprocessing.dummy import Pool as ThreadPool
with ThreadPool(processes=100) as executor:
    executor.map(func, iterable)

请问老师，Futures 和这种方式哪一种好呢？ 我在实际的网终请求中发现 Futures 请求成功的次数更少。 都是 100 个线程，处理 3000 个相同的请求。 
</div>2019-07-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er1RdQnOhMLv7dAwpBLAoUOM8icEnH8b1oSZ0cSYoryM6ng5cHcnsRRhYRny8NlrjuaQuOWy4e9Yqw/132" width="30px"><span>羁绊</span> 👍（3） 💬（0）<div>在使用executor.map()时候假如上面sites里面的url有链接超时报错的话，ThreadPoolExecutor会隐藏该异常，这个线程会在没有任何输出的情况下终止，然后线程继续执行</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7c/8a/bdeb76ac.jpg" width="30px"><span>Fergus</span> 👍（3） 💬（2）<div>老师好，看到文中为了使用.as_complete()作的修改似乎做了重复的工作，我对比了使用.as_complete()和.submit()后直接result()，得到的是相同的结果。
-- 问1：这里所做的修改只是为了展示.as_complete的功能么？我查看了文档也没想明白。
-- 问2：.as_complete()可能会在什么场景下使用得比较多？

eg.2.`.submit()`后直接`.result()`
	
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for site in sites:
            future = executor.submit(download_one, site)
            print(future.result())</div>2019-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e3/f1/346bd356.jpg" width="30px"><span>Bruce</span> 👍（1） 💬（0）<div>老师，最近在实际的工程里面用到ProcessPoolExecutor，碰到这个问题：
concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly while the future was running or pending.
怎么解决呢？
补充说明一下，我是flask应用，进程池是在某个模块的类方法里使用的</div>2022-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/5b/13/6db9ba58.jpg" width="30px"><span>Kevin</span> 👍（1） 💬（0）<div>异常处理：
def download_one_2(url):
    resp = None
    try:
        resp = requests.get(url, timeout=(3,7))
        resp.raise_for_status()
        resp.encoding = resp.apparent_encoding
    except requests.exceptions.ConnectTimeout:
        print(&#39;超时！&#39;)
    except requests.exceptions.ConnectionError:
        print(&#39;无效地址！&#39;)
    except requests.ConnectionError:
        print(&#39;超时！&#39;)
    except urllib3.exceptions.NewConnectionError:
        print(&quot;NewConnectionError&quot;)
    except urllib3.exceptions.MaxRetryError:
        print(&quot;超出最大重试次数&quot;)

    print(&#39;Read {} from {}&#39;.format(len(resp.content), url))</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/42/d7/1f1634af.jpg" width="30px"><span>无才不肖生</span> 👍（1） 💬（0）<div>在submit()后只是放入队列而并未真正开始执行，as_completed时才真正去执行，对吗？
as_completed会不会有个别future并执行完而没有输出结果，还是说就一定都会完成</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（0） 💬（0）<div>怎么知道是计算密集型还是IO密集型？</div>2024-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第21讲打卡~</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7c/ad/57b768f7.jpg" width="30px"><span>曾彪彪</span> 👍（0） 💬（0）<div>因为全局解释器锁的存在，Python中同一时刻只有一个线程在工作，这是不是意味着Python 多线程没有race condition?</div>2022-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/58/c2/51fa1f28.jpg" width="30px"><span>GEEKBANG_9388667</span> 👍（0） 💬（0）<div>老师 生成器和future可以一起使用吗？我用生成器打印出10G的文件，可以加入future之后就出现内存溢出情况</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4a/23/6800a1b6.jpg" width="30px"><span>麥白</span> 👍（0） 💬（0）<div>进阶篇得反反复复看和实践体会～</div>2022-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/b7/bf/815f0ec6.jpg" width="30px"><span>H.H</span> 👍（0） 💬（0）<div>思考题：
def download_one(url)-&gt;str:
    try:
        resp = requests.get(url)
        print(&quot;Read {} from {}&quot;.format(len(resp.content),url))
        return resp.content
    except requests.exceptions.RequestException as e:
        print(e)
        return &#39;error&#39;
    except:
        return &#39;error&#39;

def download_all(sites):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        to_do = []
        
        for site in sites:
            future = executor.submit(download_one,site)
            to_do.append(future)
        
        error_list = []
        try:
        
            for future in concurrent.futures.as_completed(to_do,timeout=0.5):
                result = future.result(timeout=0.1)
                print(len(result))
        except concurrent.futures.TimeoutError as e:
            print(&quot;time out:{}&quot;.format(e))
        except concurrent.futures.CancelledError as e:
            print(&quot;cancel error:{}&quot;.format(e))
            print(e)
        except Exception as e:
            print(&quot;other error:{}&quot;.format(e))
            </div>2021-11-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er67Ir89QuLrBQBfibYGKoUqOayBGZFMqc8lraFIdoIxZNTtdOBPxbGVZtZB7bplfa1oL2J5HEuQFQ/132" width="30px"><span>尚微</span> 👍（0） 💬（1）<div>多线程程序是在线程之间来回切换运行的，那为什么采用多线程编程还能提高效率呢</div>2021-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（0） 💬（0）<div>简单完成了以下思考题：
---

def download_all_as_completed(sites):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        to_do = []
        for site in sites:
            future = executor.submit(download_one, site)
            to_do.append(future)

        for future in concurrent.futures.as_completed(to_do, timeout=1):
            try:
                result = future.result()
            except Exception as exc:
                print(&#39;&lt;xx&gt; Threw an exception: %s&#39; % (exc))
            else:
                print(&#39;&lt;-- Read {} from {}&#39;.format(result[1], result[0]))

def download_all_with_callback(sites):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for site in sites:
            future = executor.submit(download_one, site)
            future.add_done_callback(done_callback)

def done_callback(future):
    try:
        result = future.result()
    except Exception as exc:
        print(&#39;&lt;xx&gt; Threw an exception: %s&#39; % (exc))
    else:
        if result is not None:
            print(&#39;&lt;-- Read {} from {}&#39;.format(result[1], result[0]))
</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/01/5ce8ce0b.jpg" width="30px"><span>Leoorz</span> 👍（0） 💬（1）<div>今天尝试了对之前的一个CPU-bound的工程进行多进程的重构，遇到了一些问题，来分享一下过程及遇到的问题
问题背景:将多个json格式的文件读入并并行处理，最终输出到一个excel中，每个json文件对应一个excel的sheet
改造方式:
1. 每个json文件对应一类处理方式，已经抽象出了一个 BaseClass的process方法，多个SubClass继承该方法.
2. 子类实例化后，使用 futures.ProcessPoolExecutor 及 executor.submit(subclassItem.process, args) 的方式进行任务提交.
3. 为了防止subclassItem丢失从而找不到待写入excel中的数据，submit后，将subclassItem赋值给submit返回的future对象，以便在futures.as_completed的遍历时找到对象.
4. 子类处理process，将处理后待写入excel中的数据在process执行的最后写回子类的成员中
5. 待各process任务皆处理完毕后，遍历运行结束的futures，串行进行excel的sheet写入

问题1: 步骤3存入submit返回的future中的subclassItem的id，与进入subclassItem.process处理函数中看到的self的id不一致，这就导致步骤4回写的数据，与预期挂接的对象不是一个对象，从而回写的数据是空的，我在想是不是executor.submit(subclassItem.process, args)实际传入的对象是executor，但是同样打印了id，也不是相同的，所以就不清楚进入process处理函数中，实际的实例化对象是新创建的吗...
个人理解多进程的方式以对象方法的作为submit的方式应该是比较正常的使用场景，不知道自己哪里的使用姿势不对，网上也没找到讲类似的问题

问题2: 
步骤5目前对excel的最终写入仍然是串行的，因为最开始尝试了把写入excel的动作也放入多进程的处理任务接口中，报了错，应该是多个进程访问了同一个资源，不知道是否还有其他方式，各位老哥帮忙看看</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>由于全局解释器锁的存在,Python 中同一时刻只允许一个线程运行，对 I&#47;O 操作而言，当其被 block 的时候，全局解释器锁便会被释放，使其他线程继续执行。</div>2020-08-11</li><br/>
</ul>