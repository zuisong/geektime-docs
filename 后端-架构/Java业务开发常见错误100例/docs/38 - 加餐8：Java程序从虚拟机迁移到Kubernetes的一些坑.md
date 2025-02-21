你好，我是朱晔，我们又见面了。结课并不意味着结束，我非常高兴能持续把好的内容分享给你，也希望你能继续在留言区与我保持交流，分享你的学习心得和实践经验。

使用Kubernetes大规模部署应用程序，可以提升整体资源利用率，提高集群稳定性，还能提供快速的集群扩容能力，甚至还可以实现集群根据压力自动扩容。因此，现在越来越多的公司开始把程序从虚拟机（VM）迁移到Kubernetes了。

在大多数的公司中，Kubernetes集群由运维来搭建，而程序的发布一般也是由CI/CD平台完成。从虚拟机到Kubernetes的整个迁移过程，基本不需要修改任何代码，可能只是重新发布一次而已。所以，我们Java开发人员可能对迁移这个事情本身感知不强烈，认为Kubernetes只是运维需要知道的事情。但是程序一旦部署到了Kubernetes集群中，在容器环境中运行，总是会出现各种各样之前没有的奇怪的问题。

今天的加餐，就让我们一起看下这其中大概会遇到哪些“坑”，还有相应的“避坑方法”。

## Pod IP不固定带来的坑

Pod是Kubernetes中能够创建和部署应用的最小单元，我们可以通过Pod IP来访问到某一个应用实例，但需要注意的是，如果没有经过特殊配置，Pod IP并不是固定不变的，会在Pod重启后会发生变化。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3b/df/04/791d0f5e.jpg" width="30px"><span>笨手笨脚の</span> 👍（0） 💬（1）<div>我之前部署单体 java 项目的时候遇到了这个错误：
org.springframework.context.ApplicationContextException: Unable to start web server; nested exception is java.lang.ClassFormatError: Unknown constant tag 67 in class file org&#47;apache&#47;catalina&#47;util&#47;ErrorPageSupport
我找源码是在项目启动创建 tomcat 时报的错误，但是搜 Unknown constant tag ** 错误信息网上很多文章都说是 jdk 之类的问题，后来找公司的老员工看了看，调了下 cpu 和内存的限制，就可以了。
他跟我说的是，可能因为分配的资源太少，启动非常慢，导致存活探针的 &#47;actuator&#47;health 接口在检测时项目还没启动完成，pod 一直重启。他好像也没太遇到过这个错误，想问下老师有遇到这个问题以及是怎么定位和解决的</div>2025-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/7e/5a/da39f489.jpg" width="30px"><span>Ethan New</span> 👍（0） 💬（1）<div>朱老师，期待你的新课</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/48/fae317c1.jpg" width="30px"><span>子休</span> 👍（12） 💬（0）<div>居然等到了朱老师又来加餐了，但是内容真的有点少，不知道朱老师后续还有没有别的计划，比如开个新专栏。时至今日，我买了三十门的极客课程，依旧觉得朱老师的课程最实用，也是我最快完成全部课程学习的。十分期待朱老师后续的新分享。</div>2021-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/48/7c/2aaf50e5.jpg" width="30px"><span>coder</span> 👍（3） 💬（0）<div>跟朱老师学到了很多，居然又更新了</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/8e/41/709e9677.jpg" width="30px"><span>袁帅</span> 👍（2） 💬（0）<div>朱老师再开一门课吧，太喜欢这种讲课风格了，实战性很强</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/e3/2350662b.jpg" width="30px"><span>胜勝</span> 👍（1） 💬（0）<div>哇，谢谢朱老师，最近公司就在从虚拟机到容器，虽然是开发，但是也在配合运维进行部署，看到了老师文章说的问题感觉很有用，能让人少踩很多坑</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d0/42/6fd01fb9.jpg" width="30px"><span>我已经设置了昵称</span> 👍（0） 💬（0）<div>NMT的具体使用方式，老师能加餐讲下吗，我们现在经常遇到RSS占用很高，但heapdump下来看没有任何问题。已经加上了
java -XX:NativeMemoryTracking=smmary。看了下也没啥问题。
后面这两个参数-XX:+UnlockDiagnosticVMOptions -XX:+PrintNMTStatistics也不知道使用场景</div>2022-05-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJkeOAC8k7aPMfQZ4ickiavpfR9mTQs1wGhGtIicotzAoszE5qkLfFTabkDU2E39ovSgoibJ1IiaLXtGicg/132" width="30px"><span>bigben</span> 👍（0） 💬（0）<div>存活弹针之前配置了健康检查的地址，导致系统经常重启</div>2022-05-03</li><br/>
</ul>