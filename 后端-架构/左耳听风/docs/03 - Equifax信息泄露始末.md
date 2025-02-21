你好，我是陈皓，网名左耳朵耗子。

相信你一定有所耳闻，9月份美国知名征信公司Equifax出现了大规模数据泄露事件，致使1.43亿美国用户及大量的英国和加拿大用户受到影响。今天，我就来跟你聊聊Equifax信息泄露始末，并对造成本次事件的原因进行简单的分析。

# Equifax信息泄露始末

Equifax日前确认，黑客利用了其系统中未修复的Apache Struts漏洞（CVE-2017-5638，2017年3月6日曝光）来发起攻击，导致了最近这次影响恶劣的大规模数据泄露事件。

作为美国三大信用报告公司中历史最悠久的一家，Equifax的主营业务是为客户提供美国、加拿大和其他多个国家的公民信用信息。保险公司就是其服务的主要客户之一，涉及生命、汽车、火灾、医疗保险等多个方面。

此外，Equifax还提供入职背景调查、保险理赔调查，以及针对企业的信用调查等服务。由于Equifax掌握了多个国家公民的信用档案，包括公民的学前和学校经历、婚姻、工作、健康、政治参与等大量隐私信息，所以这次的信息泄露，影响面积很大，而且性质特别恶劣。

受这次信息泄露影响的美国消费者有1.43亿左右，另估计约有4400万的英国客户和大量加拿大客户受到影响。事件导致Equifax市值瞬间蒸发掉逾30亿美元。

根据《华尔街日报》（The Wall Street Journal）的观察，自Equifax在9月8日披露黑客进入该公司部分系统以来，全美联邦法院接到的诉讼已经超过百起。针对此次事件，Equifax首席执行官理查德·史密斯（Richard Smith）表示，公司正在对整体安全操作进行全面彻底的审查。

事件发生之初，Equifax在声明中指出，黑客是利用了某个“U.S. website application”中的漏洞获取文件。后经调查，黑客是利用了Apache Struts的CVE-2017-5638漏洞。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/7a/7b/ee2e9302.jpg" width="30px"><span>廖雪峰</span> 👍（275） 💬（16）<div>struts的开发就是弱者，类似eval()的东西默认就敢开</div>2017-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/77/423345ab.jpg" width="30px"><span>Sdylan</span> 👍（119） 💬（0）<div>#Equifax信息泄露始末笔记
1.使用开源的框架必须实时关注其动态，特别是安全漏洞方面
2.任何公开的入口，都必须进行严格的安全检查
3.框架的选型十分重要，必须将安全考察进去</div>2018-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/d5/88beb15a.jpg" width="30px"><span>李志博</span> 👍（61） 💬（0）<div>Struts 漏洞那么多，最好的办法就是赶快切换spring mvc</div>2017-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（33） 💬（5）<div>使用开源框架，千万要注意其BUG和安全性，去年我们发现fastjson有个安全问题，整个公司在一个星期内都紧急检查和升级。现在github做得很好的一点是，会对我们的代码进行安全扫描，发现有包含安全性问题的版本的代码的时候，会给出升级提醒，在大一点的公司里也可以自己做这种安全扫描和提醒。</div>2018-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8e/c4/8d1150f3.jpg" width="30px"><span>Richie</span> 👍（19） 💬（0）<div>事件：
大规模数据泄露

主角：
Equifax —— 美国三大信用报告公司中历史最悠久的一家，其掌握了多个国家公民的信用档案，包括公民的学前、学校经历、婚姻、工作、健康、政治参与等大量隐私信息。

影响面：
致使1.43亿美国用户及大量的英国和加拿大用户受到影响，导致Equifax市值蒸发掉逾30亿美元。

事件原因：
在Struts高危漏洞披露后两个月仍没有升级版本及修复漏洞，导致被黑客利用。

根本原因：
Equifax 的安全意识太弱（还有很多其他未修复的漏洞）</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（18） 💬（0）<div>换spring-boot😈</div>2018-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/64/04/18875529.jpg" width="30px"><span>艾尔欧唯伊</span> 👍（13） 💬（5）<div>很好奇，这些大牛是怎么注意到这些安全漏洞的。。。</div>2018-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a2/16/4c5de4fb.jpg" width="30px"><span>月伴寒江</span> 👍（12） 💬（0）<div>struts漏洞实在太多，补都补不赢，之前的项目后来都换成了Spring MVC。对于一些安全意识不高的企业，确实没什么人关注这些。</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/85/8a/031a6fd8.jpg" width="30px"><span>风起</span> 👍（12） 💬（0）<div>作为一个新员工，终于明白公司为什么有一个团队专门坐开源组建扫描评级， 还有为啥有代码安全扫描。</div>2018-06-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/97/4593cda8.jpg" width="30px"><span>MC</span> 👍（11） 💬（0）<div>哎，我的信息也在其中…</div>2017-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/65/af/e6bf880d.jpg" width="30px"><span>yaoel</span> 👍（7） 💬（0）<div>有时项目因为赶进度，会决定先上线再加强安全问题！但经常就直接搁置了...虽然当时省了一些力，却可能（一定）在n年会付出惨痛的代价！所以安全问题不容忽视</div>2017-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f8/df/3171db9f.jpg" width="30px"><span>Lorem</span> 👍（6） 💬（0）<div>课代表来了
笔记03

