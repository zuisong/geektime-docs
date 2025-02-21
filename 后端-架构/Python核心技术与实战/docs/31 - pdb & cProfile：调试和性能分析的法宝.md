你好，我是景霄。

在实际生产环境中，对代码进行调试和性能分析，是一个永远都逃不开的话题。调试和性能分析的主要场景，通常有这么三个：

- 一是代码本身有问题，需要我们找到root cause并修复；
- 二是代码效率有问题，比如过度浪费资源，增加latency，因此需要我们debug；
- 三是在开发新的feature时，一般都需要测试。

在遇到这些场景时，究竟应该使用哪些工具，如何正确的使用这些工具，应该遵循什么样的步骤等等，就是这节课我们要讨论的话题。

## 用pdb进行代码调试

### pdb的必要性

首先，我们来看代码的调试。也许不少人会有疑问：代码调试？说白了不就是在程序中使用print()语句吗？

没错，在程序中相应的地方打印，的确是调试程序的一个常用手段，但这只适用于小型程序。因为你每次都得重新运行整个程序，或是一个完整的功能模块，才能看到打印出来的变量值。如果程序不大，每次运行都非常快，那么使用print()，的确是很方便的。

但是，如果我们面对的是大型程序，运行一次的调试成本很高。特别是对于一些tricky的例子来说，它们通常需要反复运行调试、追溯上下文代码，才能找到错误根源。这种情况下，仅仅依赖打印的效率自然就很低了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/67/bf286335.jpg" width="30px"><span>AllenGFLiu</span> 👍（15） 💬（5）<div>哥，不怀好意的问一下，你们在谷歌会用微软的vscode 吗？[奸笑脸]
每次看你都是提到pycharm ,我是从pycharm 转到vscode 上的，感觉整个世界都安静了。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（4） 💬（3）<div>我要把这个装饰器保存下来</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/85/e7/5c351369.jpg" width="30px"><span>321</span> 👍（2） 💬（2）<div>web 应用怎么调试？譬如flask或django框架开发的应用，该如何调试。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f7/f8/3c0a6854.jpg" width="30px"><span>xavier</span> 👍（1） 💬（1）<div>对应到C、C++就是gdb。现在被IDE给宠坏了，感觉还是Command Line纯粹。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（81） 💬（6）<div>全文这个装饰器最牛逼。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4b/36/ed40fb3a.jpg" width="30px"><span>(￣_￣ )</span> 👍（10） 💬（0）<div>和gdb的命令差不多</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/5b/10/0a326331.jpg" width="30px"><span>frozen</span> 👍（9） 💬（0）<div>您好，pdb调试多线程的时候目前还不支持吧</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/43/dc/4f70c936.jpg" width="30px"><span>一只眼看世界</span> 👍（8） 💬（2）<div>dict1 = {}
def fibl(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return (fibl(n-1) if n-1 not in dict1 else dict1[n-1]) + (fibl(n-2) if n-2 not in dict1 else dict1[n-2])

def all_fib(n):
    global dict1
    res =[]
    for i in range(n + 1):
        req = fibl(i)
        dict1[i] = req
        res.append(req)
    print(res)
all_fib(100000)

老师用的装饰器很高大上(看了好几遍才搞明白), 但是当数字大于995后会有超过递归深度报错, 所以过来皮一下&#47;狗头</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/cb/3162747a.jpg" width="30px"><span>JackLee</span> 👍（7） 💬（0）<div>还有一个ipdb是pdb的加强版，用法比较相近，不过需要pip安装一下</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/3c/2b642c9a.jpg" width="30px"><span>new</span> 👍（6） 💬（0）<div>老师应该在这里回顾一下装饰器的用法</div>2019-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/52/a37d2689.jpg" width="30px"><span>泥土  </span> 👍（5） 💬（3）<div>看到memoize装饰器，想起装饰器那节中的LRU_CACHE，发现比memoize性能更高
import functools

@memoize
# @functools.lru_cache(None)
def fib(n):
    ...</div>2020-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8f/84/2c2d8c47.jpg" width="30px"><span>lipan</span> 👍（5） 💬（1）<div>最近在用js撸小程序，一个console.log()搞定所有调试。</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/3a/cdf9c55f.jpg" width="30px"><span>未来已来</span> 👍（4） 💬（1）<div>被最后那个装饰器惊艳到了，以前只知道用循环，没想到 Python 还可以这么玩</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/84/70340e87.jpg" width="30px"><span>向南</span> 👍（3） 💬（0）<div>有时候会用装饰器试一下
def timeit_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func_return_value = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(&#39;{0:&lt;10}.{1:&lt;8} : {2:&lt;8}&#39;.format(func.__module__, func.__name__, end_time - start_time))
        return func_return_value
    return wrapper

@timeit_wrapper
def some_func():
    ....</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/c5/3e/2bb7edc9.jpg" width="30px"><span>一一</span> 👍（3） 💬（0）<div>cProfile真的太好用了</div>2020-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（3） 💬（0）<div>多数是直接用IDE里的功能来调试，另外用过Linux里的gdb。调优没用过，顶多在代码里直接计时。</div>2019-10-21</li><br/><li><img src="" width="30px"><span>天山</span> 👍（2） 💬（0）<div>到这儿已经忘记装饰器的用法了，赶紧回去复习下</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/10/28d5a686.jpg" width="30px"><span>Longerian</span> 👍（2） 💬（2）<div>cprofiles 里的 ncalls 为什么有些显示 31&#47;1，有些显示 31，这两种数值的含义分别是什么？</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ab/a8/eb9f186e.jpg" width="30px"><span>SuQiu</span> 👍（2） 💬（1）<div>PySnooper这个调试挺好。</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（0）<div>第31讲打卡~</div>2024-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/d0/ba/98bc816b.jpg" width="30px"><span>Shu🐹</span> 👍（1） 💬（0）<div>真是干货满满啊</div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c5/d7/f7a5775f.jpg" width="30px"><span>yupf</span> 👍（1） 💬（1）<div>这个装饰器稍微改改，就成单例模式了</div>2020-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/f6/7431e82e.jpg" width="30px"><span>xueerfei007</span> 👍（0） 💬（0）<div>老师您好，请问排查内存泄露有没有啥好用的工具推荐一下</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/28/678417c3.jpg" width="30px"><span>什么鬼额</span> 👍（0） 💬（0）<div>pdb程序要怎么中断呢？循环中的程序要怎么删除断点？</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/2d/8e4836f3.jpg" width="30px"><span>Bonaparte</span> 👍（0） 💬（0）<div>到了如何使用 pdb 就看不懂了</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/53/b74127fa.jpg" width="30px"><span>Jola💦</span> 👍（0） 💬（0）<div>老师  想问一下  假如一个问题在线上出现平常基本不复现有什么好方法可以在线调试</div>2021-03-31</li><br/><li><img src="" width="30px"><span>Geek_d848f7</span> 👍（0） 💬（0）<div>get到新方法，我只用过print、断点、装饰器的方式，print用得最多(😓）</div>2019-07-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/szNEybCR1Al4p6eDyT8atNjen7ZY9cBJSXOQl1EnrTM2efiaHlPtL7X44JeibXs9qEFLWv6HJWBwq5tVlNahGDGQ/132" width="30px"><span>leixin</span> 👍（0） 💬（0）<div>ipython  好像也带debug模式</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/44/3d/35d6670d.jpg" width="30px"><span>Claywoow</span> 👍（0） 💬（0）<div>最近工作的一段时间一直在用pdb调试。。。pdb大法好啊 : )</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ee/03/09926387.jpg" width="30px"><span>🇨🇳</span> 👍（0） 💬（0）<div>老师您好，最近使用requests.get方法遇到一个问题，返回结果部分内容是“&lt;noscript&gt;You need to enable JavaScript to run this app.&lt;&#47;noscript&gt;”，请问您遇到过这种情况吗，怎么解决呢。谢谢</div>2019-07-19</li><br/>
</ul>