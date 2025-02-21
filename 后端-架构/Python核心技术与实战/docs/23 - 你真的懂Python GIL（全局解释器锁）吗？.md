你好，我是景霄。

前面几节课，我们学习了Python的并发编程特性，也了解了多线程编程。事实上，Python多线程另一个很重要的话题——GIL（Global Interpreter Lock，即全局解释器锁）却鲜有人知，甚至连很多Python“老司机”都觉得GIL就是一个谜。今天我就来为你解谜，带你一起来看GIL。

## 一个不解之谜

耳听为虚，眼见为实。我们不妨先来看一个例子，让你感受下GIL为什么会让人不明所以。

比如下面这段很简单的cpu-bound代码：

```
def CountDown(n):
    while n > 0:
        n -= 1
```

现在，假设一个很大的数字n = 100000000，我们先来试试单线程的情况下执行CountDown(n)。在我手上这台号称8核的MacBook上执行后，我发现它的耗时为5.4s。

这时，我们想要用多线程来加速，比如下面这几行操作：

```
from threading import Thread

n = 100000000

t1 = Thread(target=CountDown, args=[n // 2])
t2 = Thread(target=CountDown, args=[n // 2])
t1.start()
t2.start()
t1.join()
t2.join()
```

我又在同一台机器上跑了一下，结果发现，这不仅没有得到速度的提升，反而让运行变慢，总共花了9.6s。

我还是不死心，决定使用四个线程再试一次，结果发现运行时间还是9.8s，和2个线程的结果几乎一样。

这是怎么回事呢？难道是我买了假的MacBook吗？你可以先自己思考一下这个问题，也可以在自己电脑上测试一下。我当然也要自我反思一下，并且提出了下面两个猜想。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（16） 💬（2）<div>思考题1：
由于GIL采用轮流运行线程的机制，GIL需要在线程之间不断轮流进行切换，线程如果较多或运行时间较长，切换带来的性能损失可能会超过单线程。

思考题2：
个人觉得GIL仍然是一种好的设计，虽然损失了一些性能，但在保证资源不发生冲突，预防死锁方面还是有一定作用的。

以上是个人的一点肤浅理解，请老师指正。</div>2019-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/37/8775d714.jpg" width="30px"><span>jackstraw</span> 👍（9） 💬（1）<div>关于绕过GIL的第二个方式：将关键的性能代码放到别的语言中（通常C++）实现；这种解决方式指的是在别的语言中使用多线程的方式处理任务么？就是不用python的多线程，而是在别的语言中使用多线程？</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/29/d6816ebf.jpg" width="30px"><span>小侠龙旋风</span> 👍（145） 💬（2）<div>先mark一下学到的知识点：
一、查看引用计数的方法：sys.getrefcount(a)
二、CPython引进GIL的主要原因是：
1. 设计者为了规避类似内存管理这样的复杂竞争风险问题（race condition）；
2. CPython大量使用C语言库，但大部分C语言库都不是线程安全的（线程安全会降低性能和增加复杂度）。
三、绕过GIL的两种思路：
1. 绕过CPython，使用JPython等别的实现；
2. 把关键性能代码放到其他语言中实现，比如C++。


问答老师的问题：
1. cpu-bound属于计算密集型程序，用多线程运行时，每个线程在开始执行时都会锁住GIL、执行完会释放GIL，这两个步骤比较费时。相比单线程就没有切换线程的问题，所以更快。
相反，在处理多阻塞高延迟的IO密集型程序时，因为多线程有check interval机制，若遇阻塞，CPython会强制当前线程让出（释放）GIL，给其他线程执行的机会。所以能提高程序的执行效率。
2. 第二个问题摘抄了知乎上的讨论：
在python3中，GIL不使用ticks计数，改为使用计时器（执行时间达到阈值后interval=15毫秒，当前线程释放GIL），这样对CPU密集型程序更加友好，但依然没有解决GIL导致的同一时间只能执行一个线程的问题，所以效率依然不尽如人意。多核多线程比单核多线程更差，原因是单核下多线程，每次释放GIL，唤醒的那个线程都能获取到GIL锁，所以能够无缝执行，但多核下，CPU0释放GIL后，其他CPU上的线程都会进行竞争，但GIL可能会马上又被CPU0拿到，导致其他几个CPU上被唤醒后的线程会醒着等待到切换时间后又进入待调度状态，这样会造成线程颠簸(thrashing)，导致效率更低。
经常会听到老手说：“python下想要充分利用多核CPU，就用多进程”，原因是什么呢？原因是：每个进程有各自独立的GIL，互不干扰，这样就可以真正意义上的并行执行，所以在python中，多进程的执行效率优于多线程(仅仅针对多核CPU而言)。所以我们能够得出结论：多核下，想做并行提升效率，比较通用的方法是使用多进程，能够有效提高执行效率。</div>2019-07-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/szNEybCR1Al4p6eDyT8atNjen7ZY9cBJSXOQl1EnrTM2efiaHlPtL7X44JeibXs9qEFLWv6HJWBwq5tVlNahGDGQ/132" width="30px"><span>leixin</span> 👍（41） 💬（3）<div>有重要的一点没讲，GIL会在遇到io的时候自动释放，给其他线程执行的机会，这样Python多线程在io阻塞的多任务中有效。</div>2019-07-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/szNEybCR1Al4p6eDyT8atNjen7ZY9cBJSXOQl1EnrTM2efiaHlPtL7X44JeibXs9qEFLWv6HJWBwq5tVlNahGDGQ/132" width="30px"><span>leixin</span> 👍（34） 💬（1）<div>老师，我曾经去某大厂面试。人家问了我几个问题，比说说，你知道元类吗？Python是如何解决循环引用的？换句话说，Python的垃圾回收机制是如何？我后来自己找了些资料看了，还是，不是理解的特别明白。老师后面的课程能帮我们讲解下吗？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（10） 💬（0）<div>python的单线程和多线程同时都只能利用一颗cpu核心，对于纯cpu heavy任务场景，不涉及到io耗时环节，cpu都是充分利用的，多线程和单线程相比反倒是多了线程切换的成本，所以性能反而不如单线程。</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（8） 💬（1）<div>1.cpu-bound任务的多线程相比单线程，时间的增加在于锁添加的获取和释放的开销结果。
2.返回到python诞生的年代，GIL相对来说是合理而且有效率的，它易于实现，很容易就添加到python中，而且它为单线程程序提供了性能提升。以至于Guido在“It isn&#39;t Easy to Remove the GIL”里面说“ I&#39;d welcome a set of patches into Py3k only if the performance for a single-threaded program (and for a multi-threaded but I&#47;O-bound program) does not decrease”。而到现在为止，任何尝试都没有达到这一条件。

