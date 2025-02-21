在正式开讲前，我们先来看看到现在为止HTTP手头都有了哪些“武器”。

协议方面，HTTPS强化通信链路安全、HTTP/2优化传输效率；应用方面，Nginx/OpenResty提升网站服务能力，WAF抵御网站入侵攻击，讲到这里，你是不是感觉还少了点什么？

没错，在应用领域，还缺一个在外部加速HTTP协议的服务，这个就是我们今天要说的CDN（Content Delivery Network或Content Distribution Network），中文名叫“内容分发网络”。

## 为什么要有网络加速？

你可能要问了，HTTP的传输速度也不算差啊，而且还有更好的HTTP/2，为什么还要再有一个额外的CDN来加速呢？是不是有点“多此一举”呢？

这里我们就必须要考虑现实中会遇到的问题了。你一定知道，光速是有限的，虽然每秒30万公里，但这只是真空中的上限，在实际的电缆、光缆中的速度会下降到原本的三分之二左右，也就是20万公里/秒，这样一来，地理位置的距离导致的传输延迟就会变得比较明显了。

比如，北京到广州直线距离大约是2000公里，按照刚才的20万公里/秒来算的话，发送一个请求单程就要10毫秒，往返要20毫秒，即使什么都不干，这个“硬性”的时延也是躲不过的。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（32） 💬（3）<div>1.自建成本太高，一般的公司玩不起
2.cache-control允许缓存的动态资源可以被CDN缓存。不允许缓存的动态资源会回源，虽然老师课上没讲，感觉回源的路径会被优化。</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0d/40/f70e5653.jpg" width="30px"><span>前端西瓜哥</span> 👍（22） 💬（5）<div>如果请求的是动态资源，走 CDN 貌似会更慢（因为无法缓存，CDN到源站多了握手过程）？

我想到两个方案：
（1）静态资源都放到一个域名里，然后这个域名使用 CDN 缓存加速。动态资源则使用另一个域名，不进行 CDN 缓存，直接访问源站。
（2）让动态资源也走 CDN，像老师说的那样， CDN 有高速网络直连源站，速度也能提高，但这里貌似也是会有不少带宽支出。

我想知道实际中，请求动态资源具体到底是怎么考虑，一般使用什么方案？</div>2019-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/11/e7/044a9a6c.jpg" width="30px"><span>book尾汁</span> 👍（8） 💬（1）<div>1 是的自建成本很高
2 虽然是动态资源会回源，但是用户通过GSLB得到的边缘节点的ip也是离用户较近的，边缘节点到中心 中心节点到源站的网络也是很快的，综合来说还是要比用户直接访问快点。支持动态加速的CDN就更快了，直接规划出一条到源站的最优路径
</div>2019-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（7） 💬（1）<div>我们公司就是生产大量视频 每天几T视频 不用cdn成本可想而知 不过每次招标换厂家都涉及视频搬迁</div>2019-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/45/e4314bc6.jpg" width="30px"><span>magicnum</span> 👍（5） 💬（1）<div>CDN不仅有专线，还可以进行边缘计算。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（4） 💬（1）<div>网站也可以自建同城、异地多处机房，构建集群来提高服务能力，为什么非要选择 CDN 呢？
确实可以，不过建大了，就成了一个CDN。

对于无法缓存的动态资源，你觉得 CDN 也能有加速效果吗？
也有加速效果，不过要注意设置好缓存过期时间，不宜太长。如果不设缓存，内容由CDN回源去源站拉取，链路上专用网络可能快一些。对于缓存不可接受的业务，最好就不要用CDN了。</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d9/78/8a328299.jpg" width="30px"><span>佳佳大魔王</span> 👍（4） 💬（2）<div>问题一，我觉得会造成数据同步困难的问题，另外在网站更新的时候，消耗的资源也比较多</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>1：网站也可以自建同城、异地多处机房，构建集群来提高服务能力，为什么非要选择 CDN 呢？
钱决定的，成本收益比导致选择CDN，假如自建更省钱那一定会选择自建。首先，小公司自建不起，没有这么多人力、财力、技术，用多少买多少多香。大公司觉得自建更好，此时就变成了使用自己的CDN。

