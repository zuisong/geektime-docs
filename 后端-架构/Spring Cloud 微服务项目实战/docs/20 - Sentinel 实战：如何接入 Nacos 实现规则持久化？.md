你好，我是姚秋辰。

在前两节课里，我们已经知道了如何配置Sentinel的降级规则和流量整形规则。不过这套方案还有一个不完美的地方。因为我们配置的这些容错规则并没有被“保存”到某个存储介质中，所以，如果你重新启动Sentinel服务器或者重启应用程序，先前配置的所有规则就都消失不见了。那如何才能解决这个问题呢？

这节课，我将带你对Sentinel的源码做一下二次开发，我们将通过集成Nacos Config来实现一套持久化方案，把Sentinel中设置的限流规则保存到Nacos配置中心。这样一来，当应用服务或Sentinel Dashboard重新启动时，它们就可以自动把Nacos中的限流规则同步到本地，不管怎么重启服务都不会导致规则失效了。

在前两节课的实战环节，我们采取了一种“直连”的方式，将应用程序和Sentinel做了直接集成。在我们引入Nacos Config之后，现有的集成方式会发生些许的变化，我画了一幅图来帮你从架构层面理解新的对接方式。

![图片](https://static001.geekbang.org/resource/image/4e/03/4e037301de04504f4d005f3babef9603.jpg?wh=1920x645)

从上面的图中，你会发现，Sentinel控制台将限流规则同步到了Nacos Config服务器来实现持久化。同时，在应用程序中，我们配置了一个Sentinel Datasource，从Nacos Config服务器获取具体配置信息。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/29/cc30bd9d.jpg" width="30px"><span>逝影落枫</span> 👍（21） 💬（1）<div>为何对接数据源，不采用启动组件的方式，要改代码这么low的？如何做平滑升级？</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ce/d7/074920d5.jpg" width="30px"><span>小飞同学</span> 👍（5） 💬（1）<div>为啥官方不提供可配置化的数据源，就像nacos那样？提供一个规则配置导出的工具也行，开源项目写的这么low不合适把(改dashborad后端代码-从test目录下复制文件,修改前端这么折腾)，应该提一个issue</div>2022-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/d7/31d07471.jpg" width="30px"><span>牛年榴莲</span> 👍（4） 💬（1）<div>小团队技术选型基本可以放弃这个组件了</div>2022-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/2a/b0/f72ee91c.jpg" width="30px"><span>来来</span> 👍（2） 💬（2）<div>老师，经过以上改造后，是不是也可以在nacos中直接修改coupon-customer-serv-flow-rules配置，达到限流的效果，而不要再经过Sentinel 控制台操作</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/11/29/23b1f889.jpg" width="30px"><span>永恒之蓝</span> 👍（1） 💬（1）<div>有没有改造1.8.2版本成功的老哥，我改造sidebar.html无法生效，对angular不是很熟悉，这个前端代码是要编译并打包之后才生效是么？这个问题排查了很久还是没有找到解决问题办法。</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>Q1：微服务为什么要从nacos获取sentinel的配置信息?
A在前面的18、19篇中，微服务已经通过注解实现了与sentinel的绑定，并不需要获取流控规则（这句话如果错误，则为“已经能从sentinel获取流控规则”）。现在sentinel集成nacos后，为什么要从nacos获取规则配置信息？
B 另外，sentinel没有与nacos集成时，微服务需要从sentinel获取规则配置信息吗？如需要，怎么获取的？
Q2：sentinel规则可以保存到其他组件吗？
Sentinel的规则，除了可以保存到nacos中外，还可以保存到其他组件吗？比如zookeeper，比如redis，比如RocketMQ。
Q3：最新的sentinel1.8.3编译失败？
我是从官网下载的最新1.8.3版本，导入idean2019，按照老师第20篇的步骤修改代码，然后编译，但编译失败了。
sentinel-adapter模块下的“sentinel-grpc-adapter”下面，
src&#47;test&#47;FooServiceClient.java报告错误：Error:(18, 49) java: 程序包com.alibaba.csp.sentinel.adapter.grpc.gen不存在，
此文件中，导入grpc.gen失败，&quot;gen&quot;在idea中为红色字体。
import com.alibaba.csp.sentinel.adapter.grpc.gen.FooRequest;
官网下载的，应该是完整的，怎么会报错呢？该怎么解决？</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/a4/8d/5347f90a.jpg" width="30px"><span>Keke</span> 👍（0） 💬（1）<div>为什么我的nacos里没有生成配置文件呢？但是重启项目后配置的规则都还在</div>2023-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d9/31/22fc55ea.jpg" width="30px"><span>Believe</span> 👍（0） 💬（4）<div>很多plugins都下不下来，还存在很多依赖包都下不下来</div>2022-11-23</li><br/><li><img src="" width="30px"><span>郭井阳</span> 👍（0） 💬（1）<div>geekbang-flow 这个数据库key怎么对应的</div>2022-06-14</li><br/><li><img src="" width="30px"><span>郭井阳</span> 👍（0） 💬（1）<div>datasource: # 数据源的key，可以自由命名 geekbang-flow: 这个值是怎么取值的</div>2022-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/e7/495068f6.jpg" width="30px"><span>文艺码农</span> 👍（0） 💬（1）<div>程序包io.envoyproxy.envoy.api.v2.ratelimit不存在</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1f/e7/495068f6.jpg" width="30px"><span>文艺码农</span> 👍（0） 💬（1）<div>请问大家都没有碰到缺少依赖的情况吗? 使用阿里云镜像仓库了,好像还是拉取不到 :</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a8/9c/643646b9.jpg" width="30px"><span>wake</span> 👍（0） 💬（2）<div>&lt;li ui-sref-active=&quot;active&quot; ng-if=&quot;!entry.isGateway&quot;&gt;
            &lt;a ui-sref=&quot;dashboard.flow({app: entry.app})&quot;&gt;
              &lt;i class=&quot;glyphicon glyphicon-filter&quot;&gt;&lt;&#47;i&gt;&amp;nbsp;&amp;nbsp;流控规则 极客时间改造&lt;&#47;a&gt;
          &lt;&#47;li&gt;

不太懂前端，但是我不加ng-if=&quot;!entry.isGateway&quot;的话，导航栏显示不出来新的流控规则菜单</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3e/29/cc30bd9d.jpg" width="30px"><span>逝影落枫</span> 👍（0） 💬（1）<div>老师，sentinel端的FlowControllerV2改造后，是否还涉及FlowServiceV2的改造？同时，新增的标签页改为dashboard.flow调用，是调用到FlowControllerV2上吗？对应的JS调用，是否也有改动？</div>2022-01-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/4VCgcBbU51SiasW8tpjYwdqBGe2RNIy6neuI7AEjCQ6t9qqXw6tXpZ2bDCoxJhWqQJv2LlFmemVYJCrLze2Aa7g/132" width="30px"><span>beatdrug</span> 👍（1） 💬（0）<div>熔断的话，后端要实现一个degradecontrollerV2，里面内容可以参考限流的，然后就是前端在sidebar文件新增一个标签li，后面需要在app.js中添加state，还要新增一个熔断页面文件这个可以参考现有的熔断页面</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/c1/2dde6700.jpg" width="30px"><span>密码123456</span> 👍（0） 💬（1）<div>我感觉，dashboard就是一个，管理页面。只要数据持久化了。离开dashboard也可以继续使用。</div>2022-04-22</li><br/>
</ul>