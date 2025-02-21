今天我们来做一个实例，看下在JMeter中，如何合理地设置参数化数据。

## 正式场景前的基准测试

在没有做业务混合场景之前，我们需要先做Benchmark测试，来确定一个登录业务能支持多少的业务量，这样就可以在业务混合场景中，根据场景中各业务的比例来确定登录的数据需要多少真实的数据。

我们继续用上一篇文章中用户登录的例子，单独测试登录业务，结果如下：

```
Java
summary +    125 in 00:00:04 =   31.0/s Avg:    28 Min:     0 Max:   869 Err:     0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +   3404 in 00:00:30 =  113.2/s Avg:    31 Min:     0 Max:   361 Err:     0 (0.00%) Active: 6 Started: 6 Finished: 0
summary +   4444 in 00:00:30 =  148.4/s Avg:    57 Min:     0 Max:   623 Err:    10 (0.23%) Active: 11 Started: 11 Finished: 0
```

从上面的结果可以看到登录业务能达到的TPS是113左右，这里我们取整为100，以方便后续的计算。

## 在测试工具中配置参数

在上面的试探性测试场景中，不需要观察系统的资源，只需要根据TPS做相应的数据统计即可。

前面我们知道，在这个示例中只做了近10万条的用户数据，为了方便示例进程。

下面我们从数据库中查询可以支持登录5分钟不重复的用户数据。根据前面的公式，我们需要30000条数据。

```
Java
100x5mx60s=30000条
```

接下来连接数据库，取30000条数据，存放到文本中，如下所示：

```
Java
username,password
test00001,test00001
test00002,test00002
test00003,test00003
test00004,test00004
test00005,test00005
test00006,test00006
test00007,test00007
...................
test30000,test30000
```

## 参数化配置在JMeter中的使用说明

我们将这些用户配置到测试工具的参数当中，这里以JMeter的CSV Data Set Config功能为例。配置如下：

