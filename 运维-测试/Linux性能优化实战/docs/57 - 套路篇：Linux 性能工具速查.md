你好，我是倪朋飞。

上一节，我带你一起梳理了常见的性能优化思路，先简单回顾一下。

我们可以从系统和应用程序两个角度，来进行性能优化。

- 从系统的角度来说，主要是对 CPU、内存、网络、磁盘 I/O 以及内核软件资源等进行优化。
- 而从应用程序的角度来说，主要是简化代码、降低 CPU 使用、减少网络请求和磁盘 I/O，并借助缓存、异步处理、多进程和多线程等，提高应用程序的吞吐能力。

性能优化最好逐步完善，动态进行。不要追求一步到位，而要首先保证能满足当前的性能要求。性能优化通常意味着复杂度的提升，也意味着可维护性的降低。

如果你发现单机的性能调优带来过高复杂度，一定不要沉迷于单机的极限性能，而要从软件架构的角度，以水平扩展的方法来提升性能。

工欲善其事，必先利其器。我们知道，在性能分析和优化时，借助合适的性能工具，可以让整个过程事半功倍。你还记得有哪些常用的性能工具吗？今天，我就带你一起梳理一下常用的性能工具，以便你在需要时，可以迅速找到自己想要的。

## 性能工具速查

在梳理性能工具之前，首先给你提一个问题，那就是，在什么情况下，我们才需要去查找、挑选性能工具呢？你可以先自己想一下，再继续下面的内容。

其实在我看来，只有当你想了解某个性能指标，却不知道该怎么办的时候，才会想到，“要是有一个性能工具速查表就好了”这个问题。如果已知一个性能工具可用，我们更多会去查看这个工具的手册，找出它的功能、用法以及注意事项。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（9） 💬（3）<div>有一个问题请教，很多时候工具有了，但是对于指标是否在合理范围好像没有明确的标准，都是经验式的</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/6e/e39e90ca.jpg" width="30px"><span>大坏狐狸</span> 👍（4） 💬（1）<div>我看到nethogs的时候去尝试理解一下，结果v0.8.0 会有如下错误：creating socket failed while establishing local IP - are you root?
即使是root用户去执行。看网上说v0.8.1 解决了这个问题。所以就下载了8.5版本。

wget -c https:&#47;&#47;github.com&#47;raboof&#47;nethogs&#47;archive&#47;v0.8.5.tar.gz
tar xf v0.8.5.tar.gz 
cd .&#47;nethogs-0.8.5&#47;

sudo apt-get install libncurses5-dev libpcap-dev
make &amp;&amp; sudo make install </div>2019-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4e/0f/c43745e7.jpg" width="30px"><span>hola</span> 👍（4） 💬（1）<div>可以做一期dtrace的讲解吗？感觉这个工具很厉害，但是挺复杂的</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/75/e3/ef489d57.jpg" width="30px"><span>Roy</span> 👍（1） 💬（1）<div>Linux什么时候有跑分软件?象安兔兔</div>2020-07-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLRwYJzyB6pdic3GeQvb5FSmMAOXepWERNT1nJsIY7M0adpbrACsdia56DCDxWhWicXHahSiaaIUpgZxg/132" width="30px"><span>youbuxiaoer</span> 👍（0） 💬（2）<div>老师，工作中遇到内存占用较高，通过meminfo确认是匿名页占用较多内存，请问匿名页内存是如何产生的？如何释放？</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（12） 💬（0）<div>思考：
⭐问题，办法，工具的关系——问题是人一生中唯一的事。解决问题的办法有很多，办法使用到的工具������️也有很多。

⭐转化——核心技术，是一种重要的工具，行之有效的工具，少了这个核心工具就做不成事情，此时的工具就转化为办法。

⭐技术，是一种工具，不要误以为是办法。只有当除此技术就无法解决问题的时候，技术工具才是办法本身，比如ai,大数据只是解决问题的办法，tensorflow,spark等是解决问题的工具。

⭐工具，似乎不可能唯一。当解决问题的办法出现后，工具也趋向多元化。所以，似乎办法比工具重要的多。

⭐办法，也就是方法，解决问题的思路，步骤。需要理解问题的结构、细节，进而采取措施。兵来将挡，水来土掩。所以，关键就是知道兵将关系，水土关系，理解问题，剖析问题是根本。

⭐问题，是程序bug？运营问题？管理问题？一个问题的出现可能由多方因素。

那么作为技术人员，能拿技术解决什么问题？解决问题，才能收货利益。比如朝九晚五写bug，夜以继日搞私活。解决的问题都不是痛点，或者并不是太痛。

⭐痛点，有多痛，就有多大价值，就可以带来多大收益。要体现自我价值，就得解决痛点。谁解决了痛点，谁就是有价值的人。但痛点本身与技术无关。
一句话：抓住痛点(方向)，剖析原理(方法)，用好工具(利剑)。
-----拿着’利剑‘用正确的’方法‘挥向正确的’方向‘--------------------</div>2020-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e0/c5/c324a7de.jpg" width="30px"><span>jorin@zou</span> 👍（2） 💬（2）<div>是我学的太快了吗，怎么越学到后面，评论越少了，得放慢脚步</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（1） 💬（0）<div>[D57打卡]
对性能分析的原理,比之前了解的多多了.
工具还是要经常用才行,不用就容易忘记. 有时用man还可以想起一点点来.

今天又把这些指标和工具又温习了一遍,以后也要常拿出来温习才行.
毕竟目前的主要工作还不是性能分析这一块.</div>2019-04-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（1） 💬（0）<div>打卡day61
这工具，还是要经常用，感觉用各个模块的套路篇，来的更快点～</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6c/40/f5ea25b1.jpg" width="30px"><span>Jiyong</span> 👍（0） 💬（1）<div>请教老师，有哪些限制cpu 内存等资源使用率的工具。谢谢啊</div>2021-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/d3/0e/ef771277.jpg" width="30px"><span>Akon</span> 👍（0） 💬（0）<div>大佬，有没有块设备稳定性测试的例子（比如iozone、fio这样的工具，以及制作或眼图的方法）</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9d/2c/6248ffbd.jpg" width="30px"><span>柏森森</span> 👍（0） 💬（3）<div>请教一个问题,我在系统中使用find  &#47;query&#47;tmp  -type f  -min +1  -exec rm -rf {} \;
用来删除文件发现这个脚本占用的资源特别多，CPU可以占用到20-30%,但系统不断地有交易上来，导致了性能的下降。系统&#47;query&#47;tmp中主要是小文件，请教下有没有好办法可以进行更高效，更快速地删除？另外，find工作的原理是什么</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c0/ce/fc41ad5e.jpg" width="30px"><span>陳先森</span> 👍（0） 💬（0）<div>原理大致清楚，但是工具不是太熟悉···还是得多练，概念性的东西当时记住了后面又容易忘，知识还是要温故而知新···还是要多看几遍，多敲几遍才记得住。慢慢的干货</div>2019-05-07</li><br/>
</ul>