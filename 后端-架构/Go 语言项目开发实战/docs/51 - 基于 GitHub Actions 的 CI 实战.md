你好，我是孔令飞。这是本专栏正文的最后一讲了，恭喜你坚持到了最后！

在Go项目开发中，我们要频繁地执行静态代码检查、测试、编译、构建等操作。如果每一步我们都手动执行，效率低不说，还容易出错。所以，我们通常借助CI系统来自动化执行这些操作。

当前业界有很多优秀的CI系统可供选择，例如 [CircleCI](https://circleci.com/)、[TravisCI](https://travis-ci.org/)、[Jenkins](https://github.com/jenkinsci/jenkins)、[CODING](https://coding.net/)、[GitHub Actions](https://github.com/features/actions) 等。这些系统在设计上大同小异，为了减少你的学习成本，我选择了相对来说容易实践的GitHub Actions，来给你展示如何通过CI来让工作自动化。

这一讲，我会先介绍下GitHub Actions及其用法，再向你展示一个CI示例，最后给你演示下IAM是如何构建CI任务的。

## GitHub Actions的基本用法

GitHub Actions是GitHub为托管在github.com站点的项目提供的持续集成服务，于2018年10月推出。

GitHub Actions具有以下功能特性：

- 提供原子的actions配置和组合actions的workflow配置两种能力。
- 全局配置基于[YAML配置](https://help.github.com/en/articles/migrating-github-actions-from-hcl-syntax-to-yaml-syntax)，兼容主流CI/CD工具配置。
- Actions/Workflows基于[事件触发](https://help.github.com/en/articles/events-that-trigger-workflows)，包括Event restrictions、Webhook events、Scheduled events、External events。
- 提供可供运行的托管容器服务，包括Docker、VM，可运行Linux、macOS、Windows主流系统。
- 提供主流语言的支持，包括Node.js、Python、Java、Ruby、PHP、Go、Rust、.NET。
- 提供实时日志流程，方便调试。
- 提供[平台内置的Actions](https://help.github.com/en/articles/about-github-actions#discovering-actions-in-the-github-community)与第三方提供的Actions，开箱即用。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（13） 💬（1）<div>最后一讲留个言，专栏基本覆盖 Go 技术栈的方方面面，还有很多工具的加餐，项目开发规范，云原生，容器等知识，物超所值。

代码质量很高，学习了很多，一路走来，多谢了～</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（3） 💬（1）<div>整个专栏质量很高，文案虽然有些瑕疵，不影响整体专栏的专业度，专栏介绍了很多编程规范，主要还是云原生范畴内，看完整个专栏有很多反思，对go语言自我的认知有一个全新的提高(比如项目目录参杂其他语言的习惯目录结构来做是错误的，还有代码规范也会参照其他语言来组织)。
也到说再见的时候了，希望老师在出高质量的专栏，订阅破万，与君共勉。。。。</div>2021-09-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（2）<div>gitlab对应的工具叫啥</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/60/2f7eb4b5.jpg" width="30px"><span>dairongpeng</span> 👍（0） 💬（1）<div>物超所值，非常感谢作者分享自己的优秀实践，自身在go语言领域又上一个台阶</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/dd/09/feca820a.jpg" width="30px"><span>helloworld</span> 👍（0） 💬（1）<div>感谢分享，非常全面的Go工程实践，建议码农们都来学习学习，不限使用语言：）</div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/3a/0dd9ea02.jpg" width="30px"><span>Summer  空城</span> 👍（0） 💬（1）<div>老哥，请教个多了服务公用common包的问题，什么样的内容应该抽出来一个独立的sdk包，供各个微服务引用？我们现在只要有两个及以上微服务重复的代码，都放在一个core lib中，甚至于一些rpc调用、配置中心查询都放在这个core lib中。我觉得这是一个不好的设计，及时两个微服务中有一些重复的代码也是ok的。请教下老哥我理解的对么？什么内容可以放在core lib中？麻烦老哥。</div>2021-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ff/5f/2a16164d.jpg" width="30px"><span>gopher523</span> 👍（4） 💬（0）<div>真的物超所值，大厂的工程师 真不一样啊，膜拜了，各种规范 各种设计。唉 如果给我一次重新上大学的机会 我一定要努力校招上。现在社招压力大啊</div>2021-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/7c/b9/80d91f82.jpg" width="30px"><span>҉我爱小笨蛋</span> 👍（2） 💬（0）<div>质量非常高，是我买的所有教材里面，最值的，没有之一！</div>2023-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（2） 💬（0）<div>很专业、很系统，感谢老师的指引。

内容覆盖了编程技巧、工程化、云原生实践的经验总结，当然还有加餐鸡腿.

收获很大，谢谢老师！</div>2021-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/96/88/454e401c.jpg" width="30px"><span>销毁first</span> 👍（1） 💬（0）<div>堪称go技术栈的软件工程，收货颇丰，谢谢老师</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（1） 💬（0）<div>老师太强了 感觉涵盖了 各个方面的</div>2021-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/26/44095eba.jpg" width="30px"><span>SuperSu</span> 👍（0） 💬（0）<div>非常棒，干货满满</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7b/b3/7c6665e6.jpg" width="30px"><span>LM</span> 👍（0） 💬（0）<div>实现方式很多，但是老师总结了最佳实践，物超所值</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/82/22/518026cf.jpg" width="30px"><span>Prince_H_23</span> 👍（0） 💬（0）<div>第一遍还有很多需要消化，期待再次回顾～</div>2022-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ac/9d/1f697753.jpg" width="30px"><span>米兔</span> 👍（0） 💬（0）<div>专栏内容很丰富，一讲就需要很多时间消化了，谢谢！</div>2021-10-21</li><br/>
</ul>