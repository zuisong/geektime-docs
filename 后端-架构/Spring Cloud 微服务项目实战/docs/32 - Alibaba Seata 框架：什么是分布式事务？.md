我第一次被问及分布式事务，是在一次面试的终面环节。多年以后，面对形形色色的面试者，我总会回想起畅谈分布式方案的那个遥远的下午。

彼时的打工人还没从996 PUA的福报催眠中觉醒，无人制裁的大厂喜欢肆无忌惮地将面试安排在周末，似乎从面试的那一刻开始，996的节奏就被它们演绎得像呼吸一样自然。在一个周六的下午我来到了约定的面试地点。

“有没有做过分布式事务？”刚和面试官对上线，他就迎面甩我一个大招。

“做过！”我的回答像古龙小说一样惜字如金。但我大概能猜到他想听的完美答案，八成就是**阿里系自研的分布式事务框架**。

“说说是怎么实现分布式事务的。”为了让一个答案变得有层次，我计划从三个阶段来回答这个问题：一个擦边球答案、一个正确但不完美的答案、一个超出预期的答案。如果用一部舞台剧来形容这三个阶段，那么就是“前戏、正戏、高潮”。

与这三个阶段相对应的话术，分别是“本地事务、传统的分布式事务、阿里系Seata分布式事务”，从平淡无奇到羽化而登仙。

## 一场前戏

“大部分传统公司的业务还是构建在单体应用集群之上，说白了，就是一种伪分布式的应用，事务在应用上下文中传播。”我先抛出了一个擦边球答案作为前戏，前戏宜速战速决不宜恋战，只为铺垫第二阶段的正戏。
<div><strong>精选留言（14）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2c/97/9d/9fe599dc.jpg" width="30px"><span>Heaven＇s Fall</span> 👍（12） 💬（2）<div>老师，我想问一下
我们传统的服务间调用可以通过调用服务失败了使用本地事务回滚业务（比如服务A调用服务B，服务B失败了我们可以在服务A上回滚业务，然后再向上游报告业务失败。。。）
使用消息队列的情况也可以使用事务型消息保证一致性
为啥还需要这样一个分布式事务的框架增加系统的复杂度呢？</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cb/df/e72646dd.jpg" width="30px"><span>多喝热水</span> 👍（7） 💬（2）<div>讲的真好，生怕哪天这节就不见了😂😂😂</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（5） 💬（1）<div>老师面试套路深啊！</div>2022-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/6d/19/204b0900.jpg" width="30px"><span>Black Jack</span> 👍（2） 💬（1）<div>老师，看起来心情不错啊</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/0e/0c/4ec2075f.jpg" width="30px"><span>薛定谔的疯兔子</span> 👍（2） 💬（1）<div>哈哈 老师说话贼有意思</div>2022-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2f/ea/a5173a49.jpg" width="30px"><span>说话的鱼</span> 👍（1） 💬（1）<div>这节课真的是风趣，有古龙小说语言风范</div>2022-06-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ6Gia1LtqJmDNlFqdd07hibCibY5z8DSoXd8c639Libe5LC3xtuEzzaeicjGCuv2F5IYDZhGxNrukVogg/132" width="30px"><span>Lonely_ZJ</span> 👍（1） 💬（1）<div>百年孤独式的开头太有喜感啦~</div>2022-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师两个问题：
Q1：MySQL只有InnoDB引擎支持XA协议吗？
文中有这样一句：“DB 这层首先得要实现 XA 协议。比如 Oracle XA 和 MySQL InnoDB，都是支持 XA 协议的数据库方案。”。
MySQL支持多种存储引擎，从这句话看，似乎只有InnoDB支持XA协议了，是吗？
Q2：2PC方案中，如果commit阶段出现问题，会是什么结果？如果有问题怎么解决？</div>2022-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ea/b7/1a18a39d.jpg" width="30px"><span>5-刘新波(Arvin)</span> 👍（0） 💬（0）<div>太精彩了！</div>2024-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/fe/04/bb427e47.jpg" width="30px"><span>码哥字节</span> 👍（0） 💬（0）<div>放飞自我的写法</div>2023-09-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/GkMk4gBlfZcljsY3Vqu7w6GM4qd7QjEy4X6c25jdtEowhjyTzOeIBDFXYcleXmfF1qFicaI8gz5k2TkUgvAYibNQ/132" width="30px"><span>杨妞</span> 👍（0） 💬（0）<div>这一讲看的我酣畅淋漓</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/db/e5/26c2f7de.jpg" width="30px"><span>奔跑的小黄牛</span> 👍（0） 💬（0）<div>自己看书有些知识点看不懂，看老师的文章一下就懂了。</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0a/e9/6fad9109.jpg" width="30px"><span>宁静志远</span> 👍（0） 💬（0）<div>讲的很好啊，有趣，有料</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/f7/ba/08044ec3.jpg" width="30px"><span>张平</span> 👍（0） 💬（0）<div>有点讲评书的感觉，非常不错；</div>2022-03-16</li><br/>
</ul>