</div>2019-07-01</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epbRibsic15KXfGEN3SSjnLhXGyhK2Uyrj5ibBJsKAjicNqtafDaQOLH4xpSJRZD1vmibFPJER1ySmwP9A/132" width="30px"><span>farFlight</span> 👍（4） 💬（2）<div>另外，在测试不加锁的 foo 函数的时候，我这里循环测试10000次也不会见到n!=100的情况，这是为什么呢？</div>2019-07-01</li><br/><li><img src="" width="30px"><span>张巡</span> 👍（3） 💬（0）<div>这是mackbook被黑的最惨的一次，哈哈哈</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/01/50/9ac4905e.jpg" width="30px"><span>Kfreer</span> 👍（2） 💬（0）<div>1在我们处理 cpu-bound 的任务（文中第一个例子）时，为什么有时候使用多线程会比单线程还要慢些？
答：由于CPython中GIL的存在（运行线程前需要先获取GIL），所以即便是多线程运行，同一时刻也只能有一个线程处于运行状态，且切线程之间切换时还要消耗一部分资源。这就导致cpu密集型任务下多线程反而没有单线程运行的快。

2你觉得 GIL 是一个好的设计吗？事实上，在 Python 3 之后，确实有很多关于 GIL 改进甚至是取消的讨论，你的看法是什么呢？你在平常工作中有被 GIL 困扰过的场景吗？
答：不是一个好的设计，仅仅是简化了解释器的设计，且并没有解决线程安全的问题。

