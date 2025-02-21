你好，我是陶辉。

上一节课，我们介绍了建立连接时的优化方法，这一节课再来看四次挥手关闭连接时，如何优化性能。

close和shutdown函数都可以关闭连接，但这两种方式关闭的连接，不只功能上有差异，控制它们的Linux参数也不相同。close函数会让连接变为孤儿连接，shutdown函数则允许在半关闭的连接上长时间传输数据。TCP之所以具备这个功能，是因为它是全双工协议，但这也造成四次挥手非常复杂。

四次挥手中你可以用netstat命令观察到6种状态。其中，你多半看到过TIME\_WAIT状态。网上有许多文章介绍怎样减少TIME\_WAIT状态连接的数量，也有文章说TIME\_WAIT状态是必不可少、不能优化掉的。这两种看似自相矛盾的观点之所以存在，就在于优化连接关闭时，不能仅基于主机端的视角，还必须站在整个网络的层次上，才能给出正确的解决方案。

Linux为四次挥手提供了很多控制参数，有些参数的名称与含义并不相符。例如tcp\_orphan\_retries参数中有orphan孤儿，却同时对非孤儿连接也生效。而且，错误地配置这些参数，不只无法针对高并发场景提升性能，还会降低资源的使用效率，甚至引发数据错误。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/82/3d/356fc3d6.jpg" width="30px"><span>忆水寒</span> 👍（15） 💬（4）<div>本节内容真的很烧脑啊！收获也很多，从来没有从这么多角度看待过这个问题。
so_linger是一个结构体，其中有两个参数：l_onoff和l_linger。第一个参数表示是否启用so_linger功能，第二个参数l_linger=0，则 close 函数在阻塞直到 l_linger 时间超时或者数据发送完毕，如果超时则直接情况缓冲区然后RST连接（默认情况下是调用close函数立即返回）。</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/36/d054c979.jpg" width="30px"><span>G.S.K</span> 👍（9） 💬（1）<div>请教老师，我有一点想不明白。假如A和B之间有个tcp连接，A主动发起关闭，A进入TIME_WAIT状态。如果B端的RTO(重传超时时间)比2msl大，2MSL后，B端还是有可能重传FIN的。感觉TIME_WAIT等待的时间应该是B端RTO+MSL啊。还请老师帮忙解惑。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（9） 💬（1）<div>老师的文章都要细品.
内核调优的参数算是见识到了,不知道啥时候才能用得上.🤦

一些边界情况老师也介绍到了:
1. tcp_tw_reuse 也是有适用条件的.
2. 四次挥手在极端情况下,可能变三次挥手.
3. CLOSING 状态确实算是第一次见,之前没考虑过这个问题.

以前在用c语言的网络编程时,会接触setsockopt函数.
最初的使用该函数的原因,只是为了端口复用.
因为在调试的过程中,经常会重启服务,如果不设置SO_REUSEADDR参数,就需要等系统释放掉端口,服务才能监听成功.

