你好，我是陈皓，网名左耳朵耗子。

上节课中，我们讲了Equifax信息泄露始末，并对造成此次事件的漏洞进行了分析。今天，我们就来回顾一下互联网时代的其他几次大规模数据泄露事件，分析背后的原因，给出解决这类安全问题的技术手段和方法。

# 数据泄露介绍以及历史回顾

类似于Equifax这样的大规模数据泄露事件在互联网时代时不时地会发生。上一次如此大规模的数据泄露事件主角应该是雅虎。

继2013年大规模数据泄露之后，雅虎在2014年又遭遇攻击，泄露出5亿用户的密码，直到2016年有人在黑市公开交易这些数据时才为大众所知。雅虎股价在事件爆出的第二天就下跌了2.4%。而此次Equifax的股价下跌超过30%，市值缩水约53亿。这让各大企业不得不警惕。

类似的，LinkedIn在2012年也泄露了6500万用户名和密码。事件发生后，LinkedIn为了亡羊补牢，及时阻止被黑账户的登录，强制被黑用户修改密码，并改进了登录措施，从单步认证增强为带短信验证的两步认证。

国内也有类似的事件。2014年携程网安全支付日志存在漏洞，导致大量用户信息如姓名、身份证号、银行卡类别、银行卡号、银行卡CVV码等信息泄露。这意味着，一旦这些信息被黑客窃取，在网络上盗刷银行卡消费将易如反掌。

如果说网络运维安全是一道防线，那么社会工程学攻击则可能攻破另一道防线——人。2011年，RSA公司声称他们被一种复杂的网络攻击所侵害，起因是有两个小组的员工收到一些钓鱼邮件。邮件的附件是带有恶意代码的Excel文件。

当一个RSA员工打开该Excel文件时，恶意代码攻破了Adobe Flash中的一个漏洞。该漏洞让黑客能用Poison Ivy远程管理工具来取得对机器的管理权，并访问RSA内网中的服务器。这次攻击主要威胁的是SecurID系统，最终导致了其母公司EMC花费6630万美元来调查、加固系统，并最终召回和重新分发了30000家企业客户的SecurID卡片。

# 数据泄露攻击

以这些公司为例，我们来看看这些攻击是怎样实现的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/95/96/0020bd67.jpg" width="30px"><span>夏洛克的救赎</span> 👍（95） 💬（4）<div>当黑客的投入和收益大大不相符时，黑客也就失去了入侵的意义。

这句话一语道破真谛，一切行为都可以看做商业行为，用商业思维和方式解决。</div>2018-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/90/11/c6632e4d.jpg" width="30px"><span>陈斌</span> 👍（42） 💬（14）<div>皓哥，有个文章中的细节问题想问您。您提到的密钥自动更换机制，“在外部系统调用 100 次或是第一个小时后就自动更换加密的密钥”，在更换后怎么处理旧密钥加密的数据呢？全部解密然后用新密钥重新加密吗？对于后期越来越大量的数据，会不会负荷过重？如果不是我理解的方法，又是怎么处理的呢？期待您的解答，谢谢~</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/34/3f/4b6cd370.jpg" width="30px"><span>Viktor</span> 👍（36） 💬（1）<div>其实在安全这一块，非常多的大公司都做得不好。有个特别简单的列子，app端输出的api接口尽然暴漏用户的手机号信息和其他信息，我光是通过接口就获取到用户所有信息了，并且接口没有做当前用户认证，修改一个参数就可以访问其他用户信息。以前学习python的时候抓取过很多有名公司的信息，所以我在做自己公司项目的时候在这些方面都做了严格校验处理。</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/97/4593cda8.jpg" width="30px"><span>MC</span> 👍（26） 💬（0）<div>安全事故常用。我前同事与他人一起成立了针对计算机网络安全的保险公司。</div>2017-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/24/afb15de3.jpg" width="30px"><span>头发茂密</span> 👍（19） 💬（1）<div>有段时间最喜欢看的一部电影就是《没有绝对安全的系统》是一个黑客组织的故事。我认为主线思路是从内部和外部出发的。
内部：
第一，提升内部人员安全意识，规范内部人员使用数据权限。
第二，提升内部数据安全技术实力。
第三，内部人员模仿外部黑客对自己的系统进行模拟攻击，提高系统的攻防弹性，但是，要注意不能对系统造成损伤和数据破坏。

