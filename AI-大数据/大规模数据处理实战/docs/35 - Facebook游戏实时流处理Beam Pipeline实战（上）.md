你好，我是蔡元楠。

今天我要与你分享的主题是“Facebook游戏实时流处理Beam Pipeline实战”。

Facebook这个社交平台我相信你一定早有耳闻。它除了能够让用户发送消息给好友，分享自己的动态图片和视频之外，还通过自身的App Center管理着各式各样的小游戏。许多游戏开发商借助Facebook的好友邀请机制让自己的App火了一把。

曾经有一段时间，在Facebook上有一款名为糖果传奇（Candy Crush Saga）的游戏风靡了整个北美。各个年龄层的玩家都会在空闲的时间拿出手机，过五关斩六将，希望尽快突破更多的关卡，并且获得高分。

![](https://static001.geekbang.org/resource/image/01/68/01d81679dc22a2049f81de1622532d68.png?wh=1920%2A1189)

当然了，除了消除游戏本身带来的乐趣以外，可以在Facebook里和自己的好友进行积分排名比拼也是另外一个能吸引用户的地方。

![](https://static001.geekbang.org/resource/image/97/6e/971c3a60862a448bedfc0676103bf36e.png?wh=1500%2A1254)

想要一个类似Facebook这样的好友间积分排行榜，你可以有很多种实现方式以及各种优化方法。那么，如果我们要利用Apache Beam的话，该怎样实现一个类似的游戏积分排行榜呢？

今天我就来和你一起研究，要如何利用Apache Beam的数据流水线来实现一个我们自定义的简单游戏积分排行榜。

为了简化整个游戏积分排行榜案例的说明，我们先来做几个方面的假设：
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJDhZkQGEnzjnu3dibxbRiblWIUjXXrXic0MStUS2ApKt5WiaoxV3IVhAtSXkknODA9oibick3NHic4Frzfw/0" width="30px"><span>suncar</span> 👍（13） 💬（0）<div>老师您好，请问一下可不可以将这种案例放一份到github上。我们可以拉到本地进行调试。在这个过程中避免不了出现各种异常，以方便更好的解决和深入了解。谢谢</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a0/f4/7e122a67.jpg" width="30px"><span>之渊</span> 👍（1） 💬（0）<div>源码https:&#47;&#47;gitee.com&#47;oumin12345&#47;daimademojihe&#47;tree&#47;master&#47;cloudx&#47;bigdata&#47;src&#47;main&#47;java&#47;test&#47;beam&#47;facebook
新手先自己试着写出来。再参考。这样才是实战啊，毕竟工作是没有抄的</div>2020-08-24</li><br/><li><img src="" width="30px"><span>Fiery</span> 👍（0） 💬（0）<div>第一个问题是，为什么pipeline里面没有针对每个关卡的aggregation？难道默认只处理一个关卡吗？那candy crush有好几百的关卡，总不能每一个关卡单独copy一份这样的代码吧？！
第二个问题是，在第5步的Composite Transform中，用Top Transform算出每个用户的Top score，输出难道不应该是PCollection&lt;KV&lt;string, long&gt;&gt;吗（Key是user id，Value是score）？而且既然已经用Top得到了每个用户的最高分，直接针对这个PCollection&lt;KV&lt;string, long&gt;&gt;进行第二次Top Transform不就能得到前100名用户的ID的分数了？为什么还要多一个中间转换产生PCollection&lt;KV&lt;string, UserScoreInfo&gt;&gt;呢？</div>2020-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/61/f6/1d6b548a.jpg" width="30px"><span>wang</span> 👍（0） 💬（0）<div>思考题：窗口值也就是事件处理阶段=》startBoundary 和 endBoundary 的值 
 触发器也就是计算触发的时间=》30min 一个点
累加模式=》丢弃</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/77/5c/8d53165e.jpg" width="30px"><span>bingo</span> 👍（0） 💬（0）<div>老师你好，我有个疑问。这里的用户数据可不可以全部放在Hbase里。
由于好友之间的排名查询涉及的数据量少，所以直接查询Hbase。而全局的总排名要涉及到所有的玩家，数据量大，这个使用流水线处理</div>2019-09-21</li><br/>
</ul>