见过SO_LINGER选项,但真未细究过.
待课代表们来解答.
</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（4） 💬（2）<div>看到一遍文章，tcp_timestamps还有这个坑吗？
https:&#47;&#47;blog.51cto.com&#47;fuyuan2016&#47;1795998</div>2020-05-21</li><br/><li><img src="" width="30px"><span>Geek_78d3bb</span> 👍（3） 💬（1）<div>为什么3次握手4次挥手？ 因为挥手的时候，需要先清空各自缓冲区中的数据，然后才能close，不是这样吗？</div>2020-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（3） 💬（2）<div>至少要听3遍</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（2） 💬（1）<div>TTL每一跳减少1，这些怎么和MSL对应起来呢，每一跳减少的1相当于1秒？</div>2020-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/h0KAdRFKjCOSLRjzictvlaIpALTISCOftCIat5ej7QZlndkxTzhKmkvHWqMjvSKcuPZ0bmYkrWiaRXxja3hibwvjHgcLBvA9Uel/132" width="30px"><span>Geek_f1c894</span> 👍（1） 💬（1）<div>老师，您好！我在想主动方处于FIN_WAIT2状态，被动方处于CLOSE_WAIT，意味可能想在半关闭连接上接收数据，且没有限制CLOSE_WAIT状态的持续时间，若被动方在CLOSE_WAIT状态还要发送的数据量耗时超过了2MSL时间，此时主动方是如何处理的？
我猜想可能情况①主动方接收了个含数据的报文后重新记时（收到最新报文的时间开始记时2MSL时间），直到在2MSL内收到FIN包或没接收到数据及FIN包做超时结束连接。②主动方在进入FIN_WAIT2状态的一分钟（2MSL）内能收到多少数据就收到，时间一到直接进入TIME_WAIT状态或者直接关闭连接</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（1） 💬（1）<div>rst报文的发送是比普通数据优先级高吗，也就是socket对端如果先接受到rst，这个socket就不可读不可写了，后面收到的数据自然也没法被进程拿到了。</div>2020-05-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/rRCSdTPyqWcW6U8DO9xL55ictNPlbQ38VAcaBNgibqaAhcH7mn1W9ddxIJLlMiaA5sngBicMX02w2HP5pAWpBAJsag/132" width="30px"><span>butterfly</span> 👍（0） 💬（1）<div>在主动方处于 TIME_WAIT状态时，如果过了2MSL时间，还是有FIN传来，那不是对新连接还是有影响吗</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/03/1c/c9fe6738.jpg" width="30px"><span>Kvicii.Y</span> 👍（7） 💬（0）<div>TCP的这几篇文章我听了有10几遍</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e4/e5/82132920.jpg" width="30px"><span>亦知码蚁</span> 👍（2） 💬（1）<div> tcp_tw_reuse 的内核配置选项和 SO_REUSEADDR 套接字选择，这两个有什么区别呢</div>2020-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>当 发送 FIN 报文后，长时间没有收到 ACK 报文就会重发 FIN, 这个 长时间是哪个参数进行控制的？ 就是多长时间 没有收到 ACK 才会重发。 这的话就可以在结合 tcp_orphan_retries 这个参数可以算出来一个会消耗多少时间</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/f7/871ff71d.jpg" width="30px"><span>Geek_David</span> 👍（1） 💬（0）<div>一篇15分钟的音频，足足花了1.5个小时
包括先听音频，再看文字，再理解每个含义，再记笔记
我敢说我懂了。
前提是对TCP想过比较了解的情况下，太南了</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/19/c058bcbf.jpg" width="30px"><span>流浪地球</span> 👍（1） 💬（0）<div>MSL的数值在所有网络环境中都一样，如果一些跨洋的长距离网络这个时间可以保证吗？如果发现这个数值无法保证，是需要调整网络传输层次结构吗？
</div>2020-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/19/fe/d31344db.jpg" width="30px"><span>lJ</span> 👍（0） 💬（0）<div>SO_LINGER 是一个套接字选项，用于控制关闭连接时的行为。当设置了 SO_LINGER 选项时，它会影响主动关闭连接的状态变化，并与系统配置参数协作以确定超时时间。

当应用程序调用 close() 函数来关闭连接时，如果设置了 SO_LINGER 选项，系统将根据 SO_LINGER 的设置来确定关闭连接的方式。SO_LINGER 选项的结构如下：

struct linger {
    int l_onoff;  &#47;&#47; 0表示禁用，非0表示启用
    int l_linger; &#47;&#47; 超时时间（以秒为单位）
};
当 l_onoff 为 0 时，表示禁用 SO_LINGER 选项，close() 函数会立即返回，但底层的 TCP 连接并不会立即关闭。系统会尝试发送所有缓冲区中的数据，然后进行正常的 TCP 四次挥手关闭连接。

当 l_onoff 非 0 时，表示启用 SO_LINGER 选项，此时 l_linger 指定了超时时间。在这种情况下，close() 函数会阻塞，直到以下条件之一满足：

所有发送的数据都被对端确认，然后进行正常的 TCP 四次挥手关闭连接。
超过指定的超时时间，系统会发送 RST 包强制关闭连接。
因此，SO_LINGER 选项影响了连接关闭的方式，可以通过设置超时时间来控制连接关闭的行为，以应对一些特定场景下的需求。

在实际使用中，SO_LINGER 的超时时间与系统配置参数协作。具体而言，与 SO_LINGER 相关的系统配置参数包括：

