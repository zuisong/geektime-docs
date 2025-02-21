你好，我是邵亚方。

如果你做过Linux上面网络相关的开发，或者分析过Linux网络相关的问题，那你肯定吐槽过Linux系统里面让人眼花缭乱的各种配置项，应该也被下面这些问题困扰过：

- Client为什么无法和Server建立连接呢？
- 三次握手都完成了，为什么会收到Server的reset呢？
- 建立TCP连接怎么会消耗这么多时间？
- 系统中为什么会有这么多处于time-wait的连接？该这么处理？
- 系统中为什么会有这么多close-wait的连接？
- 针对我的业务场景，这么多的网络配置项，应该要怎么配置呢？
- ……

因为网络这一块涉及到的场景太多了，Linux内核需要去处理各种各样的网络场景，不同网络场景的处理策略也会有所不同。而Linux内核的默认网络配置可能未必会适用我们的场景，这就可能导致我们的业务出现一些莫名其妙的行为。

所以，要想让业务行为符合预期，你需要了解Linux的相关网络配置，让这些配置更加适用于你的业务。Linux中的网络配置项是非常多的，为了让你更好地了解它们，我就以最常用的TCP/IP协议为例，从一个网络连接是如何建立起来的以及如何断开的来开始讲起。

## TCP连接的建立过程会受哪些配置项的影响？
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/05/d47cee18.jpg" width="30px"><span>wong ka seng</span> 👍（18） 💬（1）<div>老师好，请问一下， 想听说tcp成功连接后很占资源，有没有具体的解说？例如每个连接消耗多少记忆体和cpu？谢谢！</div>2020-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/8c/13/62e221c7.jpg" width="30px"><span>Abby</span> 👍（12） 💬（1）<div>老师，如果不开启abort_on_overflow, 是不是这个时候client认为连接建立成功了，就会发送数据。server端发现这个连接没有建立，直接就再次发送reset回去咯？所以设置成1意义不大</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（7） 💬（1）<div>“如果不维持 TIME_WAIT 这个状态，那么再次收到对端的 FIN 包后，本端就会回一个 Reset 包，这可能会产生一些异常。”  老师，我有两个问题：
1. 如果不维持TCP状态，最后一次ACK结束，Client端认为已经结束，就会关闭连接。这时候Server端在发送FIN包，客户端应该就收不到了吧？
2. 假设客户端收到了，回复RESET，会产生什么样的异常？</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/f0/abb7bfe3.jpg" width="30px"><span>机制小风风</span> 👍（7） 💬（3）<div>半连接，即收到了 SYN 后还没有回复 SYNACK 的连接，Server 每收到一个新的 SYN 包，都会创建一个半连接，然后把该半连接加入到半连接队列（syn queue）中。

开启 SYN Cookies 后，还会创建半连接吗？如果不创建是不是不用设置半连接队列了？
如果创建半连接，还会加入队列吗？如果加入，是收到ack,确认好cookies加入，还是什么时候加入？

不保存客户端信息，是不是指的不创建半连接？</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/81/02/59f5f168.jpg" width="30px"><span>小白debug</span> 👍（5） 💬（2）<div>老师你好，文章里提到&quot;有些情况下 1s 的阻塞时间可能都很久，所以有的时候也会将三次握手的初始超时时间从默认值 1s 调整为一个较小的值，比如 100ms&quot; ，这里面怎么把第一次握手syn的初始超时时间从1s改成100ms？查了很多资料只看到介绍改超时次数tcp_syn_retries，而没有看到改默认超时时间。</div>2020-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/91/1d332031.jpg" width="30px"><span>我能走多远</span> 👍（4） 💬（1）<div>在一些文章中看到TIME_WAIT 和 FIN_WAIT2 状态的最大时长都是 2 MSL，由于在 Linux 系统中，MSL 的值固定为 30 秒，所以它们都是 60 秒。下面时我环境中
[13:47:18]root:workspace$ cat &#47;proc&#47;sys&#47;net&#47;ipv4&#47;tcp_fin_timeout
60
TIME_WAIT 状态存在这么长时间，也是对系统资源的一个浪费，所以系统也有配置项来限制该状态的最大个数，该配置选项就是 tcp_max_tw_buckets=10000，如果当前环境TIME_WAIT数量达到10000时，又是怎么处理的？
</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（2） 💬（1）<div>isn和paws老师可以细讲不，还有nat转换会转换seq吗？</div>2020-09-22</li><br/><li><img src="" width="30px"><span>地下城勇士</span> 👍（1） 💬（1）<div>看了好多篇，老师的图都很到为，请问一下老师的图是用什么工具画的？</div>2020-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKT9Tk01eiaQ9aAhszthzGm6lwruRWPXia1YYFozctrdRvKg0Usp8NbwuKBApwD0D6Fty2tib3RdtFJg/132" width="30px"><span>欧阳洲</span> 👍（1） 💬（5）<div>老师好：
FIN_WAIT_2 超时时间是 tcp_fin_timeout 控制，
TIME_WAIT 默认也是 60s，但是 &#47;proc&#47;sys&#47;net&#47;ipv4&#47; 下没有wait相关文件名，
TIME_WAIT 是与 FIN_WAIT_2 共用了同一个选项吗?</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9c/85/d9614715.jpg" width="30px"><span>Felix</span> 👍（0） 💬（1）<div>收到SYN还没有回复SYNACK的是半连接，那回复了SYNACK还没有收到ACK的连接算不算是半连接，这也是一个中间状态，是否也在syn queue里面，即syn queue只包含第一次握手还是只包含第二次握手还是第一次第二次都包含</div>2021-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/1e/74d65100.jpg" width="30px"><span>jack motor</span> 👍（0） 💬（1）<div>TIME_WAIT 状态持续时间是60s，修改这个是不是必须要重新编译内核？</div>2020-11-27</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIt0nAFvqib3fpf9AIKUrEJMdbiaPjnKqCryevwjRdqrbzAIxdOn3P5wCz28MNb5Bgb2PwEdCezLEWg/132" width="30px"><span>KennyQ</span> 👍（4） 💬（0）<div>这块内容学习到了，可以运用到自己在生产中碰到的问题，吹牛可以吹很久！</div>2020-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/1d/0c1a184c.jpg" width="30px"><span>罗辑思维</span> 👍（3） 💬（0）<div>这个章节收获满满，老师把抽象的网络三次握手和四次挥手的过程，跟Linux网络参数配置对应起来，而且还根据场景给了具体的优化建议。