![](https://static001.geekbang.org/resource/image/d4/a6/d40134621469079dd7b9de6e19165ca6.png?wh=1120%2A350%3Fwh%3D1120%2A350)

在JMeter的参数化配置中，有几个技术点，在这里说明一下。
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/51/50/f5f2a121.jpg" width="30px"><span>律飛</span> 👍（16） 💬（5）<div>JMeter 的 CSV Data Set Config 功能用来从文件中读取数据行，并将它们拆分后存储到变量中。个人理解，Recycle on EOF的优先级高于Stop thread on EOF，也就是说，需要先判断Recycle on EOF，如果是Flase，直接在文件结束时就停止了线程，根本不考虑Stop thread on EOF参数值；如果是True，就要根据Stop thread on EOF参数值来确定线程是否停止运行。在明白组合逻辑关系后，可以更高效的设置参数、更准确的达到测试目的。
各种测试工具有各种测试功能，可能其中就会存在有关联的参数配置，这也需要我们特别关注。如果查阅资料还不能清晰认识，就按老师的做法，通过对不同组合进行实验，最终弄清楚组合关系，归纳总结出优先顺序，从而在平时测试中帮助我们快速有效地找到最优的组合。</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（10） 💬（2）<div>今日思考题：
为什么参数化数据要符合生产环境的数据分布？
因为如果不符合生产环境的话，我们做这个性能测试就没有意义了。

为什么参数化数据要关注组合逻辑关系，而不是随意设置组合？
随意设置就会出现逻辑矛盾或者没有意义的组合。这样看上去节省了时间，其实反而浪费了时间。

今日感悟：
CSV Data Set Config这个功能之前学过，但是只是别人告诉我怎么填，我就照着填了，没有深入思考各个参数不同组合会有什么样的效果。这节课听下来，对这个功能的理解又深入了些。超值超值，感谢老师。

看了评论为了验证Recycle on EOF和Stop thread on EOF这两个参数的关系，我去JMeter里实践了一下，我的CSV文件里有7条数据，线程数我设置的8。
得出结论是：如果Recycle on EOF是Flase，Stop thread on EOF是Flase，由于线程数比文件数据多，JMeter会继续执行，但是由于没有数据，会报错，然后停止；如果Recycle on EOF是Flase，Stop thread on EOF是True，就直接停止。所以两个参数我认为需要结合起来看，虽然Recycle on EOF的优先级高一些，但也不是能起决定性作用的。


然后回过头来再看一遍文章发现其实我练习的这两种情况老师都讲了并且举了例子。我刚学完的时候是清楚的（至少自己感觉是清楚的），但是看了评论我发现还是有点懵，然后决定自己试一试。练习过之后，是真的明白了。所以真的要动手去做呀。</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/0f/ee37a7fe.jpg" width="30px"><span>zuozewei</span> 👍（7） 💬（3）<div>第一个问题：为什么参数化数据要符合生产环境的数据分布？

在「01丨性能综述：性能测试的概念到底是什么」中已经讲过，性能模型中的业务模型是真实场景的抽象，即需要的数据通常都是从生产环境中的数据中统计来的，其关键就是「数据必须保证仿真」。
那么性能测试的时候我们需要特别注意压测流量以及相关的数据，必须保证它们的多样化和代表性，否则会导致测试结果会严重失真。
比如，当使用相同的测试数据进行重复测试时，如果压测请求不够大，那么各种缓存可能会严重影响测试结果。

第二个问题：为什么参数化数据要关注组合逻辑关系，而不是随意设置组合？

因为参数化数据要组合逻辑关系会直接影响参数化数据的分布情况，即数据是否均匀？数据是否稳定？是保否证测试时间足够长？满足测试的负载请求足够多和数据足够多样化，从而最大限度地减少或者掩盖缓存等其他因素的影响。</div>2020-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/40/7c/43bafeb8.jpg" width="30px"><span>善行通</span> 👍（5） 💬（1）<div>感谢老师总结；
1、罗列出需要参数化的数据及相对应的关系；
2、将参数化数据从数据库中取出或设计对应的生成规则；
3、合理地将参数化数据保存在不同的文件中；
4、在压力工具中设置相应的参数组合关系，以便实模拟真实场景

之前做行测不太去理解：
Recycle on EOF? ：这里有三个选择，False、True 和 Edit。
Stop thread on EOF?：这里有三个选择，False、True 和 Edit。含义和上面一致。
Sharing mode : 这里有四个选择，All threads、Current thread group、Current thread、Edit。
这几个用户，经过老师这样一步一步分析，收获很大，谢谢老师分享

第一个问题：为什么参数化数据要符合生产环境的数据分布？
1、减少数据命中率；
2、减少缓存命中率；
3、符合性能压测价值,测试结果更真实；

第二个：为什么参数化数据要关注组合逻辑关系，而不是随意设置组合？
1、业务规则决定参数文件不能随便组合；
2、如果随意组合参数，会影响事务成功率；
</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/7d/0d/c753174e.jpg" width="30px"><span>筱の简單</span> 👍（3） 💬（1）<div>1、为什么参数化数据要符合生产环境的数据分布？
因为压测本身就是服务于生产环境，为使项目满足真实用户的需要，所以做压测的宗旨都是以实际业务逻辑出发满足用户需要，所以参数化也依赖业务逻辑，故在参数化之前，需要分析真实业务逻辑中如何使用数据，再在工具中选择相对应的组合参数的方式去实现。
2、为什么参数化数据要关注组合逻辑关系，而不是随意设置组合？
因为不关注组合的逻辑关系而随意设置组合，有些组合会存在没有意义且不符合逻辑关系的情况。影响参数化设置的有效性，也侧面反映压测人员的技术专业性。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/5a/5e/de904c17.jpg" width="30px"><span>陈陈陈小芮</span> 👍（2） 💬（2）<div>老师您好，我是刚接触性能测试没多久，所以有点疑问想请教下：
1、tps每秒100，5分钟需要的用户数据就是5x60x100，意思就是一秒钟需要的用户数据就是100个吗？举个例子，我的线程数、循环数都设置为1，一个线程组下有13个接口请求，但其中只有login这一个请求需要用到账号密码，其余的12个都不需要，此时执行显示13个请求在3秒处理完成，tps为平均每秒4.2个请求，按上面的逻辑，也就是一秒需要4.2个用户账号密码吗，但是这就跟我原本只需要一个账号密码相悖了，所以不太理解这个所需用户数的计算
2、在之前的基础篇您有讲过，tps是指的一个完整的事物，这个事物可以自己定义，若按这个理解，那么tps就应该是一个登陆操作带来的一系列请求（用我举的例子就是包含login在内的13个请求），可是此处的tps似乎是每秒处理的请求数（3秒请求数13，每秒就是4.2左右），好像又并不是事物数，这个点也不太理解</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/40/73/4e555fcb.jpg" width="30px"><span>兰澜</span> 👍（2） 💬（2）<div>高楼老师，听了这个课收获很多，理清了一些思路。刚刚学习性能测试，做了一些简单的项目，有一个很问题一直很困惑，做一个项目的性能测试是我们获得了项目中需要测试性能的各接口的TPS和响应时间指标，跑基准场景测试时，使用LR工具，我要如何来设置start new iteration中的第3个选项中的每间隔多长时间迭代一次的值呢，这个可以依据什么来计算呢？或者怎么设置比较合理？还有就是start vusers中的用户数，每隔多长时间启动多少个用户，这个怎么设置比较合理呢？刚踏入性能测试，不知道如何去设置跑场景时的这些参数值，不知道怎样才是合理的</div>2020-03-10</li><br/><li><img src="" width="30px"><span>武先生爱学习</span> 👍（2） 💬（1）<div>请问，在公司里，做性能测试用的是什么负载机，用的自己的机器还是Linux负载机呢，这一块能否介绍下？</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（2） 💬（1）<div>1，EOF处理不同对性能测试有什么影响？2，参数化用DB来获取，对性能测试结果的有无影响。</div>2020-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6e/7e/5a231c8f.jpg" width="30px"><span>VintageCat</span> 👍（1） 💬（1）<div>
Java
summary +    125 in 00:00:04 =   31.0&#47;s Avg:    28 Min:     0 Max:   869 Err:     0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +   3404 in 00:00:30 =  113.2&#47;s Avg:    31 Min:     0 Max:   361 Err:     0 (0.00%) Active: 6 Started: 6 Finished: 0
summary +   4444 in 00:00:30 =  148.4&#47;s Avg:    57 Min:     0 Max:   623 Err:    10 (0.23%) Active: 11 Started: 11 Finished: 0


这个登录接口的数据是怎么来的呢？我是指用什么策略执行的 ，没有很明白，看active分别是1 6 11这个是指不同的压力线程组情况下吧</div>2023-05-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/cJwhYkXicLBFezDEU6PibfNNXnkPGHpc11AqgKXppSUWstkmB8RZiag3OWvZBlXo8sPMy6XnZs1rFu1shX0HpCeOA/132" width="30px"><span>galsangflower</span> 👍（1） 💬（1）<div>csv文件读变量会影响性能吗</div>2022-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0c/6b/47fd3459.jpg" width="30px"><span>🌻eleven</span> 👍（1） 💬（1）<div>一直没明白，选择“当前线程”是什么意思，怎么判断当前线程
</div>2022-06-09</li><br/><li><img src="" width="30px"><span>章鱼</span> 👍（1） 💬（1）<div>问题一：数据必须保证仿真，否则性能压测将没有意义
问题二：因为参数化数据要组合逻辑关系会直接影响参数化数据的分布情况，即数据是否均匀？数据是否稳定？是保否证测试时间足够长？满足测试的负载请求足够多和数据足够多样化，从而最大限度地减少或者掩盖缓存等其他因素的影响</div>2022-03-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLERLpErfNmox2qxXAcuIIgrMX9DOX5utibwDzORysQxAWAzKNkKHGgcdMH22aD7qdm0lgic0vvEZgw/132" width="30px"><span>敢不敢y-- 不敢</span> 👍（1） 💬（1）<div>我想知道这个数据是从哪里能看到的？？？？
Java
summary +    125 in 00:00:04 =   31.0&#47;s Avg:    28 Min:     0 Max:   869 Err:     0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +   3404 in 00:00:30 =  113.2&#47;s Avg:    31 Min:     0 Max:   361 Err:     0 (0.00%) Active: 6 Started: 6 Finished: 0
summary +   4444 in 00:00:30 =  148.4&#47;s Avg:    57 Min:     0 Max:   623 Err:    10 (0.23%) Active: 11 Started: 11 Finished: 0</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b5/72/bb10f3d0.jpg" width="30px"><span>bolo</span> 👍（1） 💬（1）<div>1、为什么参数化数据要符合生产环境的数据分布？
个人理解因为测试用的数据要尽可能的贴近生产环境的。比如需要MQ相关的测试，我们一般通过从生产环境MQ平台查找符合条件的的消息，然后进行特定字段的修改后拿到测试环境经行测试（自己构造的话，很容易出现信息偏差，风险也较高）
另外一个例子是，我们有一个项目需要将媒体上报的设备字段落入到数据库，因为真实的用户的设备字段是不一样的，所以针对设备参数化的时候需要满足一定的位数，以及数字及字母的组合来模拟真实的线上用户。数据库层面根据设备字段又进行了数据的分库分表，如果参数化不合理（或者采用同一条数据），会导致数据分布的不够均匀，也是不符合产品需求的

2、实际操作了Jmeter里的CSV Data Set Config配置，
第1种场景：（更加贴近实际需要，循环执行的时候仅使用csv的数据。当循环次数超出时，终止执行。）
a)  Recyele on EOF 设置为 False(不再循环使用参数)
b)  Stop thread on EOF 设置为True (在参数不足时停止线程)
c)  Sharing mode设置为 All thead (所有线程)
CSV内的数据仅有6条，而线程数设置为1， 循环次数设置为8 
执行后，执行6次  成功后结束


