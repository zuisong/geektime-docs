你好，我是七牛云许式伟。

基于 HTTP 协议提供服务的好处是显然的。除了 HTTP 服务有很多现成的客户端、服务端框架可以直接使用外，在 HTTP 服务的调试、测试、监控、负载均衡等领域都有现成的相关工具支撑。

在七牛，我们绝大部分的服务，包括内部服务，都是基于 HTTP 协议来提供服务。所以我们需要思考如何更有效地进行 HTTP 服务的测试。

七牛早期 HTTP 服务的测试方法很朴素：第一步先写好服务端，然后写一个客户端 SDK，再基于这个客户端 SDK 写测试案例。

这种方法多多少少会遇到一些问题。首先，客户端 SDK 的修改可能会导致测试案例编不过。其次，客户端 SDK 通常是使用方友好，而不是测试方友好。服务端开发过程和客户端 SDK 的耦合容易过早地陷入“客户端 SDK 如何抽象更合理” 的细节，而不能专注于测试服务逻辑本身。

我的核心诉求是对服务端开发过程和客户端开发过程进行解耦。在网络协议定好了以后，整个系统原则上就可以编写测试案例，而不用等客户端 SDK的成熟。

不写客户端 SDK 而直接做 HTTP 测试，一个直观的思路是直接基于 http.Client 类来写测试案例。这种方式的问题是代码比较冗长，而且它的业务逻辑表达不直观，很难一眼就看出这句话想干什么。虽然可以写一些辅助函数来改观，但做多了就会逐渐有写测试专用 SDK 的倾向。这种写法看起来也不是很可取，毕竟为测试写一个专门的 SDK，看起来成本有些高了。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/8c/8fba0bdd.jpg" width="30px"><span>debugtalk</span> 👍（26） 💬（1）<div>之前我做的一个开源项目 HttpRunner 和这个倒有些相似之处。
https:&#47;&#47;github.com&#47;httprunner&#47;httprunner

对于DSL，有个痛点就是没法像代码那样进行单步调试。所以我也在HttpRunner中探索了语法提示和自动补全功能，以及和 python代码的互转</div>2019-10-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7a/08/4d3e47dd.jpg" width="30px"><span>Aaron Cheung</span> 👍（4） 💬（2）<div>测试先行在目前的开发环境下有无必要 开发人员的边界条件之类有可能没有覆盖业务条件</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/c2/e9fa4cf6.jpg" width="30px"><span>Charles</span> 👍（1） 💬（2）<div>加餐加的太好了，谢谢！请问下许老师，后端对应的数据库产生的测试数据如何处理的？测试环境还好，生产环境呢？如果是代码处理的话，处理逻辑是放在后端吗？</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/0f/93d1c8eb.jpg" width="30px"><span>mickey</span> 👍（0） 💬（1）<div>如果后端是连接数据库的，怎样做动态的自动化测试呢？</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（4） 💬（0）<div>笔记
1  准备上班后下载使用，做中学
2 去关注开发人员日常工作过程中的不爽和低效率是非常有必要的。任何开发效率提升相关的工作，其收益都是指数级的。</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/d3/31208e3b.jpg" width="30px"><span>alswl</span> 👍（0） 💬（0）<div>跟之前设计的基于 pyresttest 集成测试（e2e）方案思路挺一致的
https:&#47;&#47;testerhome.com&#47;topics&#47;6134

现在一旦让我设计 DSL，第一反应就是往 YAML 作为载体。</div>2022-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/b9/8d/00bded19.jpg" width="30px"><span>不温暖啊不纯良</span> 👍（0） 💬（0）<div>读完第一段的时候我脑子里出现了一个场景,一个叫http的店铺在街上吆喝:&quot;服务便宜卖,客户端服务1元1斤,服务的服务2元1斤,服务后测试&#47;调试&#47;监控&#47;负载均衡等&quot;,一个叫七牛的人说:&quot;来个服务端的测试服务&quot;.接着他又找到github店铺,看见今日特价:httptest DSL测试工具,心想:&#39;这个不错,刚好好http测试服务配合用,买回家改造改造&#39;.接着就是使用场景了,七牛把客户端和服务端交给了两个不同的人去干,于是用http测试服务使得他俩不用在一起干活,就能完成互相测试.最后是隐藏敏感信息,测试用例是写好了,但ip&#47;密码&#47;AK&#47;SK等信息一定要配置起来,于是就有了后面的 host foo.com等代表敏感信息的单词.</div>2021-05-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLMDBq7lqg9ZasC4f21R0axKJRVCBImPKlQF8yOicLLXIsNgsZxsVyN1mbvFOL6eVPluTNgJofwZeA/132" width="30px"><span>Run</span> 👍（0） 💬（0）<div>很好</div>2021-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/00/f4/cc5f0896.jpg" width="30px"><span>Jowin</span> 👍（0） 💬（0）<div>测试用例是移定的，SDK是不断变化的。</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/69/187b9968.jpg" width="30px"><span>南山</span> 👍（0） 💬（0）<div>测试数据一直是耗费精力的地方</div>2020-03-20</li><br/>
</ul>