请问老师，能再推荐些Linux参数配置的优化建议学习资料么。网络上的资料要么只讲概念，没导入具体场景，或者是没确认基准线下进行优化，适用面很窄。</div>2020-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/05/431d380f.jpg" width="30px"><span>拂尘</span> 👍（3） 💬（0）<div>老师，有以下疑惑，希望能解答一下。
连接建立3次握手过程
1.client每次超时重试的超时时间，是采用指数级回退的，那linux有相应的配置参数，可以配置这个指数回退的策略吗？
2.根据回退策略和重试次数，可以计算出client总体connect的阻塞时间，linux有没有参数可以精细化或者单独配置这个总体阻塞超时时间呢？
连接断开4次挥手过程
3.连接断开是分主被动方的。除了client会作为主动方断开连接，server也可以作为主动方断开连接吗？如果是，在这种情况下，client和server双方，他们整体的时间轴状态转换图又是如何的呢？（因为基本上搜索到的资料，都是只描述了client作为主动方发起关闭的流程）
4.如果server的ack和fin是打包一起发给client的话，client会有fin_wait_2状态吗？
5.您提到选项tcp_tw_recycle用来控制TIME_WAIT状态，而且很危险。能否详细描述一下此选项配置的意义，会影响time_wait的什么行为？以及具体的危害内容？
6.您提到，如果在server中CLOSE_WAIT状态的连接很多，基本断定是应用程序里漏掉了close调用。这里的close调用是指client端的吗？</div>2020-11-07</li><br/><li><img src="" width="30px"><span>dbo</span> 👍（0） 💬（0）<div>tcp_syn_retries 的默认值是 6，也就是说如果 SYN 一直发送失败，会在（1 + 2 + 4 + 8 + 16+ 32 + 64）秒，即 127 秒后产生 ETIMEOUT 的错误。

这里表示有误，实际情况如下：

果 SYN 一直发送失败，会在（1 + 2 + 4 + 8 + 16+ 32）秒，即 63 秒后产生 ETIMEOUT 的错误。</div>2023-09-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/mfZN0Rvvg3fhxtX3vglErbp2rwlwviccS3LXTRXZAdsB88UEwtuCurrWhjlgcHYicQcXoukbbRKWKRAFQNZh9RBQ/132" width="30px"><span>打工人</span> 👍（0） 💬（0）<div>老师好，我学习这门课比较晚了，不过最近测试发现不管是somax还是syn_backlog都设置成多少，模拟syn flood攻击时，netstat里查看syn_recv状态的连接都是256，求解</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/85/1dc41622.jpg" width="30px"><span>姑射仙人</span> 👍（0） 💬（1）<div>图中的client和server不是确定的吧？还是要看是谁发起的关闭操作。也就是说客户端和服务端都会存在time wait状态的连接，对吗？</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/c4/35/2cc10d43.jpg" width="30px"><span>Wade_阿伟</span> 👍（0） 💬（0）<div>这节课干活满满，熟悉了tcp的三次握手和四次挥手的过程，以及可以通过哪些配置来调整优化上述过程。</div>2021-09-01</li><br/><li><img src="" width="30px"><span>威威</span> 👍（0） 💬（1）<div>看了第三遍 最近遇到了一个问题 0.0.0.0 dns域名反解ptr，想要快速定位哪些进程发送了此udp服务，通过tcpdump可以看到这些流，得到原端口，但通过lsof查看端口对应进程查不到，猜测是实效性问题，好啥好办法</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/9d/13/a8b614b8.jpg" width="30px"><span>小孩不乖</span> 👍（0） 💬（0）<div>学到了</div>2020-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/7f/746a6f5e.jpg" width="30px"><span>Q</span> 👍（0） 💬（0）<div>第一次看到把内核网络参数和TCP-IP建连和断连图结合起来的讲！！之前看陶辉老师的Nginx也有讲过，但只是文字版，理解起来有点费劲。这期课图文并茂，更容易理解了！</div>2020-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>不错， 老师总结得很好</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/7e/74/69bfb430.jpg" width="30px"><span>Su</span> 👍（0） 💬（0）<div>高产啊.</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/96/47/93838ff7.jpg" width="30px"><span>青鸟飞鱼</span> 👍（0） 💬（0）<div>又涨知识了</div>2020-09-12</li><br/>
</ul>