你好，我是蔡元楠。

今天我要与你分享的主题是“Workflow设计模式”。

在上一讲中，我们一起学习了大规模数据处理的两种处理模式——批处理和流处理。

利用好这两种处理模式，作为架构师的你就可以运筹帷幄，根据实际需求搭建出一套符合自己应用的数据处理系统。

然而，光是掌握了这两种数据处理模式就足够自如应对大规模数据世界中的需求挑战吗？从我的实战经验中看来，其实未必。

我们每个人在最开始学习大规模数据处理的时候，可能都是以WordCount作为教学例子来进行学习的。

WordCount这个例子，只需要一个单词集合作为输入，数据处理的结果是统计单词出现的次数，中间只需要经过一次数据处理的转换，就如同下图所示。

![](https://static001.geekbang.org/resource/image/1b/9c/1b82384d37d37653721613e49933359c.jpg?wh=1798%2A650)

但在现实的应用场景种中，各式各样的应用需求决定了大规模数据处理中的应用场景会比WordCount复杂很多倍。

我还是以我在第一讲中所提到过的例子来说明吧。

在根据活跃在街头的美团外卖电动车的数量来预测美团的股价这个例子中，我们的输入数据集有可能不止一个。

例如，会有自己团队在街道上拍摄到的美团外卖电动车图片，会有第三方公司提供的美团外卖电动车数据集等等。

整个数据处理流程又会需要至少10个处理模块，每一个处理模块的输出结果都将会成为下一个处理模块的输入数据，就如同下图所示。
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/5a/e708e423.jpg" width="30px"><span>third</span> 👍（85） 💬（1）<div>用户注册，入库，合并模式

购买机票，分为查询机票和购买

查询机票，读取特定机票，过滤模式

购买机票，将所有渠道的票和合并起来，合并模式

24小时提醒，过滤出这班航班的机票，过滤模式
发送短信和电子邮箱，复制模式之后，进行分类模式发送</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/40/bd/acb9d02a.jpg" width="30px"><span>monkeyking</span> 👍（49） 💬（3）<div>这几个模式就是sql的几个operator吗？
复制 → subquery
过滤 → where
分离 → group by
合并 → join
</div>2019-05-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/9chAb6SjxFiapSeicsAsGqzziaNlhX9d5aEt8Z0gUNsZJ9dICaDHqAypGvjv4Bx3PryHnj7OFnOXFOp7Ik21CVXEA/132" width="30px"><span>挖矿的小戈</span> 👍（32） 💬（1）<div>1. 注册：合并模式（因为注册渠道可能会有手机号注册、邮箱注册、微信注册等等不同的渠道，所以需要合并）
2. 购买机票：过滤+合并（首先过滤出用户查找的航班机票信息、之后查找出符合条件的机票由于可能来自不同的渠道，所有需要合并后返回给用户）
3. 提醒：复制+过滤+分离
          过滤：根据时间、地点等因素过滤出需要给予提醒的用户 and 机票
          复制：有可能需要对同一份数据（勾选多种提醒方式的用户）进行不同的处理（邮件通知 or 电话通知 or 短信通知）
          分离：将前面过滤出的用户进行分成3组，分别对应（邮件通知 + 电话通知 +短信通知）
请大佬指教，理解有误没</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/45/ebd94d28.jpg" width="30px"><span>缪斯</span> 👍（8） 💬（1）<div>用户注册需要用到合并模式（不同客户端），购票过程需要用到过滤模式（对时间地点进行筛选过滤选票），提醒需要用到分离模式（进行不同渠道的分发提醒通知，如短信，电话等）。</div>2019-05-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epRUsrkh6HY63ia54D56zUWAKzBGibgUZ6ibgettorCuMYTF1VgwYKObvFjCuJia4DqLTxx9aRv5lYZRg/132" width="30px"><span>nuclear</span> 👍（5） 💬（1）<div>感觉合并模式可能会有问题，如果两个流有差速怎么办？</div>2019-06-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7k4uHp6TAAWGgfEhkVHYMK2gZegn9JJU14osmhpX8qibibsV0ff5aibZI4Mt89NlYnk09lAqiaRDNuCMXH5m5oqceA/132" width="30px"><span>linkzhang</span> 👍（3） 💬（1）<div>极客星球评论功能不好用啊（汗）
请问老师，看到很多回答里面都提到，提醒功能需要用到复制模式，但我理解只需要过滤和分离，过滤出需要提醒的用户后，如果一个用户需要多种方式通知，在分离的过程中是不是已经隐含了复制数据，不然上面的例子中，一个数据无法通过分离模式输入到两个处理模块</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f3/dc/80b0cd23.jpg" width="30px"><span>珅剑</span> 👍（1） 💬（1）<div>workflow是否只适用于批处理？</div>2019-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/78/23c56bce.jpg" width="30px"><span>james</span> 👍（1） 💬（2）<div>题目用mq可以搞定，没啥模式信手拈来</div>2019-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/49/28e73b9c.jpg" width="30px"><span>明翼</span> 👍（1） 💬（1）<div>注册如果多个系统对新用户都处理就复制，如果按照区域注册可能是分离模式，购买不知道是否有根据会员等级提供不同服务的如果有那就分离，买不同地方这个高并发先过滤到不同机器？至于通知，合并模式多个购买渠道信息合并一起通知所有用户</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f9/180f347a.jpg" width="30px"><span>朱同学</span> 👍（1） 💬（1）<div>如果用户从注册到购买到提醒是一个工作流的话，那么注册到购买是合并模式，因为并发的购买请求可能需要进入队列排队，到提醒的话，考虑到推送实时性，我会选择分类模式，如果系统按照整分钟推送，我会将未来几天的每分钟作为一个分类，下单处理完成后，我会把新的订单集合通过复制模式分发给不同的处理分支，推送只是其中的一个分支，推送提醒处理就是把订单分到以分钟为单位分类中，到了整分推送时间直接推送对应的分类即可。</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/ca/a379f032.jpg" width="30px"><span>长大的肚腩</span> 👍（0） 💬（1）<div>可能原始数据源的物理存储位置不同需要用合并模式，但如果针对这个注册的场景，不同渠道我们一般不用模式吧，直接一个canal同步数据库binlog日志到MQ就可以了吧。</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（0） 💬（1）<div>用户注册完之后，并不一定所有用户都马上买票，所有这里需要一个过滤模式过滤掉没有买票的用户；之后需要一个分离模式，根据用户出行时间分组，发送通知</div>2019-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d7/7e/6b6384e9.jpg" width="30px"><span>不贰过先生</span> 👍（0） 💬（1）<div>用户注册是会将用户信息用于多个不同的工作流属于复制模式；
购买机票：用户会根据自己要求查询特定时间和地点的机票这是过滤模式，买票完毕后会发生合并模式，即通过合并模式让可卖的总机票数减一；
出行前24小时提醒，用户可选择多种提醒方式的一种或多种属于分离模式。</div>2019-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/80/baddf03b.jpg" width="30px"><span>zhihai.tu</span> 👍（0） 💬（1）<div>1、用户注册：使用到了合并模式，系统需要整合网页端注册的用户以及手机端app注册的用户。
2、购买机票：使用到了分离模式，系统根据不同的用户等级，分离出来各个群体，针对不同群体提供不同的折扣力度。同样使用到了过滤模式，例如享有招行信用卡支付优惠2%。
3、出行前24小时提醒：使用到了分离模式，提供短信提醒、邮件提醒、电话提醒等服务。</div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f5/5f/217c6a14.jpg" width="30px"><span>Liu C.</span> 👍（0） 💬（1）<div>注册：合并模式，把用户合并起来储存
购票：分离模式，把用户按照机票分类，之后合并模式进行储存
24小时提醒：过滤模式过滤出需要提醒的用户，之后分离模式，按照所需的提醒方式分类提醒</div>2019-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/43/b89372d1.jpg" width="30px"><span>T</span> 👍（0） 💬（1）<div>注册～复制模式
购票～过滤模式
提醒～合并&#47;过滤模式</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e8/4a/c2a539a0.jpg" width="30px"><span>段斌</span> 👍（0） 💬（1）<div>用户注册（复制注册服务）-&gt;注册成功（过滤成功注册用户）-&gt;购买机票（合并购买动作）-&gt;购买机票成功（过滤成功购买用户）-&gt;出行前24小时提醒（分离提醒消息系统）

请元楠给个反馈，评估当前的认知是否正确</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/57/3ffdfc8d.jpg" width="30px"><span>vigo</span> 👍（5） 💬（0）<div>秦始皇统一六国过程中都使用什么模式！</div>2019-09-28</li><br/><li><img src="" width="30px"><span>潘腾</span> 👍（2） 💬（0）<div>就spark应用而言，过滤模式可以通过filter实现，

合并模式可以通过join实现。

至于复制模式，一般来讲一个rdd在后续处理中被多次使用到，应该就算是复制模式了吧，为了提高效率，可以使用persist持久化。

分离模式就是groupByKey吧。

这四种模式在spark中还有没有其他的实现方式呢？</div>2019-07-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7k4uHp6TAAWGgfEhkVHYMK2gZegn9JJU14osmhpX8qibibsV0ff5aibZI4Mt89NlYnk09lAqiaRDNuCMXH5m5oqceA/132" width="30px"><span>linkzhang</span> 👍（1） 💬（0）<div>请问老师，看到很多回答里面都提到，提醒功能需要用到复制模式，但我理解只需要过滤和分离模式，过滤出需要提醒的用户后，如果一个用户勾选了多种通知方式，在分离的过程是不是已经隐含了复制数据，不然前面例子中</div>2019-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/df/19/42e0ec30.jpg" width="30px"><span>罗鹏程</span> 👍（0） 💬（0）<div>1、看了下面的答案，有个核心问题是数据流输入是什么，我认为是用户在航空预定系统中的操作是数据源
2、用户会有很多行为，查看机票，登录、注册等行为，一份数据会有不同的操作，所以用户注册是复制模式
3、购买机票是在用户注册之后的行为，相当于是从用户中过滤出已经注册的，所以购买机票是过滤模式
4、出行前24小时的提醒，应该是机票数据的和购买机票用户进行合并关联，所以是合并模式</div>2024-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/9b/611e74ab.jpg" width="30px"><span>技术修行者</span> 👍（0） 💬（1）<div>看了大家的留言，感觉分析的好全面！

用户注册，考虑不同类型的接入端，使用合并模式。

购票，过滤模式加合并模式。

航班提醒，分类模式。</div>2020-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/63/21902253.jpg" width="30px"><span>Siping</span> 👍（0） 💬（0）<div>这个系列不错</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/96/4a7b7505.jpg" width="30px"><span>Eden2020</span> 👍（0） 💬（0）<div>过滤模式和分离模式，针对不同用户进行分离处理，分离前先过滤出不同用户</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/61/f6/1d6b548a.jpg" width="30px"><span>wang</span> 👍（0） 💬（0）<div>思考题：我的理解是，还是一个本质，数据集的来源，和数据集的去向去判断设计模式，用户注册的行为可以涉及到的数据集是一个实时首页的航班信息展示，那么是filter mode，从全量的航班信息数据集中找到当前时间段的满足需求的数据集， 购买机票可能涉及到就是某一个条件的数据集合展示，那么可以是filter mode，或者是正对一个相对全量的数据集合，进行多维度的分离，比如按照时间段的处理到一个数据集合，又或者按照价格处理到一个数据集，那么就是splitter mode， 出行前的24小时提醒，数据集来源是所有购买了票的用户，通过时间段的处理filter 到满足某一个时间前24小时这个条件的用户集合，然后进行提醒，这是filter mode，除此之外，对于join mode 的划分还是取决于是否有多个数据源集合的条件，比如一个航空系统的航班信息的设置，是需要收集各种维度的数据决定的，比如其他航空公司的路线数据，天气等数据，这些数据的某一些相同的维度可以join 进行设置该系统的航班信息。</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8f/35/f1839bb2.jpg" width="30px"><span>风中花</span> 👍（0） 💬（0）<div>老师这么一分析，我们这个机票预定流程。就包含了四种模式。真是仔细一想，还就是这个模式。不学习，永远不知道有这样的模式，我们一直在走着这样的模式。真是生在模式中不知模式。</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8f/35/f1839bb2.jpg" width="30px"><span>风中花</span> 👍（0） 💬（0）<div>看来同学们得分析，确实学到了！ 购买机票 过程是登录-&gt;验证有效性-&gt;查询 -&gt; 选择-&gt;验证选择-验证用户有效性-&gt;购买 结束 。 登录和验证 就是一个过滤   查询 就是一个先复制 因为一份查询到多个平台拿数据。其次过滤 在合并 返回给用户  。用户选择如果不同平台数据必将涉及一个 多平台得预定 所以有一个 数据分离到不同平台预定 然后返回合并返回给用户。机票预定我想也就这么多流程了，至少现在我们现在是这样的，哈哈</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/71/9273e8a4.jpg" width="30px"><span>时间是最真的答案</span> 👍（0） 💬（0）<div>出行前24小时的提醒用到了过滤模式</div>2019-05-01</li><br/>
</ul>