外部：
第一，定期跟进使用框架和版本的更新说明，对于已经发现的漏洞，短时间内迅速处理。
第二，利用经济学思维和技术手段，提高黑客攻击成本，但是也要平衡好维护成本。

初次阅读，只是粗浅的想到这么多，大家还有其他想法，欢迎一起讨论，我认为耗子前辈把我们聚在一起也是一种缘分大家可以一起学习一起成长。
</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/6e/c4fa7cbc.jpg" width="30px"><span>二师哥</span> 👍（13） 💬（0）<div>信息安全也是商业问题，
如果攻击成本高于收获成本，那么攻击者的行为便毫无意义。
如果赔偿成本低于安全成本，那么又何必浪费更多的资源和成本。
没有完全安全的系统，却可以有不断追求成功的解决方案！</div>2018-06-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e4/a0/73f6507e.jpg" width="30px"><span>转型很痛</span> 👍（12） 💬（0）<div>我参与的项目都是，赔偿小与安全，对安全问题在实际开发中往往都不重视，公司测试都是人工一个一个功能进行点击，完全没有接触过自动化测试。</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/aa/acbbedea.jpg" width="30px"><span>清水</span> 👍（9） 💬（1）<div>我想知道目前亚马逊，阿里做到了吗？这里不是抬杠只是咨询。新业务普遍是增长优先。这些安全要求会影响业务进度。而且项目都是有排期的。作为一线的领导怎么协调，怎么协调才好？求教。</div>2019-05-24</li><br/><li><img src="" width="30px"><span>哈软糖</span> 👍（7） 💬（0）<div>不同网站使用不同密码实在难以维护，想知道1password这类的密码管理软件安全不安全</div>2018-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c4/c9/90c8a53e.jpg" width="30px"><span>missa</span> 👍（7） 💬（0）<div>提高安全意识，做好系统的审计，关注相关开源系统的漏洞情况，及时更新升级。把控好风险，做到风控成本小于赔偿的成本。</div>2018-03-13</li><br/><li><img src="" width="30px"><span>delete is create</span> 👍（6） 💬（1）<div>您好 我是一名java后端程序员，在公司负责一些模块，平时自己开发一些感兴趣的个人web项目，但是对于web开发中的安全问题总是考虑不周到，比如SQL注入等等，您有针对开发者的安全书籍推荐吗？</div>2018-06-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2b/2b/bebf6eed.jpg" width="30px"><span>酱了个油</span> 👍（5） 💬（0）<div>各种最佳实践，赞</div>2018-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/22/71/9d6eab72.jpg" width="30px"><span>j0hnniang</span> 👍（4） 💬（0）<div>没有绝对安全的系统！</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/85/3a4b31fc.jpg" width="30px"><span>rjava</span> 👍（4） 💬（0）<div>安全无小事，防范与未然。学习了，同时还应该增加定期的安全演练来验证一系列的防护</div>2017-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9c/e9/5ba8b1a3.jpg" width="30px"><span>郭新鹏</span> 👍（3） 💬（0）<div>好想搞下公司的各种接口。</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/7e/08/dd205b4f.jpg" width="30px"><span>天行者阿七</span> 👍（2） 💬（0）<div>当黑客的投入和收益大大不相符时，黑客也就失去了入侵的意义。这是本质啊~！</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（2） 💬（0）<div>以前做客户端，没有什么安全意识存在；现在做了服务端，深知安全意识很重要很重要很重要</div>2019-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/a9/3f8c7418.jpg" width="30px"><span>冰糕不冰</span> 👍（2） 💬（0）<div>长见识了</div>2018-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/77/423345ab.jpg" width="30px"><span>Sdylan</span> 👍（2） 💬（0）<div>#从Equifax信息泄露看数据安全笔记
大意浏览全文，发现上一篇自己的留言，过于狭窄，没看到更宽的世界。此篇中提到的安全防范可以分为：安全意识和安全技术，很多时候不是技术不够，而是意识差了。
</div>2018-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/13/8bdd4b71.jpg" width="30px"><span>小侯子</span> 👍（2） 💬（0）<div>安全意识太差，讲的内容挺多，需要再消化消化</div>2018-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（1） 💬（0）<div>我对大规模数据泄漏印象比较深的可能是 CSDN 的那一次，作为一个程序员社区，居然犯了比较低级的密码明文保存错误……所以，CSDN 现在看上去也愈发业余了。