1.使用开源的框架必须实时关注其动态，特别是安全漏洞方面
2.任何公开的入口，都必须进行严格的安全检查
3.框架的选型十分重要，必须将安全考察进去</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/b7/b5dba54d.jpg" width="30px"><span>iDev_周晶</span> 👍（6） 💬（0）<div>没想到 Struts2 现在还有那么大的份额</div>2018-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9e/d3/abb7bfe3.jpg" width="30px"><span>wholly</span> 👍（5） 💬（0）<div>使用开源软件，一方面需要及时关注开源社区发布的安全预警及版本迭代时的changelog，另一方面，如果使用过程发现问题，及时向开源反馈，做到使用开源，回馈开源。</div>2019-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/74/53/54fb0b05.jpg" width="30px"><span>渡鹤影</span> 👍（5） 💬（0）<div>今天网传12306信息也泄露了……</div>2018-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/df/6c/5af32271.jpg" width="30px"><span>Dylan</span> 👍（5） 💬（0）<div>吸取教训了～安全意识不管是大公司或者像我现在自己创业的项目，对于安全总是想得很侥幸，但是一旦爆发出来可能就对公司产生致命影响了</div>2018-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/4d/29a93491.jpg" width="30px"><span>niuniu</span> 👍（4） 💬（0）<div>两个critical的漏洞都是华人上报的</div>2019-09-06</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLAHCRt6dBUDTFX4EotyV5NDbYiaUXH109SOdRprLky1PUc9jm2K7QvoCpkZuCyqMCNSogUpdFzMJw/132" width="30px"><span>Geek_ce6971</span> 👍（2） 💬（0）<div>log4j JNDI 漏洞引起的动静也不小</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（2） 💬（0）<div>安全意识薄弱是大部分工程师的通病，业务开发主要关注于增删改查！公司整体安全意识薄弱，依赖中间件未深入研究关注，只是停留在基本使用上！提高自己的认知，提高公司的整体意识非常重要！</div>2021-09-28</li><br/><li><img src="" width="30px"><span>Fallon</span> 👍（2） 💬（0）<div>从Equifax的事件，我想到另外一个问题，一个企业该如何做好漏洞管理。不只是软件包存在漏洞，OS也存在漏洞，大部分漏洞都是通过补丁进行修复的。你使用的软件包越多，OS越多，修复的频率就会非常高，不是在打补丁，就是在打补丁的路上，对于架构设计不合理的应用，更有可能需要停机另外补丁修复，成本非常高。那么漏洞应该怎么管理呢？欢迎大家来聊聊</div>2020-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/85/db/f978ddcd.jpg" width="30px"><span>BeginYan</span> 👍（2） 💬（0）<div>发现java开发的项目的漏洞貌似比其他语言比如Python要多。。</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/37/51/94/7f2357dd.jpg" width="30px"><span>苏非辞</span> 👍（1） 💬（0）<div>看不懂咋整😭😭</div>2023-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/23/18/4284361f.jpg" width="30px"><span>易飞</span> 👍（1） 💬（0）<div>能发现漏洞的都是大佬</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/3b/47d832f4.jpg" width="30px"><span>书豪</span> 👍（1） 💬（0）<div>前期不注重，后期懒得管，丢下的隐患，迟早要暴露</div>2020-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/03/4d5c017f.jpg" width="30px"><span>艺漫漫</span> 👍（1） 💬（0）<div>最近出了一个微信数据结构和加密算法被吕某用反编译手段破了 这也是安全事故了吧。看来程序员在写代码或用算法是都需要考虑这些安全问题了</div>2020-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/qc4pasMqznVJfdcpltOEbwVHH5zF1NUvKYuIzWvQMqxHEPUH6QpF8VDm0XNkaWwvHSWhEYTNCY3yNgCJSQQAvw/132" width="30px"><span>孙剑平</span> 👍（1） 💬（0）<div>现在大公司都特别重视安全，敏感文字都需要打码</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（1） 💬（1）<div>安全意识为零，再多的漏洞也补不过来</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/68/006ba72c.jpg" width="30px"><span>Untitled</span> 👍（1） 💬（0）<div>怎么才能有加强自己对互联网各个方面都有所见解？像我这种只会使用一些编程语言，可惜专业也不是IT方面的，真希望有天能站在一个高度上看待问题，现在在恶补网络知识，后面想从这个点开始扩展自己的视野</div>2018-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9e/6e/c4fa7cbc.jpg" width="30px"><span>二师哥</span> 👍（1） 💬（0）<div>安全无小事，
但是创业公司，更关注的项目落地和功能实现。这个就很难办？
作为大企业，安全意识这么差就不能理解了。
我想问下，创业公司，团队就几号人物，如何在安全上有所防范，是不是就应该先做功能开发，上线了再说！</div>2018-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ab/10/b812ff3e.jpg" width="30px"><span>Hesher</span> 👍（1） 💬（0）<div>Spring MVC 借机上位</div>2018-04-26</li><br/>
</ul>