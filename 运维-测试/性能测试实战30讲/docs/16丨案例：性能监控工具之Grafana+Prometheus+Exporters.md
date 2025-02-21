在本模块中，我将把几个常用的监控部分给梳理一下。前面我们提到过，在性能监控图谱中，有操作系统、应用服务器、中间件、队列、缓存、数据库、网络、前端、负载均衡、Web服务器、存储、代码等很多需要监控的点。

显然这些监控点不能在一个专栏中全部覆盖并一一细化，我只能找最常用的几个，做些逻辑思路的说明，同时也把具体的实现描述出来。如果你遇到了其他的组件，也需要一一实现这些监控。

在本篇中，主要想说明白下图的这个监控逻辑。

![](https://static001.geekbang.org/resource/image/e0/39/e0aa269a7f528f393b859cc8ed69ac39.jpg?wh=1894%2A1022)

这应该是现在最流行的一套监控逻辑了吧。

我今天把常见的使用Grafana、Prometheus、InfluxDB、Exporters的数据展示方式说一下，如果你刚进入性能测试领域，也能有一个感性的认识。

有测试工具，有监控工具，才能做后续的性能分析和瓶颈定位，所以有必要把这些工具的逻辑跟你摆一摆。

所有做性能的人都应该知道一点，不管数据以什么样的形式展示，最要紧的还是看数据的来源和含义，以便做出正确的判断。

我先说明一下JMeter和node\_exporter到Grafana的数据展示逻辑。至于其他的Exporter，我就不再解释这个逻辑了，只说监控分析的部分。

## JMeter+InfluxDB+Grafana的数据展示逻辑
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（7） 💬（2）<div>今日思考题：
问题1：JMeter 是如何把数据推送到 Grafana 中的？
共分为两个大步骤：
1、JMeter 将数据发给 InfluxDB：
（1）在JMeter 中配置 Backend Listener ；
（2）使用InfluxdbBackendListenerClient将JMeter运行的统计结果添加到metric中，并保存metric；
（3）使用InfluxdbMetricsSender将metric发送到Influxdb；
2、Grafana从 InfluxDB获取数据：
（1）在Grafana 中配置InfluxDB 数据源
（2）添加 JMeter dashboard，导入模板，选择对应的数据源即可看到界面


问题2：同样是监控操作系统的计数器，监控平台中的数据和监控命令中的数据有什么区别？
就数据的值来说，没有区别；
就数据量来说，监控平台的数据通常比监控命令中查到的数据会少一些。


今日感悟：
高老师的专栏，音频总会比文章多讲一些，知道这一点之后，我就调整了学习方式，我先听音频，再细读文章（以前我的习惯是先看文章，再听音频）。这节内容，不适用了，不知道是因为我太弱，还是老师语速变快了，边听边看文章，听的真是一脸懵。
大概听了3遍之后，这节课在我眼里变成了高不可攀的形象。甚至让我有一种，这个专栏我可能就卡在这里学不动了的感觉。然后抵触心理就出来了，有点不想学。
但是吧，不能轻言放弃，于是我不听音频了，开始细细读文章。边读边整理笔记，梳理思路。
神奇般的，我觉得我又能懂了，虽然不是说完全能把这个监控平台搭起来，但是我觉得我体会到了老师这节课想强调的东西。
最后，作为一个小白，这节课我对自己的要求就是：达到一个感性的认识。

其实归根结底还是自己手头没有实际的性能项目来练习，边学边练其实才是最好的。

最最后：文中“通过 writeAndSendMetrics，就将所有保存的 metrix 都发给了 InfluxDB。” 老师单词是不是拼错啦，应该是metric吧（或者是metrics?）</div>2020-03-30</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83epFQPMPrP3V6HhlGLPp0JKMiaHQDibFKnE7z8To27tYEH42XvvmmQGyYvL4CK1lLJBIUAw7jtBnezibA/132" width="30px"><span>bettynie</span> 👍（7） 💬（1）<div>老师，按照你讲的原理，其实我们需要搭建 jmeter+influxdb+grafana 和 prometheus+exports+grafana 2套系统来分别监控我们需要的性能指标，是么？
 jmeter+influxdb+grafana用来监控jmeter中的线程数，响应时间和吞吐量，prometheus+exports+grafana 用来监控系统资源或者数据库以及其他资源, 对么？
并且prometheus+exports+grafana 只能监控linux和uinx系统，无法监控windows,并且只能监控mysql数据库，感觉好像就是为监控docker之内的容器而生的~</div>2020-02-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/44/b0/c196c056.jpg" width="30px"><span>SeaYang</span> 👍（6） 💬（1）<div>老师您好，backend listener本身没有问题，可能我描述的不够清楚，我再描述一次我的问题：
1、背景
我们基于jmeter做了个压测平台，在平台的前端页面上编写接口、场景等，点击压测，后端会调度多台压力机，每台压力机会将接口、场景数据使用jmeter的api生成jmx文件，然后调用jmeter的命令行启动压测。生成jmx文件的过程中会创建一个backend listener元件，每台压力机backend listener元件的application字段设置为了同一个值，这样子我们可以通过这个application值调用InfluxDB的http接口，获得所有压力机的tps总和

2、遇到的问题
1）实验过程
使用控制目标TPS的方式，TPS目标是2000，启动20台压力机，每台压力机的目标TPS为2000 &#47; 20 = 100，注意，单台压力机就能达到2000TPS。
2）现象
通过观察前端页面的tps曲线，会发现TPS经常达不到2000，经常是1800， 1900左右，看上去像是有一两台压力机没有将数据抛到InfluxDB中，查看InfluxDB，会发现每秒确实只有18条、19条的数据。
3）分析
查看每台压力机的jmeter输出日志，有summary输出，说明每台压力机都正常调起了jmeter并正常压测了，查看InfluxDB的连接也没有问题。
后来同时启动30台压力机，也是看上去像是有一两台压力机没有抛数据一样，但jmeter日志都没问题，这就很奇怪了，如果是InfluxDB不支持20台压力机同时抛数据，那么30台压力机同时抛数据就应该最多每秒只有十几条数据啊。难道是因为每台压力机的application值都一样，有一定概率发生数据覆盖？

3、解决办法
将每台压力机的backend listener的application字段设置为不同的值，但是有一个相同的前缀，通过这个前缀值去查询总的TPS数据，经过几十次的测试，都是正常的，没有再出现问题了。但是之前是不是发生了数据覆盖也不确定，但暂时也不管了。</div>2020-11-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLibCKJYwlyLEIWicNxJSuIwIbCZqfGIbzfF5mKicjWIrGkibBgM4E0dSNekhzdaoyzabmZPTxicTCv7TQ/132" width="30px"><span>障碍物</span> 👍（5） 💬（1）<div>Prometheus有插件能监控sqlserver或者oracle等其他数据库么</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/87/5066026c.jpg" width="30px"><span>dao</span> 👍（3） 💬（2）<div>如果有人和我一样安装的是 influxdb 2.0，那么需要在 JMeter Backend Listener 设置 influxdbUrl 和 influxdbToken。比如我的设置
influxdbUrl：http:&#47;&#47;192.168.1.196:9999&#47;api&#47;v2&#47;write?bucket=test&amp;org=dao
influxdbToken：好长的一串 base64 编码的 token</div>2021-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/0f/a8/956452cd.jpg" width="30px"><span>蔚来懿</span> 👍（3） 💬（1）<div>老师，有一个疑问，我的情况是这样的，我们公司环境有很多（测试环境，开发环境，预发布环境，开发环境），很多个项目，每个项目结构复杂，机器有很多，如果按照这样的部署的话，需要安装很多软件，还有防火墙的问题，请问是否有轻量级的监控方式，比如说，直接在服务器上装工具（类似nmon，但是直观），</div>2021-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e6/94/ba217a11.jpg" width="30px"><span>涓涓</span> 👍（3） 💬（1）<div>高老师，好。
你看这样配置行不行:
1. 要监控的每台服务器都配置一个node_exporter
2.  然后再找台服务器安装prometheus，在prometheus.yml中添加每个node_exporter的配置
3. 最后在grafana中配置prometheus，查看采集的各台服务器数据。</div>2021-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/44/b0/c196c056.jpg" width="30px"><span>SeaYang</span> 👍（3） 💬（1）<div>1、JMeter 是如何把数据推送到 Grafana 中呢？
JMeter实际上是将数据推送到Influxdb中，Influxdb本身对外提供了HTTP接口，Grafana通过HTTP接口轮询性能指标，若自己去画前端页面图表的话，也可以不用Grafana，直接调用Influxdb的HTTP接口

2、另外，同样是监控操作系统的计数器，监控平台中的数据和监控命令中的数据有什么区别？
没有区别，只是命令可能能看到更多的值

有时候压测过程中，压力机本身的资源情况也是需要关注的，通过Prometheus + node_exporter + Grafana可以很方便的查看压力机集群的资源情况，比传统一台台登录方便很多，顺便熟悉监控的部署</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/84/7f584cb2.jpg" width="30px"><span>杜艳</span> 👍（3） 💬（16）<div>感觉老师讲的都是偏理论，知道数据的来龙去脉了，但是使用过程怎么搭建这个整体的监控平台步骤能不能详细介绍，让我们可以用在项目中呢？</div>2020-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/52/56/6ac8be3c.jpg" width="30px"><span>Cheese</span> 👍（2） 💬（1）<div>老师，如果用nodeexporter监控容器要怎么监控，因为容器IP是变化的，是通过端口来监控吗</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d4/c3/d41e8c79.jpg" width="30px"><span>不将就</span> 👍（2） 💬（1）<div>问题1:：Jmeter直接面向的是influxdb,Granfana通过官方插件取指定的influxdb中抓取数据做展示
问题2：监控平台的数据本质上还是通过操作系统命令获取的，而且有抓取周期，通过网络传过来，实时性不如直接在操作系统获取，但是好处也是明显的，就是图形化展示和历史监控数据的便捷查询</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（2） 💬（3）<div>上来安装了 InfluxDB 2.0 ，结果悲剧了，找了一天没找到怎么创建 database，后来看官方文档，感觉是理念变了，全部通过 API 完成。请选择 InfluxDB v1.8 ，避免 2.0 的尴尬。</div>2020-10-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Nv7iaxevWVukvxaZf6TjbcNicgatCUpUcp7hTah0JQxvr7ZjMlLbopEaveichKRLQJjKXR6geB5LBntf7XCP8F4kQ/132" width="30px"><span>Geek_a55bf0</span> 👍（2） 💬（1）<div>高老师，我的jmeter传到influxdb的数据没有事务名，请问您知道原因吗？如果没有碰到过麻烦提供下您的软件版本，我按您的版本安装试试</div>2020-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c2/20/fb3861e8.jpg" width="30px"><span>Joie</span> 👍（2） 💬（1）<div>我在项目中用到了jmeter+influxDB+grafana，拉长时间段来看TPS和响应时间 还有分事务来看不同趋势 效果很明显。不过有时候不知道为什么在趋势显示时中间会有断开曲线的情况，在jmeter自身的log中是没有出现的</div>2020-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/26/74/92646820.jpg" width="30px"><span>郑频雅</span> 👍（1） 💬（1）<div>请问老师，除了这套工具，nmon为什么没有介绍，这个工具不是必不可少的？</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/a1/80/9801443f.jpg" width="30px"><span>Daisy</span> 👍（1） 💬（1）<div>老师好，想问一下，top这个监控命令应该是监控整个服务器吧，像我们公司用的docker，每个docker又部署了一个服务，我想对具体这个服务监控，top还能用吗，或者用什么命令。谢谢</div>2021-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/de/d4/b83c4185.jpg" width="30px"><span>David.cui</span> 👍（1） 💬（1）<div>Prometheus+Grafana或InfluxDB+Grafana 是不是可以用python或其他工具分析自己想要的指标，然后插入InfluxDB或Prometheus，通过Grafana展示出来即可呢？</div>2020-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/87/6f/a1c56129.jpg" width="30px"><span>chailyn</span> 👍（1） 💬（1）<div>高老师，压力机和安装influxdb是两台机子，数据传送失败，难道压力机和influxdb要安装到一台机子？</div>2020-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（1） 💬（1）<div>获得了监控的神器，很炫酷、很强大！感谢老师！</div>2020-10-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Nv7iaxevWVukvxaZf6TjbcNicgatCUpUcp7hTah0JQxvr7ZjMlLbopEaveichKRLQJjKXR6geB5LBntf7XCP8F4kQ/132" width="30px"><span>Geek_a55bf0</span> 👍（1） 💬（2）<div>
SELECT last(&quot;count&quot;) &#47; $send_interval FROM &quot;$measurement_name&quot; WHERE (&quot;transaction&quot; =~ &#47;^$transaction$&#47; AND &quot;statut&quot; = &#39;ok&#39;) AND $timeFilter GROUP BY time($__interval)     高老师，我基础比较差，请问下1.$send_interval是脚本跑一个循环的时间吗？   2.~ &#47;^$transaction$这一段怎么理解   3.$timeFilter和$__interval是什么意思</div>2020-06-23</li><br/><li><img src="" width="30px"><span>赵娜</span> 👍（1） 💬（1）<div>老师，JMeter+InfluxDB+Grafana组合采集到的数据和jmeter本身收集到的数据一致，为什么还要采用这种方式呢？使用node_exporter+Prometheus+Grafana的组合采集数据，当数量大时会影响被监控的系统吗，同时在收集数据时也会对被监控的服务器有影响吧？</div>2020-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIUw2n2cOLticrdgJWu5ibM1Hib58XNRt5jQwRibT27ZLvqKvsPoZDicrFmUic2GF9vtI2EjgMWVpiatwgFw/132" width="30px"><span>Geek_f9e0e5</span> 👍（1） 💬（5）<div>Prometheus+Grafana+Exportor，这个接口级的集成方式，能给个文档参考下吗</div>2020-03-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIV7iaia7Ko59UJk3oap1XZEg6JW999tIibuTicWfVXgaXicUHjABI6ibXErd2tY527VMsib5ElZJxSW8nFw/132" width="30px"><span>刘志鹏</span> 👍（0） 💬（1）<div>插件看tps，rt，错误率不准吗？</div>2024-01-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKHzrvlV4HLmR5IWUiad4sqich3QZXxWRxFicvqxPtRaWITLibic16eibRaJia1FxRjq81Pcs2NsB5Hg1WoQ/132" width="30px"><span>枫林听雪落</span> 👍（0） 💬（2）<div>高老师，influxdb+grafana在本地的pc搭建会影响到负载机的测试吗？监控平台是否需要独立的一套环境吗？</div>2023-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7d/28/423df492.jpg" width="30px"><span>碎碎念</span> 👍（0） 💬（1）<div>老师您好，请问influxdb这是是要安装到被压测的服务器中吗，还有 Grafana是不是本地安装就可以了。流程上还是不是很清楚，希望老师解答，或者提供安装的步骤手册，感谢</div>2023-03-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/cf/28/eb90fa13.jpg" width="30px"><span>樱峻小猴子</span> 👍（0） 💬（1）<div>怎么联系您 我想要实践详细一点的课程资料 您讲的偏理论</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/d7/812442cf.jpg" width="30px"><span>奔跑的萝卜</span> 👍（0） 💬（1）<div>老师您好，请问tps的曲线图如何配置的那，我看数据库里就是一条聚会报告的数据，怎么展示tps曲线图到grafana</div>2022-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7c/cd/223083a6.jpg" width="30px"><span>黄炳焱</span> 👍（0） 💬（1）<div>为啥没有画面
</div>2022-04-24</li><br/><li><img src="" width="30px"><span>梁之秋</span> 👍（0） 💬（3）<div>jmeter跑压力为什么是大忌呢？有谁知道？</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/20/8f4e0810.jpg" width="30px"><span>thinkers</span> 👍（0） 💬（1）<div>老师，你文章里面显示tps曲线用的什么插件？我找了几个都没有</div>2021-09-18</li><br/>
</ul>