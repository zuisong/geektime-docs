经过前面几大模块的学习，你已经完全掌握了HTTP的所有知识，那么接下来请收拾一下行囊，整理一下装备，跟我一起去探索HTTP之外的广阔天地。

现在的互联网非常发达，用户越来越多，网速越来越快，HTTPS的安全加密、HTTP/2的多路复用等特性都对Web服务器提出了非常高的要求。一个好的Web服务器必须要具备稳定、快速、易扩展、易维护等特性，才能够让网站“立于不败之地”。

那么，在搭建网站的时候，应该选择什么样的服务器软件呢？

在开头的几讲里我也提到过，Web服务器就那么几款，目前市面上主流的只有两个：Apache和Nginx，两者合计占据了近90%的市场份额。

今天我要说的就是其中的Nginx，它是Web服务器的“后起之秀”，虽然比Apache小了10岁，但增长速度十分迅猛，已经达到了与Apache“平起平坐”的地位，而在“Top Million”网站中更是超过了Apache，拥有超过50%的用户（[参考数据](https://w3techs.com/technologies/cross/web_server/ranking)）。

![unpreview](https://static001.geekbang.org/resource/image/c5/0b/c5df0592cc8aef91ba961f7fab5a4a0b.png?wh=1222%2A340)

在这里必须要说一下Nginx的正确发音，它应该读成“Engine X”，但我个人感觉“X”念起来太“拗口”，还是比较倾向于读做“Engine ks”，这也与UNIX、Linux的发音一致。

作为一个Web服务器，Nginx的功能非常完善，完美支持HTTP/1、HTTPS和HTTP/2，而且还在不断进步。当前的主线版本已经发展到了1.17，正在进行HTTP/3的研发，或许一年之后就能在Nginx上跑HTTP/3了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（40） 💬（2）<div>你是怎么理解进程、线程上下文切换时的成本的，为什么 Nginx 要尽量避免？
当从一个任务切换到另一个任务，当前任务的上下文，如堆栈，指令指针等都要保存起来，以便下次任务时恢复，然后再把另一个任务的堆栈加载进来，如果有大量的上下文切换，就会影响性能。

试着自己描述一下 Nginx 用进程、epoll、模块流水线处理 HTTP 请求的过程。
Nginx 启动进程，一个master，多个worker，创建epoll，监听端口，多路复用来管理http请求，http请求到达worker内部，通过模块流水线处理，最后返回http响应。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/4e/d71092f4.jpg" width="30px"><span>夏目</span> 👍（15） 💬（1）<div>好像高性能的服务都是这样玩的，nginx这个架构类似于netty中的多线程reactor模式，redis则是单线程reactor</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（13） 💬（2）<div>一个线程的时间片没用完就系统调用被系统调度切换出去，浪费了剩余的时间片，nginx通过epoll和注册回调，和非阻塞io自己在用户态主动切换上下文，充分利用了系统分配给进程或者线程的时间片，所以对系统资源利用很充分</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（9） 💬（1）<div>老师，以下问题，麻烦回答一下，谢谢：

1. 把进程“绑定”到独立的 CPU 上。意思是一个CPU专门负责管理进程嘛？

2. 不过 master 进程完全是 Nginx 自行用 C 语言实现的，这就摆脱了外部的依赖，简化了 Nginx 的部署和配置。这句话没理解。</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（9） 💬（1）<div>多线程就好比一条流水线有多个机械手，把一件事情中途交给其他线程处理，要交接处理中间状态信息。
单进程就好比一条流水线只有一个机械手，切换时间片时暂停状态就可以，不用交接信息，减少无用功，所以效率高。</div>2019-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bd/b0/8b808d33.jpg" width="30px"><span>fakership</span> 👍（7） 💬（1）<div>老师，有个问题咨询下
虽然nginx是使用了epoll做了io的多路复用，但对于队头阻塞的话感觉并没有帮助啊，因为还是要等io事件回调后发送http响应报文，所以还是阻塞了下一个请求。</div>2020-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（6） 💬（1）<div>老师好!我打算学习nginx，有适合初学者的书推荐么?Java工程师，c全忘了。
线程切换开销:线程切换需要进行系统调用。需要从用户态-&gt;内核态-&gt;用户态。上下文切换，需要保存寄存器中的信息，以便于完成系统调用后还原现场。会多跑很多指令，出入栈会比寄存器慢很多。相对来说开销就很大了。
nginx和redis一样采用单线程模型。是因为cpu计算不可能是它们瓶颈(所以有些耗cpu资源高的计算不适合放在nginx上做会导致响应时间变长)?进程池+单线程是指，每个worker进程都是单线程是么?</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a4/7e/963c037c.jpg" width="30px"><span>Aaron</span> 👍（4） 💬（3）<div>对『进程池 + 单线程』的模式还是不太透彻。

我理解，『单线程』指的是所有 HTTP 请求放在同一个线程里通过『I&#47;O 多路复用』的技术处理，实际就是高度集中（无阻塞）地占用了 CPU（核心）地运算能力。

那么，既然请求是单线程的，那进程池地作用又是什么呢？如果是多进程的，不就又回到进程间上下文切换的消耗问题了吗？

另，Nginx 通过 cpu affinity 将进程绑定到 CPU，假设是单 CPU，将三个 worker 进程绑定到同一个物理 CPU 地意义又在哪呢？

个人认为效率最高的方式，是按照 CPU 的核心数量创建一个『线程池』，将所有请求分配到『线程池』内不同的线程，这样在『I&#47;O 多路复用』的加持下能跑满 CPU 的性能。</div>2020-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/WtHCCMoLJ2DvzqQwPYZyj2RlN7eibTLMHDMTSO4xIKjfKR1Eh9L98AMkkZY7FmegWyGLahRQJ5ibPzeeFtfpeSow/132" width="30px"><span>脱缰的野马__</span> 👍（3） 💬（1）<div>老师你好，tomcat不主流吗？</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（3） 💬（1）<div>说一下http2和nginx的多路复用区别和联系：
http2的多路复用：多个请求复用同一个连接并行传输数据，且每个请求抽象为流传输的对象为帧序列。
nginx的IO多路复用：将多个线程的请求打散，汇入同一个线程中传输，epoll监听到事件通道可读或者可写的时候取出或者写入数据，所以nginx的IO多路复用是基于linux内核epoll实现的一种事件监听机制，是NIO非阻塞IO。
</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（3） 💬（3）<div>切换cpu需要保存线程的上下文，然后再切回去，这是开销</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（2） 💬（3）<div>Nginx这种异步处理方式叫“协程”吧？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/79/fa/48b481fe.jpg" width="30px"><span>zero</span> 👍（2） 💬（1）<div>老师，您好，我想写博客，我写的博客里面能盗一下您的图么（您的图做的太直观了一看就懂了），我会著名图片的出处😇😇</div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（2） 💬（3）<div>缓存服务器，是属于正向代理还是反向代理，还是根据情况而定。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/60/ea88b933.jpg" width="30px"><span>zyd-githuber</span> 👍（1） 💬（1）<div>感觉和nodejs的单线程机制非常像</div>2022-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（1） 💬（2）<div>线程上下文的切换消耗感觉主要是用户态和内核态不断切换。也就是堆栈，指令指针之类的。</div>2021-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/10/de/dbf2abde.jpg" width="30px"><span>萤火之森</span> 👍（0） 💬（1）<div>多进程 对缓存管理的数据竞争如何处理？</div>2023-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/1b/83ac7733.jpg" width="30px"><span>忧天小鸡</span> 👍（0） 💬（1）<div>这里说的nx的epoll是指模仿epoll的交互逻辑，还是指从epoll的base上做了对tcp的改装？</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/96/1f/a4e3f3a5.jpg" width="30px"><span>三千世界</span> 👍（0） 💬（2）<div>老师我想问一下，nginx为什么要设计让多个worker进程竞争accpet，这样导致 惊群 问题，还要加锁来解决，反而造成了性能下降。
所以，为什么不让master通过epoll监听有连接可以accept，通过调度，找一个不怎么忙的worker，然后通过管道通知这个worker呢，这样就不会出现惊群问题了</div>2021-11-29</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4faqHgQSawd4VzAtSv0IWDddm9NucYWibRpxejWPH5RUO310qv8pAFmc0rh0Qu6QiahlTutGZpia8VaqP2w6icybiag/132" width="30px"><span>爱编程的运维</span> 👍（0） 💬（1）<div>老师您好，nginx采用IO多路复用技术，使用单线程处理多个IO流数据流
是不是也可以多线程+IO多路复用技术？多个线程处理多个IO数据流
</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/3f/ec/00904faa.jpg" width="30px"><span>连长</span> 👍（0） 💬（1）<div>Nginx 使用进程池加单线程的工作方式，master进程管理进程池，利用IO多路复用提供并发性能。epoll连接管理由操作系统处理，减少应用层操作。</div>2021-09-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（0） 💬（1）<div>老师，看了越来越多的框架，觉得epoll是真的牛，epoll是哪个人&#47;框架首创的呀？</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>请问老师多路复用那张图里的中间横轴应该是nginx 线程吧？</div>2020-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（0） 💬（1）<div>老师,有个问题问您一下,我们生产环境有两套系统A B,都是使用的https(通过https访问nginx,nginx转发请求给后台应用)，我们现在出现一个问题,同一个网络部分用户(前天都是好的,昨天一个用户,今天两个用户)无法与A系统的nginx建立TLS连接,但是都可以正常访问B系统的nginx,两套系统使用的nginx的配置是一样的
在无法正常访问A系统的电脑上,通过curl -v发现只有一个 TLSv1.3（OUT），client hello(1):
没有看到服务端的server hello,只看到SSL connection被重置了</div>2020-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/84/19/7ed2ffa6.jpg" width="30px"><span>风</span> 👍（0） 💬（1）<div>老师请问『进程池 + 单线程』指的是:通过进程池接收处理HTTP请求,然后每个进程处理请求是单线程的?这样对于同一进程处理的所有请求都位于同一线程,如果同一进程里的处理过程发生阻塞就不需要保存阻塞任务的堆栈,简单的理解是不是相当于有多台服务器进行服务支持,每台服务器都是单进程线程单CPU</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/2f/3aee5f24.jpg" width="30px"><span>宋雄斌</span> 👍（0） 💬（1）<div>老师，您好，我的理解是，线程池的作用是处理不同任务，但是每个任务都是由单线程进行处理的，这样对不对呢</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（0） 💬（1）<div>不太明白：1.每个worker进程都绑定到独立的cpu们？2.单线程也是应该存在于具体的某一个进程里边的吧，那进程间切换是怎么做的？</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>1：你是怎么理解进程、线程上下文切换时的成本的，为什么 Nginx 要尽量避免？
这是个好问题，也是面试常客。
首先，需要回答什么是进程？什么是线程？然后，进程或线程，在进行切换时都需要做什么？然后，就能发现进程或线程的切换为什么会消耗大量的成本啦！
首先，程序就是人写的各种代码，告诉计算机需要做什么事情，只需要存储资源。当程序运行起来的时候，需要的不光是存储资源，还有其他的为了弥补速度差这些东西都以各种寄存器的形式存在，比如：指令寄存器、地址寄存器、数据寄存器、程序计数器等等，当然还需要CPU的时间片。好像做一道菜，需要各种油盐酱醋锅碗瓢盆一样，如果做的过程中，要停下来，做另外一道菜，想想都够费事的。进程或线程的切换就类似这样吧！而且没做好的菜，要继续做需要记录做到那一步了，继续做需要怎么继续。切换进程或线程上下文，确实太耗成本了。
OK，那进程、线程到底有啥区别？我的理解，这两个概念是相对的或者线程是相对进程而言的，进程先存在表示跑起来的程序，不过进程内有许多的动作，有些还比较慢，进程切换上下文又太费成本，为了提高性能就出现了线程，线程依附于进程公用进程的存储资源，切换上下文时仅切换自己独有的资源让其他就绪的线程继续跑，这样切换上下文的成本能够少一些。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（0） 💬（1）<div>买书为敬。</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/77/b2ab5d44.jpg" width="30px"><span>👻 小二</span> 👍（0） 💬（1）<div>线程是用来解决IO阻塞时CPU浪费的问题， 如果没有IO阻塞的问题， 单线程最能发挥CPU的能力，多线程反而要花时间切换。
由于CPU一般有多核， 所以不考虑阻塞的话， 几个核就 几个线程， 将是最佳选择。</div>2019-08-23</li><br/>
</ul>