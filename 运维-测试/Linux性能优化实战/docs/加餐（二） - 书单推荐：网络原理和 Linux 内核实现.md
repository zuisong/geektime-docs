你好，我是倪朋飞。欢迎来到 Linux 性能优化专栏的加餐时间。

上一期的专栏加餐，我给你推荐了一些 Linux 入门、体系结构、内核原理再到性能优化的书籍。这里再简单强调一下，主要包括下面这几本。

- Linux基础入门书籍：《鸟哥的Linux私房菜》
- 计算机体系结构书籍：《深入理解计算机系统》
- Linux编程书籍：《Linux程序设计》和《UNIX环境高级编程》
- Linux内核书籍：《深入Linux内核架构》
- 性能优化书籍：《性能之巅：洞悉系统、企业与云计算》

你可以通过学习这些书，进一步深入到系统内部，掌握系统的内部原理。这样，再结合我们专栏中的性能优化方法，你就可以更清楚地理解性能瓶颈的根源，以及性能优化的思路。

根据前面几个模块的学习，你应该也感觉到了，网络知识，要比 CPU、内存和磁盘等更为复杂；想解决相应的性能问题，也需要更多的基础知识来支撑。

而且，任何一个高性能系统，都是多台计算机通过网络组成的集群系统。网络性能，在大多数情况下，自然也就成了影响整个集群性能的核心因素。

今天，我就来给你推荐一些，关于网络的原理，以及 Linux 内核实现的书籍。

## 计算机网络经典教材《计算机网络（第5版）》

![](https://static001.geekbang.org/resource/image/ce/36/cef3bf15fa095140d499ba56fe4f2e36.png?wh=586%2A800)

既然想优化网络的性能，那么，第一步当然还是要熟悉网络本身。所以，今天我推荐的第一本书，就是一本国内外广泛使用的经典教材——《计算机网络（第5版）》。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKQMM4m7NHuicr55aRiblTSEWIYe0QqbpyHweaoAbG7j2v7UUElqqeP3Ihrm3UfDPDRb1Hv8LvPwXqA/132" width="30px"><span>ninuxer</span> 👍（6） 💬（1）<div>打卡day48
网络的书具有神奇的催眠作用😂</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（5） 💬（1）<div>计算机网络经典教材《计算机网络（第 5 版）》是不是讲IOS七层协议？我1996年大学学的，现在出入大吗？</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b2/71/76481005.jpg" width="30px"><span>Kingdom</span> 👍（1） 💬（1）<div>好多都是大学的原课本啊，大学的时候总是学不下去，工作了才知道大学基础课程的重要性</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/75/ba/ac35ac17.jpg" width="30px"><span>chich chung kai</span> 👍（1） 💬（1）<div>web页面终于优化了，看起来舒服多了，更加便利了。</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/2d/4b7f12b6.jpg" width="30px"><span>死后的天空</span> 👍（0） 💬（1）<div>TCP&#47;IP协议是当初考NP的时候买的，第一本看完了，第二本看了一点，UNIX网络编程买来，信誓旦旦的说每天坚持看10页，但是看了200也就坚持不住了 T _ T。</div>2019-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（14） 💬（0）<div>学了老师的课，是时候肯一下大部头的书了</div>2019-03-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（5） 💬（0）<div>网络还是值得投入时间的知识。长期有效 变化更新相对慢 适用面广。加油！</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（2） 💬（0）<div>[D48打卡]
还是先把手上已有的书看完了再买吧.
要不然买了也是在那躺着.😂</div>2019-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（1） 💬（0）<div>读书有点像游戏里的加技能点，技能点是有限的，要根据计划、设计、自身角色的特点，有针对性的对书籍进行“过滤”，构建自己的技术体系，有自己的特色。</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3f/0d/1e8dbb2c.jpg" width="30px"><span>怀揣梦想的学渣</span> 👍（1） 💬（0）<div>TCP&#47;IP那个，要么自己买原版，要么在图书馆看，千万别白嫖网上那些电子版，目前网上有些电子版，里面有残缺的，还有一些印错的。看的时候还是慎重。</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/c1/d402bfbf.jpg" width="30px"><span>一生一世</span> 👍（1） 💬（0）<div>老师出书了？我像拿到这门课的书</div>2019-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（0） 💬（0）<div>bgp有什么好书</div>2023-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（0） 💬（0）<div>谢谢老师带我起飞</div>2020-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/00/3b/2543b3ca.jpg" width="30px"><span>苏煌</span> 👍（0） 💬（0）<div>打卡，看不完的书</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c3/48/3a739da6.jpg" width="30px"><span>天草二十六</span> 👍（0） 💬（0）<div>wireshark功能强大，入门使用较难。工具类的出书，也足以说明～</div>2019-09-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4a/fb/70f14340.jpg" width="30px"><span>maoxiajun</span> 👍（0） 💬（0）<div>加餐打卡，最近自己也在做性能优化方面的一些事情，虽然还没有看全，但是已经深受帮助，这是我认为最划算的一门课了</div>2019-04-23</li><br/><li><img src="" width="30px"><span>如果</span> 👍（0） 💬（0）<div>打卡</div>2019-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（0） 💬（0）<div>突然发现书籍中中高级的3本都买了：初中级的4本反而没看过，下手-补基础了；怪不得内核我啃到崩溃，原来是漏了底层、、、</div>2019-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（0） 💬（0）<div>这样书有的自己买了躺起，看了一部分就不想看了
</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/cb/3ebdcc49.jpg" width="30px"><span>怀特</span> 👍（0） 💬（0）<div>行动起来，复习一遍！</div>2019-03-08</li><br/>
</ul>