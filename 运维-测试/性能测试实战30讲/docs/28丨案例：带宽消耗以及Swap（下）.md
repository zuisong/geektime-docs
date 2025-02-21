上一篇文章我主要分析了带宽消耗，今天，我们来看一下分析的第二和第三阶段，也就是Swap分析和数据库分析。

## 分析的第二阶段

### Swap的原理和对TPS的影响

前面有一个扣，是说swap多的问题。要理解swap为什么是黄的，得先知道什么是swap。我先画个简易的示意图。

![](https://static001.geekbang.org/resource/image/1f/e5/1fd061cbf986f9cea3509bd4699ddbe5.jpg?wh=285%2A111)

这里先解释一下，对于一个Linux系统来说，如果配置并开启了swap分区，那么默认的swappiness参数是60。

swappiness是在内存reclaim的时候生效的，而reclaim方式同时有两个动作：1. 将file相关内存进行回收；2. 将anon内存交换到swap分区。

所以swapiness值越大，swap分区就用得越多。

对我们现在分析的这个系统来说，来看一下：

![](https://static001.geekbang.org/resource/image/e2/7f/e29ec84d980fb9e667e41010b209427f.png?wh=735%2A268)

我们看到这里配置了一个内存为8G左右，已经使用了7G多了，swappiness配置为30%。

通过free看到现在只有145M的物理内存剩余，可用内存也只有254M了。  
所以上面图中的swap飘黄也是很合理的喽！

下面我们就针对应用服务器的swap来看是不是可优化。

所有人都知道，当swap被用的时候，性能肯定会下降，所以在我的测试过程中，一般我都建议把swap直接关掉测试性能，有人说这样有什么问题？
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUHvicvia3fpBfsNh78uuUIhsLyrk0AwSN1Dau7pR3hrEsERANT6UyrSd3gIBVyQibD2nPRzkibJLxibA/132" width="30px"><span>Geek_8e5c47</span> 👍（7） 💬（1）<div>慢查询信息和网络信息是使用什么命令查看到的啊？</div>2020-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（6） 💬（1）<div>在虚拟机或dock环境中可进行性能测试吗？</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/01/7a0bfa9a.jpg" width="30px"><span>alley</span> 👍（4） 💬（1）<div>老师查看网络带宽满的命令是什么</div>2021-01-17</li><br/><li><img src="" width="30px"><span>nelson</span> 👍（4） 💬（4）<div>对于为什么打开查询缓存，没有给出相关的表和SQL，没有任何理论依据，而是直接打开缓存尝试。颇有实践主义的色彩。
现在十分不建议打开查询缓存，一旦数据更新之前费劲建立起来的缓存都全部清空了，另外实在命中率不高涂层消耗，除非在非常特殊的场景
另外在My SQL 8.0中，干脆废掉了查询缓存</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（4） 💬（1）<div>老师的功力太深厚了，感觉性能测试要会的东西很多，测试，开发，运维，架构等等，我是小开发，看这种排查问题的文章真是爽，要是能在工作中这样酣畅淋漓的排查，爽啊</div>2020-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/40/e2/c464a6f7.jpg" width="30px"><span>孙奕意</span> 👍（2） 💬（1）<div>文中JVM截图是jconsole工具的？在liunx系统上也可以用jconsole 进行JVM监控的吗？</div>2020-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/71/48/44df7f4e.jpg" width="30px"><span>凯</span> 👍（2） 💬（2）<div>如果真得示客户网络带宽导致瓶颈，有什么推荐的方法，比如10M带宽，如果要扩大的话，需要怎么扩大。扩大的到什么程度，</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/bb/7068f251.jpg" width="30px"><span>老姜</span> 👍（2） 💬（1）<div>mysql用的是什么监控工具？</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/18/a51730da.jpg" width="30px"><span>Rachel</span> 👍（1） 💬（1）<div>监控工具可以安装在独立于应用服务器、数据库服务器、压力机等之外机器吗？</div>2021-12-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/VHujEJQglWzlG82auxYg4ibLccovhB8jBD1SMvqWZPdNf6fhTgK5wic5WHqbnR5sZF5Agrwgw39Q30Ccmib81qwBA/132" width="30px"><span>lin~</span> 👍（1） 💬（1）<div>老师，swap飘黄的逻辑有些疑问，这里swapiness设置为30，如果设置为80的话，在available mem不够的情况下还会飘黄么</div>2021-10-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/a9/d55838b9.jpg" width="30px"><span>李大.shu</span> 👍（1） 💬（1）<div>老师，我在一次性能测试过程中，cache的值一直上升，然后将物理内存占满后，cache的值趋于稳定，程序用的used也趋于稳定(内存利用率在45%左右)。但通过vmstat统计观察swpd的值一直在上涨，通过jconsole查看也没有内存泄漏的问题。压测了48小时，tps和响应时间都在要求的指标范围内，这种情况算是正常情况吗，有没有风险，我担心swpd继续涨下去会有问题</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dd/84/fe116a80.jpg" width="30px"><span>TavisD</span> 👍（1） 💬（1）<div>高老师，请教下JVM配置是用哪种测试场景去调优呢。比如系统有好几个应用，测试场景也有基准测试、混合测试，那是测基准测试时去调优JVM配置？还是混合测试时？还是所有的场景都要去做这个JVM调优配置？如果出现多个场景JVM的最佳配置不一样，是以哪个为准？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（1） 💬（2）<div>应用开发人员，但是啥都可能干，包括部分运维，还有性能和安全。对我来说，这两节课我要记住的就是：主机（节点）压不出来，那就是路（网络）出了问题。

遇到过的问题是网络链接释放不干净，导致CLOSE_WAIT大量出现，最后内存使用过多，导致进城挂了的事。作为开发，那时还没有这么多分析操作系统的知识。只能从网络一点着手。

老师能不能再补充一些事故后的“尸检”环节呀？</div>2020-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhuGLVRYZibOTfMumk53Wn8Q0Rkg0o6DzTicbibCq42lWQoZ8lFeQvicaXuZa7dYsr9URMrtpXMVDDww/132" width="30px"><span>hello</span> 👍（1） 💬（1）<div>老师这两篇案例分析特别流畅，一口气看完，思路真的很清晰，感谢老师！</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/40/dd/a79ca0f0.jpg" width="30px"><span>林义的奥妙</span> 👍（0） 💬（1）<div>老师，JVM的堆设置为原来的一半之后，为什么使用率就降底到1.5G左右？</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3b/01/7a0bfa9a.jpg" width="30px"><span>alley</span> 👍（0） 💬（1）<div>好厉害啊，干货满满，像侦探片一样，引人入胜。</div>2021-01-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/orTaVwTib3ribTl5wibBQPnicjlOekZB3nwLj2ibsZ5Gvh987qGaCsAyxt9n3zBTTCfLicyIX0xDZzKjRlKtg7PThGXg/132" width="30px"><span>万伟</span> 👍（0） 💬（1）<div>您好，请问一下，Spotlight on Linux配置好ssh连接后，点connect为什么总报conection lost?
环境：
本地：win7          SpotlightonUnix_70.exe
linux：centos7</div>2020-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（0） 💬（1）<div>这两篇案例很棒</div>2020-02-25</li><br/>
</ul>