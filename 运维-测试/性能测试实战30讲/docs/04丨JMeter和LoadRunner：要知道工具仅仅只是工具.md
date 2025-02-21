做性能测试工作的人总是离不了性能测试工具，但当我们刚开始接触这类工具或者压测平台的时候，总是难免处在一种顾此失彼，焦虑又没想法的状态。

## 性能工程师的三大学习阶段

在我看来，对性能测试工程师本身来，多半会处在以下三个大的阶段。

### 性能工具学习期

JMeter和LoadRunner是我们常用的两个性能测试工具。曾经有人问我，应该学JMeter还是LoadRunner呢？我反问的是，你学这样的工具需要多久呢？一般对方因为初学并不清楚要多久，然后我会告诉他，如果你是认真努力的，想要全职学习，那么我觉得一个工具，纯从功能的使用的角度来说，自学两个星期应该就差不多了。如果你是在工作中学习，那就更简单了，工作中需要什么就学习什么，不用纠结。

而应该纠结的是什么呢？当你把JMeter、LoadRunner的基本功能学会了，你会发现这些工具其实就做了两件事情，做脚本和发压力。

但问题在于，脚本的逻辑和压力场景的逻辑，和工具本身无关，和业务场景有关。这时你可能就会问，场景怎么配置呢？

这才进入到了另一个阶段。

通常在这个阶段的时候，你会觉得自己有非常明确的疑问，有经验的人可能一句话就可以指点你了，解决掉你的疑问，就是告诉你选择什么工具，如何来用。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/dd/0f/ee37a7fe.jpg" width="30px"><span>zuozewei</span> 👍（99） 💬（5）<div>第一个问题：
大概会考虑怎么几个方面：
- 学习成本：对人员的水平要求，培训时间成本等；
- 脚本编写：能否录制测试脚本，是否支持GUI操作等；
- 安装部署成本：是否支持一键安装，是否支持docker等；	
- 是否免费：开源工具一般都是免费的；但是很多收费工具也的确物有所值；	
- 是否支持多协议：比如是否支持 HTTP 协议、RPC 协议等等	
- 测试场景：是否有链路、场景编排管理，支持支持将请求编排成业务场景，即常见的一串联场景；
- 流量控制：支持纵向的，上下游链路的请求量逐渐减少，整体呈现一个漏斗模型；也可以是横向的；
- 压力控制：指压测时并发用户数、 TPS 的控制等；
- 数据驱动：大量的测试数据的参数化；
- 分布式支持：支持压力机集群；
- 测试报告：压测结果是否能够图形化展示，提供美观且丰富的测试报告；
- 二次开发的成本：由于时间或人力关系，也需要考虑二次开发成本；
- 性能开销：执行机开销、软件可靠性、执行效率、业务处理能力等。
....

第二个问题：
我觉得一个好的监控系统大概需要包括以下几个方面：
- 全栈系统监控是前提；
- 关注于整体应用的 SLA：主要从为用户服务的 API 来监控整个系统；
- 关联指标聚合：把有关联的系统及其指标聚合展示。主要是三层系统数据：基础层、平台中间件层和应用层。并提供一个全局的系统运行数据大盘，帮助快速找到系统瓶颈。
- 快速故障定位：快速定位问题需要对整个分布式系统做一个用户请求跟踪的 trace。 

只有做到了上述的这些关键点才能是一个好的监控系统，而显然目前的测试工具监控是不满足的。

另外测试工具本身在做监控也有其局限性，如 jmeter 在压测量较大的情况下回传测试结果 Master 节点会成为容易成为瓶颈。
</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ec/de/2377aced.jpg" width="30px"><span>calm</span> 👍（30） 💬（1）<div>高老师，能否推荐一些性能测试这方面的书籍？</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/16/c1/db559c42.jpg" width="30px"><span>私人领域</span> 👍（15） 💬（5）<div>现在在公司做的还是不太顺利，概念不理解，大家对并发的不理解，这包括开发，产品，项目，部分运维可以理解；还有就是无理要求要求8000并发，这个怎么跟他们解释都无用，一说就是客户要求的，这8000并发发包出去就几g的流量了，真不明白他们怎么想的，这做技术的人一点基础都没有，真的很难工作</div>2019-12-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdesQy0moaicYTicoHRQXzbmJm15wohb77qD1OdbuSqPCSUerbcZHzxJJunfmEhTx4kBLxbGaxQ9iag/132" width="30px"><span>村夫</span> 👍（14） 💬（1）<div>老师请教一个问题。关于事物的定义，假如有一个兑奖的活动，进去活动页面会请求三个接口，一个个人积分接口，一个是任务列表接口，还有一个是兑奖列表接口。在页面点击兑奖按钮会去请求兑奖接口，兑奖成功页面会去调用用户接口刷新用户当前积分。这样的情况应该怎么去定义事物？</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（7） 💬（1）<div>要测试一个在线运行的网站性能，应该使用什工具比较好？设置的被测网站的IP地址可以是公网IP吗？</div>2019-12-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Cyuxk6Ej9B5G9icGd2h9OicjdbuWMsQsB0cOZoRXLN6zX5bfmCXB4yHiaicOcE5OUicGDIaodS9T4Ws6lGBibFWoSlKQ/132" width="30px"><span>Geek_081377</span> 👍（6） 💬（2）<div>支持高老师，希望听完能成为公司的性能大牛，哈哈</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/51/50/f5f2a121.jpg" width="30px"><span>律飛</span> 👍（6） 💬（1）<div>第一个问题：
    企业选择性能测试工具无外乎两种策略，一是性价比优先，花最少的钱最快地完成最多最需要完成的任务，比如租用云压测平台，属于头痛医头，脚疼医脚的临时策略，小公司、发展初期公司等常采用的策略，可以快准稳完成压力测试。二是结合长期发展目标，分阶段规划测试工具购买及测试人员培养，甚至自己开发测试工具，积累并形成自己的压测能力。这个策略与公司测试人员以及测试团队能力也有很大的相关性。其实老师已经讲得很清楚了。
