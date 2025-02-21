你好，我是孔令飞。

上一讲，我们学习了如何分析Go代码的性能。掌握了性能分析的基本知识之后，这一讲，我们再来看下如何分析API接口的性能。

在API上线之前，我们需要知道API的性能，以便知道API服务器所能承载的最大请求量、性能瓶颈，再根据业务对性能的要求，来对API进行性能调优或者扩缩容。通过这些，可以使API稳定地对外提供服务，并且让请求在合理的时间内返回。这一讲，我就介绍如何用wrk工具来测试API Server接口的性能，并给出分析方法和结果。

## API性能测试指标

API性能测试，往大了说其实包括API框架的性能和指定API的性能。不过，因为指定API的性能跟该API具体的实现（比如有无数据库连接，有无复杂的逻辑处理等）有关，我认为脱离了具体实现来探讨单个API的性能是毫无意义的，所以这一讲只探讨API框架的性能。

用来衡量API性能的指标主要有3个：

- 并发数（Concurrent）：并发数是指某个时间范围内，同时在使用系统的用户个数。广义上的并发数是指同时使用系统的用户个数，这些用户可能调用不同的API；严格意义上的并发数是指同时请求同一个API的用户个数。这一讲我们讨论的并发数是严格意义上的并发数。
- 每秒查询数（QPS）：每秒查询数QPS是对一个特定的查询服务器在规定时间内所处理流量多少的衡量标准。QPS = 并发数 / 平均请求响应时间。
- 请求响应时间（TTLB）：请求响应时间指的是从客户端发出请求到得到响应的整个时间。这个过程从客户端发起的一个请求开始，到客户端收到服务器端的响应结束。在一些工具中，请求响应时间通常会被称为TTLB（Time to last byte，意思是从发送一个请求开始，到客户端收到最后一个字节的响应为止所消费的时间）。请求响应时间的单位一般为“秒”或“毫秒”。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（3） 💬（1）<div>这篇文章系统的介绍了性能指标的测试
性能指标主要是：不同并发量下的QPS+延迟
此处有2个疑问：
1. 如何选取性能指标作为服务能力的上限（并发+QPS+延迟）
2. 如何保护服务的访问不会超过性能上限？（使用微服务的治理方法，限流、熔断之类的？）</div>2021-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/0a/e4/c576d62b.jpg" width="30px"><span>阿波罗尼斯圆</span> 👍（1） 💬（1）<div>为什么写类接口通常不会有性能问题，写接口不是一般都比读接口慢吗</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（1） 💬（1）<div>总结：
性能测试一般包括框架测试和API接口测试。
API 性能测试指标：并发数、QPS、请求响应事件（TTLB），注意QPS与TPS的区别。TPS是针对多个接口进行测试。离开并发数谈QPS，毫无意义。
框架性能测试：提供一个很简单的接口，如 &#47;healthz，与 net&#47;http 框架进行对比；
API 性能接口：针对写类接口可通过单元测试来测试其性能，针对读类接口，可通过wrk进行测试
介绍 wrk 的使用方法
介绍基于wrk 的输出结果：并发数、QPS、平均响应时间，平均错误数，使用工具绘制图表。</div>2021-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/a1/45ffdca3.jpg" width="30px"><span>静心</span> 👍（0） 💬（1）<div>在本机压测远程服务的时候，经常由于线程或打开文件数的限制，导致测试机客户端成为并发的瓶颈。不知道老师有没有什么解决的好办法？</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/70/4a/30cf63db.jpg" width="30px"><span>丁卯</span> 👍（0） 💬（1）<div>在满足预期要求的情况下，服务器状态稳定，单台服务器QPS要求在1000+，这个服务器的QPS怎么测？</div>2021-10-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLDUJyeq54fiaXAgF62tNeocO3lHsKT4mygEcNoZLnibg6ONKicMgCgUHSfgW8hrMUXlwpNSzR8MHZwg/132" width="30px"><span>types</span> 👍（0） 💬（1）<div>这篇文章系统的介绍了性能测试的方法
通过性能测试可以得到在一定并发下的QPS和延迟
得到性能数据以后，产生一个疑问：
1. 如何选取一个性能指标作为服务器的上限（并发 QPS 延迟）</div>2021-08-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（1） 💬（0）<div>太硬核了，写shell来画图</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9a/d4/8632497b.jpg" width="30px"><span>沙可</span> 👍（0） 💬（0）<div>请教老师，性能测试在内网操作，但是这样会不会忽略了网络的因素，</div>2024-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/83/17/df99b53d.jpg" width="30px"><span>随风而过</span> 👍（0） 💬（0）<div>一般都是使用Jmeter，wrk倒是没用过，这个工具比Jmeter优秀很多，学到了</div>2021-09-09</li><br/>
</ul>