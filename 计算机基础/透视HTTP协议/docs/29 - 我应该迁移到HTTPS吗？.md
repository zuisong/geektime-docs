今天是“安全篇”的最后一讲，我们已经学完了HTTPS、TLS相关的大部分知识。不过，或许你心里还会有一些困惑：

“HTTPS这么复杂，我是否应该迁移到HTTPS呢？它能带来哪些好处呢？具体又应该怎么实施迁移呢？”

这些问题不单是你，也是其他很多人，还有当初的我的真实想法，所以今天我就来跟你聊聊这方面的事情。

## 迁移的必要性

如果你做移动应用开发的话，那么就一定知道，Apple、Android、某信等开发平台在2017年就相继发出通知，要求所有的应用必须使用HTTPS连接，禁止不安全的HTTP。

在台式机上，主流的浏览器Chrome、Firefox等也早就开始“强推”HTTPS，把HTTP站点打上“不安全”的标签，给用户以“心理压力”。

Google等搜索巨头还利用自身的“话语权”优势，降低HTTP站点的排名，而给HTTPS更大的权重，力图让网民只访问到HTTPS网站。

这些手段都逐渐“挤压”了纯明文HTTP的生存空间，“迁移到HTTPS”已经不是“要不要做”的问题，而是“要怎么做”的问题了。HTTPS的大潮无法阻挡，如果还是死守着HTTP，那么无疑会被冲刷到互联网的角落里。