第2种场景 循环csv的文件（循环使用参数后，不会存在参数不足的情况了。没有意义）
a)  Recyele on EOF 设置为 True(循环使用参数)
b)  Stop thread on EOF 设置为True (参数不足时，停止线程)
c)  Sharing mode设置为 All thead (所有线程)
CSV内的数据仅有6条，而线程数设置为1， 循环次数设置为8 
执行后，执行8次成功后结束


第3种场景 循环csv的文件（循环使用参数后，不会存在参数不足的情况了。没有一直）
a)  Recyele on EOF 设置为 True(循环使用参数)
b)  Stop thread on EOF 设置为False (参数不足时，不停止线程)
c)  Sharing mode设置为 All thead (所有线程)
CSV内的数据仅有6条，而线程数设置为1， 循环次数设置为8 
执行后，执行8次成功后结束


第4种场景 循环csv的文件（不符合场景，不循环使用参数，再循环次数设置的比较大的时候，肯定会存在参数不足的情况的）
a)  Recyele on EOF 设置为 False(不循环使用参数)
b)  Stop thread on EOF 设置为False (参数不足时，不停止线程)
c)  Sharing mode设置为 All thead (所有线程)
CSV内的数据仅有6条，而线程数设置为1， 循环次数设置为8 
执行后，执行8次，前6次成功，后2次失败</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/c6/88d0c7b2.jpg" width="30px"><span>一默</span> 👍（1） 💬（5）<div>
Java
summary +    125 in 00:00:04 =   31.0&#47;s Avg:    28 Min:     0 Max:   869 Err:     0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +   3404 in 00:00:30 =  113.2&#47;s Avg:    31 Min:     0 Max:   361 Err:     0 (0.00%) Active: 6 Started: 6 Finished: 0
summary +   4444 in 00:00:30 =  148.4&#47;s Avg:    57 Min:     0 Max:   623 Err:    10 (0.23%) Active: 11 Started: 11 Finished: 0

