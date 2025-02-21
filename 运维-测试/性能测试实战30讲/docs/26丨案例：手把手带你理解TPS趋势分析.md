在性能分析中，前端的性能工具，我们只需要关注几条曲线就够了：TPS、响应时间和错误率。这是我经常强调的。

但是关注TPS到底应该关注什么内容，如何判断趋势，判断了趋势之后，又该如何做出调整，调整之后如何定位原因，这才是我们关注TPS的一系列动作。

今天，我们就通过一个实际的案例来解析什么叫TPS的趋势分析。

## 案例描述

这是一个案例，用一个2C4G的Docker容器做服务器。结构简单至极，如下所示：

![](https://static001.geekbang.org/resource/image/17/1d/177cd65abdaaba1e8056e676cdf96b1d.jpg?wh=384%2A258)

当用个人电脑（上图中压力工具1）测试云端服务器时，达到200多TPS。但是当用云端同网段压力机（上图中压力工具2）测试时，TPS只有30多，并且内网压力机资源比本地压力机要高出很多，服务器资源也没有用完。

在这样的问题面前，我通常都会有一堆的问题要问。

- 现象是什么？
- 脚本是什么？
- 数据是什么？
- 架构是什么？
- 用了哪些监控工具？
- 看了哪些计数器？

在分析之前，这些问题都是需要收集的信息，而实际上在分析的过程中，我们会发现各种数据的缺失，特别是远程分析的时候，对方总是不知道应该给出什么数据。

我们针对这个案例实际说明一下。

这个案例的现象是TPS低，资源用不上。

下面是一个RPC脚本的主要代码部分。

```
public SampleResult runTest(JavaSamplerContext arg0) {
    // 定义results为SampleResult类
    SampleResult results = new SampleResult();
    // 定义url、主机、端口
    String url = arg0.getParameter("url");
    String host = arg0.getParameter("host");
    int port = Integer.parseInt(arg0.getParameter("port"));
    results.sampleStart();


    try {
        message=detaildata_client.detaildata_test(url);// 访问URL并将结果保存在message中
        System.out.println(message); //打印message，注意这里
        results.setResponseData("返回值："+ message, "utf-8");
        results.setDataType(SampleResult.TEXT);
        results.setSuccessful(true);
    } catch (Throwable e) {
        results.setSuccessful(false);
        e.printStackTrace();
    } finally {
        String temp_results=results.getResponseDataAsString();
        results.setResponseData("请求值："+arg0.getParameter("url")+"\n"+"返回值:"+temp_results, "utf-8");
        results.sampleEnd();
    }


    return results;
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/72/72a8bcfd.jpg" width="30px"><span>大拇哥</span> 👍（13） 💬（1）<div>Ramp-up 配置有什么样的作用？
答：Ramp-up 配置的时间是指启动所有配置的线程总数所用的时间，例如设置的线程总数为500，Ramp-up设置的时间为50s,意为：启动500个线程数需要50s，平均为每一秒启动10个线程
为什么说压力工具中 TPS 和响应时间曲线抖动过大会不易于分析？
答：性能分析一定要分析曲线的趋势，通过趋势的合理性来判断性能瓶颈所在的原因，光靠平均值、最大值、最小值、中位数是无法确切的分析处压测过程中服务器的具体情况，只有通过分析曲线趋势，增加对趋势的敏感程度才是压测过程中更好的保障和前提。</div>2020-02-22</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（12） 💬（1）<div>
老师，你这里压力工具1是公网，压力工具2是内网，为何内网的TPS反而低，公网的反而快，按普通理解内网的网速是最快的啊，为何网速快反而TPS低？</div>2021-02-03</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（4） 💬（3）<div>这篇文章给人没有写完整的感觉，最好TPS上去了，也没提服务端有没积压的数据，以及cpu 内存这些大的指标有没提升？  实际操作很难得到完美的TPS幅度曲线，都有一点波动， 还有后面TPS曲线有了之后，就没有完整的描述到定位到是打印耗费时间多？如果是有经验的人可能会一下子定位到打印问题</div>2021-01-30</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（4） 💬（2）<div>当用个人电脑（上图中压力工具 1）测试云端服务器时，达到 200 多 TPS。但是当用云端同网段压力机（上图中压力工具 2）测试时，TPS 只有 30 多，并且内网压力机资源比本地压力机要高出很多，服务器资源也没有用完。  老师，下面又说是日志打印，  那最先的TPS差异是因为打印吗？</div>2021-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（4） 💬（1）<div>今天好像明白一些东西，发现自己之前好像是一直是错的（好像一直理解这个都错了），就是Ramp-up是启动所有线程的时间，但是只是启动，实际上所有线程启动后压力时间是Duration，可以这样理解吗？然后tps抖动过大，那其实中间值这些数据就是完全没有意义的。</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/92/bd/cc7a77d2.jpg" width="30px"><span>🌻Naomi</span> 👍（4） 💬（1）<div>TPS的趋势是否应该跟线上流量分布一致？</div>2020-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/fb/84/a1f866e7.jpg" width="30px"><span>涵涵</span> 👍（3） 💬（3）<div>老师，请教2个问题
1、参数化数据的时候是读取文件比较合适，还是读取数据库数据比较合适？
2、BeanShell取样器中对请求数据进行加签加密处理，会对测试结果有影响吗？</div>2021-07-30</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（3） 💬（2）<div>第三阶段
通过注释掉打印日志的代码，可以得到如下结果：  仔细看这个阶段第二个图的标识，不是TPS，而是hit s，这有点偷换概念了吧？</div>2021-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0e/80/e7c846fb.jpg" width="30px"><span>cathy</span> 👍（3） 💬（2）<div>老师好，老师讲的都是通过压出梯度来确定并发数，想跟老师确认一下以下做法是正确的吗：使用jmeter，然后设置集合点（同步定时器），大量的线程数（几百个），循环次数设为1，来做瞬间一次性并发，看看系统能不能承受住，如果没报错并且响应时间可接受，就说可以支持几百个并发</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/45/33/cdea4bca.jpg" width="30px"><span>zwm</span> 👍（3） 💬（1）<div>Ramp-up 配置有什么样的作用？为什么说压力工具中 TPS 和响应时间曲线抖动过大会不易于分析？
（1）ramp-up就是线程启动时间 。比如10个线程120s基本就是  梯度加压  5个线程运行60s之后再启动50线程运行，是否停止要看是否设置循环等，是一个等比例的梯度加压。
（2）   曲线抖动过大，可以肯定会有异常，这个题确实不会做</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/8c/bc76ecd3.jpg" width="30px"><span>吴小喵</span> 👍（3） 💬（1）<div>老师，怎么计算压测服务器已使用的带宽可以详细说一下吗</div>2020-02-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epLfZ2FNzHAwuiaia5LvbaTGnK4MVdc0SQppqA5ERuOtl2o16iaUE93N0bIqHqUnUAdt4s7qtHcFe6zA/132" width="30px"><span>Geek_admin</span> 👍（2） 💬（1）<div>请教几个问题：
1. 我看留言中有说梯度压测是通过Ramp-up来实现
但网上普遍再说用Stepping Thread Group插件来做，这两者哪种更合适？
2. 另外Ramp-up假如是10s内启动10个线程，那就是平均1s启动1个
对于接口而言，请求到拿到返回的时间是较短的，那么前1秒请求的接口已经返回了，第二个10秒也只会有一个请求，这时候等于每1s内只有一个请求，TPS曲线应该不会存在梯度?</div>2022-01-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJ6G2xZvNRmhyXBjmGbI5G8icGCCMPupr6yxZ1IcURwp7GTRHcpWGWpg9A0fLlyicmVdDwzqZqwiaOQ/132" width="30px"><span>jy</span> 👍（1） 💬（1）<div>1.文中说“将粒度改小，JMeter 默认是 60 秒，这里改为 1 秒”，请问这是在哪里改？

2.看了队列，发送队列大，这个是什么原因呢？这里没动，后面就转到了客户端压力工具了。

请老师解答下，谢谢</div>2021-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKSLiaFwjjzNImuMWNmvVa9YSniacc7sel4Uv2xHeA35Uqibj1ibABMIFIZDgmY82Tw8hDCr8hUIaoKibg/132" width="30px"><span>小破鸟儿</span> 👍（1） 💬（1）<div>老师我看输出message的脚本是在RPC里，是说服务端的接口代码中不要有打印信息的代码是吗，不是说的jmeter工具吧？而且后面也说，不管是什么压力工具，都要在压力测试中把日志关掉，关的都是服务端代码里的吧。</div>2020-07-10</li><br/><li><img src="" width="30px"><span>Geek_66dcc6</span> 👍（1） 💬（1）<div> 问题1.Ramp-up 配置有什么样的作用
Ramp-up 时间长度决定了启动所有线程数所用的时间，如果ramp-up 时间过短，就不能看到阶梯型的TPS 和RT 时间的变化过程，不利于分析TPS 和RT，同时有可能数据不可信。调整ramp-up的值， 到能看到RPS和RT的趋势变化。
问题2：为什么说压力工具中 TPS 和响应时间曲线抖动过大会不易于分析
分析TPS 和RT 的曲线是基础数据，如果基础数据抖动过大，那分析结果也会不完美。所以要尽量找到原因拿到完美的阶梯上升曲线。</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/c3/d41e8c79.jpg" width="30px"><span>不将就</span> 👍（1） 💬（3）<div>老师，请问文章中提到的Send-Q大，是因为服务端网卡往压力机写数据需要排队导致的吗？如果客户端IO大，服务端就会等待，导致Send-Q积压大，我这样理解有问题吗？</div>2020-04-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELPbuPriaqYkRIoPn9SUWFepwprpZJsLReQKYfHz0liamBnxMpibrN6qvoUyq3JzVO9G2QeJrBiciaSibcQ/132" width="30px"><span>Geek_f9f78f</span> 👍（0） 💬（1）<div>下面是一个 RPC 脚本的主要代码部分。  老师好这个RPC是什么意思？？？</div>2023-10-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaELPbuPriaqYkRIoPn9SUWFepwprpZJsLReQKYfHz0liamBnxMpibrN6qvoUyq3JzVO9G2QeJrBiciaSibcQ/132" width="30px"><span>Geek_f9f78f</span> 👍（0） 💬（1）<div>System.out.println(message); 这段代码 是在jmeter 的beanShell中写的吗 </div>2023-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/cd/dbafc7d1.jpg" width="30px"><span>全麦小面包</span> 👍（0） 💬（1）<div>我最大要用1500个线程，Ramp-up怎么做梯度测试呀？总不能每3秒增加一个线程吧？这是不是只能让线程呈斜线增长了？比如1秒增加15个线程？</div>2023-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b4/94/2796de72.jpg" width="30px"><span>追风筝的人</span> 👍（0） 💬（1）<div>在性能分析中，前端的性能工具，我们只需要关注几条曲线就够了：TPS、响应时间和错误率。</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/52/56/6ac8be3c.jpg" width="30px"><span>Cheese</span> 👍（0） 💬（1）<div>之前碰到过开了日志之后tps比较低，但我理解的是压力发起机的问题，因为读取不到所有的数据，而实际的tps在内网肯定会比公网高，这样理解对不。</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（2）<div>响应时间 和 PTS 的曲线趋势 必要要有明显的梯度趋势吗？ 翻了一下之前的阿里云PTS压测报告，好像都没有出现明显的梯度趋势，刚开始都是斜线上升的</div>2021-01-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLaVg4ibQT3CztmMLYMGOEVyXav4SJDl3ktB20AXMpwSFEMnzmibECEl1icViaibrN8wWwkdV9kP1Xiabaw/132" width="30px"><span>windy</span> 👍（0） 💬（1）<div>Ramp-up 配置的调整，可以使tps的趋势变缓或者变抖。请问老师，经过参数调整，趋势图合理后，是用趋势图中的最大线程数进行后续的测试吗？如果测试目标是找到系统最大的tps的话。
</div>2020-11-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a0/1b/9a05e821.jpg" width="30px"><span>sunflower</span> 👍（0） 💬（2）<div>老师，我用梯度递增的方式加压，tps也已经乘递增趋势，但每次到第二个梯度运行一段时间tps就陡降，响应时间长甚至出错，每个接口都是这样，我看服务器的内存占用也不高，请问老师这种情况是正常的吗？造成这种情况的原因可能会是什么呢？</div>2020-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/63/5e/799cd6dc.jpg" width="30px"><span>🎧重返归途</span> 👍（0） 💬（1）<div>这篇文章看过后对与性能分析思路有帮助，性能分析就是以点带面，通过某个瓶颈点，深入分析深层次的系统问题，但有时，引起这个问题的关键往往在一个不是关键的问题上。在这个例子中，我了解到造成测试结果不理想的原因是因为负载测试脚本引起的而不是系统瓶颈，这钟情况有时又是实际测试中常场遇到的。从实际出发，深入研究。</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/63/5e/799cd6dc.jpg" width="30px"><span>🎧重返归途</span> 👍（0） 💬（1）<div>这个案例到最后发现的瓶颈是哪里呢？ 还是压力发起方式？</div>2020-05-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/24/a2/55077969.jpg" width="30px"><span>逸浩(大头针)</span> 👍（0） 💬（1）<div>老师你好  最近一直在看你的专栏 受益匪浅  本文讲到了梯度合理性  在实际工作中调式脚本的时候监控打开可视化判断趋势 在正式压测的时候关闭可视化监控 那我们怎么判断这个趋势呢</div>2020-05-14</li><br/><li><img src="" width="30px"><span>nelson</span> 👍（0） 💬（1）<div>对于最初是的问题，压力工具1测的的TPS有200，压力工具2测的TPS很低只有30。导致这个表象的原因是什么（尽管当时服务端有问题，测试脚本也有问题）</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6a/59/ba3cad16.jpg" width="30px"><span>G</span> 👍（0） 💬（4）<div>打印日志不是和io有关系吗，怎么测出来是网络发送队列高哈</div>2020-03-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erdesQy0moaicYTicoHRQXzbmJm15wohb77qD1OdbuSqPCSUerbcZHzxJJunfmEhTx4kBLxbGaxQ9iag/132" width="30px"><span>村夫</span> 👍（0） 💬（4）<div>老师，今天用你的方式测试了一个接口。发现一个线程下tps可以达到80左右，2个线程能到200左右，再往上增加线程tps就不怎么增加了。这个时候应该怎么去定位呢。我试着10个线程100秒启动起来，10个线程150秒启动起来，随着线程增加，响应时间也在缓慢增加，但是tps到200左右就不增加了，只会上下波动。</div>2020-02-28</li><br/>
</ul>