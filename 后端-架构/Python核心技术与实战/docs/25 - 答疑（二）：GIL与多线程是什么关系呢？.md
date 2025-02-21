你好，我是景霄。

不知不觉中，我们又一起完成了第二大章进阶篇的学习。我非常高兴看到很多同学一直在坚持积极地学习，并且留下了很多高质量的留言，值得我们互相思考交流。也有一些同学反复推敲，指出了文章中一些表达不严谨或是不当的地方，我也表示十分感谢。

大部分留言，我都在相对应的文章中回复过了。而一些手机上不方便回复，或是很有价值很典型的问题，我专门摘录了出来，作为今天的答疑内容，集中回复。

## 问题一：列表self append无限嵌套的原理

![](https://static001.geekbang.org/resource/image/9d/a0/9d6c8c7a5adc13e9119d08dc3f1052a0.png?wh=1534%2A950)

先来回答第一个问题，两个同学都问到了，下面这段代码中的x，为什么是无限嵌套的列表？

```
x = [1]
x.append(x)
x
[1, [...]]
```

我们可以将上述操作画一个图，便于你更直观地理解：

![](https://static001.geekbang.org/resource/image/00/5f/001a607f3f29f68975be3e706711325f.png?wh=764%2A298)

这里，x指向一个列表，列表的第一个元素为1；执行了append操作后，第二个元素又反过来指向x，即指向了x所指向的列表，因此形成了一个无限嵌套的循环：\[1, \[1, \[1, \[1, …]]]]。

不过，虽然x是无限嵌套的列表，但x.append(x)的操作，并不会递归遍历其中的每一个元素。它只是扩充了原列表的第二个元素，并将其指向x，因此不会出现stack overflow的问题，自然不会报错。

至于第二点，为什么len(x)返回的是2？我们还是来看x，虽然它是无限嵌套的列表，但x的top level只有2个元素组成，第一个元素为1，第二个元素为指向自身的列表，因此len(x)返回2。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/f9/caf27bd3.jpg" width="30px"><span>大王叫我来巡山</span> 👍（6） 💬（1）<div>第一次完全明白GIL，照顾方便性的同时在实现上偷了懒，但是本身设计就是解决特定问题，而不是解决所有问题的，但是随着受众的增多，是会发展变化，就行脚本语言中引入类型系统，编译型语言中引入类型推断，都是为了语言更好的发展。</div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ba/3c/2b642c9a.jpg" width="30px"><span>new</span> 👍（5） 💬（1）<div>目前项目不用python看过了似乎是懂了，过一段时间又啥都想不起来了，学习最好的方式是边学边用，可是没机会用。感觉老师确实底蕴深厚呀，好多东西对老师来说似乎很简单，比如图，有向图，有向边，我都不懂呀，感觉差的好多好多</div>2019-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/62/1f/cd1cbdb1.jpg" width="30px"><span>晓冰</span> 👍（3） 💬（2）<div>老师你好，python同一时刻只能执行一个线程，那么多核cpu的场景下就没办法充分利用硬件资源，我们在生产环境中是怎么玩的呢？</div>2019-08-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqEacia8yO1dR5Tal9B7w8PzTRrViajlAvDph96OqcuBGe29icbXOibhibGmaBcO7BfpVia0Y8ksZwsuAYQ/132" width="30px"><span>杰洛特</span> 👍（1） 💬（1）<div>请教老师，对于网络请求等待较多的场景，是不是也参考I&#47;O密集型任务，采用多线程好一些？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（21） 💬（3）<div>看到这，终于搞明白多线程和协程的差异，感谢老师。</div>2019-07-05</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（8） 💬（1）<div>我个人认为，线程是CPU调度的最小单元，但是Python，因为GIL的存在让并行无法在线程这个粒度上运行，只好在更大粒度的进程上并行，进程切换的代价比线程大，Python并行的效率低于支持多线程同时在多核上跑的语言。协程是在一个线程内调度资源，无法实现并行，但对IO操作有效，也就是说可以并发利用CPU和IO资源，但是无法并行利用多个CPU资源。我的观点是否正确，请老师指正。</div>2019-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/18/be/aa622bf8.jpg" width="30px"><span>爱学习的小迪</span> 👍（2） 💬（0）<div>在多核CPU的场景下，多线程可以充分利用CPU，实现并行；但是Python由于存在GIL，要求同一个时刻只能有一个线程运行，从而导致无法利用多核CPU的优势，也就是造成了“伪并行”；
GIL只存在于CPython解释器中。主要出于Python的内存管理和CPython大量使用线程不安全的C库的角度来考虑引入GIL</div>2022-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/94/c8bc2b59.jpg" width="30px"><span>yshan</span> 👍（2） 💬（0）<div>继续加油，虽然学习了后面，前面有些已经忘记了，还是需要多复习和实践</div>2019-07-05</li><br/><li><img src="" width="30px"><span>min</span> 👍（1） 💬（1）<div>老师，前次讲的垃圾回收之分代回收，系统默认第二代和第三代阈值为10；对于一个系统来说，这么多全局变量，那么第二代和三代不就在一直很高频的回收？</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第25讲打卡~</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/6f/4f/3cf1e9c4.jpg" width="30px"><span>钱鹏 Allen</span> 👍（0） 💬（0）<div>多线程并不代表cpu同时让多个线程在同一时间一起跑，而是每次执行一个任务</div>2022-11-21</li><br/><li><img src="" width="30px"><span>吴昊</span> 👍（0） 💬（0）<div>对问题一中的x,为什么x==x，没有触发异常？或者说，__eq__()函数在遍历列表元素前还做了其他事情吧，这个事情是什么呢？</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/fa/60/a4366b9c.jpg" width="30px"><span>ZY</span> 👍（0） 💬（0）<div>Python 中进程，线程，协程分别应用于哪些日常开发中的场景呢</div>2021-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/c2/4c/01a6ef47.jpg" width="30px"><span>晓骏</span> 👍（0） 💬（0）<div>老师，学习python量化是要立即订阅吗？我怎么按了立即订阅跳出来是Python核心技术与实战？和量化有关系吗？</div>2020-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/31/bb/26fa71ce.jpg" width="30px"><span>isaiahqian</span> 👍（0） 💬（0）<div>老师，想提供GPU预测的异步接口，这个属于IO密集还是CPU密集？主要计算是使用GPU，不在CPU，而且最后返回结果需要从GPU搬回CPU，应该属于IO操作。所以用多线程更合适？</div>2019-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/b0/26c0e53f.jpg" width="30px"><span>贺宇</span> 👍（0） 💬（0）<div>在单核单线程的计算机下，是不是任何语言的多线程都是分时间片来操作，也就是所说的伪并行。但是Python的多线程无论在几核计算机下都是单进程在跑，而别的语言的多线程会调用多进程。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/d4/bdd3ed27.jpg" width="30px"><span>converse✪</span> 👍（0） 💬（0）<div>之前不是说io slow的时候用asyncio，heavy的时候用多线程么？为啥这里说heavy用asyncio？</div>2019-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0d/45/b88a1794.jpg" width="30px"><span>一叶知秋</span> 👍（0） 💬（0）<div>感觉问题三非常类似单核cpu的时间片轮转算法</div>2019-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（0） 💬（1）<div>&gt;&gt;&gt; x = [1]
&gt;&gt;&gt; y = [1]
&gt;&gt;&gt; x.append(x)
&gt;&gt;&gt; x == x
True
&gt;&gt;&gt; x == y
False
&gt;&gt;&gt; x
[1, [...]]
&gt;&gt;&gt; y
[1]

第一个同学所说的无限递归问题，我这试了下并未出现，Python 3.7.1</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/43/2d/af86d73f.jpg" width="30px"><span>enjoylearning</span> 👍（0） 💬（3）<div>asyncio这是要代替requests的节奏？

</div>2019-07-05</li><br/>
</ul>