老师您好，现在tps是在148报错，有10个错误，但不能证明tps在120或者130左右是否会报错，这样是否需要在精确tps在120或者130左右的系统情况</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/b4/ff82483d.jpg" width="30px"><span>邵俊达</span> 👍（1） 💬（4）<div>
Java
summary +    125 in 00:00:04 =   31.0&#47;s Avg:    28 Min:     0 Max:   869 Err:     0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +   3404 in 00:00:30 =  113.2&#47;s Avg:    31 Min:     0 Max:   361 Err:     0 (0.00%) Active: 6 Started: 6 Finished: 0
summary +   4444 in 00:00:30 =  148.4&#47;s Avg:    57 Min:     0 Max:   623 Err:    10 (0.23%) Active: 11 Started: 11 Finished: 0

请问这个是在哪里能看到？我开了 summary report, view result tree 都没有这个。</div>2020-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（1） 💬（1）<div>老师，在没有做业务混合场景之前，我们需要先做 Benchmark 测试，来确定一个登录业务能支持多少的业务量，这样就可以在业务混合场景中，根据场景中各业务的比例来确定登录的数据需要多少真实的数据。
这段文章我可以理解为，在系统没有什么性能指标的时候我们可以先用Benchmark 来估计系统业务量，然后在实际压测时自己就有个压力范围值，今天试用了一下Apache benchmark但是好像资料不是很多，默认不能测试https，但是没找到很好的文档参考。老师有这Benchmark测试学习推荐吗？或者推荐使用工具。谢谢老师</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/7d/0d/c753174e.jpg" width="30px"><span>筱の简單</span> 👍（1） 💬（1）<div>老师请问：文章开篇时的登录业务的并发 看是代码形式的耶，这个的登录并发是用的locust工具吗？</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/41/d8/5a9fbb71.jpg" width="30px"><span>晴空</span> 👍（1） 💬（1）<div>1、为什么参数化数据要符合生产环境的数据分布？
尽可能少的数据应用覆盖到尽可能多的测试场景中。
2、为什么参数化数据要关注组合逻辑关系，而不是随意设置组合？
关注组合逻辑关系，可以理解为了解数据生成规则，换句话说也就是有效的数据是有哪些实际业务场景产生的。

