你好，我是黄佳。

今天我们正式进入“业务场景闯关篇”模块。我在开篇词中介绍过，在这个模块中，我会围绕电商场景下的运营环节，带你挑战5个关卡：获客关、变现关、激活关、留存关和裂变关，帮你逐步掌握机器学习的相关知识和实操技巧。今天，我们就从第一关“获客关”开始！

![](https://static001.geekbang.org/resource/image/76/08/76466435764dc810ab26d93a8a2b5a08.jpg?wh=2284x1033)

人们常说移动互联网的运营已经进入了下半场，几乎所有的企业都希望能用更优质的产品和更精准的服务留住用户，这就需要制定出合适的获客策略。而要做到这一点，前提就是为用户精准画像，也就是根据用户的人口统计信息和消费行为数据，给用户分组，然后推测出用户的消费习惯和价值高低。

所以，为用户分组、画像，找到不同用户的特点，进而挖掘出哪些才是最有价值的用户，是目前互联网大厂中的数据分析师和机器学习工程师常做的工作。既然如此，那么我们就在获客关，结合一个具体的电商项目，来看看怎么根据用户的基本信息和消费行为数据，给用户分组画像。

# 定义问题

按照我们前两讲所说的机器学习“实战5步”，我们首先要做的就是，把项目的问题定义清楚。在我们这个项目中，你可以想象自己就职于一家名为“易速鲜花”的创业公司，担任这家公司的运营团队机器学习工程师。你现在要接手的第一个项目就是为公司的用户分组画像。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/23/bb/a1a61f7c.jpg" width="30px"><span>GAC·DU</span> 👍（15） 💬（2）<div>上班偷偷摸鱼，把老师分享的课程由粗到细品味了三遍，老师不仅技术高超，运营也这么牛，真是望尘莫及，在没订阅课程之前，我一点运营的知识都没有，看完今天的课程感觉自己又可以了。聊下老师的思考题，我想起当年的瑞幸和滴滴就这么搞的，通过下载APP注册，发送大量的消费券，获取很多的用户。然后经过时间的沉淀，利用RFM技术对用户进行分组，对于用户粘性较高的，进行精细化推荐。对于用户粘性较低的，发送消费券，进行召回用户。对于用户关系管理，可以把R理解为最近一次见面的时间，F理解为多长时间见一次面，M理解为见面聊天的深度，如果只是say hi， 那M的值很低，如果是畅谈人生，M值就会很高。

群里老师说把解决google colab中文乱码的方法分享出来，我说一下大概的思路，然后我会在最后根据本次课程的代码分享测试地址(需要科学上网访问)。

首先是下载你喜欢的中文字体，然后通过FontProperties来指定你下载的字体和展示大小，最后在需要展示中文的地方进行调用。
https:&#47;&#47;colab.research.google.com&#47;drive&#47;1EuXud71LiM6QsNIA9hsCeOlMiyrB6zLV?usp=sharing</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/77/95/0d10d4b2.jpg" width="30px"><span>茜茜</span> 👍（14） 💬（3）<div>我觉得RFM适用于高频交易的场景，如零售，不适用于低频交易场景，如赛事演出票务。通过RFM将可以用户分为高中低等价值用户，在需要对某些产品进行营销推广时，可以将高价值用户定为主要营销群体，从而获得更高的订单转化率。但在计算RFM时，可能会面临以下问题：1.用户id与用户并不是一一对应或用户id不统一：如用户有多个账号，或者是多人使用该用户的id发生购买行为，或者部分消费记录未记入该用户，通过的RFM值无法真实反应用户的消费情况。2.关于F值：对于耐用性高的商品，可能一年就买一次，这时可以去掉F值里的时间限制，用该用户累计购买值代替。最后我的感悟是：模型只是基础，不能直接套用，需要结合相应业务场景对模型进行不同程度的修正，来满足业务运营的目标。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/43/13/649ccaa9.jpg" width="30px"><span>海林Lin</span> 👍（9） 💬（2）<div>课程很有收获，有个问题请教老师，为什么说RFM分析能够应用在获客环节呢，个人理解这个时候往往没有用户的行为数据</div>2021-09-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLgWP0AWxax7DR8zh7Pd1U8UqzX4lAlkvMGCBgAOzpnvpgD1FxLwqQoH3T5vVcd7j8RRdpETjPB1w/132" width="30px"><span>Geek_80f43d</span> 👍（8） 💬（1）<div>近度不应该是datetime.now()和最近一次的消费时间差值吗</div>2021-11-16</li><br/><li><img src="" width="30px"><span>yk</span> 👍（4） 💬（2）<div>佳哥好，有个问题，现在例子的数据集都比较小，如果是上亿的数据，也是这么处理吗？全加载到内存会不会很大。</div>2022-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f5/73/f7d3a996.jpg" width="30px"><span>！null</span> 👍（2） 💬（1）<div>对于实战课，手不能懒，得敲一下熟练熟练。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/89/50/aee9fdab.jpg" width="30px"><span>小杰</span> 👍（1） 💬（1）<div>比如客服，针对不同的用户，推送不同的内容，针对R最新消费的时间越短的用户，可以推送更多的新品；针对F消费频率高的用户：可以推送更多的优惠；针对M消费金额高的用户：可以推送更高质量的商品。最后推荐搭大家走一遍代码流程，具体细节可以不用关注，老师说了，代码是很简单的，要知道如何分析，处理，提取数据，这个才是重点</div>2023-02-12</li><br/><li><img src="" width="30px"><span>Geek_ro</span> 👍（1） 💬（2）<div>F值为什么不是订单号的unique数？这里单纯对消费日期计数的话不会导致重复计数吗？</div>2022-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/51/9b/ccea47d9.jpg" width="30px"><span>安迪密恩</span> 👍（1） 💬（1）<div>业务场景：大数据杀熟。</div>2022-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/66/8f/02be926d.jpg" width="30px"><span>在路上</span> 👍（1） 💬（2）<div>佳哥好，看到github上更新了这节课的最新代码，非常开心，这对于我这种初次接触Jupyter和Python的学员来说太重要了，调试非常方便。
RFM 模型是我今天学到的新知识，F代表行为的频率，M代表行为的程度，如果行为是消费，M就是消费金额，如果行为是充值，M就是充值金额，F和M是行为的两个特征，就像我们用振频和振幅来描述振动的特征。R代表行为最近发生的时间，RFM从不同维度描述了一个行为，当然具体的行为可能还能找到特殊的特征。
把行为量化成数值，就可以根据数据聚类，大部分行为都会呈现28分布，就像80%的性能问题是20%的代码引起的，而真正的原因往往出乎你的预料，所以通过聚类可以让我们认识到事先想不到的问题。</div>2021-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bf/6f/1916fba0.jpg" width="30px"><span>贝贝</span> 👍（0） 💬（1）<div>拉了几行数据，终于明白这里R值的求解意思....orz df_recent_buy[&#39;最近日期&#39;].max()是指最近日期这一列的最大值，也就是最近的一天。df_recent_buy[&#39;最近日期&#39;]是每一个用户上次购买的日期。  实际使用中大概应该使用   datetime.now() -     df_recent_buy[&#39;最近日期&#39;]， 但是因为历史数据，now每次都变，    df_recent_buy[&#39;最近日期&#39;]  确实不变的，会导致每次跑数据R值都不一样，所以用了max吧
        用户码	最近日期	R	R_max	R_latest
0	14681	2021-03-30 15:52:00	70	2021-06-09 12:31:00	2021-03-30 15:52:00
1	14682	2020-12-04 12:12:00	187	2021-06-09 12:31:00	2020-12-04 12:12:00
2	14684	2021-05-15 11:33:00	25	2021-06-09 12:31:00	2021-05-15 11:33:00
3	14687	2021-02-23 11:59:00	106	2021-06-09 12:31:00	2021-02-23 11:59:00
4	14688	2021-06-02 12:26:00	7	2021-06-09 12:31:00	2021-06-02 12:26:00</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bf/6f/1916fba0.jpg" width="30px"><span>贝贝</span> 👍（0） 💬（1）<div>用户码	最近日期	R	R_max	R_latest
0	14681	2021-03-30 15:52:00	70	2021-06-09 12:31:00	2021-03-30 15:52:00
1	14682	2020-12-04 12:12:00	187	2021-06-09 12:31:00	2020-12-04 12:12:00
2	14684	2021-05-15 11:33:00	25	2021-06-09 12:31:00	2021-05-15 11:33:00
3	14687	2021-02-23 11:59:00	106	2021-06-09 12:31:00	2021-02-23 11:59:00
4	14688	2021-06-02 12:26:00	7	2021-06-09 12:31:00	2021-06-02 12:26:00</div>2024-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/1f/95/42f7ea8d.jpg" width="30px"><span>honmio</span> 👍（0） 💬（1）<div>哪位可以共享一下测试数据呢？ github上的文件已经无法下载了，先行谢过</div>2024-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/4f/61/018352d4.jpg" width="30px"><span>静静呀</span> 👍（0） 💬（1）<div>一千多行负数，有没有可能是退货呢？属于正常数据</div>2023-11-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJicdicz5mZgj4VMPSe8iaUyia4zAZUCsddKewJX6XAZS70TsTNZ4icibUQk5kEicRdTXXGKaGTkVFnVstA/132" width="30px"><span>Geek_5b6270</span> 👍（0） 💬（1）<div>文件下载不了了</div>2023-01-31</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKJicdicz5mZgj4VMPSe8iaUyia4zAZUCsddKewJX6XAZS70TsTNZ4icibUQk5kEicRdTXXGKaGTkVFnVstA/132" width="30px"><span>Geek_5b6270</span> 👍（0） 💬（1）<div>大数据量怎么处理的，不可能都放内存里搞吧？</div>2022-11-01</li><br/><li><img src="" width="30px"><span>Geek_fc90ae</span> 👍（0） 💬（3）<div>df_recent_buy[&#39;R值&#39;] = (df_recent_buy[&#39;最近日期&#39;].max() - df_recent_buy[&#39;最近日期&#39;]).dt.days
老师这个有点不太明白，df_recent_buy数据表里保存的最新日期了，如何知道上一次消费的日期</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/56/5f/99c924f7.jpg" width="30px"><span>左超文</span> 👍（0） 💬（1）<div>这个下载的数据为什么和第四关的是一样的
</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d3/89/fcf95d32.jpg" width="30px"><span>Allen</span> 👍（0） 💬（1）<div>老师，关于例子中最后一条的数据，demo里执行的结果是
4	14688	7	324	5579.10
和文章中的M值不一样</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/97/035a237b.jpg" width="30px"><span>Jove</span> 👍（0） 💬（1）<div>RFM 模型感觉也可以运用到更多的场景，假设我要针对的是一群没有开通会员的用户，来提高付费率。
那么这里的 R 记忆强度；F 忠诚度；M 在这里就没有金额，或者说可以用用户的地理位置和手机型号等来代替。
按重要程度来看 F &gt; R &gt; M，也就是不同场景下，各自的权重是不一样的。</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9e/20/3de4b71d.jpg" width="30px"><span>timothywei</span> 👍（0） 💬（1）<div>催更了，期待继续更新</div>2021-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/6a/74/c39efead.jpg" width="30px"><span>吴悦</span> 👍（0） 💬（1）<div>正好 最近在做这个RFM模型  ，期待后面的聚类模式是怎么处理的 </div>2021-09-08</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKoV0ufI5riaUyWXZWgCX2FQlibc71VGwnxROTbickvhw2IUKFYIcf0VhDcibE0AEIgx8rJicRQ8vnnN9g/132" width="30px"><span>梦浩然</span> 👍（0） 💬（0）<div>R：最近有没有想我
F:   是天天想我吗？
M:  很想我吗？</div>2024-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/cb/680635e2.jpg" width="30px"><span>wiki</span> 👍（0） 💬（0）<div>df_recent_buy[&#39;R值&#39;] = (df_recent_buy[&#39;最近日期&#39;].max() - df_recent_buy[&#39;最近日期&#39;]).dt.days #计算最新日期与上次消费日期的天数
这里R值的计算，不应该是最后一次消费时间和当前时间的差值吗。这里是不是有点问题呢</div>2024-08-01</li><br/>
</ul>