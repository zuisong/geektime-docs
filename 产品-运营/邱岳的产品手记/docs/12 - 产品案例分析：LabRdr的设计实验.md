LabRdr是一个非常精巧的新闻阅读应用，它是由卫报的移动创新实验室负责设计和研发的。它和我之前介绍的卫报客户端属于同一东家，不同的是，LabRdr是一个完全实验性的产品。

**从用户场景出发，贴着场景设计产品**

在第一次使用这款应用的时候，LabRdr 会问你几个问题。第一个问题是你早晚的通勤开始时间，也就是上班时间和下班时间；第二个问题是问，你花在早晚通勤上的时间长度，你可以分别作出选择。在此之后，LabRdr 会根据你的选择，为你挑选适合你通勤长度的文章集合，在你每天早晨和晚上通勤开始的时候推送给你。

在这里，LabRdr 有一个有趣的特性，就是它的文章同步是在后台进行的。这应对的是一个什么样的场景呢：我们出门坐地铁或者其他交通工具，手机有可能会没有信号。这时我们一般会在上地铁之前先打开离线一些数据，然后在地铁上读；LabRdr在后台同步的功能就会离线下载，用户也就无需打开应用手动下载。

这是LabRdr整个的设计起点。就像我在之前分享 Hopper 的时候提到，越来越多的产品在改变自己的设计起点，产品不再从我们有什么出发，而是从用户需要和用户场景出发。LabRdr就是这样，它不是将大量的新闻分类排序，和盘托出摆在用户面前；而是去理解用户阅读新闻的场景，从场景里面长出功能。

我们可以看到 Labrdr 上的文章并不会一直保留。当一天过去后，这一天文章集合就会消失不见，这跟传统的新闻客户端永无止境拉不到头的时间线形成了鲜明的对比。

这个设计跟我们做的 Readhub 有些类似，我们不希望对用户来说，信息是无尽的，它只会让用户消耗更多无意义的时间，并陷入到信息焦虑中。
<div><strong>精选留言（19）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/8b/38b93ca0.jpg" width="30px"><span>听天由己</span> 👍（15） 💬（1）<div>交易思维非常赞，无论是产品与用户的关系还是人际关系，这本身就是一条亘古不变的原则。我们总是想着用户能给我带来什么价值，很多时候缺乏同理心，也就顾不得每次的提示或是互动反馈了。这在产品初期非常考验产品经理的能力。

现在越来越多的产品都做得有人情味，当然前提条件还是产品本身是能够满足用户的基本需求，并且符合用户的使用习惯，在「即刻」上学习了不少。

