我们前面说到玄奘西行，要出网关。既然出了网关，那就是在公网上传输数据，公网往往是不可靠的，因而需要很多的机制去保证传输的可靠性，这里面需要恒心，也即各种**重传的策略**，还需要有智慧，也就是说，这里面包含着**大量的算法**。

## 如何做个靠谱的人？

TCP想成为一个成熟稳重的人，成为一个靠谱的人。那一个人怎么样才算靠谱呢？咱们工作中经常就有这样的场景，比如你交代给下属一个事情以后，下属到底能不能做到，做到什么程度，什么时候能够交付，往往就会有应答，有回复。这样，处理事情的过程中，一旦有异常，你也可以尽快知道，而不是交代完之后就石沉大海，过了一个月再问，他说，啊我不记得了。

对应到网络协议上，就是客户端每发送的一个包，服务器端都应该有个回复，如果服务器端超过一定的时间没有回复，客户端就会重新发送这个包，直到有回复。

这个发送应答的过程是什么样呢？可以是**上一个收到了应答，再发送下一个**。这种模式有点像两个人直接打电话，你一句，我一句。但是这种方式的缺点是效率比较低。如果一方在电话那头处理的时间比较长，这一头就要干等着，双方都没办法干其他事情。咱们在日常工作中也不是这样的，不能你交代你的下属办一件事情，就一直打着电话看着他做，而是应该他按照你的安排，先将事情记录下来，办完一件回复一件。在他办事情的过程中，你还可以同时交代新的事情，这样双方就并行了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/dd/4f53f95d.jpg" width="30px"><span>进阶的码农</span> 👍（48） 💬（7）<div>AdvertisedWindow=MaxRcvBuffer-((NextByteExpected-1)-LastByteRead)。
我根据图中例子计算 14-((5-1)-0) 算出来是10 ，括号里边的-1是减的什么，为啥和图例算出来的结果不一样，还是我计算的有问题，麻烦详细说一下 谢谢</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/42/52/19553613.jpg" width="30px"><span>刘培培</span> 👍（72） 💬（4）<div>BBR 论文原文：https:&#47;&#47;queue.acm.org&#47;detail.cfm?id=3022184</div>2019-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bf/8f/51f044dc.jpg" width="30px"><span>谛听</span> 👍（23） 💬（4）<div>不太清楚累积应答，比如接收端收到了包1、2、3、4，它的应答应该是5吗？也就是说中间的包就不用应答了吗？</div>2018-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/bb/9299fab1.jpg" width="30px"><span>Null</span> 👍（21） 💬（1）<div>BBR 不填满缓存还是不填缓存？不填缓存那么缓存干啥用，如果填了了，即使不满，但是不是还有延迟。。。</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/4b/34e7ceca.jpg" width="30px"><span>秋去冬来</span> 👍（13） 💬（1）<div>快速重传那块6.8.9   7丢了为什么会发送3个冗余的6的3个ack</div>2018-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d1/15/7d47de48.jpg" width="30px"><span>咖啡猫口里的咖啡猫🐱</span> 👍（12） 💬（2）<div>老师，TCP协议栈，保证包一定到吗，，哪几种情况下会丢失，，，能不能总结下</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6f/63/abb7bfe3.jpg" width="30px"><span>扬～</span> 👍（10） 💬（9）<div>2个问题：
1. TCP可靠的连接会不会影响到业务层，比如超时重传导致了服务端函数调用2次，那岂不是业务都要考虑幂等性了，我很懵逼，果然是懂得越多越白痴。
2. 拥塞控制的窗口跟流量控制的窗口一回事吗，还是流量控制的窗口的出来后就会进入拥塞控制窗口？</div>2018-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/5d/1ccee378.jpg" width="30px"><span>茫农</span> 👍（10） 💬（2）<div>有一个值 ssthresh 为 65535 个字节，，这个是什么意思？</div>2018-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/68/ef/6264ca3d.jpg" width="30px"><span>Magic</span> 👍（8） 💬（1）<div>祝刘超老师教师节快乐，专栏很棒，受益良多</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/cd/2c3808ce.jpg" width="30px"><span>Yangjing</span> 👍（6） 💬（1）<div>对于发送端，为什么会保存着“已发送并已确认”的数据呢？已确认的不是已经没用了吗？</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/75/af67e5cc.jpg" width="30px"><span>黑猫紧张</span> 👍（6） 💬（2）<div>内核是将从网络接收的tcp数据 都接收完成再一次发给应用层呢 还是在tcp接收的过程中就已经开始发给应用层了 求回复</div>2019-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/ad/6e3e9e15.jpg" width="30px"><span>产品助理</span> 👍（5） 💬（2）<div>问题：

