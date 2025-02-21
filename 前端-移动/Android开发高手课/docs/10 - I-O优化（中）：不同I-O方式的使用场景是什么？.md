今天是2019年的第一天，在开始今天的学习前，先要祝你新年快乐、工作顺利。

I/O是一个非常大的话题，很难一次性将每个细节都讲清楚。对于服务器开发者来说，可以根据需要选择合适的文件系统和磁盘类型，也可以根据需要调整内核参数。但对于移动开发者来说，我们看起来好像做不了什么I/O方面的优化？

事实上并不是这样的，启动优化中“数据重排”就是一个例子。如果我们非常清楚文件系统和磁盘的工作机制，就能少走一些弯路，减少应用程序I/O引发的问题。

在上一期中，我不止一次的提到Page Cache机制，它很大程度上提升了磁盘I/O的性能，但是也有可能导致写入数据的丢失。那究竟有哪些I/O方式可以选择，又应该如何应用在我们的实际工作中呢？今天我们一起来看看不同I/O方式的使用场景。

## I/O的三种方式

请你先在脑海里回想一下上一期提到的Linux通用I/O架构模型，里面会包括应用程序、文件系统、Page Cache和磁盘几个部分。细心的同学可能还会发现，在图中的最左侧跟右上方还有Direct I/O和mmap的这两种I/O方式。

那张图似乎有那么一点复杂，下面我为你重新画了一张简图。从图中可以看到标准I/O、mmap、直接I/O这三种I/O方式在流程上的差异，接下来我详细讲一下不同I/O方式的关键点以及在实际应用中需要注意的地方。
<div><strong>精选留言（12）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/N0NACGUr8dNAbN6BdiagPHBaB0EnyDsI9zWpwJteqTY38apOEnTOA7JkBAQnzYKJBgxu3Q8YMUILwLAB6camn4w/132" width="30px"><span>Swing</span> 👍（6） 💬（2）<div>很好奇，像微信这样一个权限普通的app，怎么接入的自己的小文件系统（或者说 替换原生的文件系统）？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a1/6b/bebb4342.jpg" width="30px"><span>星风雪雨</span> 👍（3） 💬（1）<div>mmap，一次拷贝；我的理解是磁盘拷贝到主存，而普通文件是两次拷贝：磁盘--&gt;页缓存--&gt;用户空间，虽然是两次拷贝，但是页缓存--&gt;用户空间是在内存拷贝，虽然多了一次，但是这次是内存操作，应该是很快的；那mmap速度相对读文件快，主要原因是系统调用少引起的吗？</div>2019-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/fd/035f4c94.jpg" width="30px"><span>欢乐小熊</span> 👍（3） 💬（3）<div>Binder 通信的图有些不能理解

进程的用户空间与内核空间是通过 binder_mmap 类似匿名映射的方式分配的, 用户与内核之间是不需要拷贝的
数据的拷贝, 应该在内核空间不同进程的 Binder 缓冲区

不知理解的是否正确, 请老师指教</div>2019-06-20</li><br/><li><img src="" width="30px"><span>taotaomami</span> 👍（1） 💬（1）<div>“iowait高，io一定有问题” 这个观点有点异议，借用网上一篇文章对iowait的解释“%iowait 表示在一个采样周期内有百分之几的时间属于以下情况：CPU空闲、并且有仍未完成的I&#47;O请求”   iowait这个参数的值对我们观察io活动意义比较小</div>2019-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>想请教下，mmap 映射的是用户缓冲区和 page cache 页缓存吗？copy&#47;write 也只需要发生在 page cache 和磁盘？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/25/ba0e44af.jpg" width="30px"><span>恒</span> 👍（12） 💬（0）<div>老师好，文件IO这一块您讲的非常好，对我的帮助很大，谢谢了</div>2019-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（3） 💬（1）<div>文中提到“我们使用 mmap 仅仅只需要一次数据拷贝”，这个说法是不准确的，内存映射的场景直接操作的就是映射到的内存，不需要额外的一次拷贝。
Binder的方案确实需要一次数据拷贝，那是Binder的机制决定的，而不是因为内存映射需要一次数据拷贝。

在Binder机制中，内存映射在一次通信过程中是单侧的：数据发送方通过transact将数据写入到内核态，这个过程需要一次数据拷贝(写入过程非内存映射，否则不需要“写”)；而接收方直接映射到了这一块内存，接收的过程不需要内存拷贝，所以Binder机制需要一次数据拷贝。</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3e/19/873abe8a.jpg" width="30px"><span>董尚斌</span> 👍（3） 💬（0）<div>真值，以前就只知道，写文件，读文件，具体实现的代码，怎么写。现在发现有些情况下的文件读写速度在不同设备上的表现方式的原因。

我做的最多的文件读操作是，全盘扫描本地文件（涉及读文件里面的字节来区分是否符合要求），以及多进程写日志的问题（aidl统一交给主应用的主进程，涉及文件锁和磁盘io频繁的问题）

听了最近的两节，感觉，这些地方可以适当的优化下。

谢谢，老师。</div>2019-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/8f/d8596c40.jpg" width="30px"><span>elephant</span> 👍（2） 💬（1）<div>&quot;微信也开发了一套叫 SFS 的小文件管理系统，主要用在朋友圈图片的管理....&quot;

真的是跪着看微信的技术方案 orz</div>2019-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e0/87/b7242f1c.jpg" width="30px"><span>Mograine</span> 👍（1） 💬（0）<div>老师，我补习了一下iowait相关知识，因为我发现有些地方跟我的认知是冲突的，网上搜索后发现，很多博客纠正说，%iowait 高并不表示I&#47;O有瓶颈问题。老师可以回答下我这个问题吗。比如https:&#47;&#47;www.cnblogs.com&#47;probemark&#47;p&#47;5862293.html，老师你能解答下这个问题吗</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（1） 💬（0）<div>看了中这部分，已经对I&#47;O有了更深刻的认识，感觉自己学的Android都是皮毛呀</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1a/82/f039ae08.jpg" width="30px"><span>gk</span> 👍（0） 💬（0）<div>好强</div>2019-06-14</li><br/>
</ul>