总结：CPU密集型任务用多进程并行处理（CPU需多核），I&#47;O密集型任务用协程，理论上协程比多线程的效率还要高。</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（2） 💬（8）<div>t1 = Thread(target=CountDown, args=[n &#47;&#47; 2]) 老师，这段代码里面n&#47;&#47;2是什么意思？</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8a/bc/cb39ed38.jpg" width="30px"><span>自由民</span> 👍（1） 💬（0）<div>思考题
1.线程切换有开销成本，另外最主要是由于GIL的存在使python的并行为伪并行。
2.我觉得不是好设计，像戴着镣铐跳舞，好处仅仅是简化了解释器的设计。而且它并不能完全解决线程安全问题。但我平时很少用多线程编程，所以还没有实际体会。而像解释器这样的基础设施应该是把脏活留给自己，尽量减少用户的复杂性。类似还有从python2到python3的大变动。</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（1） 💬（0）<div>通过老师的讲解，我觉得GIL有点像java的Synchronized 监视器锁，同一时刻只有一个线程获得监视器锁。所以线程的频繁切换，会增加CPU开销，导致多线程反而速度变慢。</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第23讲打卡~</div>2024-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（0） 💬（0）<div>如果是通过Threading创建多线程，多线程跑python API封装的C++程序，这样是受限GIL的。而把创建多线程的工作放到C++程序里，就不被GIL所累了。</div>2022-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/bc/5a/855160ca.jpg" width="30px"><span>锋</span> 👍（0） 💬（0）<div>check_interval有可能导致线程饿死吗</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/53/79/327ef30e.jpg" width="30px"><span>sugar</span> 👍（0） 💬（0）<div>处理计算密集任务，多线程的来回切换消耗资源，所以不及单线程</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/47/8d/5d2f4acd.jpg" width="30px"><span>zys</span> 👍（0） 💬（0）<div>一核心的cpu对应一个完美的python执行.
需要多核心并行,多开,或者调用,其他库来使用就行了,,本质来讲,gil习惯了,也没什么啊 </div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e2/c4/25acaa38.jpg" width="30px"><span>苹果</span> 👍（0） 💬（0）<div>自己的比喻理解
1，单线程，有语文（1），数学（2），英语（3）作业，按照顺序123写问作业
2，多线程，在Cpython解释器种，有GIL存在，按照check interval 机制，是语文作业写5分钟，换着数学作业写5分钟，英语5分钟，在换着语文写：线程阻塞的情况，理解为数学有道题目很难，（I&#47;O密集）提前不做，释放出来，
3，多进程，找两个人帮忙做，三个人分别做语文，数学，英语，最后完成的算终止时间，
线程安全理解为，做语文作业时，不需要用到数学作业里的资料，工具，</div>2020-02-04</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>GIL在Python作为脚本或者客户端程序没问题，作为高性能程序多少有点问题。当引入协程后，并发被很好处理，现在只剩下并行不太理想，用的是多进程模型，没有利用操作系统最小调度单元。</div>2019-11-21</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（0）<div>Python 多线程是伪多线程。</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2e/74/88c613e0.jpg" width="30px"><span>扶幽</span> 👍（0） 💬（0）<div>第一问：因为Python中有GIL的存在，使得在每一个时刻都只能有一个线程在运行。如果强行使用多线程的话，线程的切换回耗费额外的资源，所有运行更慢；
第二问：有，使用Python编写的有限元数值程序运算很慢，而且当时也不懂什么线程安不安全，也不会加锁，最后算出来的结果怎么都跟标准答案对不上。
:-P</div>2019-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（0） 💬（0）<div>1、线程切换对性能有消耗      2、GIL的设计方便了CPython的编写，但是对使用者不太友好</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d7/39/6698b6a9.jpg" width="30px"><span>Hector</span> 👍（0） 💬（0）<div>我有个问题，多核cpu下的多线程比单核cpu下的多线程(假设一个进程)的效率是更低的，原因是线程颠簸。老师能解释下线程颠簸么?多核cpu下的多线程GIL是怎么释放的，其他线程是怎么争夺的?</div>2019-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/bc/38/de0b8d90.jpg" width="30px"><span>Nick</span> 👍（0） 💬（3）<div>老师，想请教一下：文中在“Python 的线程安全”的一节中，以foo函数的字节码为例，说“这四行 bytecode 中间都是有可能被打断的”。我觉得，即使比如在某行bytecode执行完之后线程被打断了，等这个线程重新获得GIL后不是会继续接着执行后面的bytecode吗，因此从结果看，最终每一条bytecode都被执行完了，那么对结果应该是不会有影响的呀？</div>2019-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3b/fc/04a75cd0.jpg" width="30px"><span>taoist</span> 👍（0） 💬（0）<div>1. 线程切换需要成本（CPU资源） ，CPU密集场合使用多线程会更慢
2. 刚开始是一个好设计，可以更快更简洁更高效的实现代码，后来就成了历史的遗留的包袱，有大量的库依赖GIL 带来的线程安全，废除的成本非常高，因此CPython 只能不断改进 GIL，很难一次性彻底取消。</div>2019-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/23/5df1f341.jpg" width="30px"><span>且听疯吟</span> 👍（0） 💬（0）<div>1. pyhton的多线程按照文中所说的实际上还是单线程的实现，表面上使用了python的多线程，但实际还是单线运行，相比较单线程而言还多了许多进程切换的锁的开销，因此多线程版本反而比单线程版本要慢。</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/b0/26c0e53f.jpg" width="30px"><span>贺宇</span> 👍（0） 💬（0）<div>和ruby一样</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1c/01/5aaaf5b6.jpg" width="30px"><span>Ben</span> 👍（0） 💬（0）<div>1. 多线程适合处理多个独立的子任务, 如果n是列表, 那么多线程&#47;多进程可以大大减少执行时间. 但是针对单个数字n的计算, 多线程计算时变量n, 可以视为被竞争的资源, 会lock住非执行线程, GIL机制会check_interval, 强制更换为其他线程, 额外增加了执行时间. 形象来说, 就是一个人要干的活, 非要几个人一起干, 一个人干的时候. 其他人只能干看着, GIL换人时, 还要额外的时间.
2. 每一种设计都是为了解决问题设计的, I&#47;O慢时使用asyncio, 也就是GIL适合的场景. 但是I&#47;O快时, 适合多线程, 此时GIL能去掉就好了</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/45/d1621188.jpg" width="30px"><span>学渣汪在央企打怪升级</span> 👍（0） 💬（0）<div>1.在第一例子中多线程间切换需要时间，所以多线程比单线程慢。
2.关于思考题2，我最近在写一个GUI，左边需要实时显示摄像头，右边做一些常规处理。用的是tk，左边摄像头多线程显示，直接用多线程摄像头视频会闪，然后用tk的update更新摄像头显示，图像会稍微卡顿。
能不能指点一下，怎么才能在界面上左边显示摄像头不卡不闪？</div>2019-07-05</li><br/>
</ul>