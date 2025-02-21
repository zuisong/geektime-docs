你好，我是刘超。

模块六有关数据库调优的内容到本周也正式结束了，今天我们一起串下MySQL中InnoDB的知识点。InnoDB存储引擎作为我们最常用到的存储引擎之一，充分熟悉它的的实现和运行原理，有助于我们更好地创建和维护数据库表。

## InnoDB体系架构

InnoDB主要包括了内存池、后台线程以及存储文件。内存池又是由多个内存块组成的，主要包括缓存磁盘数据、redo log缓冲等；后台线程则包括了Master Thread、IO Thread以及Purge Thread等；由InnoDB存储引擎实现的表的存储结构文件一般包括表结构文件（.frm）、共享表空间文件（ibdata1）、独占表空间文件（ibd）以及日志文件（redo文件等）等。

![](https://static001.geekbang.org/resource/image/f2/92/f26b2fad64a9a527b5ac0e8c7f4be992.jpg?wh=1768%2A1020)

### 1. 内存池

我们知道，如果客户端从数据库中读取数据是直接从磁盘读取的话，无疑会带来一定的性能瓶颈，缓冲池的作用就是提高整个数据库的读写性能。

客户端读取数据时，如果数据存在于缓冲池中，客户端就会直接读取缓冲池中的数据，否则再去磁盘中读取；对于数据库中的修改数据，首先是修改在缓冲池中的数据，然后再通过Master Thread线程刷新到磁盘上。

理论上来说，缓冲池的内存越大越好。我们在[第38讲](https://time.geekbang.org/column/article/120160)中详细讲过了缓冲池的大小配置方式以及调优。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（30） 💬（4）<div>到此刻Java性能调优实战算是从头到尾的学习了一遍，首先，为老师的敬业态度点赞，跟着老师也学习到了许多性能调优的方法和技巧。之前也看过书，加入目前的公司后加班比较严重，看书的效率也不高了，从去年在极客时间学习后就一发不可收拾买了几十个专栏，现在还有许多未开始学习，不过买专栏有种令人安心的感觉，每天也在不断的学习，看的多了发现不同的专栏重复的内容也多了，当然，看不完了还继续买，我觉得买专栏的钱其实相对于学习到的知识来讲是非常值得的。哪怕只学习一遍，有些专栏值得一刷再刷，毕竟写专栏的老师水货少，极客时间选择讲师的专业性，也是我不断在这里付费的一个原因。我发现没有九阳神功真是学什么都慢，在计算机的世界里计算机组成原理&#47;操作系统原理&#47;编译原理&#47;计算机网络原理&#47;计算机数据库原理&#47;数据结构与算法这些就是九阳神功，如果这些精通，什么这个那个招式全都一学就会且速度快印象深。
计算机界所有的这个理论那个原理基本都是围绕性能和容量在做文章，都想要更快的速度更大的存储空间，在升一层就是为了和时间赛跑开拓更为广阔的空间，快能占据许多的先机，不管什么行业快都具有优势。在极客时间我感觉增长见闻的效率还是挺高的，不过不看书还是不行，深度细致度系统性这些知识体验还是不能和书媲美。不学习是不可能的，人生如逆水行舟不进则退，其实学习的慢也会渐渐失去竞争优势。好奇老师这么多知识积累了多久？都是怎么积累的?除了坚持还有什么别巧妙嘛？
我的同事中有一位非常拼命，两年学习的东西顶别人四五年，住在公司附近几乎每天都疯狂加班学习，现在也非常厉害从工资上来说已经秒杀了许多工作七八年的人。先去阿里再去拼多多，真是太拼了，生活就是上班加班学习。其实我也想这么拼，我也想年入百万，不过即使时间付出的差不多，人的脑回沟及过往的受教育经历特别是思维方式的训练加英语的加持也会导致非常大的差异。
嗯，感慨有点多，继续加油吧!保持好学习的节奏，买的专栏或书，如果不看不学，还不如买几卷卫生纸。
再次感谢老师的分享，我相信有朝一日我也会像老师一样牛逼!</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5f/73/bb3dc468.jpg" width="30px"><span>拒绝</span> 👍（6） 💬（3）<div>老师，本讲的缓存池是基于引擎层的缓存吗？与server层的缓存有什么不同？
每个页存放的行记录也是有硬性定义的，最多允许存放 16KB&#47;2-200行，即7992行，是怎么计算来的？</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/78/99/6060eb2d.jpg" width="30px"><span>平凡之路</span> 👍（4） 💬（4）<div>老师，您好，我一直有个疑问，如果数据库设置最大连接数为1000，如果像电商系统这样的网站，同时有10000个人访问登录，那不是有9000人都要等待？电商系统是用的其他数据库存储系统吗？</div>2019-12-04</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eotSSnZic41tGkbflx0ogIg3ia6g2muFY1hCgosL2t3icZm7I8Ax1hcv1jNgr6vrZ53dpBuGhaoc6DKg/132" width="30px"><span>张学磊</span> 👍（2） 💬（1）<div>老师，客户端读取数据时，如果数据存在于缓冲池中，客户端就会直接读取缓冲池中的数据，否则将磁盘中的数据加载到缓冲池，再从缓冲池中读取，客户端始终和缓冲池交互，准确的说是不是应该这样？
另外有一处编辑错误，InnoDB 存储引擎是面向列的（row-oriented)，应该写成行。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/57/ce10fb1b.jpg" width="30px"><span>天天向上</span> 👍（1） 💬（1）<div>老师在：MySQL8.0取消cache 那岂不是每次查询都要访问磁盘 这样不合理吧 的回复中回答：还有一层缓冲池。但是缓冲池命中的概率很低很低吧。
</div>2020-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/69/5dbdc245.jpg" width="30px"><span>张德</span> 👍（1） 💬（2）<div>老师  MySQL8.0取消cache   那岂不是每次查询都要访问磁盘  这样不合理吧  还是我理解错了</div>2019-09-03</li><br/><li><img src="" width="30px"><span>ty_young</span> 👍（0） 💬（1）<div>老师您好，请问Master Thread回收的undo页和Purge Thread回收的undo log是一回事么</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>老师讲得很好，这个知识串讲很不错，跟着老师一起精进。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6e/3f/49e5079f.jpg" width="30px"><span>楞伽山人</span> 👍（1） 💬（2）<div>老师 您好 undo log是解决ACID中的A吧 不是C吧</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/6e/3a0b4930.jpg" width="30px"><span>FiRerOUNd</span> 👍（0） 💬（0）<div>我理解的innodb没有实现redolog，这个是mysql服务器层实现的，所有存储引擎共同这个文件。</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/9c/2413fd6f.jpg" width="30px"><span>ETLshow</span> 👍（0） 💬（0）<div>性能调优还是要多刷几遍</div>2022-04-10</li><br/><li><img src="" width="30px"><span>ty_young</span> 👍（0） 💬（0）<div>“Pager Cleaner Thread 是新引入的一个用于协助 Master Thread 刷新脏页到磁盘的线程”，老师好，请问这个脏页值的是什么</div>2021-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/81/e6/6cafed37.jpg" width="30px"><span>旅途</span> 👍（0） 💬（1）<div>Buffer Pool 中更新的数据未刷新到磁盘中，该内存页我们称之为脏页  
问下老师 这句话的意思是更新的数据未成功刷新到磁盘还是在内存中未刷新到磁盘</div>2020-09-13</li><br/>
</ul>