无论是问题1还是问题2，都是以实际业务场景为基础进行展开测试与规划的</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/6d/8596513f.jpg" width="30px"><span>亘亘</span> 👍（0） 💬（1）<div>咨询一个问题，我压测过程中添加了CSV Data Set Config，包含100万用户数据，其中Sharing mode为All threads，jmeter 线程数为40，压测过程中发现jmeter会随机重复取数，并不是按照顺序进行取数，这种如果想让所有线程顺序取数要如何设置？</div>2024-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/98/fab9bd2a.jpg" width="30px"><span>Mingyan</span> 👍（0） 💬（3）<div>老师，请问下遇到这种登录业务要怎么跟用户沟通？用户说系统总用户达到6000个，一开始说用户是并发500登录，后面说500相对于6000太少了，要求1800并发登录，但是这个登录是基于微软云的sso登录，登录账号提供不了，要做UI层面的登录，说只提供10个账号让我们并发1800，我跟他们解释在线用户数和并发数并不是同一个概念，而且并发1800的sso太极端了，帐号重复登录也没有意义不符合实际场景，但是对方觉得别人的系统能做几百万的登录，不可能搞几百万个账号啊。我口拙，不知道怎么说和沟通。</div>2024-05-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eovjNRNjPcwyoVfLELrqEdLiazqeZyDgvsFGQ7sEXhbmSuFSiarWvy3an1FHbcPhlWBQEXguh3msJdg/132" width="30px"><span>问号和感叹号</span> 👍（0） 💬（1）<div>老师 用jmeter和loadrunner压测结果差了1000TPS，服务器资源利用情况也是一致的，这种是工具上的差异吗？</div>2022-05-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLERLpErfNmox2qxXAcuIIgrMX9DOX5utibwDzORysQxAWAzKNkKHGgcdMH22aD7qdm0lgic0vvEZgw/132" width="30px"><span>敢不敢y-- 不敢</span> 👍（0） 💬（1）<div>E:\jmter&gt;jmeter -n -t test.jmx
Creating summariser &lt;summary&gt;
Created the tree successfully using test.jmx
Starting the test @ Sun Mar 20 21:41:39 CST 2022 (1647783699799)
Waiting for possible Shutdown&#47;StopTestNow&#47;HeapDump&#47;ThreadDump message on port 44
45
summary =     10 in 00:00:02 =    5.7&#47;s Avg:   145 Min:    75 Max:   348 Err:
  0 (0.00%)
