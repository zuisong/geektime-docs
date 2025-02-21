你好，我是LMOS。

从这节课开始，我们进入IO相关基础知识的学习，想要开发高性能的应用程序，这些基础知识必不可少。

前面的课程里，我们已经对进程和内存有了一定了解。进程在运行时刻和CPU是紧密相关的，抽象出进程就是为了提高CPU的利用率。因此，我们关注进程和内存，等同于关注CPU和RAM。

一个计算机系统，无论是PC，还是手机，除了有CPU和RAM，还有各种外设，如键鼠、硬盘、显卡、以太网卡、声卡等各种USB扩展设备。

这些设备独立在CPU和内存之外，统称为外设。但是，外设通信的速度、大小、数据类型和传输方式各不相同，所以为了实现系统的整体效率最大化，操作系统实现了IO Cache和IO调度。今天我们就来研究它们。

### IO Cache

顾名思义，Cache即为缓存，IO是指令外设传输（IN/OUT）数据的操作。

缓存是怎么回事我们都知道，由此我们就可以这样理解IO Cache：把外设的IO操作的数据保存起来，当重新执行IO操作时，先从之前保存的地方开始查找，若找到需要的数据，即为命中，这时就不要去操作外设了；若没有命中就去操作外设。其中的数据，会根据IO操作频率进行组织，把操作最频繁的内容放在最容易找到的位置，达到性能最优化。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/47/b5/2729f25c.jpg" width="30px"><span>ryohei</span> 👍（3） 💬（1）<div>牛逼 这节课，很多之前不清楚的概念 弄明白了</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/7b/cbe07b5c.jpg" width="30px"><span>顾琪瑶</span> 👍（2） 💬（1）<div>很多不明白的点, 都在这个课程中解答了, 真的牛逼.
想问下这些资料都是从哪获取的呢</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（2） 💬（1）<div>文件系统有ntfs和ext4，很多游戏软件只支持ntfs格式，由于磁盘运行效率远低于cpu，好的算法文件系统可以提高磁盘的利用效率（包括跳过磁片中的坏点）
io cache是必须的，就好比如把d盘的文件a剪切到c盘中，观察可以得知，假如传输过程中故意关机等，再次开机文件a还在d盘。预计cpu是传输完再删除，这样尽可能的减少磁盘碎片（特别的减少不能被系统识别的碎片冗余存在），io cache也方便操作系统部分情况下延迟应对硬件需求！</div>2022-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2f/d7/77/0bbdc9af.jpg" width="30px"><span>VMNode</span> 👍（0） 💬（1）<div>图是 page cache 建立在 buffer cache 上，文稿写反了吧……</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/14/66/70a6a206.jpg" width="30px"><span>后视镜</span> 👍（0） 💬（1）<div>想问下，mmap 文件的话，是否经过pagecache啊，没搞清楚mmap和pagecache的关系，希望得到老师的指点。</div>2022-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>一直有个疑问，如果一个写操作，写到cache，还没写到磁盘，断电了，上层应用能感知吗？</div>2022-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f8/2c/92969c48.jpg" width="30px"><span>青玉白露</span> 👍（0） 💬（1）<div>固态硬盘的出现大大降低了io的耗时</div>2022-10-16</li><br/>
</ul>