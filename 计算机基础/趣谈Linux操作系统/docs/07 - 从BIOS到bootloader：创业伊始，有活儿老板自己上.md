有了开放的营商环境，咱们外包公司的创业之旅就要开始了。

上一节我们说，x86作为一个开放的营商环境，有两种模式，一种模式是实模式，只能寻址1M，每个段最多64K。这个太小了，相当于咱们创业的个体户模式。有了项目只能老板自己上，本小利微，万事开头难。另一种是保护模式，对于32位系统，能够寻址4G。这就是大买卖了，老板要雇佣很多人接项目。

几乎所有成功的公司，都是从个体户模式发展壮大的，因此，这一节咱们就从系统刚刚启动的个体户模式开始说起。

## BIOS时期

当你轻轻按下计算机的启动按钮时，你的主板就加上电了。

按照我们之前说的，这时候你的CPU应该开始执行指令了。你作为老板，同时也作为员工，要开始干活了。可是你发现，这个时候还没有项目执行计划书，所以你没啥可干的。

也就是说，这个时候没有操作系统，内存也是空的，一穷二白。CPU该怎么办呢？

你作为这个创业公司的老板，由于原来没开过公司，对于公司的运营当然是一脸懵的。但是我们有一个良好的营商环境，其中的创业指导中心早就考虑到这种情况了。于是，创业指导中心就给了你一套创业公司启动指导手册。你只要按着指导手册来干就行了。

