在苍茫的性能分析道路上，不管你是一只多老的鸟，在经历了多个性能测试的项目之后，你都会发现对于性能问题而言，你仍然不敢说能全部解决。因为下一个问题可能真的是你完全没有见过的。

再加上技术的飞速发展，想跟得上技术的进步都是一件痛苦的事情，更别说要完全掌握并且融会贯通了。

我经常看到有些人在简历中动辄说自己做过上百个性能项目，以彰显自己有充足的经验。事实上，如果一个性能项目需要做两个星期的话，基本上做不到调优的层面，最多是弄个脚本压个报告。在我的经验中，基本上一个完整的架构级的性能项目从准备开始到写出测试报告、调优报告，需要1.5个月以上。你可以想像，这样的项目，就算一年不停地做，做10个都算是非常快的了，而要做上百个这样的项目，至少需要10年的时间。

并且不是每一个项目都能让你有分析性能瓶颈的机会，因为有很多问题都是重复的。

所以性能分析是一个需要不断总结出自己的分析逻辑的工作，有了这些分析逻辑，才能在新项目中无往不利。请注意我的描述，我强调的是要有自己分析的逻辑，而不是经历多少个性能问题。因为问题可能会遇到新的，但是分析逻辑却是可以复用的。

在今天的文章中，我仍然用一个之前项目中出现过的案例给你讲一讲性能分析的思路。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/9a/76c0af70.jpg" width="30px"><span>每天晒白牙</span> 👍（10） 💬（1）<div>读完老师的文章，有下面几点疑惑
1. TCP 四次挥手中，主动断开链接的一方才会处于 TIME_WAIT 状态呢，老师在文中有说 客户端主动断开，服务端也会出现 TIME_WAIT 状态，这是什么情况呢？
2. nf_conntrack 模块对 TCP 链接进行追踪，然后 nf_conntrack 的表有限制，表满了就丢包，这个因导致了服务器出现大量的 TIME_WAIT 状态，但为什么反应到 TPS 是锯齿状呢？一会儿好，一会儿坏，就算是 nf_conntrack 表会释放，难道还会瞬时释放很多，这样 TPS 就上去了，然后又满了，TPS 又下降？

思考题
1.如何在分析一通后，最后定位到防火墙？
因为老师在经过对操作系统的 CPU、I\O、内存等资源还有数据库、Tomcat、Nginx 等监控数据没有发现什么问题，最后定位到网络连接状态有问题，即出现了大量的 timewait 状态的链接，然后老师想通过修改 TCP 相关的参数来达到复用处于 timewait 状态的链接（这些参数的本质是释放服务端的句柄和内存资源，但不能释放端口，而 源IP+源端口+目的IP+目的端口+协议号才是 TCP 五元组），修改完后没有解决问题

然后老师分析客户端主动断开时，服务端也会处于 timewait 状态（这块是我疑惑的，应该是主动断开链接的一方才会处于 timewait 状态），然后打开了 Nginx 的 proxy_ignore_client_abort 配置，即让 Nginx 忽略掉客户端主动断开时报的错，但问题还是没有解决，然后把 Nginx 和 Nginx 所在服务器也换了，问题没有解决。

开始考虑操作系统层面，网络收发数据那儿可以通过查看发送端和接收端的 Recv_Q 和 Send_Q 这四个队列是否有值，来判断瓶颈点，然后没有发现问题。

在最后才考虑防火墙了

2.为什么 timewait 的 TCP 链接只是问题的现象？
因为能引起链接处于 timewait 状态的原因还是有很多的，这就需要不断透过现象看本质，根据不断地排查锁定最根本的原因</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/9f/c2/3d1c2f88.jpg" width="30px"><span>蔡森冉</span> 👍（9） 💬（1）<div>感觉学到了什么，又感觉好像都不懂，看完估计前面的也忘了差不多了。这真是要不断时间和经验的积累，总结方法。但是一点记住的就是全局--定向</div>2020-03-26</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（4） 💬（1）<div>
既然跟加入的nginx没有关系，那么第一次性能测的时候为啥没有发现有这种性能问题呢？</div>2021-01-14</li><br/><li><img src="" width="30px"><span>Geek6198</span> 👍（3） 💬（1）<div>现象：
	* 测试环境压测曲线正常，线上环境曲线杂乱
	* “TPS 在上升到一个量级的时候就会掉下来，然后再上到同样的量级再掉下来，非常规律”
	* “响应时间，在第一次 TPS 掉下来之后，就变得乱七八糟了。响应时间不仅上升了，而且抖动也很明显”