关于收集用户数据，目前使用的 Gyroscope 就是典型案例，从各个渠道获得的数据都有清晰的指示与说明，对于分享或是与用户的互动做的很棒。</div>2017-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/8f/68bde1af.jpg" width="30px"><span>Milk喝了牛奶</span> 👍（8） 💬（1）<div>看到上面的留言，想补充一下，从推荐引擎的角度来看，播放&#47;阅读完成度，播放&#47;阅读时长指标优化可以很好地降低误点的影响，推荐系统不会有太大的bias. 目前在我自己负责的百万级日活产品上是也是这么验证的。不过如果训练数据少，bias肯定会比较大。</div>2018-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/91/1a/c7c62da3.jpg" width="30px"><span>文</span> 👍（5） 💬（1）<div>我之前就有想过，现在国内各种软件的push信息，各种没有用，用户甚至都不想看到，结果就是把权限关闭，我考虑一个事，如果不是绝对必要的请求，用户打开第一次时，都不提醒（避免第一时间就被用户关闭），直到需要这个功能的权限时提醒，包括运营的push如果滥用的话，导致用户关闭该权限时，就得不偿失了。</div>2018-01-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/13/e82a6582.jpg" width="30px"><span>张星彩</span> 👍（4） 💬（1）<div>zaker新闻，每刷新一次，都会有10多条更新内容，你觉得信息流产品是有节制的给用户推荐内容比较好，还是只要用户刷新，不管刷新多少次都给用户推荐更新的内容。</div>2017-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/94/04/c3bd4db4.jpg" width="30px"><span>一只企鹅</span> 👍（4） 💬（2）<div>如果是误点的话   阅读时间就会比较短  合理的算法应该可以识别出这类阅读时间异常短的情况吧</div>2017-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/e6/87197b10.jpg" width="30px"><span>GeekAmI</span> 👍（3） 💬（1）<div>很好奇二爷如何发现这些APP的</div>2017-12-20</li><br/><li><img src="" width="30px"><span>Geek_1264b9</span> 👍（0） 💬（2）<div>labRdr国内的Appstore搜索不到，是没法下载吗？</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/11/4261c1e6.jpg" width="30px"><span>幼儿园学霸</span> 👍（2） 💬（0）<div>感觉可以用人性化一词来形容这款APP，无论深揪十分细小场景的功能设计，还是用户数据的透明化收录，或者是交易性思维，都能够感受到这款APP都在从用户的角度（使用场景、用户心理、用户价值感知）来设计和思考产品的功能设计，使得产品更有温度。有温度的产品更容易得人心吧。
想想国内的产品网易云音乐、即刻、一罐等APP之所以会获得较多的“死忠粉”，都是因为产品本身都十分的具有“温度性”。</div>2018-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/94/ee/8451dfc4.jpg" width="30px"><span>Dylan</span> 👍（2） 💬（0）<div>“价值高于用户对于自己所付出资源的成本预期”这个衡量标准说的特别好。用过太多app，初次打开就跳出一堆请求权限的弹窗。即便点了确定，也触发了用户的防御机制，原因在于这些权限出现的时机不精准，也没有展示用户价值。所以在潜意识里，用户对这种请求行为一般都是抵制的。
其实简单的设计就是在需要调用通讯录的时候请求，初次进行地理定位时请求，诸如此类设计，开发成本低，用户体验也好。
好的设计，从不为难用户。</div>2018-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d9/ac/26ada7b8.jpg" width="30px"><span>强劲九</span> 👍（1） 💬（0）<div>对于同一个应用，产品经理和技术人员所看到的就是很不一样的角度，产品经理要更加敏感，去思考这个应用中的各个功能为何这样设置，不同的功能为何要让其存在。</div>2021-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f9/d7/1616ece6.jpg" width="30px"><span>猪猪娜</span> 👍（1） 💬（1）<div>这款软件最让我觉得有特点的地方是，用户数据透明化，并且用户可以编辑自己的阅读数据，这样可以更加准确推测用户的阅读习惯和兴趣，这比优化算法系统等，效率更高。</div>2018-10-07</li><br/><li><img src="" width="30px"><span>方薇</span> 👍（0） 💬（0）<div>非常好</div>2022-10-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e2/4c/2c2704b0.jpg" width="30px"><span>马辉</span> 👍（0） 💬（0）<div>原则：仅当我们提供的利益比它的投入要大时，才有意义，才合理。
用户付出了时间或注意力甚至金钱，必须要说清楚，我们提供了什么，明示、暗示。
即使是一次与用户交互，都是一次交易，确保我们站在用户角度，解决了问题或提供了价值。
这样会发现，很多多余的点击是没有意义的，很多复杂的设置功能是没有意义的，很多是我们想让用户而不是用户想要的东西是没有意义的</div>2021-04-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM5KDGy7tfCLQ22iamneeYsnIy3KO8lJq9CusURib9rHIeeuN9M4gXGsOyggdogLkNZufH1ytyYpQYfw/132" width="30px"><span>Geek_d79502</span> 👍（0） 💬（0）<div>在后台被杀死了怎么办呢？iOS不会让程序活过20分钟吧，他是怎么做到的？</div>2021-03-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/41/9113d93f.jpg" width="30px"><span>悟空来 |  Arthur李华栋  |  👍</span> 👍（0） 💬（0）<div>体会到你们的用心</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/fa/da/423873f6.jpg" width="30px"><span>Rui</span> 👍（0） 💬（0）<div>删log让我感觉是在改库啊，这种操作风险会很高吧，加标签倒是可以</div>2020-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/66/11/f7408e3e.jpg" width="30px"><span>云师兄</span> 👍（0） 💬（0）<div>贴着场景设计，让功能从场景里长出来
告知用户收集数据的目的
以交易思维设计每次互动</div>2019-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/7e/c38ac02f.jpg" width="30px"><span>北冥Master</span> 👍（0） 💬（0）<div>这个app中国市场搜不到？</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/79/7e/c38ac02f.jpg" width="30px"><span>北冥Master</span> 👍（0） 💬（0）<div>这个app中国市场搜不到？</div>2018-11-29</li><br/>
</ul>