Tidying up ...    @ Sun Mar 20 21:41:42 CST 2022 (1647783702191)
... end of run
E:\jmter&gt;jmeter -n -t test.jmx
Creating summariser &lt;summary&gt;
Created the tree successfully using test.jmx
Starting the test @ Sun Mar 20 21:42:00 CST 2022 (1647783720875)
Waiting for possible Shutdown&#47;StopTestNow&#47;HeapDump&#47;ThreadDump message on port 44
45
summary +      1 in 00:00:01 =    1.4&#47;s Avg:   443 Min:   443 Max:   443 Err:
  0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +      9 in 00:00:01 =    9.2&#47;s Avg:   104 Min:    86 Max:   139 Err:
  0 (0.00%) Active: 0 Started: 1 Finished: 1
summary =     10 in 00:00:02 =    5.8&#47;s Avg:   137 Min:    86 Max:   443 Err:
  0 (0.00%)
Tidying up ...    @ Sun Mar 20 21:42:03 CST 2022 (1647783723230)
... end of run

执行两次结果得到不同，这是什么原因？</div>2022-03-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLERLpErfNmox2qxXAcuIIgrMX9DOX5utibwDzORysQxAWAzKNkKHGgcdMH22aD7qdm0lgic0vvEZgw/132" width="30px"><span>敢不敢y-- 不敢</span> 👍（0） 💬（1）<div>前面我们知道，在这个示例中只做了近 10 万条的用户数据，为了方便示例进程。

-----有这个过程吗？</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/35/04f1ad16.jpg" width="30px"><span>你比昨天快乐🌻</span> 👍（0） 💬（1）<div>CSV Data Set Config的Sharing mode选择了Edit，准备有两个线程组名称分别为：Thread Group1、Thread Group2，参数化文件只想在Thread Group1中使用，不想在Thread Group2中使用，Edit 选项，在这里我有输入：SharedWithThreadGroup1（或SharedWithThreadGroupThreadGroup1）。期望结果应该是：Thread Group1能从参数化文件取到值，Thread Group2取不到值，但是执行结果是：Thread Group1和Thread Group2取值完成一样，请问哪里问题出在哪里呢</div>2020-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/8d/b4/ff82483d.jpg" width="30px"><span>邵俊达</span> 👍（0） 💬（0）<div>
Java
summary +    125 in 00:00:04 =   31.0&#47;s Avg:    28 Min:     0 Max:   869 Err:     0 (0.00%) Active: 1 Started: 1 Finished: 0
summary +   3404 in 00:00:30 =  113.2&#47;s Avg:    31 Min:     0 Max:   361 Err:     0 (0.00%) Active: 6 Started: 6 Finished: 0
summary +   4444 in 00:00:30 =  148.4&#47;s Avg:    57 Min:     0 Max:   623 Err:    10 (0.23%) Active: 11 Started: 11 Finished: 0</div>2020-05-05</li><br/>
</ul>