第二个问题，我个人认为不应该在测试工具中做监控。现在处于一个分工很细的世界，术业有专攻，专业人做专业事，一来可以保持工具的简洁，二来可以保持工具的通用性，增加使用的灵活性。当然这对做性能测试的人的能力要求就更高了。不过工作的乐趣不就在于此吗？</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（5） 💬（1）<div>思考题：
你觉得企业选择性能工具应该考虑哪些方面呢？
1、企业规模及性质
2、系统性能目标（想要支持多少TPS）
3、系统架构
4、员工的学习成本
5、工具的优势是否满足要求，工具的缺点是否对性能测试没有影响或影响不大
（感觉自己的思维还是不够开阔呀，需要继续努力）


性能测试工具中是否必须做监控呢？
1、如果压测工具中必须做监控，那么大概率也就不会有监控工具了吧。因此监控工具的存在本身就表示了压测工具做监控这件事儿不是必须的。
2、第二点就是文中说的，数据流向不同，不符合真实的场景。


本文虽然是讲工具，但并非单纯的讲工具。老师不断强调的一个点都是，性能测试一个完整的流程是测试验证、分析和调优。（可能是有太多人以为性能测试=会工具的使用吧）
性能测试工具，本质上还是个工具，工具都是人发明的，为的是解决某个问题，同时都有自己的优势和不足。比如交通工具，上班的时候可以选择步行、骑自行车、骑电动车、开车、坐公交、坐地铁等等，开车肯定是最舒服的，但是可能会堵车；骑自行车是最健康的，但是耗时会长一些而且还要风吹日晒。其实选哪个都可以，只要能到公司就行。但是每个人的向往、喜好和财力不同，比如有人不怕日晒雨淋，更向往健康的生活方式，那我就选择骑自行车上班；有人讨厌堵在路上的感觉，所以选择地铁出行；有人没钱，买不起车，那就只能选择相对便宜的交通工具。
因此，不用过分纠结用哪个性能测试工具，只要我们能拿到需要的数据就行。</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/20/1d/0c1a184c.jpg" width="30px"><span>罗辑思维</span> 👍（4） 💬（2）<div>最近在得到学习《薄世宁·医学通识50讲》 08丨病与症：为什么这些“病”不用治？文中对病与症的解读，让我能理解工具，性能指标，性能分析人员之间的关系。

比如风寒感冒（症状是怕冷，流稀鼻涕），吃风寒感冒颗粒，热水泡脚。
风热感冒（症状是咽喉肿痛，发烧），吃退烧片，热水泡脚，多喝淡盐水。

对应性能分析
性能指标 &lt;---&gt;  症
性能分析者的判断 &lt;---&gt; 病
性能优化 &lt;---&gt; 药

