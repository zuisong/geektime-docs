机器指令里面的内存地址都是虚拟内存地址。程序里面的每一个进程，都有一个属于自己的虚拟内存地址空间。我们可以通过地址转换来获得最终的实际物理地址。我们每一个指令都存放在内存里面，每一条数据都存放在内存里面。因此，“地址转换”是一个非常高频的动作，“地址转换”的性能就变得至关重要了。这就是我们今天要讲的**第一个问题**，也就是**性能问题**。

因为我们的指令、数据都存放在内存里面，这里就会遇到我们今天要谈的**第二个问题**，也就是**内存安全问题**。如果被人修改了内存里面的内容，我们的CPU就可能会去执行我们计划之外的指令。这个指令可能是破坏我们服务器里面的数据，也可能是被人获取到服务器里面的敏感信息。

现代的CPU和操作系统，会通过什么样的方式来解决这两个问题呢？别着急，等讲完今天的内容，你就知道答案了。

## 加速地址转换：TLB

上一节我们说了，从虚拟内存地址到物理内存地址的转换，我们通过页表这个数据结构来处理。为了节约页表的内存存储空间，我们会使用多级页表数据结构。

不过，多级页表虽然节约了我们的存储空间，但是却带来了时间上的开销，变成了一个“以时间换空间”的策略。原本我们进行一次地址转换，只需要访问一次内存就能找到物理页号，算出物理内存地址。但是用了4级页表，我们就需要访问4次内存，才能找到物理页号。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/fd/be/079c78c7.jpg" width="30px"><span>焰火</span> 👍（20） 💬（3）<div>地址空间布局随机化。虽然进程里的段乱序了，但是他的虚拟地址和乱序前没有改变吧，只是又多了一层地址转换而已？这样理解对么？</div>2019-09-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QYKSUV20DMgBHAPLfgngdw4N8FHRCSBLCJueVRu9Ya1Ba2x4icx70zoVVFOZtG1K6TkHj5CFbuztQhRFyCjWXHQ/132" width="30px"><span>zaab</span> 👍（45） 💬（2）<div>想通了一个问题: 你知道sql里面不用sql拼接 而使用占位符可以防止sql注入攻击吧
那么为什么使用占位符可以防止攻击呢 我没想明白。
简单来说就是将占位符当成数据解析 而不当作指令解析， 不管这个占位符给得什么 我都把它当成是数据 而不会是指令</div>2019-10-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pTD8nS0SsORKiaRD3wB0NK9Bpd0wFnPWtYLPfBRBhvZ68iaJErMlM2NNSeEibwQfY7GReILSIYZXfT9o8iaicibcyw3g/132" width="30px"><span>雷刚</span> 👍（10） 💬（0）<div>1. 简单页表：类似数组，时间复杂度为 O(1)。但空间复杂度为数组的长度，即页的个数。32 位的内存地址为 4MB（= 2^20 * 4byte）。
2. 多级页表：类似 B+ 树，时间复杂度为 O(n)，如 4 级页表就需要查询 4 次。但程序只需要存储正在使用的虚拟页的映射关系，空间复杂度大大降低。
3. TLB：使用缓存保存之前虚拟页的映射关系。因为指令和数据往往都是连续的，存在空间局部性和时间局部性。也就是说，连续执行的多个指令和数据往往在同一个虚拟页中，没必要每次都从内存中读取页表来解析虚拟地址。</div>2020-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bf/aa/abb7bfe3.jpg" width="30px"><span>免费的人</span> 👍（7） 💬（2）<div>linux下  内存空间随机化是否开启  是有配置的吗  还是跟内核版本有关？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/e6/163eb9f8.jpg" width="30px"><span>宇宙超人</span> 👍（4） 💬（2）<div>问个问题 
cpu.缓存和mmu是怎么个顺序
先mmu转换地址 然后去cache看命中还是反过来</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（4） 💬（3）<div>如果是这个salt是保存在db中，这个随机化策略只是增加了黑客的破解成本，并非完全安全。
一个解决方案是将一个从密码机生成的秘钥通过算法将其生成为一个安全图片，同时提供一个sdk来封装对安全图片的读取，并提供加解密方法。
业务方每次加解密时，调用sdk来做加解密，这样秘钥就不会落盘，不会有日志记录。安全性得到极大提升

</div>2019-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a3/4d/59390ba9.jpg" width="30px"><span>排骨</span> 👍（3） 💬（0）<div>局部性原理无处不在啊</div>2022-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/83/fb/621adceb.jpg" width="30px"><span>linker</span> 👍（2） 💬（0）<div>还有使用哨兵进行堆栈溢出检测等</div>2020-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7a/e3/145adba9.jpg" width="30px"><span>不一样的烟火</span> 👍（2） 💬（0）<div>地址随机化后不再局部 是不是牺牲了效率</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/60/5c1227a2.jpg" width="30px"><span>xta0</span> 👍（2） 💬（6）<div>问一下，对于使用salt加密的策略，salt是需要存入数据库的吧？这样当用户登录时，先取出salt，然后重新计算hash值进行比对？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/9a/89/babe8b52.jpg" width="30px"><span>A君</span> 👍（1） 💬（0）<div>进程布局的随机化减少了被黑客猜到数据地址的危险。原来哈希值也有可能通过彩虹表猜出来，应对方法是用一个随机值和用户的输入一起作哈希。</div>2020-07-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6BNrtko7d9ZXic04QhUuQic7N9XEVFtXciaHNlYMVvIic8bv4k52GmFRuYotiaJpjGiaj35rCdhWcFojKsgFIvZ5XlMA/132" width="30px"><span>Geek_7f28ff</span> 👍（1） 💬（0）<div>老师，最近也在学习计算机网络，能不能推荐一下，这方面的书籍和好点的视频，趣味网络协议已经买了。</div>2019-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（1） 💬（0）<div>老师你好，TLB的原理给多介绍一下吗？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/e9/d131dd81.jpg" width="30px"><span>Mamba</span> 👍（0） 💬（0）<div>堆栈保护：
Stack Canaries：在函数的返回地址之前插入一个随机生成的值（canary），如果堆栈被溢出并修改了这个值，程序会在返回前检测到并终止。
Stack Cookies：与canaries类似，用于检测堆栈溢出。</div>2024-09-06</li><br/><li><img src="" width="30px"><span>Geek_88604f</span> 👍（0） 💬（0）<div>最重要的安全机制是虚拟内存机制，进程看不到实际的物理地址，使用哪个物理地址完全由操作系统决定</div>2024-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/67/0f/3cb10900.jpg" width="30px"><span>菜鸟</span> 👍（0） 💬（0）<div>共享内存是不是没有启用地址保护？</div>2022-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/d2/0f/8f14c85b.jpg" width="30px"><span>红薯板栗</span> 👍（0） 💬（0）<div>spectre漏洞：CPU流水线优化- 分支预测-边信号-https:&#47;&#47;www.sohu.com&#47;a&#47;318447401_132567</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（0）<div>绍了最常用的两个内存保护措施，可执行空间保护和地址空间布局随机化。</div>2019-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/2e/1522a7d6.jpg" width="30px"><span>活的潇洒</span> 👍（0） 💬（0）<div>局部性原理应用的淋漓尽致
day41 笔记：https:&#47;&#47;www.cnblogs.com&#47;luoahong&#47;p&#47;11385395.html</div>2019-08-21</li><br/>
</ul>