目前国内外的许多知名大站都已经实现了“全站HTTPS”，打开常用的某宝、某东、某浪，都可以在浏览器的地址栏里看到“小锁头”，如果你正在维护的网站还没有实施HTTPS，那可要抓点紧了。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（70） 💬（1）<div>感谢老师的这篇文章！今天我成功将个人博客网站迁移到 HTTPS 了，高兴。
我之前一直没有把网站迁移到 HTTPS ，主要是因为需要学很多东西，比如如何配置 nginx，https 的相关知识，证书的申请等等（做开发的都知道，配置这种东西真的很麻烦）。此外误解申请证书是要花很多钱的（看了这章才知道有这么方便简单的免费证书），另外又觉得我这个只是个个人技术博客网站，http 其实也可以，就一直放在那里不做了。
不过学了这章和前面的内容，就明白的 HTTPS 大概的过程，也学会了迁移 HTTPS 需要注意的一些细节。今天也是成功将自己的个人博客迁移到 HTTPS 了，期间也是各种问题不断，也是一一解决，折腾了很久。不过看到自己的网站上在也没有“不安全”的标签，也是觉得非常有成就感。</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/10/bb/f1061601.jpg" width="30px"><span>Demon.Lee</span> 👍（13） 💬（1）<div>安全篇学习完了，大部分都没记住，看样子，起码得刷3遍以上🐮</div>2019-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（7） 💬（1）<div>个人博客网站很早就用上了https，但老师说的那些Nginx优化参数没有用上，我这就去加上。</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/49/585c69c4.jpg" width="30px"><span>皮特尔</span> 👍（6） 💬（2）<div>ESNI把请求域名也加密了，GFW的拦截是不是就失效了？</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/35/51/c616f95a.jpg" width="30px"><span>阿锋</span> 👍（4） 💬（2）<div>上文提到的虚拟主机，跟正向代理，反向代理，有什么区别。</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（3） 💬（1）<div>老师你好，刚才搞了半天编译好了Nginx新版本With OpenSSL才开启TLSv1.3，不知道老师是怎么安装这些软件的，有什么好的建议吗？
nginx version: nginx&#47;1.16.0
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC) 
built with OpenSSL 1.1.1  11 Sep 2018</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/b0/d3/200e82ff.jpg" width="30px"><span>功夫熊猫</span> 👍（2） 💬（1）<div>vue-cil的vue-config里可以直接选择发送协议是http还是https，只需要在https选项后设置为true就可以，但好像还是需要数字证书申请之类的</div>2021-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>大势所趋，那就要跟上，我司已切😄</div>2020-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>天才们努力奋斗，凡人坐享其成</div>2023-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b0/c4/0aae22ef.jpg" width="30px"><span>疯狂的书生</span> 👍（1） 💬（2）<div>我主要做嵌入式软件端的开发，最近开发个物联网的项目，碰上了一个有关SNI的问题。
使用移远4G模组Open方案，https连服务器，实名手机SIM卡https post请求均正常；但使用物联网卡https post请求，TCP三次握手后，进入SSL握手阶段就连接断开了，(物联网卡没有设置白名单)。后来在技术支持的帮助下设定了开启SNI，稀里糊涂的此问题就修复了。
看到这个课程的SNI，才隐约了解这个参数的作用，看来我还要回去继续复盘一下这个问题，更深入巩固一下SSL &#47; 证书相关知识。</div>2022-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/81/2331554c.jpg" width="30px"><span>Lostoy</span> 👍（1） 💬（1）<div>老师能否说一下浏览器&#47;移动端APP和服务端进行https请求的完整加密配置和通信过程？上面只说了服务端的配置，难道移动端APP或者浏览器不用做任何配置？如果不用配置那整个安全通信机制是什么样的？为什么只用服务器配置就可以了？</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/6a/6b96edbd.jpg" width="30px"><span>学不动了</span> 👍（1） 💬（1）<div>这两章对于我这种门外汉来说，真的是干货满满</div>2021-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/3c/d6fcb93a.jpg" width="30px"><span>张三</span> 👍（1） 💬（1）<div>1. 公司有一台服务器的应用配置了http和https，用不同的端口来区分，可是chrome每次都是默认用https，所以就会出现不能访问http的问题，而ie就不会，不知道和HSTS有没有关系？</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（1） 💬（1）<div>1. 结合你的实际工作，分析一下迁移 HTTPS 的难点有哪些，应该如何克服？
(说下我经历的）
a. 梳理所有外部连接是否为https。因为切换https后，有的浏览器会有安全机制限制发起http请求。
b. 开启http强制跳转https后，如果httpclient(代码)没有处理302状态，那么接口会调不通。要通知外部接口调用变更https。
先在测试环境开启强制跳转https强制跳转。生产环境有一个共存过度期，最后再强制跳转。</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（1） 💬（2）<div>2、TLS1.3的pre-shared-key，实现0-RTT；OCSP Stapling；</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/91/d0/35bc62b1.jpg" width="30px"><span>无咎</span> 👍（0） 💬（1）<div>更新 @2024&#47;05&#47;09: nginx.org 和 apache.org 已经使用https了，颁发者就是Let&#39;s Encrypt
```
Common Name (CN)	R3
Organization (O)	Let&#39;s Encrypt
Organizational Unit (OU)	&lt;Not Part Of Certificate&gt;
```</div>2024-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/23/6c/785d9cd3.jpg" width="30px"><span>Snooker</span> 👍（0） 💬（1）<div>1.我理解的大致分为运维侧和业务侧，运维配置不太懂，大概的：常规配置、安全策略配置、证书定期更新；
业务侧，具体跟场景有关，一般业务系统会有多个域名（升级1个或多个），主要全业务量的回归测试，正常访问不报错，不影响体验、cdn静态资源缓存？ 同时准备好应急回退方案
2.参考上一讲提到的性能优化方案，软件部分争取一步到位：协议优化，TLS版本、加密套件排序等；证书优化，返回ocsp的ca响应；本章节也提到的回话复用；硬件部分可以根据公司情况有矿就加满配置；
其他硬件优化</div>2024-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>你好，我想请教一下，是不是NG到upstream这一跳还是用明文传输的？</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/6d/ea/2c5fcdb1.jpg" width="30px"><span>睡觉也在笑</span> 👍（0） 💬（1）<div>老师，内部spring boot写的微服务之间有什么https的优化方案吗？因为是银行领域，所以监管部门有一些强制的安全基线。因此我想问一下有没有什么支持国密算法的好的方案。sm2算法是椭圆曲线的一种扩展算法，但是不知道需要怎样的改造才能支持TLS1.3.</div>2021-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a9/12/e041e7b2.jpg" width="30px"><span>Ping</span> 👍（0） 💬（1）<div>老师不知道您了解S2N吗，能不能讲解下什么是S2N?</div>2020-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/07/53/05aa9573.jpg" width="30px"><span>keep it simple</span> 👍（0） 💬（1）<div>请教下老师，启用了session ticket，但注意到new session ticket有效期只有300秒，这个参数能改长吗？我们用的是阿里云的SLB</div>2020-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cb/9d/2bc85843.jpg" width="30px"><span>　　　　　　　鸟人</span> 👍（0） 💬（1）<div>请问如果网站HTTPS证书过期会怎么样？</div>2019-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（0） 💬（1）<div>Mac 电脑查看 openssl 的版本，发现是这个：LibreSSL 2.6.5

LibreSSL 怎么和 openSSL 版本对应的？</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/86/e3/a31f6869.jpg" width="30px"><span> 尿布</span> 👍（1） 💬（0）<div>”HSTS“无法防止黑客对第一次访问的攻击，所以Chrome等浏览器还内置了一个”HSTS preload“的列表（chrome:&#47;&#47;net-internals&#47;#hsts），只要域名再这个列表里，无论何时都会强制使用HTTPS访问

之前在实验室环境访问HTTP协议时可以看到请求头里有”Upgrade-Insecure-Requests: 1“，它就是GSP的一种，表示浏览器支持升级到HTTPS协议</div>2020-09-10</li><br/>
</ul>