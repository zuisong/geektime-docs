你好，我是何为舟。

在前面的课程中，我们已经介绍了防火墙、WAF和入侵检测。这些产品都有一个共同的特性，就是基于网络请求或者系统行为对攻击的特征进行检测，然后再采取相应的防控手段。这些安全产品基本都和应用本身解耦。也就是说，基本上我们不需要对应用做任何开发和改动，就能够部署这些安全产品。

尽管解耦在部署上能够节省很大的成本，但解耦同样意味着，安全产品和应用本身是通过接口、请求等形式来进行数据交换的。换一句话说，安全产品只能够看到应用输入和输出的数据，并不知道数据在应用内的流动情况。因此，这种工作模式不可避免会产生一定的误判和漏报。

我们来看一个关于WAF检测SQL注入的例子。下面是请求代码：

```
http://server.com/login?username=test&password=" or ""="
```

WAF可能会检测到password参数中的SQL注入痕迹进行拦截。如果应用采用的是安全的PreparedStatement方法，那这个SQL注入就不会生效，也就不需要拦截。但是WAF和应用解耦，让WAF不知道应用的逻辑，从而产生了误报。

所以，对于任何安全产品来说，能获取到的数据和信息越多，检测的能力就越强，误判和漏报的概率也就越低。因此，2012年，Gartner提出了RASP（Runtime Application Self Protection）的概念，就是希望将安全产品部署在应用的底层，完全站在应用的视角去发现攻击行为，从而实现更加完善的安全防护。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（4） 💬（1）<div>提一下课中的内容：以及对于课程对于RASP的理解；
1.目前其实是暂时处于初期阶段，即我们所说的软件1.0，其后续的许多支持暂时并未出现
2.RASP目前最大的问题在于对于编程语言的支持力度不够，尤其分布式中用的最多的PYTHON和GO语言尚未支持
3.它的部署不是有Ops去做：开发团队本身就能力高低差异巨大，开发又恰恰是最不懂这块的人，各种不确定性就更加难以把控。
故而东西虽好，可是真正能用它有能力用好的人在实际团队中并不多；个人觉得初期用WAF与RASP同时分场景结合使用相对合适。这就如同现在的数据系统已经很少中大型团队用单一的关系型数据库解决一切问题，都是相互结合使用；可能当某天它的使用门槛降降低兼容性做的更好，2.0或3.0时再适当调整使用比例。
      以上是我对于课程的一点见解：谢谢老师今天的分享。
</div>2020-02-07</li><br/><li><img src="" width="30px"><span>illman</span> 👍（1） 💬（2）<div>老师，是否可以用一个具体的例子（最好是Python代码段）来说说rasp是如何实现恶意行为识别的，这样更具象，更能引发思考。谢谢老师。</div>2021-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/d3/bcb7a3fd.jpg" width="30px"><span>半兽人</span> 👍（1） 💬（1）<div>开发人员的思路：“我负责解决SQL注入、XSS，对于中间件的漏洞，是运维人员负责的。”在这种情况下肯定没有动力去用RASP。除非DevOps真的推广开，开发人员发现运维工作太麻烦才会去动手改善。</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（1） 💬（2）<div>RASP和WAF支持微服务吗？</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/bf/cd6bfc22.jpg" width="30px"><span>自然</span> 👍（0） 💬（1）<div>个人比较讨厌 waf rasp 一类的东西，这类东西部署后（经常在你不知道的情况下被部署），经常拦截或者做其他处理，任何信息都不报，让人无法定位故障（还以为是应用的问题，排查了半天）。</div>2022-06-20</li><br/><li><img src="" width="30px"><span>一键修复</span> 👍（0） 💬（0）<div>请问下老师，使用部署在K8S的微服务应用，推荐使用什么应用安全检测工具呢？WAF、RASP 或者是有其他建议？</div>2021-01-20</li><br/><li><img src="" width="30px"><span>一键修复</span> 👍（0） 💬（0）<div>请问在微服务K8S部署环境下，有哪些比较推荐的应用检测或防护方案？</div>2021-01-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/2b/3ba9f64b.jpg" width="30px"><span>Devin</span> 👍（0） 💬（0）<div>【SELECT、 *、FROM、Users、WHER、Username、=、&quot;&quot;、AND、Password、=、&quot;&quot;、or、&quot;&quot;、=、&quot;&quot;】
应该是下面这样的？
【SELECT、 *、FROM、Users、WHER、Username、=、&quot;&quot;、AND、Password、=、&quot; &quot;、or、&quot; &quot;、=、&quot;&quot;】</div>2020-07-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/78/a11a999d.jpg" width="30px"><span>COOK</span> 👍（0） 💬（0）<div>增长了见识，感谢老师！</div>2020-03-26</li><br/>
</ul>