2：对于无法缓存的动态资源，你觉得 CDN 也能有加速效果吗？
无法缓存的资源，只能回源获取，正好能够利用CDN与源服务器之间的高速通道（看评论才知道），也能起到加速的效果吧！
话说什么动态资源不能够缓存？自建机房，异地多机房不是什么都有了嘛？只是又引入了一致性问题。</div>2020-04-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>学习了，干货满满</div>2023-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/67/8a/babd74dc.jpg" width="30px"><span>锦</span> 👍（1） 💬（2）<div>现实中为了减少回源率，降低宽带费用，一般cdn厂商也会提供伪源，那云厂商是怎么解决这个回源问题的呢？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/57/6e/b6795c44.jpg" width="30px"><span>夜空中最亮的星</span> 👍（1） 💬（1）<div>老师，我又回来啦，😄</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（1） 💬（1）<div>1.网站也可以自建同城、异地多处机房，构建集群来提高服务能力，为什么非要选择 CDN 呢？
因为CDN有大量边缘节点，网站只需要专注于自身业务，无需关心早专业的CDN复杂调度逻辑。
2.对于无法缓存的动态资源，你觉得 CDN 也能有加速效果吗？
有一定的效果，因为动态资源可以走cdn专线回源。</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/75/aa/21275b9d.jpg" width="30px"><span>闫飞</span> 👍（1） 💬（3）<div>TB级别的硬盘看起来也不是特别高端厉害的样子，因为普通的PC机也标配TB级SATA盘或者512GB SSD了吧。我猜CDN厂商是不是需要用专有的服务器硬盘保证比较长的服务寿命，还是大家就到市面上买买普通的硬盘挂上去就用了?</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d9/78/8a328299.jpg" width="30px"><span>佳佳大魔王</span> 👍（1） 💬（1）<div>问题二，文章指出了如果动态资源指定了 Cache-Control  那么也可以在很短时间内缓存
我觉得在这种情况比较有用：打开一个网站，打到一半的时候关闭，此时服务器已经开始了运算，当我们在很短时间内再次打开相同的网站时，很快就进入了</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f2/35/c3589990.jpg" width="30px"><span>北冥有鱼</span> 👍（0） 💬（1）<div>1.自建多地缓存集群，成本巨高，只有少数top级互联网公司承担的起。
2.CDN依托于自己搭建的网络，通过计算最优路由来实现加速效果。另外还能优化跨运营商访问，省去了源站的BGP带宽开销</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（0） 💬（1）<div>1.成本高，维护困难；

2.数据一致性要求不高，同步慢等，可以设置短时间缓存</div>2021-06-28</li><br/><li><img src="" width="30px"><span>牛</span> 👍（0） 💬（1）<div>CDN已经是一项互联网领域的基本服务了。对于受众分布广泛，比如全国性、全世界性的互联网产品，都用得上，而且费用还不便宜。那些个视频网站，这项开支巨大。</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/60/f5439f04.jpg" width="30px"><span>Geek_dn82ci</span> 👍（0） 💬（1）<div>问题1:主要是互联网形态的业务终端用户分布范围太广，还需要考虑一些边远地区甚至三大运营商覆盖不到的地方，这时候考验cdn的节点和运营商覆盖了，此外尽可能优化终端体验也是产品的一大竞争优势
问题2:对于动态内容可以采用动态加速或者所谓的“全站加速”，即通过cdn服务商提供动态内容请求的最优回源路线</div>2020-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/d7/b102034a.jpg" width="30px"><span>do it</span> 👍（0） 💬（1）<div>1、为了省钱
2、线路优化</div>2020-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/43/1aa8708a.jpg" width="30px"><span>子杨</span> 👍（0） 💬（3）<div>老师好，对于 CDN 而言，如何判断是源站造成的异常还是 CDN 的异常？为了监控源站是否异常，我们目前采用的是在源站放一个文件，不断的去探测文件的长度，一致的话就表示正常。总觉得会有更好的办法。。。</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（0） 💬（1）<div>2019-10-05 打卡。</div>2019-10-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/62/dc/8876c73b.jpg" width="30px"><span>moooofly</span> 👍（0） 💬（1）<div>关于国内，国外 CDN 选型不知道有何建议和推荐？之前了解过 aws 的 cloudfront ，网宿和阿里云 CDN，公司实际使用情况，国外部分用了 cloudfront ，国内上了网宿，后面打算国内外都用网速，而阿里云也一致在考虑之内</div>2019-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/9d/abb7bfe3.jpg" width="30px"><span>Carson</span> 👍（0） 💬（1）<div>1.自建多地业务源站，花费的人力，物力，财力要比使用cdn都多不止多少倍，我猜cdn当时就是这么产生的
2.动态资源cdn缓存没有问题，关键是要控制好缓存时间和业务调用逻辑，别张三访问命中了李四的信息了</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/af/e6/9c77acff.jpg" width="30px"><span>我行我素</span> 👍（0） 💬（1）<div>1.成本问题还有维护问题，既然已有现成的何必自找麻烦
2.感觉可以优化访问的线路</div>2019-08-21</li><br/>
</ul>