1、如下公式的 -1  到底是为什么？

	AdvertisedWindow=MaxRcvBuffer-((NextByteExpected-1)-LastByteRead)

   图例中的LastByteRead是0还是1？NextByteExpected是6还是5？MaxRcvBuffer是14吗？

2、如果按照上述公式，那下面又是为了什么？

	NextByteExpected 加 AdvertisedWindow 就是第二部分和第三部分的分界线，其实也就是 LastByteRead 加上 MaxRcvBuffer。

	按照第一条的公式，NextByteExpected + AdvertisedWindow = NextByteExpected + （MaxRcvBuffer-((NextByteExpected-1)-LastByteRead))
	= MaxRcvBuffer + 1 + LastByteRead

	应该有个+1啊。。

多谢老师！	</div>2018-11-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4AyMqvLia5xW0d1CxlPYoHJk2LQhaDzAialczCIuRKibiczWHkJIra0DpmtxREwibtPiajk3NhQVSicXMKxB0Oyb5GEsg/132" width="30px"><span>旭风</span> 👍（4） 💬（1）<div>在传统算法和快速算法的对比描述中，对于快速算法中提到 cwnd减半为cwnd&#47;2，sshthresh=cwnd ，后面cwnd=sshthresh+3，转折点是20变为13，这里的cwnd为10吗？

2018-06-15

 作者回复

cwnd先是为10，后面变为13

继上一个问题，传统算法，cwnd 从1,2,4,8,16指数增长，这时cwnd为16，收发是不是各占8个？然后由16变成17，满8个确认时cwnd＋1，就是17，那么增加到20这里，cwnd为20，这时产生拥塞，如果是传统的话，立马降下来，如果是快速，那么减半，也就是10，等待3个确认包＋3，，后续每一个确认cwnd就＋1吗？还是？这样子理解吗？</div>2018-06-19</li><br/><li><img src="" width="30px"><span>起风了001</span> 👍（3） 💬（1）<div>这一章感觉比前面好一些, 比喻比较形象.也挺详细. 谢谢, 就是有一点音频和文字不完全一样, 有时候边看变听有点跟不上</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（2） 💬（1）<div>网络_12

看了一些资料，还是没有最终弄明白，只知道了Cubic是基于丢包的，BBR是基于测量的。

关于UDP与TCP的程序，它们的选型以及“坑”都与特点密切相关。
- UDP特点是快，不可靠。所以在需要无法容忍高时延的场景要选择它，当然，这个时候，一些必要校验和重发逻辑就留给了应用层，这里应该是最大的“坑”。
- TCP特点是可靠，慢。在我开发过的程序中，“坑”比较多地存在于长连接的keepalive阶段，需要在资源消耗与稳定性之间取得平衡。</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/2c/919e5773.jpg" width="30px"><span>Abirdcfly</span> 👍（2） 💬（1）<div>问个问题。最刚开始ssthres 是65535字节.然后一个mss是1460字节。那么指数增长应该是到44才变慢啊。为啥是16呢？</div>2019-06-13</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKficy9MkomP4658kicbqNwoAibL71byWowtjnrMqS3rdqTicTl41hCGu7Jjf0Dp6J7YZcd43yQevuaJw/132" width="30px"><span>Geek_hustnw</span> 👍（2） 💬（1）<div>（1）文章提到下面这段话：
    每收到一个确认后，cwnd 增加 1&#47;cwnd，我们接着上面我们接着上面的过程来，一次发送八个，当八个确认到来的时候，每...
（2）然后快速重传算法里面提到拥塞时：
    cwnd 减半为 cwnd&#47;2，然后 sshthresh =...