![](https://static001.geekbang.org/resource/image/a4/6a/a4009d3de2dbae10340256af2737c26a.jpeg?wh=2113%2A1162)

计算机系统也早有计划。在主板上，有一个东西叫**ROM**（Read Only Memory，只读存储器）。这和咱们平常说的内存**RAM**（Random Access Memory，随机存取存储器）不同。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/8e/10/10092bb1.jpg" width="30px"><span>Luke</span> 👍（64） 💬（3）<div>看到很多人留言需要资料，我来推荐一本新书《一个64位操作系统的设计与实现》，如果你有汇编基础，很感兴趣底层的细节，可以看李忠的那本《从实模式到保护模式》</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8e/10/10092bb1.jpg" width="30px"><span>Luke</span> 👍（64） 💬（1）<div>这部分的实验，大家可以去github看我的工程哈，icecoobe&#47;oslab，已经进入保护模式了，还有很远的路，一起加油！</div>2019-04-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eor68N3pg8Joqw3XH1EkFjmLVK5fkKokj1025XjR4va1CW8CdsKSytbw3f4WPjIbiazEbACOibNDnnA/132" width="30px"><span>Geek_9y01z7</span> 👍（59） 💬（5）<div>查了一些资料，关于 Gate A20 我的理解是：

- 8086 地址线20根 -&gt; 可用内存 0 ~ FFFFF
  寄存器却是16位，寻址模式为 segment(16位):offset(16位)， 最大范围变成 0FFFF0(左移了4位) + 0FFFF = 10FFEF
  后果是多出来了 100000 ~ 10FFEF （访问这些地址时会回绕到 0 ~ FFEF）

- 80286 开始地址线变多，寻址范围大大增大，但是又必须兼容旧程序，8086在访问 100000 ~ 10FFEF时会回绕，但是 80286 不会 ，因为有第21根线的存在，会访问到实际的 100000 ~ 10FFEF 地址的内存。
于是 Gate A20 开关就诞生了，它的作用是：

- 实模式下 （存在的唯一理由是为了兼容8086）：
  - 打开 -&gt;  寻址100000 ~ 10FFEF会真正访问
  - 关闭-&gt; 回绕到 0 ~ FFEF

- 保护模式下：
  - 打开 -&gt; 可连续访问内存
  - 关闭 -&gt; 只能访问到奇数的1M段，即 00000-FFFFF, 200000-2FFFFF,300000-3FFFFF…  
</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/54/3f/46c3060a.jpg" width="30px"><span>我爱北京天安门</span> 👍（55） 💬（5）<div>看来从这篇开始我要看三遍四遍五遍的节奏了</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9d/f4/d8260b2b.jpg" width="30px"><span>Memoria</span> 👍（33） 💬（2）<div>大家有兴趣实践的话可以参考清华大学的操作系统实验课，里面第一个实验讲的就是启动的过程，可以让人理解的更加透彻。https:&#47;&#47;github.com&#47;chyyuu&#47;ucore_os_lab</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/0a/fa152399.jpg" width="30px"><span>wahaha</span> 👍（18） 💬（2）<div>grub2 是一个非常牛的 Linux 启动管理器
这句应该去掉Linux，因为GRUB2也能启动其它操作系统</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/79/3d/29746a4b.jpg" width="30px"><span>赵又新</span> 👍（17） 💬（1）<div>之前课上说的，如果没有理解错的话：
32位，分为16位寻址空间和16位偏移量。但通过左移4位的方式，将寻址空间扩充为20位。所以，0xFFFF的位置实际指的是0xFFFF0。</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/88/fe/c18a85fe.jpg" width="30px"><span>随风</span> 👍（10） 💬（5）<div>当电脑刚加电的时候，会做一些重置的工作，将 CS 设置为 0xFFFF,将 IP 设置为 0x0000,所以第一条指令就会指向 0xFFFF0。这个所以怎么得到的结果？为什么上面都是五位0xFFFFF, cs&#47;ip都是四位0xFFFF? 小白越看越不明白了。
</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/d7/454a1b90.jpg" width="30px"><span>leon</span> 👍（9） 💬（2）<div>32位处理器不是有32根地址线嘛？为啥只打开第21根地址线的控制线？这里可以再稍微解释一下吗？控制线是另外一种线嘛？</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/35/64/1ad5530d.jpg" width="30px"><span>马上想好</span> 👍（7） 💬（1）<div>当电脑刚加电的时候，会做一些重置的工作，将 CS 设置为 0xFFFF，将 IP 设置为 0x0000，所以第一条指令就会指向 0xFFFF0，正是在 ROM 的范围内。 为什么第一条指令会指向0xFFFF0呢</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/df/ca/7c223fce.jpg" width="30px"><span>天使也有爱</span> 👍（7） 💬（2）<div>老师 我现在看这些内容有点晕 太细了 我是要用那本书做配套看 还是直接用内核源码结合着看呢</div>2019-04-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAl7V1ibk8gX9qWZKLlCmKAl6nicoTZ03PWksrUbItVraTGk5zpne1BEtUam8w8VID4EzcyyhC1LAw/132" width="30px"><span>aingwm</span> 👍（6） 💬（1）<div>“将 CS 设置为 0xFFFF，将 IP 设置为 0x0000”是以往的做法，Intel没有再延续，新的做法是“将 CS 设置为 0xF000，将 IP 设置为 0xFFF0”，当然，CS:IP的指向仍然是 0xFFFF0 ，这一点倒是没有变。</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/fc/5627215c.jpg" width="30px"><span>小何</span> 👍（6） 💬（3）<div>文章对boot.image说的比较清楚，是在第一个扇区存放，core.image这些内容是在什么地方存放的呢？是某个扇区还是在文件系统的某个路径？</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0c/46/dfe32cf4.jpg" width="30px"><span>多选参数</span> 👍（4） 💬（2）<div>对于启动这一节的实验可以做一下公开课中 mit 6.824 的启动一节，当然国内的清华大学也有类似的。有个读者提到了。其实个人感觉 bootloader 或者 bios 阶段来说都可以说不是必须，我甚至把硬件自检操作和 kernel 都直接放到 ROM 中。有这bootloader 和 bios 我感觉更多是为了管理等，比如加载不同操作系统等。</div>2020-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/b2/abb7bfe3.jpg" width="30px"><span>徐庆新</span> 👍（4） 💬（1）<div>RAM是Random Access Memory，不是Read Access Memory</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/af/8b/0a2fdaa4.jpg" width="30px"><span>痴痴笑笑(Bruce)</span> 👍（3） 💬（1）<div>我有个小白问题请教一下老师和同学们，grub2使用了配置文件，我的理解是grub运行的时候操作系统还没有开始运行，它是通过什么方式访问文件系统的呢？访问文件系统并不依赖于操作系统对不对？</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/e8/12cb8e99.jpg" width="30px"><span>小松松</span> 👍（3） 💬（1）<div>感觉要看懂这个专栏，我先要学习好另一个专栏 《深入浅出计算机组成原理》</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a0/d7/52cdecf4.jpg" width="30px"><span>启曙</span> 👍（3） 💬（1）<div>看Linux0.12内核的时候，没有grub，而是内核有个bootsect.s的编译后写入MBR。文中grub是在MBR和bootsect.s直接增加的一个多系统引导功能。但是GRUB看起来不是必须的，为什么后来的内核要加入GRUB</div>2019-04-12</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（2） 💬（1）<div>打卡day8
最后图片是精华啊～</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/2a/43101709.jpg" width="30px"><span>myj</span> 👍（1） 💬（1）<div>有几个问题，希望老师帮忙解答下：

1、配置系统启动项的指令：grub2-mkconfig -o &#47;boot&#47;grub2&#47;grub.cfg
这个命令是在哪里执行呢？在Linux命令行执行吗？这个时候都还没有进入操作系统，要如何执行？

2、BIOS初始化更详细的资料老师有没有推荐？

3、文中有个地方：
“所以在真正的解压缩之前，lzma_decompress.img 做了一个重要的决定，调用real_to_prot”
这句话我理解为lzma_decompress.img自己调用了real_to_prot，这个程序还没有解压，怎么能调用呢？
还是说，这个real_to_prot函数是在其他地方定义的？由boot或diskboot执行？因为这里只看到xxx加载，而没有看到取指载入CPU执行的过程

4、启动盘的第1个扇区存储着主引导记录，这个主引导记录是怎么存储到硬盘上的呢？

我描述可能有些啰嗦，见谅</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（1） 💬（1）<div>第二遍看懂了，这次决定坚持看完</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b2/b5/b1b42785.jpg" width="30px"><span>凌尘</span> 👍（1） 💬（3）<div>老师，你说启动盘一般在第一个扇区，占512个字节；后面又提到grub2第一个安装的就是boot.img，将它安装到启动盘的第一个扇区。这两句话，把我搞得有点蒙，第一句话不是表明启动盘占一个扇区共512个字节吗，那后面一句话安装到启动盘的第一个扇区，这又怎么理解啊？启动盘不是就占一个扇区吗，根据前1句话。希望老师解答下，谢谢～</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/1f/6bc10297.jpg" width="30px"><span>Allen</span> 👍（1） 💬（1）<div>cs*16+ip=内存地址</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/2e/93812642.jpg" width="30px"><span>Amark</span> 👍（1） 💬（1）<div>老师，从BIOS到bootloader，最后到保护模式，你说的这是计算机的发展过程还是，说比如我自己的电脑，每次启动都会经历从BIOS到bootloader，最后到保护模式? </div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（1） 💬（1）<div>为什么在刚加电的时候将 CS 设置为 0xFFFF，将 IP 设置为 0x0000, 第一条指令就指向 0xFFFF0了呢? 请问老师这个因果关系是怎么成立的?


</div>2019-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/51/14/c800c859.jpg" width="30px"><span>N0mansky</span> 👍（1） 💬（1）<div>请问下，我装系统的时候grub应该安装在&#47;dev&#47;sda还是&#47;dev&#47;sda1分区？按道理mbr只读取硬盘的第一个扇区，应该只能装在&#47;dev&#47;sda吧</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e6/3a/5e8be862.jpg" width="30px"><span>fenghuo</span> 👍（1） 💬（1）<div>我如痴如醉的看了两遍，写得太生动了。</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/29/629d9bb0.jpg" width="30px"><span>天王</span> 👍（1） 💬（1）<div>32位地址能寻址32位，4g内存，内存超过4g，怎么寻址？</div>2019-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（1） 💬（1）<div>研究起来不容易，今天也要加油鸭。</div>2019-04-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ecruTrMgzvqIs5iaWVibZw4Rxic42ZXGTflvOFHiaZEkf32Su01gDCWT8tdIcEoybg0ibAYU2Q8f9bleL7Q37fKguxQ/132" width="30px"><span>做一个积极的跳蚤</span> 👍（0） 💬（1）<div>我发现留言区的不止有内核基础，好多还是大佬高手，来学刘老师的课程估计是加强补充知识的。评论区推荐的那些好书和帖子我就不去看了，不然会慢慢忘记初衷跑题了。</div>2020-06-18</li><br/>
</ul>