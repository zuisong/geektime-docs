经过前面的预习和上一期我们聊的，大数据技术主要是要解决大规模数据的计算处理问题，但是我们要想对数据进行计算，首先要解决的其实是大规模数据的存储问题。我这里有一个直观又现实的问题想问你：如果一个文件的大小超过了一张磁盘的大小，你该如何存储？

我的答案是，单机时代，主要的解决方案是RAID；分布式时代，主要解决方案是分布式文件系统。

其实不论是在单机时代还是分布式时代，大规模数据存储都需要解决几个核心问题，这些问题都是什么呢？总结一下，主要有以下三个方面。

1.**数据存储容量的问题**。既然大数据要解决的是数以PB计的数据计算问题，而一般的服务器磁盘容量通常1～2TB，那么如何存储这么大规模的数据呢？

2.**数据读写速度的问题**。一般磁盘的连续读写速度为几十MB，以这样的速度，几十PB的数据恐怕要读写到天荒地老。

3.**数据可靠性的问题**。磁盘大约是计算机设备中最易损坏的硬件了，通常情况一块磁盘使用寿命大概是一年，如果磁盘损坏了，数据怎么办？

在大数据技术出现之前，我们就需要面对这些关于存储的问题，对应的解决方案就是RAID技术。今天我们就先从RAID开始，一起看看大规模数据存储方式的演化过程。

RAID（独立磁盘冗余阵列）技术是将多块普通磁盘组成一个阵列，共同对外提供服务。主要是为了改善磁盘的存储容量、读写速度，增强磁盘的可用性和容错能力。在RAID之前，要使用大容量、高可用、高速访问的存储系统需要专门的存储设备，这类设备价格要比RAID的几块普通磁盘贵几十倍。RAID刚出来的时候给我们的感觉像是一种黑科技，但其原理却不复杂，下面我慢慢道来。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/47/d217c45f.jpg" width="30px"><span>Panmax</span> 👍（15） 💬（1）<div>3. 数据可靠性的问题。使用 RAID 0、RAID 5 或者 RAID 6 方案的时候，由于数据有冗余存储，或者存储校验信息，所以当某块磁盘损坏的时候，可以通过其他磁盘上的数据和校验数据将丢失磁盘上的数据还原。

这里应该是 RAID1 吧</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（175） 💬（1）<div>连续写入：写入只寻址一次 存储位置与逻辑位置相邻 不用多次寻址

随机写入：每写一次 便寻址一次 增加了磁盘的寻址时间
</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/e6/a69cff76.jpg" width="30px"><span>lyshrine</span> 👍（42） 💬（4）<div>老师，为啥通常情况一块磁盘使用寿命大概是一年？磁盘不是能用很多年吗？一年一换成本会不会太高了？</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4f/d6/fd4794e0.jpg" width="30px"><span>o°cboy</span> 👍（30） 💬（1）<div>磁盘的读写过程，最消耗时间的地方就是在磁盘中磁道寻址的过程，而一旦寻址完成，写入数据的速度很快。
顺序写入只要一次寻址操作，而随机写入要多次寻址操作。所以顺序写入速度明显高于随机写入。
个人的理解，不正确的地方，还请多多指教。</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f3/89/fcfecb46.jpg" width="30px"><span>杰哥长得帅</span> 👍（18） 💬（2）<div>2. 数据读写速度的问题。RAID 根据可以使用的磁盘数量，将待写入的数据分成多片，并发同时向多块磁盘进行写入，显然写入的速度可以得到明显提高；同理，读取速度也可以得到明显提高。不过，需要注意的是，由于传统机械磁盘的访问延迟主要来自于寻址时间，数据真正进行读写的时间可能只占据整个数据访问时间的一小部分，所以数据分片后对 N 块磁盘进行并发读写操作并不能将访问速度提高 N 倍。

还是不能理解为何不能提高n倍。。。。