而工具只是观察性能指标（症）的手段，就像医生用仪器测量血压。
</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/73/16/595b0342.jpg" width="30px"><span>slark</span> 👍（3） 💬（1）<div>Jmete和Locust都学过，J感觉有GUI，L是Python，编写测试脚本更便捷</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/41/6d/e8a6f9e3.jpg" width="30px"><span>要不要菜</span> 👍（2） 💬（2）<div>说的太对了，目前就是到了尴尬的第三个阶段，会用工具会执行场景，就是不会分析调优</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/3e/82202cc8.jpg" width="30px"><span>月亮和六便士</span> 👍（2） 💬（2）<div>高老师，推荐几款监控Java语言接口和方法执行时间的工具，比响应时间细分到Java某个工程的jar包，我怎么监控这个jar包里的接口执行时间，方法执行时间，还有算法执行效率，等等</div>2019-12-24</li><br/><li><img src="" width="30px"><span>Geek_615688</span> 👍（1） 💬（1）<div>我看到这里，说压测都是用TPS来计算，为啥我们每次要压测，都是QPS计算，比如上次压测，研发说我期望你们压到1000QPS</div>2022-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（1） 💬（1）<div>1.成本 ，易用性  
2.不必要监控</div>2022-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（1） 💬（2）<div>jmeter对go开发者不友好，go的程序比较容易改和扩展，部署也方便，性能也强很多，老师可以推荐一款golang的性能测试工具不？</div>2021-05-08</li><br/><li><img src="" width="30px"><span>Geek_359b73</span> 👍（1） 💬（1）<div>老师能否再说说性能场景的设计，现在对于测试场景的设计还是没有一个思路</div>2021-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/5a/4a/b763a1c9.jpg" width="30px"><span>张乐乐</span> 👍（1） 💬（1）<div>我还是比较推荐Jmeter毕竟性价比非常好，安装也没那么麻烦，兼容性也好，一般企业足够用。2、监控必须做，我们公司有普罗米修斯+Grafana，长期监控各项目运营平台。</div>2021-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>对性能测试工程师的职责有了清晰的认知</div>2020-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/8f/fcfaf45a.jpg" width="30px"><span>莫西 👫 小妞儿 👼 🎵</span> 👍（1） 💬（1）<div>老师，想问一下前端性能的测试工作都有哪些呢？比如想知道实际用户看到页面中所有元素都加载完的时间</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c7/8f/fcfaf45a.jpg" width="30px"><span>莫西 👫 小妞儿 👼 🎵</span> 👍（1） 💬（2）<div>老师，我们单位属于国企，现在是用jmeter来压测，用nomn作为监控工具，这样是否可行。或者有什么更好的推荐么？</div>2020-01-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/20ic9dve9ysLva9LVzImmque2LG9jXrDR0P6VUdepicFedKfrFU0TnKJLWGQ62lNs8xtddrrSdYlbdF4I8zFsqow/132" width="30px"><span>Geek_0849d2</span> 👍（1） 💬（2）<div>什么样的业务可以线上直接压测，什么样的业务不可以？如何控制线上的性能测试？我遇到的项目都不能直接压测线上，直接线上压测，万一压塌了，影响正常用户使用怎么办？</div>2020-01-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJBbpHBlZcGbwicdA9VN7YHegZALice19Rjo5MAhosU4Z34x2aaz5YiaJyqtpNibdkS89ItspIjSIFbPQ/132" width="30px"><span>Geek_alair俊</span> 👍（1） 💬（1）<div>工具只是工具，通过工具的使用，分析出性能瓶颈，并且给出解决方案，这才是王道！神马各种压测工具，监控工具，看得见的没多少价值，分析这部分看不见的过程才是最有价值的！高老师一语中的。</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/4b/05/db6b70dc.jpg" width="30px"><span>玉面小肥猫</span> 👍（1） 💬（1）<div>老师您好，“比如说压力策略，应该用一秒 Ramp up 10 个用户，还是 20 个用户，还是 100 个用户？这应该怎么判断呢？”可否回答一下，最近正在纠结这个问题，谢谢！</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/31/7c/52e8a87d.jpg" width="30px"><span>Geek_ih8bk6</span> 👍（1） 💬（1）<div>高老师，什么时候更新啊?希望尽快看到你后面的章节</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（1） 💬（1）<div>我们单位基本用jemter来压测，主要的测试为接口级测试，接口基本为数据给出接口，属于查询类事务</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/fa/cf/d35705ac.jpg" width="30px"><span>两叶扁舟</span> 👍（0） 💬（1）<div>您好，我是一个MQ内核开发工程师，请问这些测试工具可以用来压测 MQ的性能瓶颈吗？
在过往的经验的，我都是自己根据客户端 手写一个 性能压测的工具类，然后打成Jar后在机器上运行。
JMeter可以帮助管理运行这些Jar吗？ </div>2024-10-02</li><br/><li><img src="" width="30px"><span>Geek_d0aaec</span> 👍（0） 💬（1）<div>如何选择性能工具，结合下两方面考虑：
1、清楚自己的目标，条件（愿意负担的成本，团队的能力，限制条件等）
2、了解工具的能力，能做什么不能做什么，优势和缺点</div>2024-09-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ajNVdqHZLLAhj2fB8NI2TPI1SNicgiciczuMUHyAb9HHBkkKJHrgtR162fsicaTqdAneHfuVX7icDXaVibDHstM9L47g/132" width="30px"><span>Geek_0c1732</span> 👍（0） 💬（1）<div>想起我研究java内存溢出的日子，有内存监控数据，有控制台日志，就是不知道原因</div>2023-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/fb/ecae913a.jpg" width="30px"><span>小安</span> 👍（0） 💬（1）<div>1、你觉得企业选择性能工具应该考虑哪些方面呢？
答：从ROI投入产出比去考虑
2、以及性能测试工具中是否必须做监控呢？
答：应该尽量少的监控，因为监控越多信息，消耗的资源越多。</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6e/7e/5a231c8f.jpg" width="30px"><span>VintageCat</span> 👍（0） 💬（1）<div>最近开始学 发现高老师人也太好了吧 每个遇到问题的留言不管问题是否低级高级都会回复！！难怪大家的留言很多 看完课程内容光是看完留言都花了很久，不像我之前买的课程，老师回答的很敷衍，也只挑以前的回复少数几个，遇到问题百度又解决不了的时候就很焦虑了</div>2023-05-22</li><br/>
</ul>