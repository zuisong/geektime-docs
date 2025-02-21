> 250GB容量，512MB DDR4缓存，连续读取不超过550MB/s，连续写入不超过520MB/s。

“双十一”在天猫看到一款固态硬盘有上面的这些介绍，这些数字分别代表了什么意思？

在专栏前面卡顿和启动优化里，我也经常提到I/O优化。可能很多同学觉得I/O优化不就是不在主线程读写大文件吗，真的只有这么简单吗？那你是否考虑过，从应用程序调用read()方法，内核和硬件会做什么样的处理，整个流程可能会出现什么问题？今天请你带着这些疑问，我们一起来看看I/O优化需要的知识。

## I/O的基本知识

在工作中，我发现很多工程师对I/O的认识其实比较模糊，认为I/O就是应用程序执行read()、write()这样的一些操作，并不清楚这些操作背后的整个流程是怎样的。

![](https://static001.geekbang.org/resource/image/60/d4/60928bc51c0d04b1c39b24282e8126d4.jpg?wh=2223%2A1053)

我画了一张简图，你可以看到整个文件I/O操作由应用程序、文件系统和磁盘共同完成。首先应用程序将I/O命令发送给文件系统，然后文件系统会在合适的时机把I/O操作发给磁盘。

这就好比CPU、内存、磁盘三个小伙伴一起完成接力跑，最终跑完的时间很大程度上取决于最慢的小伙伴。我们知道，CPU和内存相比磁盘是高速设备，整个流程的瓶颈在于磁盘I/O的性能。所以很多时候，文件系统性能比磁盘性能更加重要，为了降低磁盘对应用程序的影响，文件系统需要通过各种各样的手段进行优化。那么接下来，我们首先来看文件系统。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKw77qmuyx5tPjGznNo7DmKvpU688GpazMQtfdafxj6Z0MSviaIlBtuEs2ibtYxCmibfWpOkKIoXibiavA/132" width="30px"><span>menty</span> 👍（7） 💬（2）<div>请问，微信debug模式下，运行会很卡吗。目前我司的app在debug模式下就超卡，非得在debug=false下才运行顺畅，不知是何原因导致</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/8d/a3fd8957.jpg" width="30px"><span>Kenny</span> 👍（4） 💬（1）<div>张老师，你好，mmap技术是首先通过业缓存去拿数据，如果没有就发生缺页中断，然后发生物理io从磁盘拿数据到业缓存，然后再从业缓存拿数据，这样相对普通文件io就少了一次逻辑io(即与文件系统的io)，是可以这样理解么？</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（1） 💬（1）<div>真的是高手课，如果之前没看过内存分析的教程，有些东西我都不大懂</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3f/29/e09e9ab8.jpg" width="30px"><span>Lll</span> 👍（1） 💬（1）<div>&quot;我们知道，CPU 和内存相比磁盘是高速设备，整个流程的瓶颈在于磁盘 I&#47;O 的性能。&quot;这句话好像有歧义，请问是笔误了吧？</div>2019-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/9d/f30ef86c.jpg" width="30px"><span>一把紫茶壶</span> 👍（1） 💬（1）<div>请问下在文件遍历方面，(尤其是层级比较多的文件，例如微信的image2)，有什么好的方案提高遍历速度吗？</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/5b/ac/78491d1d.jpg" width="30px"><span>有生丶之莲</span> 👍（1） 💬（1）<div>张老师好，之前遇到过一些anr，定位到firebase中的tokenRefresh这块方法，但是自己重写这个方法也就只是用SP把token保存下来，请问SP读写会导致这个吗？SP的apply和commit都试过，apply说是异步的，但主线程会等着保存完成的回调，是这样吗？</div>2018-12-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOiaS2BtAEuc7ndTkWb74nKXcZfgmCrbke0ia4b7zTyiatXm5WMyrKWB2qoibN0TibHufz94FLGfJAPWA/132" width="30px"><span>Geek_a24664</span> 👍（0） 💬（1）<div>你好老师，我遇到过在向文件中写入字符串时，最终发现文件中内容和写入顺序不太一致，能不能指点一下思路，现在毫无头绪</div>2019-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3d/3d/a9c8d564.jpg" width="30px"><span>Joyce</span> 👍（0） 💬（1）<div>IO优化，应用层可以做什么</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/8d/a3fd8957.jpg" width="30px"><span>Kenny</span> 👍（0） 💬（1）<div>hi，张老师，刚你说业缓存在内存紧张的时候会被回收，那么发生GC一定会回收吗？还是说跟GC无关联？是有另外一套内存检测回收业缓存的机制？那么启动优化，除了资源重排，降低总内存也能提升io次数？</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/19/6f037647.jpg" width="30px"><span>东方</span> 👍（21） 💬（0）<div>看到很多朋友提到SP的问题，SP造成ANR的原因大家也知道，我来说说我的经验。

1.把sdk中SP的实现剥离出来，重写Application的getSharedPreferencen方法。这里需要注意几点，a.低版本multidex，b.Activity Service中getSP的context必须是ApplicationContext。

2.上述的方案依然是普通File操作，解析xml，线上依然有fsync导致ANR。

3.自己使用mmap实现sp的映射，或者使用微信的MMKV，但是getAll方法需要自己兼容。

4.增加大kv的监控。

大家伙还有更好的方案可以继续交流</div>2018-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/b9/4ef297e5.jpg" width="30px"><span>itmagic_jack</span> 👍（8） 💬（0）<div>Java应用层的I&#47;O优化，可以考虑使用square公司出品的Okio框架（Okhttp底层IO实现），在Java平台上使用，简化了api调用，支持IO超时检测，优化了资源缓存等</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/bb/323a3133.jpg" width="30px"><span>下雨天</span> 👍（3） 💬（0）<div>大佬，好！SharedPreference 跨进程读写就非常容易出现数据丢失的情况。从io性能方面来看，应用层有什么更好的方案和设计来提SharedPreference跨进程访问数据的可靠性么？</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/19/6f037647.jpg" width="30px"><span>东方</span> 👍（1） 💬（0）<div>对于io，如果使用glide作为默认的图片加载库，启动glide后，会把上一次符合条件的图片都一次给加载到内存中，这个是disklrucache做的，想问一下张老师，有什么经验或者办法，只load感兴趣的图片。再者微信的图片加载框架底层是mmap实现吗？</div>2018-12-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKKsdByrvUyfhPcKTubI1JnP5SAPib3dw1vMffmkEK64iaTFoKCACgzLA819XwzKW7FC9GBjpWqD5XA/132" width="30px"><span>Geek_0c63f5</span> 👍（0） 💬（0）<div>张老师你好，关于数据库文件损坏这种问题，有什么可分享的问题定位思路吗？大部分原因是应用自身导致的，所以重点是多进程或者多线程操作io这个方向吗？</div>2023-03-12</li><br/><li><img src="" width="30px"><span>扈丽霞</span> 👍（0） 💬（0）<div>文件读取不是以page为单位，擦除以block为单位吗？</div>2022-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（0） 💬（0）<div>连续写入限制指的是一秒最多写入多大小吗？</div>2019-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ef/9e/78420b67.jpg" width="30px"><span>0928</span> 👍（0） 💬（1）<div>说到io，我有个问题想咨询一下：
场景大概是，有26亿的数据需要读取从HBase中读取出来分别写到12个文件中取，有什么方式能高效且数据不错乱的写到文件中去呢？
想法：
1.读取出来的数据需要并发写到文件中
2.每次读取一定的缓存大小批量写入，不能一条一条写入
3.文件并发写入会出现错位等问题，所以需要一个写队列来处理
问题：
目前1和2两种方式没什么问题，但是在写队列的设计上有一定问题，希望给点意见。
如果最终写文件还是单线程的话性能瓶颈都在这里，这里应该怎么设计呢？</div>2018-12-28</li><br/>
</ul>