检查过程：
	1. 问题检查
		* 看操作系统CPU&#47;io&#47;memory&#47;net
	 	* 看数据库、tomcat&#47;nginx
	2. 第1阶段结论： 网络连接有问题
		* 发现了大量timewait
	3. 尝试优化
		* timewait是发起断开后的一个状态，修改服务端TCP相关配置
			1. timewait资源允许重用+快速回收 等
		* 修改nginx，只做转发，去除其它逻辑
		* 将nginx部署到另一台服务器上
		* 上述都没发现问题===》防火墙还没看
	 	* 关闭防火墙，服务TPS正常
	4.  第2阶段结论：瓶颈在防火墙
	5. 问题分析
		* dmesg 查下系统日志
		* 发现 nf_conntrack 数据满了
		* 查文档，知道其是干什么的；怎么改
		* 修改配置，重新打开防火墙==》服务正常
	6.  结束：瓶颈处理完成</div>2021-11-30</li><br/><li><img src="" width="30px"><span>Geek_6a9aeb</span> 👍（2） 💬（1）<div>老师，linux  tcp连接的限制(最大不能超过65535) ，对吗？ 既然nf-conntrack默认也是65535 对最大tcp连接对应的？  这边没有看到 系统究竟建立了多少tcp连接，如果是超过65535个，那么丢包是合理的吧？</div>2021-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fe/26/c675c4db.jpg" width="30px"><span>浩祥</span> 👍（2） 💬（2）<div>如果用1.5个月做性能测试，那就不要做了，1.5个月一个全新的产品可以上线了，预期线下费时，从投入产出比看，不如灰度放量，让实际场景暴露问题</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fa/20/0f06b080.jpg" width="30px"><span>凌空飞起的剪刀腿</span> 👍（2） 💬（1）<div>想起了自己以前处理iptables限制tcp  syn次数的性能调优，</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bc/25/1c92a90c.jpg" width="30px"><span>tt</span> 👍（2） 💬（1）<div>说TIME_WAIT是现象，是因为它只是“果”，导致它的“因”有很多可能，就是本课里老师采取的多种尝试。

当然，从分析链路的角度来说，它是TPS不稳的一个中间“因”，但还不能作为全局——定向分析的最终定位，所以是“现象。”</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（1） 💬（1）<div>分析思路很重要，还有分析问题的时候不要着急</div>2021-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/45/33/cdea4bca.jpg" width="30px"><span>zwm</span> 👍（1） 💬（1）<div>看不大明白只感觉nb，要学习的太多了</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/ab/a5f88914.jpg" width="30px"><span>kubxy</span> 👍（1） 💬（1）<div>老师，请教您一个问题：
按照TCP四次挥手的过程，timewait应该出现在主动断开连接的一方。而您在第二次尝试中说“考虑到当客户端主动断开时，服务器上也会出现大量的timewait”。这句描述是否不准确，如果是客户端主动断开连接，那么timewait应该出现在客户端上，而不是服务器上。</div>2020-02-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKHzrvlV4HLmR5IWUiad4sqich3QZXxWRxFicvqxPtRaWITLibic16eibRaJia1FxRjq81Pcs2NsB5Hg1WoQ/132" width="30px"><span>枫林听雪落</span> 👍（0） 💬（2）<div>向各位请教一下，tps出现规律性的突然降低，对应的响应时间出现突然的升高，整体资源没有怎么使用，但是网络连接出现很多wait_timeout。这种情况应该从什么地方进行分析和调整呢？</div>2023-04-11</li><br/><li><img src="" width="30px"><span>学员141</span> 👍（0） 💬（1）<div>老师，我们也是ngnix cpu迅速增长100%，添加的实例网关主机都比应用的多了，我看了我们服务器防火墙是关闭的，是不是就不是防火墙影响导致的？
   Loaded: loaded (&#47;usr&#47;lib&#47;systemd&#47;system&#47;firewalld.service; disabled; vendor preset: enabled)
   Active: inactive (dead)
     Docs: man:firewalld(1)
</div>2021-08-02</li><br/><li><img src="" width="30px"><span>学员141</span> 👍（0） 💬（1）<div>停了这个，感觉我们最近遇到的问题有点像，也是nginx也是单纯转发，CPU一下子就接近100了，加的服务器比应用还要多，太奇怪了，当时没有往防火墙上考虑，毕竟是全公司都一样的防火墙</div>2021-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/31/08216356.jpg" width="30px"><span>努力努力再努力</span> 👍（0） 💬（1）<div>压测机器怎么看有没有出现网络瓶颈？导致发的请求有限，测不出服务最大性能水平</div>2020-08-06</li><br/>
</ul>