还有就是想问下数据校验信息是怎么实现的？
谢谢老师👨‍🏫</div>2020-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/64/86/f5a9403a.jpg" width="30px"><span>yang</span> 👍（17） 💬（1）<div>老师居然回我信息了，好开心！ 我最喜欢那种 讲课做事都亲自来的老师！ 听了老师四节课了，都是老师自己读，有的话是老师的原汁原味的话，在文稿里没有！ 给智慧老师打call!</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/67/3d/e336de58.jpg" width="30px"><span>hashmap</span> 👍（13） 💬（1）<div>磁盘寻址是耗时操作，是时间大于写入时间
连续写入，可以寻址一次，然后写入
随机写入，需要寻址多次，然后写入
所以连续写入快
这个问题可以延伸回答，为什么很多数据库索引采用b+树，而不是完全二叉树？
因为b+树的节点包含多个信息，可以连续读写磁盘
有一疑问？RAID技术是实现在哪里？
需要安装软件，还是磁盘的驱动实现</div>2018-11-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKugZjntLzMGvDicZaX7pAuwNw3aneI2zZlicKh0fqsmmlJ9VRrSjBBJc1m8K6CPuV6WQuHic4zNZT8Q/132" width="30px"><span>Geek_vqdpe4</span> 👍（10） 💬（1）<div>我想问一下，RAID 3的任意一块磁盘损坏，通过其他磁盘的数据修复，是怎么修复的？有点不理解这段话</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/19/95ff4cbd.jpg" width="30px"><span>格非</span> 👍（6） 💬（1）<div>跟机械磁盘的构造有关，随机读写时，磁头需要不停的移动，时间都浪费在了磁头寻址上</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/70/51/f1825adb.jpg" width="30px"><span>Lugyedo</span> 👍（3） 💬（2）<div>RAID技术会不会被淘汰</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（3） 💬（1）<div>传统机械硬盘的读写耗时主要在寻址上，连续读写一般只寻址一次，所以速度会快。</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/77/b3/991f3f9b.jpg" width="30px"><span>公号-技术夜未眠</span> 👍（3） 💬（1）<div>1 计算写入地址更简单快速
2 磁盘机械机构移动的距离更少，寻址更快
3 由于空间的连续性，写入也更快</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/12/c7/a7a5df8b.jpg" width="30px"><span>达子不一般</span> 👍（2） 💬（1）<div>raid5的磁盘使用率是n-1&#47;n,raid5不是校验信息写在所有磁盘上吗？raid6校验信息写在2块磁盘上，不是raid3的升级吗？没有频繁更新的问题吗？校验信息是类似数据压缩信息吗？2块磁盘能放的下吗？</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/db/66d5b3f4.jpg" width="30px"><span>Leo</span> 👍（2） 💬（1）<div>老师，问一个比较低级的问题：为什么说RAID提高了存储容量，不都是N快磁盘吗？如果不用RAID，N快磁盘不也是固定的容量吗？计算机数据本来不能存在多块硬盘上吗？</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/93/27/e32e111e.jpg" width="30px"><span>沙鱼</span> 👍（2） 💬（1）<div>老师请问一下：如果部署hdfs集群，还有没有必要单台机器做raid5浪费磁盘呢？想听听老师的分析。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/05/d6547381.jpg" width="30px"><span>才才</span> 👍（2） 💬（1）<div>批量地址连续，指针的寻址没那么跳跃</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f8/cf/e73c402f.jpg" width="30px"><span>高国君</span> 👍（1） 💬（1）<div>磁盘IO是需要机械寻址的，相比较数据写或读的时间来说是耗时操作。连续写入，只需要寻址一次，随机写入，每次写都要寻址。所以，</div>2018-11-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/vhOPEib27xAuTycN0eQekLzsCe9zwcTTcrOb98cIfpgibgcweZBDN38tIicABibuZBwah9jnGVr02H2Zjuue1fLfEQ/132" width="30px"><span>Ahikaka</span> 👍（1） 💬（1）<div>机械硬盘读取数据需要依靠读针头在盘上移动来进行读书操作，连续读取的时候针头只需要转动就好了，随机读取的时候不不仅要转动跳过无用的数据，还要再轴上前前后后移动，浪费了太多时间。</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/89/09/d660509d.jpg" width="30px"><span>intuition</span> 👍（1） 💬（1）<div>老师 我实战经验减少 我一直有个疑惑 mysql是水平拓展的 那存在哪些问题呢 这和一些nosql比例如hbase 有哪些不足呢 我们的架构何时才会由mysql集群升级为这些nosql呢</div>2018-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0c/d6/2677ec43.jpg" width="30px"><span>jack</span> 👍（1） 💬（1）<div>影响磁盘读写效率最主要因素是磁盘寻址，连续读写只有一次寻址，随机写入每一次都要寻址。</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/c6/1ac9edae.jpg" width="30px"><span>summer ₂ ₀ ₁ ₈</span> 👍（1） 💬（1）<div>这个应该是文中提到的寻址有关，找到了这个表的存储文件后，一次寻址多次写入，望老师指点！</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（1） 💬（1）<div>随机写入相对于连续写入增加了寻址时间。
连续写入磁头移动范围小，随机写入磁头移动范围大，所以连续写入速度快。</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ef/d0/d0925f9f.jpg" width="30px"><span>李强</span> 👍（1） 💬（1）<div>减少了寻址时间，关系型数据库，直接将日志写入到固定的地址，而随机还需要寻址，然后再写入</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/39/c8772466.jpg" width="30px"><span>无形</span> 👍（1） 💬（1）<div>顺序io比随机io快</div>2018-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/59/63/f4a0f3b9.jpg" width="30px"><span>Django</span> 👍（0） 💬（1）<div>raid5、6如何通过其他磁盘数据加上检验数据来还原损坏的磁盘数据的？这一点没想通，麻烦解答一下谢谢</div>2021-05-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7J1ef5o74bywMG5zftY8ZpTO1Vs6YKpjiaXXzyWbWPtcf5TX5eCrX0pzk2UaIDGjXtYVlNG5YtTmg/132" width="30px"><span>HarveyHanzy</span> 👍（0） 💬（1）<div>RAID5的螺旋写入不是太理解，在螺旋写入过程中，第N块磁盘与前面的N-1 块磁盘承载的校验数据功能有何不同呢？</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/c3/2c53acd7.jpg" width="30px"><span>雄鹰</span> 👍（0） 💬（2）<div>老师你好：有个关于磁盘做raid问题请教您，测hdfs的基准性能，现在每个服务器上有4块磁盘，是把这4块磁盘做成raid0(单考虑性能)的读写性能好还是4块磁盘都是挂裸盘的读写性能好？</div>2020-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/74/29/73d97f93.jpg" width="30px"><span>士冰突击</span> 👍（0） 💬（1）<div>传统机械磁盘读写时主要浪费时间的是寻址。连续的写入可以大大提升寻址，而随机写入在寻址上会耗费很多时间，故而连续的写入比随机写入时速率更高。</div>2018-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e6/3a/991c0e7a.jpg" width="30px"><span>班戟鱼</span> 👍（0） 💬（1）<div>raid这个数据恢复机制让我想到里所码，hdfs里面有用到里所码策略吗？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ce/d4/99c857e8.jpg" width="30px"><span>李永康Leo</span> 👍（0） 💬（1）<div>以后raid的方案是不是要逐渐的被淘汰掉了？</div>2018-11-15</li><br/>
</ul>