你好，我是海纳。

上节课，我们学习了为什么要设计缓存，以及缓存和内存的映射方式。你还记得吗？在上节课结束的部分，我讲到了只要数据的访问者和被访问者之间的速度不匹配，就可以考虑使用缓存进行加速。

但是我们知道，天下没有免费的午餐，缓存在带来性能提升的同时，也引入了缓存一致性问题。缓存一致性问题的产生主要是因为在多核体系结构中，如果有一个CPU修改了内存中的某个值，那么必须有一种机制保证其他CPU能够观察到这个修改。于是，人们设计了协议来规定一个CPU对缓存数据的修改，如何同步到另一个CPU。

今天我们就来介绍在多核体系结构下，如何解决缓存一致性问题。另外，按照从简单到困难的顺序，我还会介绍最简单的VI协议和比较完善的MESI协议。学习完这节课后，你就知道缓存一致性问题是如何被解决的，还会了解到如何设计协议对缓存一致性进行管理。

在缓存一致性的问题中，因为CPU修改自己的缓存策略至关重要，所以我们就从缓存的写策略开始讲起。

## 缓存写策略

在高速缓存的设计中，有一个重要的问题就是：当CPU修改了缓存中的数据后，这些修改什么时候能传播到主存？解决这个问题有两种策略：**写回（Write Back）和写直达（Write Through）**。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKtlEYuHnR8VdRkNPcmkIqTM9DKahpcpicDdBvcmBWMIAAhBrd0QNWvl09slqrzB5TibryVcIfPmb7Q/132" width="30px"><span>raisecomer</span> 👍（8） 💬（1）<div>有一个问题，当IO设备通过DMA通道修改内存数据时，如果这个内存数据刚好被一个CPU已经加载到本地缓存了，也就是内存数据修改的源头不是CPU，那么缓存一致性怎么保证的，也是MESI协议吗？</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/b6/27412d76.jpg" width="30px"><span>sc</span> 👍（1） 💬（2）<div>老师，请问

1. 在 基于“写直达”的缓存一致性协议 中，&quot;&quot;“写传播”的缓存一致性的缺点是需要很高的带宽。原因是对于缓存块的每次写入，都会触发 BusWr 从而占用带宽。相反的是，在“写无效”缓存策略下，如果同一个缓存块中的数据被多次写入，只需占用一次总线带宽来失效其他处理器的缓存副本即可。&quot;，这个相反的是，说的是什么意思，读了好几次，没有读明白，我理解的是：前面说的是缓存块的每次写入，都会触发 BusWr，后面说的是在写无效策略下，即使每次写入都会触发 BusWr，但是对于 I 状态的缓存块，即使侦听到 BusWr ，也不会有影响，请问老师是这样吗

2. 在最后总结中，说的是 “在写回策略中主要包括失效和有效两种状态；在写直达策略中又通过引入独占和修改状态，提升了缓存同步的效率。”，老师这里是不是写反了，看上面的文章中，应该是写直达只有两种状态，然后在写回中又增加了独占和修改状态。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/39/d2/845c0e39.jpg" width="30px"><span>送过快递的码农</span> 👍（0） 💬（2）<div>老师，你这边讲的总线上什么总线啊？是cpu内部的总线，还是负责cpu和内存通讯的总线啊？</div>2021-12-02</li><br/><li><img src="" width="30px"><span>shenglin</span> 👍（0） 💬（1）<div>还有一个问题，一个 CPU 发起请求的同时，也会产生总线事件，导致其他CPU的缓存的状态改变，这样不是会频繁占用总线带宽？</div>2021-12-02</li><br/><li><img src="" width="30px"><span>shenglin</span> 👍（0） 💬（1）<div>VI协议的状态机示意图中，右边的情况，当缓存处于valid状态时，收到BusWr事件，此缓存不会产生总线事务，但是会变成invalid状态，示意图的箭头画反了吧，由V指向I？</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/25/d0/3d5696d8.jpg" width="30px"><span>无嘴小呆子</span> 👍（0） 💬（1）<div>既然MESI保证CPU缓存一致性了，为何java还要使用volatile关键字呢？就是MESI何时触发老师没有讲解清楚呀！硬件篇应该加上这个吧～</div>2021-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/ac/9cc5e692.jpg" width="30px"><span>Corner</span> 👍（0） 💬（2）<div>所以缓存一致性协议是硬件保证吗？也就是不管你怎么写代码，它都是存在的？</div>2021-12-02</li><br/><li><img src="" width="30px"><span>springXu</span> 👍（0） 💬（4）<div>提个小建议，有没有这个协议的说明资料，比如intel的哪个文档中有这个介绍？又或者是AMD的。能给个链接么？</div>2021-12-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/82/0c/cc106ab1.jpg" width="30px"><span>Samaritan.</span> 👍（1） 💬（0）<div>“因为写直达会导致更新直接穿透缓存，所以这种情况下只能采用写不分配策略”
实在没有理解以上这句话，它的含义是以下哪一点呢？
1、【写直达】和【写不分配】完全无法共存
2、出于实现难度和性能，【写直达】最好不要和【写不分配】共存</div>2024-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（1） 💬（0）<div>在写回策略中主要包括失效和有效两种状态；在写直达策略中又通过引入独占和修改状态，提升了缓存同步的效率。 

这个总结写反了吧</div>2022-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4f/7f/5dc11380.jpg" width="30px"><span>苏志辉</span> 👍（1） 💬（1）<div>mesi的右图中，e状态只会产生busrdx不会产生busupgr吧，因为当前是e其他核应该都没有效数据。</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>当要把内存中的数据flush到磁盘上时，要触发cpu cache line的flush吧？这个是谁触发的？操作系统内核么？</div>2023-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（0）<div>好奇，当N个cpu中有N-1个的缓存同一个地址都是S时，第N个读取的时候发出BusRd，是从哪个cpu读的呢？</div>2023-09-05</li><br/><li><img src="" width="30px"><span>Geek_4a813a</span> 👍（0） 💬（2）<div>文中提到 ： 当 CPU 采取写回策略时，对缓存的修改不会立刻传播到主存，只有当缓存块被替换时，这些被修改的缓存块，才会写回并覆盖内存中过时的数据。
问题： 1. 什么时候情况下 会触发 缓存块被替换？
2.被替换不会出现数据丢失吗</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（0） 💬（0）<div>前面讲&quot;因为写直达会导致更新直接穿透缓存，所以这种情况下只能采用写不分配策略&quot;，后面总结时又说&quot;写不分配在现实中比较少出现&quot;，那这里可以理解为 现实中写直达出现的也比较少吗</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/5d/65e61dcb.jpg" width="30px"><span>学无涯</span> 👍（0） 💬（0）<div>&quot;在具体的实现中，绝大多数 CPU 都会采用写无效策略。这是因为多次写操作只需要发起一次总线事件即可，第一次写已经将其他缓存的值置为无效，之后的写不必再更新状态，这样可以有效地节省 CPU 核间总线带宽。&quot;
这里有个问题请教老师：CPU0第一次写操作后，将CPU1中缓存设置为无效；假如这时CPU1重新读取了数据，然后CPU0进行了第二次写操作。
这种情况下CPU0不需要发起总线事件吗？</div>2022-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（0）<div>思考题
redis写入数据时，多个节点需要同步数据。</div>2021-12-01</li><br/>
</ul>