tcp_fin_timeout：指定了在发送最后一个数据包后，等待对端发送 FIN 包的最大时间。当 SO_LINGER 超时时间大于 tcp_fin_timeout 时，SO_LINGER 的超时时间将被 tcp_fin_timeout 所取代。</div>2023-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/dc/6d/03130ea9.jpg" width="30px"><span>JW</span> 👍（0） 💬（0）<div>不同系统的TTL不一样，30秒是比较少的</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ae/8b/43ce01ca.jpg" width="30px"><span>ezekiel</span> 👍（0） 💬（0）<div>如果主动方不保留 TIME_WAIT 状态，会发生什么呢？此时连接的端口恢复了自由身，可以复用于新连接了。然而，被动方的 FIN 报文可能再次到达，这既可能是网络中的路由器重复发送，也有可能是被动方没收到 ACK 时基于 tcp_orphan_retries 参数重发。这样，正常通讯的新连接就可能被重复发送的 FIN 报文误关闭。
-----------------------------------------------------------------------------------------------------
报文不都是有编号的吗？重新启用的端口，会处理过期的报文吗？</div>2021-09-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKsUJP9VV8iaZOuQxfRgzUvxqA09EjlCHfdDGSof9ibXWxpPjl6UpjEsWtTTbiay0RrKjrp814wnibkkQ/132" width="30px"><span>Foxyier</span> 👍（0） 💬（0）<div>有一个地方没看懂， 文中先说了「互联网中往往服务器才是主动关闭连接的一方」，后续的内容中又把客户端称为主动方，服务端称为被动方。 所以有一些混乱， 四次挥手的过程中到底是谁先关闭的连接。</div>2021-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/2d/cd/f4a16584.jpg" width="30px"><span>神经蛙</span> 👍（0） 💬（0）<div>老师好，tcp_tw_reuse 配合 tcp_timestamps 可以作为客户端来复用TIME_WAIT的端口。那么作为服务端，应该怎么来减少TIME_WAIT的状态呢？</div>2021-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/da/cb/02bf0f14.jpg" width="30px"><span>liutebin</span> 👍（0） 💬（0）<div>这一节干货满满！光看这些知识，却很少在工作中运用。老师有没有好的办法，让我们自己可以模拟这些问题，并调优实践。</div>2021-04-15</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoH9Mlw0kLK0p39vhQpdvkbQP5TX96DB9HMJ1POaTVDpMZg4rjlO3WCAqiaWWMc77ffS3vTo8qWdXA/132" width="30px"><span>xdargs</span> 👍（0） 💬（0）<div>一直攒着没看，只是听的话效果不大，每次产生大量TIME_WAIT和CLOSE_WAIT就要去查一遍到底是谁的问题，一知半解两三年，上一篇加这一篇理顺了自己好久的模凌两可</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5f/83/bb728e53.jpg" width="30px"><span>Douglas</span> 👍（0） 💬（0）<div>【当然，tcp_max_tw_buckets 也不是越大越好，毕竟内存和端口号都是有限的。有没有办法让新连接复用 TIME_WAIT 状态的端口呢？如果服务器会主动向上游服务器发起连接的话，就可以把 tcp_tw_reuse 参数设置为 1，它允许作为客户端的新连接，在安全条件下使用 TIME_WAIT 状态下的端口。】 文章的意思【如果服务器会主动向上游服务器发起连接的话】 是，只有主动发起连接的一端，才可以复用这个端口么</div>2020-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（0） 💬（2）<div>“有没有办法让新连接复用 TIME_WAIT 状态的端口呢？”
---------------------------------------------------------------
老师，TCP的状态与端口之间究竟是什么关系？这块表面知道有点关系但是有点模糊。</div>2020-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（0） 💬（1）<div>如果设置了SO_LINGER选项且超时时间大于0，如果超时时间之内发完了缓冲区的数据，之后是不是走正常的4次挥手呢？ 四次挥手如果再超时的话才直接发rst ？ 

老师得课后问题中说SO_LINGER 选项希望用四次挥手代替rst关闭连接的方式。应该是想说用rst代替四次挥手吧？ </div>2020-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/fa/dceae1c9.jpg" width="30px"><span>陈先生</span> 👍（0） 💬（0）<div>请问安全复用的原理是什么呢？SO_REUSEADDR是不是做不到安全复用？</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cb/92/cfc1cfd3.jpg" width="30px"><span>贝氏倭狐猴</span> 👍（0） 💬（0）<div>“如果服务器会主动向上游服务器发起连接的话，就可以把 tcp_tw_reuse 参数设置为 1，它允许作为客户端的新连接，在安全条件下使用 TIME_WAIT 状态下的端口。” 问下什么情况还是安全条件呢？</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/72/15/a8b97a39.jpg" width="30px"><span>LubinLew</span> 👍（0） 💬（0）<div>提问，当主动方关闭连接时，被动方仍然可以在不调用 close 函数的状态下，长时间发送数据，此时连接处于半关闭状态。这一特性是 TCP 的双向通道互相独立所致，却也使得关闭连接必须通过四次挥手才能做到。

这里指的是主动方调用 shudown(fd,SHUT_WR) 这种特殊情况吧</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/5f/e6/8a5f9951.jpg" width="30px"><span></span> 👍（0） 💬（0）<div>老师，你好，请问服务端的接收窗口是针对所有客户端的TCP连接还是单个TCP连接，如果是客户端所有的TCP连接，那这个SQE如何保持有序，如有是单个连接又如何把接收窗口占满</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f7/d5/e63ee90f.jpg" width="30px"><span>Cola</span> 👍（0） 💬（0）<div>有个问题请教一下，关于so_linger选项，在一个网络框架服务端源码上看到针对监听socket，会设置l_onff=1, l_linger=0，针对accept之后建立的连接socket，会设置l_onff=0, l_linger=0，这里的用意是什么呢，l_onff=1, l_linger=0可以避免TW状态，但是在监听socket上如此设置还是这个目的吗？</div>2020-05-24</li><br/>
</ul>