问题：快速重传拥塞处理里面，为什么遇到3个包返回的时候，是“sshthresh + 3”，而不是“sshthresh + 3&#47;cwnd”</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/63/f4/6fdc1508.jpg" width="30px"><span>陈栋</span> 👍（2） 💬（1）<div>第三部分和第四部分分界线写错了，应该是lastByteSent+advertisedWindow</div>2018-06-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/4AyMqvLia5xW0d1CxlPYoHJk2LQhaDzAialczCIuRKibiczWHkJIra0DpmtxREwibtPiajk3NhQVSicXMKxB0Oyb5GEsg/132" width="30px"><span>旭风</span> 👍（2） 💬（1）<div>在传统算法和快速算法的对比描述中，对于快速算法中提到 cwnd减半为cwnd&#47;2，sshthresh=cwnd ，后面cwnd=sshthresh+3，转折点是20变为13，这里的cwnd为10吗？</div>2018-06-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（1） 💬（1）<div>为什么填缓存还会加大时延，有缓存不是更快了么</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/d0/b7cbde62.jpg" width="30px"><span>zjw</span> 👍（1） 💬（1）<div>所以我每次用uplay这种服务器很烂的应用下游戏时速度有时候会一下子掉下来，然后又慢慢回上去。是因为tcp在传输过程中丢包了，然后自动降低了传输速度了吗</div>2019-07-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLTPmSgD6QSgicqsbzibiau9xWSYgdsvYlnVWBg91ibHQBYg39MT4O3AV5CHlJlVUvw9Ks9TZEmRvicfTw/132" width="30px"><span>InfoQ_0ef441e6756e</span> 👍（1） 💬（1）<div>请问老师，比如发送方 发送了 【1，2，3，4】，接收方回了3的ack，这种情况窗口怎么动啊？   </div>2019-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/14/06eff9a4.jpg" width="30px"><span>Jerry银银</span> 👍（1） 💬（2）<div>请教老师一个概念性的问题：packet   chunk   segment  block   这几个词在“网络”文章或者书籍中经常初出现，感觉它们很相似，又感觉它们又有些细微的区别，但是具体的也说不清！</div>2019-05-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/txBsdmdDUEzC356b5sICOJdw8Ls7blql0vWeXbeWQQw6NEQtk85JBIvGGdwLTXxJYVTmicFbITfnQwUofEhGQqA/132" width="30px"><span>wildmask</span> 👍（1） 💬（1）<div>如果接收方发现7丢了，为什么不能直接要求重发7，发送3个ack 有必要吗？</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/98/ffaf2aca.jpg" width="30px"><span>Ronnyz</span> 👍（1） 💬（1）<div>接收端是采用累计确认机制的吗</div>2019-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/99/d3/5434e6e0.jpg" width="30px"><span>德道</span> 👍（1） 💬（1）<div>当三个包返回的时候，cwnd = sshthresh + 3，当三个包返回是什么意思，为什么要加3</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/bb/9299fab1.jpg" width="30px"><span>Null</span> 👍（1） 💬（1）<div>而且，老师行文过程，哪些是现象，问题，算法解决方案，目前最优，或者广泛采用的是哪个没有清晰的脉络，很容易看完一遍一头雾水。</div>2019-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0b/90/f161b09a.jpg" width="30px"><span>赵大宝</span> 👍（1） 💬（1）<div>不是很理解第三部分和第四部分的分界线，老师能说明下么</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/f4/fb729388.jpg" width="30px"><span>(-.-)</span> 👍（1） 💬（1）<div>&quot;快速重传，接收方发现 6、8、9 都已经接收了，就是 7 没来，发送三个6的ack，要求下一个是7.客户端收到 3 个，就会发现 7 的确又丢了，不等超时..&quot;
这个不应该是服务端收到三个6的ack包吗?
</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/33/56f8bcbe.jpg" width="30px"><span>yinhua_upc</span> 👍（1） 💬（1）<div>
&quot;6、7 是等待接收的；8、9 是已经接收，但是没有 ACK 的&quot;
从接收端的图看6-14都是等待接收未确认，为什么8、9是已经接收？
</div>2018-11-09</li><br/>
</ul>