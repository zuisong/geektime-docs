在上一篇文章中，我们讲述了性能场景，下面就要说性能需求指标了。

通常我们都从两个层面定义性能场景的需求指标：业务指标和技术指标。

这两个层面需要有映射关系，技术指标不能脱离业务指标。一旦脱离，你会发现你能回答“一个系统在多少响应时间之下能支持多少TPS”这样的问题，但是回答不了“业务状态是什么”的问题。

举例来说，如果一个系统要支持1000万人在线，可能你能测试出来的结果是系统能支持1万TPS，可是如果问你，1000万人在线会不会有问题？这估计就很难回答了。

我在这里画一张示意图以便你理解业务指标和性能指标之间的关系。

![](https://static001.geekbang.org/resource/image/1b/c2/1bb1222c53e8b16414458a8572e786c2.png?wh=2304%2A1556)

这个示意显然不够详细，但也能说明关系了。所有的技术指标都是在有业务场景的前提下制定的，而技术指标和业务指标之间也要有详细的换算过程。这样一来，技术指标就不会是一块飞地。同时，在回答了技术指标是否满足的同时，也能回答是否可以满足业务指标。

有了这样的关联关系，下面我们看一下性能测试行业常用的性能指标表示法。

![](https://static001.geekbang.org/resource/image/53/83/533fa609f8607dbd65878fb52ef87183.jpg?wh=3934%2A2849)

我将现在网上能看到的性能指标做了罗列，其中不包括资源的指标。因为资源类的比较具体，并且理解误差并不大，但业务类的差别就比较大了。

## 对这些性能指标都有哪些误解

我记得我还年轻的时候，还没有QPS、RPS、CPS这样的概念，只有TPS。那个时候，天总是那么蓝，时间总是那么慢，“你锁了人家就懂了”。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="" width="30px"><span>飞翔</span> 👍（95） 💬（12）<div>如果这时响应时间是 100ms，那显然并发线程数是 500TPS&#47;(1000ms&#47;100ms)=50(并发线程)。 这没看明白是什么意思</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/9c/30cd6840.jpg" width="30px"><span>nana</span> 👍（22） 💬（4）<div>老师好，有个问题麻烦问下jmeter压测constant throughput timer中设置的qps ，实际中的threads是怎么分配的？对于number of threads（users）和ramp-up period设置压上去的throughput和前面提到的qps这个不同点，麻烦解释下，辛苦多谢啦</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/0f/ee37a7fe.jpg" width="30px"><span>zuozewei</span> 👍（18） 💬（1）<div>第一个问题：
这个命题的争论有个bug，问题在于「快、好」的定义上。做为不同业务下的性能水平，快的定义是不一样的，比如在数据处理业务中，常分OLAP（联机分析处理）、OLTP（联机事务处理），比如一个简单的 OLTP 查询有大厂是要求微妙级别的，OLAP 统计报表类的业务查询几分钟也是可以接受啊。

第二个问题：
在一个具体的业务场景中，性能场景中的业务模型和二八原则并没有什么关系，即使从宏观上来说有关系，也是很牵强的，至少至今为止，还没看到任何有数据和数学公式的支撑证明。</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b2/dc/67e0e985.jpg" width="30px"><span>顺利</span> 👍（14） 💬（6）<div>同学提问： 那是不是jmeter测试每秒500个用户并发 就是设置50个线程 Ramp-Up为1秒？老师的回复: 不一定，要看响应时间是多长，做出有梯度的场景来。
我的问题是：如果响应时间是10ms，如何得出这个梯度的场景。求解答</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/51/50/f5f2a121.jpg" width="30px"><span>律飛</span> 👍（9） 💬（1）<div>第一个问题，世界上没有一个放之四海而皆准的原则理论，拿来就用必出问题，唯有知其然，知其所依然，才能正确使用。感谢老师给我们上了生动的一课，在学习中始终保持一份好奇心，多思考，多问几个问题，才能学以致用。
第二个问题，二八定律是19世纪末20世纪初意大利经济学家帕累托发现的。帕累托从大量具体的事实中发现：社会上20%的人占有80%的社会财富，即：财富在人口中的分配是不平衡的。现在这个定律被广泛用在很多领域，比较有名如时间管理认为，20%的时间完成80%的工作。其实我个人认为，就时间管理而言，这个二八定律也是不合适的，是学渣们自我偷懒的借口。所以很喜欢老师说的，不要满口理论、定律等花架子，应该按照业务，按照样本数据分析结果，从实际出发，这样才能实事求是，做出符合实际的业务预估。
        这堂课还需好好消化，也建议老师结合自己的实践，提出你自己的模型，让我们学习参考借鉴！</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ff/e1/d2e4ed37.jpg" width="30px"><span>miminiMei</span> 👍（9） 💬（1）<div>老师的声音好好听，可以一直听，反复听😉</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c9/9e/ce7c8522.jpg" width="30px"><span>秋水共长天一色🌄</span> 👍（8） 💬（1）<div>老师你好，我在读了你的这篇文章之后也产生了几个疑问。
    1.就在文中你在解释TPS中的T的定义时，你提到了三种脚本情况，1是接口级，2是业务级，3是用户级。主要用户级中有提到一个点击的动作的这个步骤，如果在jmeter中进行压测是要怎样体现这个步骤？还有我们定义业务接口层脚本时是只将主流程的接口收录呢还是说会将这个页面下所有的接口都收录呢？（例如在一些商城项目中，确认订单页面有生成订单的接口，这个我们可以认为这是主流程的接口，但是也有可能有调一些关于获取广告信息的接口，但是这个接口与主流程下单流程没什么关系，但是又确实消耗了服务器资源了，那我们在写脚本时是否还需要把这部分也写进去）
    2.一个事务的完成我理解的是主要看这个脚本是如何编写的，如果这个事务的脚本中只有针对一个接口而已，那么接口请求完成后就算是完成一个事务。如果这个事务脚本中有10个接口组成的事务，那就需要10个接口都请求完成了才算一个事务的完成，这样理解对吗？
    3.对于QPS，我们在实际工作中我们要如何得知数据库查询在整个请求中所占的比重呢？
    4.在解释RPS的时候给出了一个例子（如果一个用户点击了一次，发出来 3 个 HTTP Request，调用了 2 次订单服务，调用了 2 次库存服务，调用了 1 次积分服务），这三个http请求我能理解，但是中间你是用了“调用”这个词，这里的调用是指订单服务内部去调用库存服务和积分服务的外放接口还是说调用的库存服务和积分服务公开的方法？
    5.还有在并发线程时有提到一个公式（500TPS&#47;(1000ms&#47;100ms)=50(并发线程)），我想知道其中的这个100ms的这个响应时间是如何得出的？是通过对一个脚本进行单一线程执行一次的方式得出的响应时间吗？
    6.还有这个课程解答了很大一部分我对与性能测试中想不通的点，这个课程很值，感谢老师的分享。
</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（8） 💬（1）<div>这一篇超值了</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e1/ed/b0284986.jpg" width="30px"><span>妍</span> 👍（7） 💬（5）<div>老师您好，有个问题请教一下 ，在jmeter中，设置200 并发，1s内发出，，执行结果中 平均响应时间为6ms，，那我的TPS 计算是200还是200*（1&#47;0.006）呢？
</div>2020-04-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoYs6FqOibbPfLRJxV2E2l6ibQz5GgwtI9KibxqDs5o4Uklno24pulGoUI0W8QNL4ruO4gn7CmTLD5VQ/132" width="30px"><span>大脸猫</span> 👍（7） 💬（1）<div>老师，请问吞吐量怎么理解我一直没明白，吞吐量和TPS，响应时间之间有什么关系</div>2020-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b7/00/12149f4e.jpg" width="30px"><span>郭刚</span> 👍（6） 💬（2）<div>我们经常遇到这样的问题，系统注册用户有2万，我们的公式是2万*5%*5%，第一个5%是在线用户数，第二个5%是压力测试的用户数。 用户不同意，至少要测试并发数1千，测试环境的机器又不行，经常鸡飞狗跳，无语啊！</div>2019-12-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Ce5DHQHpoeWBDMtibPAO9QKfRgRz9RvA3jgibMfJnyIXmOgZulVW02NYtn6ibF2fGNMQZ7z6LopHrknqB6MAzP1pw/132" width="30px"><span>rainbowzhouj</span> 👍（6） 💬（1）<div>第一个问题：
不合理之处在于没有结合实际场景去规定它的响应时间。响应时间是否合理是要进行对比的，例如现在的大数据技术测试，在不同的条件配置下处理TB级的数据，响应时间半天、一天都可以说是合理的响应时间。因为影响响应时间的因素有很多（存储方式，调度方式，参数调优等），单独拿“258”说明是没有意义的。

第二个问题：
常识的适用情况在于通用，但实际场景中经常会有各种“意外”。以12306购票系统为例，以前春运抢票时经常会有朋友、家人吐槽12306好卡、好慢，我估计之前就是业务模型用了28原则，虽然已经进行过了压力测试、疲劳测试，但还是抵挡不住全国人民着急回家的心情，拼命的发送请求......所以实际情况要实际考虑，以通用估意外肯定会才很多坑，只有不断地优化，更新才能一步步满足用户地需要。（PS：现在12306系统已经好很多了）</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/4f/2ba81594.jpg" width="30px"><span>棋子</span> 👍（6） 💬（1）<div>有没有一套相对普适的测试场景、衡量指标以及对应的测试方法论？看完3篇感觉思维有点儿混乱。也可能是自身想通过课程走捷径，有点急躁，谢谢🙏</div>2019-12-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/aCVlj0fom8geRoXFkO34JWPCbrsOEmDOOficXvxBZ3kic9pot0mbZ8p5FIkkkibvAXdxfoWJHdmLBV47aib78RTxQw/132" width="30px"><span>Geek_618ac5</span> 👍（6） 💬（3）<div>有点虚，都是讲一些 指标计算方式 不准，能否给一个准的？ 新的刚开发的系统什么都没有，怎么收集线上业务数据？ </div>2019-12-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/B7mcB2ZFuTbB4OgjR9nXQsL6nlZFLq6Y1XDicdp8KhoNmzLCRsvEJxD584SampUsialBgYuxN3ibfXJHqdx0RMWmA/132" width="30px"><span>大白</span> 👍（5） 💬（3）<div>老师，有时间请踩一下我
1、如何进行基准测试，基准测试如何进行数据分析？
2、之前我理解的并发用户数 就是并发线程数（单接口）， TPS是服务器单位时间内事务处理数，看了文章后为什么并发用户数会是TPS呢? 难道是这么理解？--&gt;服务端的单位时间内的处理能力才是大家口中的并发数？ </div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ae/79/da524393.jpg" width="30px"><span>sharpdeep</span> 👍（5） 💬（2）<div>在这种情况下，我们可以根据现有的数据，做统计分析、做排队论模型，进而推导以后的系统容量。

做统计分析，做排队论模型，这个具体是怎么操作？</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/bd/6b/9bf96783.jpg" width="30px"><span>月半虫工🍧</span> 👍（5） 💬（2）<div>老师，我有些点不太确定：
1.在线用户数是通过监控得出的数据吗？
2.并发度是主要业务才会大些，其他业务的并发度在1%～5%？
3.TPS是有上面两个业务指标计算得出来的？
4.响应时间是通过生产数据得出的，算是已知条件？
5.并发线程是由TPS *响应时间得出的，是需要计算的？
我把我的理解写在笔记里，希望能得到解答：
https:&#47;&#47;mubu.com&#47;doc&#47;x98c71O2aZ</div>2019-12-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/1uP7K0RUIQZ87oXE5GVDDclD3GRIDPRyhYfmSic7hq9GBYvjibgBaSPXLTWYjEqbSYbwFhunw6ibntgLa3C7VyibWw/132" width="30px"><span>start</span> 👍（5） 💬（1）<div>并发度一般怎么分析获取</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f2/e1/3366ed5f.jpg" width="30px"><span>漫漫</span> 👍（5） 💬（1）<div>一模一样，每个人都认为不是自己的问题</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/07/09cc4bdc.jpg" width="30px"><span>吃饭睡觉打豆豆</span> 👍（5） 💬（2）<div>其实我觉得这个什么所谓的28，258，25810原则都是虚的，直接点就是测目前系统实际的并发数和吞吐量</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（4） 💬（1）<div>老师是一个有故事的人，文章很精彩，例子很生动。把技术文章写成了小说。</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/32/42/667cc7ab.jpg" width="30px"><span>钟</span> 👍（4） 💬（5）<div>在上面这张示意图中，其实压力工具是 4 个并发线程，由于每个线程都可以在一秒内完成 4 个事务，所以总的 TPS 是 16。这非常容易理解吧。而在大部分非技术人的脑子里，这样的场景就是并发数是 4，而不是 16。

——————————————
这里的场景tps是16没错， 并发数是4为什么错了呢？
并发的意思不就是同时请求数量吗？ 4个线程， 每一刻都是只有4个同时的请求在处理</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/43/8a/cbf0a470.jpg" width="30px"><span>漏沙</span> 👍（4） 💬（1）<div>新的系统没有业务数据支撑，很多都说参考行业或者竞品系统，行业数据或者竞品的信息也没有公开，要怎么收集呢，大神是怎么做的呀！</div>2019-12-17</li><br/><li><img src="" width="30px"><span>学员141</span> 👍（3） 💬（1）<div>还是不是很明白上面对T的定义，如业务级和用户级在脚本编写上区别是什么？异步同步脚本上怎么编写？</div>2021-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/e7/c3/ad741cdf.jpg" width="30px"><span>沙棘</span> 👍（3） 💬（1）<div>老师，请教一下，接口容量和业务容量有什么区别？</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/45/21/4d3de923.jpg" width="30px"><span>Geek_f20bfb</span> 👍（3） 💬（4）<div>在并发的时候，TPS达1000左右，服务端的6w多个端口一下就满了，然后报错了，这种要怎么处理？</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/c5/dc/4e81dc1e.jpg" width="30px"><span>pengyang</span> 👍（2） 💬（1）<div>对一个线程来说，如果响应时间是100ms，那这个线程在一秒内不就是：1000ms&#47;100ms = 10tps了吗？ 如果要达到500TPS，那需要多少线程呢？就是500TPS&#47;10TPS=50线程。
想问一下这个时间是平均响应时间吗</div>2021-12-15</li><br/><li><img src="" width="30px"><span>Geek_23ac57</span> 👍（2） 💬（4）<div>我想知道怎么分析这个并发度呀，我们实际业务场景是在一分钟会有10000多个用户进行登陆注册，那么这段时间的并发度取0.6%嘛还是怎么计算的，我懵了</div>2021-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/77/72/8f77ddb0.jpg" width="30px"><span>johnny</span> 👍（2） 💬（1）<div>“拿 5% 来计算，就是 10000 用户 x5%=500(TPS)，注意哦，这里是 TPS，而不是并发线程数。”
老师， 10000 用户 x5%=500(TPS)这个计算过程是不是应该有个前提条件？这个前提就是一个用户只完成一个T(即事物)，或者说一个用户对应一个T(即事物)。
如果是每个用户对应2个T(即事物)，那么TPS还要翻倍，就是500(TPS)*2=1000(TPS)。</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/91/bb/f1d1483f.jpg" width="30px"><span>Cyx</span> 👍（2） 💬（3）<div>老师，没有性能基础，看完完全蒙掉，后面的课程也这么难吗？或者老师有没有推荐的基础点的东西？</div>2020-12-14</li><br/>
</ul>