携程泄露的那次，比较有意思的是暴露了用户的开房记录。

数据泄漏估计会永远伴随着信息社会，比如最近的美军文件泄漏事件，当然也有人说可能是有意为之。

不知道现在的 GPT 是否可以帮助攻击或者防止数据泄露。

其实目前国内很多团队也在或明或暗的使用开源框架，谈不上及时的升级补丁，估计安全隐患也不少。

专栏最后的技术建议里面提到，首先是定义关键数据，并将其隔离到安全级别非常高的地方。

我看到的更多的是对于密级的定义过于宽泛，带来的问题就是工作效率的降低以及对于关键数据的保护不足。

可能大部分的公司最终都需要有专门的安全团队，或者外部的安全顾问。</div>2023-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（1） 💬（0）<div>多层防护确实重要，我们内网在搭建统一鉴权中心，防止内网网站被外网攻击！</div>2021-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/8e/7b/701c741f.jpg" width="30px"><span>难得自然萌</span> 👍（1） 💬（0）<div>自动化测试感觉在国内实践率很低的</div>2020-08-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/BJjGmy4ooNjeURBDhVeJ7EslNbyVd6jNricALVsx1QriczD2EXddKLkXxLQK02nExosCJdyfvicVcZwfpDk64iazmQ/132" width="30px"><span>style_月月</span> 👍（1） 💬（0）<div>app的信息泄漏挺严重的，你并不知道他们的日志会保存什么信息以及日志是否加密等</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/db/4d/8dec7917.jpg" width="30px"><span>迪</span> 👍（1） 💬（2）<div>很好奇开源软件的提供者需要对安全漏洞负责吗？尤其是法律意义上的负责。用户被泄露信息貌似也没有办法弥补损失。</div>2020-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9a/09/b90c93d6.jpg" width="30px"><span>名扬四海</span> 👍（1） 💬（0）<div>对于小公司来说，安全问题一般是不受重视的，更多是的实现业务逻辑的快速验证。
所以如果想搞好安全最好去大公司的安全部门吗？</div>2019-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/59/37/bd2de0a4.jpg" width="30px"><span>edisonhuang</span> 👍（1） 💬（0）<div>互联网上安全和速度总是一对矛盾，在追求效率的今天我们应该逐渐建立安全机制，树立安全意识。
因为当注重安全的时候不可避免的要加入很多权限控制，安全隔离的措施，从而在一定程度上会影响到迭代速度。由于今天国内的互联网竞争太过激烈，大家对速度的追求远胜于对安全的保护，因此导致国内未修复的安全漏洞远多于其他国家。但是安全也很重要，意识是关键</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/f4/244f0c5e.jpg" width="30px"><span>Rain</span> 👍（1） 💬（0）<div>前段时间刚在公司内部系统讨论过安全问题，耗子哥跟我们CTO的思路高度一致👍🏻</div>2018-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b4/96/d2481b7d.jpg" width="30px"><span>大黄</span> 👍（1） 💬（0）<div>安全这课非常受教，一直注重于业务应用的开发，安全意识差太多了。学了这堂课，才意识到安全的重要性。</div>2018-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/af/e6bf880d.jpg" width="30px"><span>yaoel</span> 👍（1） 💬（0）<div>总结的太好了 学习</div>2017-10-22</li><br/>
</ul>