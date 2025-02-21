上一节，我们看到了网站的一般访问模式。

当一个用户想访问一个网站的时候，指定这个网站的域名，DNS就会将这个域名解析为地址，然后用户请求这个地址，返回一个网页。就像你要买个东西，首先要查找商店的位置，然后去商店里面找到自己想要的东西，最后拿着东西回家。

**那这里面还有没有可以优化的地方呢？**

例如你去电商网站下单买个东西，这个东西一定要从电商总部的中心仓库送过来吗？原来基本是这样的，每一单都是单独配送，所以你可能要很久才能收到你的宝贝。但是后来电商网站的物流系统学聪明了，他们在全国各地建立了很多仓库，而不是只有总部的中心仓库才可以发货。

电商网站根据统计大概知道，北京、上海、广州、深圳、杭州等地，每天能够卖出去多少书籍、卫生纸、包、电器等存放期比较长的物品。这些物品用不着从中心仓库发出，所以平时就可以将它们分布在各地仓库里，客户一下单，就近的仓库发出，第二天就可以收到了。

这样，用户体验大大提高。当然，这里面也有个难点就是，生鲜这类东西保质期太短，如果提前都备好货，但是没有人下单，那肯定就坏了。这个问题，我后文再说。

**我们先说，我们的网站访问可以借鉴“就近配送”这个思路。**

全球有这么多的数据中心，无论在哪里上网，临近不远的地方基本上都有数据中心。是不是可以在这些数据中心里部署几台机器，形成一个缓存的集群来缓存部分数据，那么用户访问数据的时候，就可以就近访问了呢？
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（26） 💬（1）<div>搜了一圈儿，没找到cdn权威指南这本书，您是不是写错了？</div>2018-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/72/67/aa52812a.jpg" width="30px"><span>stark</span> 👍（23） 💬（2）<div>我有个疑问，CDN是内容分发系统，之前在NGINX的学习中，那个老师说主要是为了静态资源，我有点不理解，超哥能稍微解释一下么</div>2019-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/12/f799997f.jpg" width="30px"><span>ZACK</span> 👍（17） 💬（7）<div>由于多dc，静态资源图片同步是个很大的问题，因为网速，后来我们尝试用cdn去解决，但被公司一自称很牛的哥们否掉，原因是cdn只支持外网的，至今没有完全理解是否正确</div>2018-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/2c/92c7ce3b.jpg" width="30px"><span>易轻尘</span> 👍（5） 💬（1）<div>貌似cdn要访问的节点比直接的dns更多啊，要是内容命中率不高的话反而得不偿失。所以cdn的边缘节点是有像cache那样的缓存机制吧，最近最少访问之类的？</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/ac/37afe559.jpg" width="30px"><span>小毅(Eric)</span> 👍（3） 💬（2）<div>听了专栏20集,每天上班中午休息的时候听一级然后做记录. 感觉将的听上去明白,但是其实不明白.由于在工作中其实并没有碰到那么多关于网络优化的实例(仅仅做后开开发的工作),所以有点一知半解.感觉似懂非懂.不知道后面如何继续?</div>2019-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/cd/2c3808ce.jpg" width="30px"><span>Yangjing</span> 👍（2） 💬（1）<div>那 CDN 是怎么样把数据推送到到各个节点的呢？ 运营商给的规则吗</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（1） 💬（1）<div>文中说cdn部署在数据中心；但老师评论的回复提到：cdn在数据中心之外。所以cdn到底是在数据中心之内还是之外呢？。。。。。
</div>2020-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e5/39/951f89c8.jpg" width="30px"><span>信信</span> 👍（1） 💬（3）<div>老师，这里有个疑问：
再访问的就不是 web.com 的权威 DNS 服务器了，而是 web.cdn.com 的权威 DNS 服务器，这是 CDN 自己的权威 DNS 服务器。
那本地dns是怎么知道CDN 自己的权威 DNS 服务器的ip的？   上一步的web.com 这个权威 DNS 服务器只返回了 CNAME 别名吧？</div>2020-05-30</li><br/><li><img src="" width="30px"><span>起风了001</span> 👍（1） 💬（1）<div>时间戳防盗链这个不是很清楚, 如果客户端可以得到加密字符串, 那么盗版网站也可以先获取这个字符串然后再进行同样的加密, 是不是也可以呢?</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/01/4c000f56.jpg" width="30px"><span>c</span> 👍（1） 💬（3）<div>web.com的权威dns服务器为啥不直接cname到cdn的负载均衡服务器？</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/0e/2b987d54.jpg" width="30px"><span>蜉蝣</span> 👍（0） 💬（1）<div>老师，这一句我没懂：“然后 CDN 服务端有了资源及路径，时间戳，以及约定的加密字符串”。

CDN 服务端是如何获得资源路径，时间戳等客户端给的信息的？因为客户端已经加密过了。如果说服务端可以解密，那么为什么要把这些数据“根据相同的签名算法计算签名”，再去匹配呢？直接把解密出来的、之前约定的加密字符串对比就可以了吧。</div>2019-07-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKicUXKVXIQAmToH3CkpQGjjDHRGSh0RjBpUf82r9WibfrrJMHxZXcuNVgCy8icpI9Mo4He8umCspDDA/132" width="30px"><span>Geek_8cf9dd</span> 👍（0） 💬（1）<div>cdn和httpcdn区别没看太明白，小白要多刷几遍了</div>2019-05-05</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzqiaZnBw2myRWY802u48Rw3W2zDtKoFQ6vN63m4FdyjibM21FfaOYe8MbMpemUdxXJeQH6fRdVbZA/132" width="30px"><span>kissingers</span> 👍（0） 💬（1）<div>dns负载均衡是根据用户配置的本地dns地址作智能调度，不是用户实际的ip。http 负载均衡是根据用户ip做作调度的吧</div>2019-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/21/6c3ba9af.jpg" width="30px"><span>lfn</span> 👍（0） 💬（1）<div>老师，您好。能推荐一些讲cdn比较好的资料或书么？</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/36/2d61e080.jpg" width="30px"><span>行者</span> 👍（61） 💬（0）<div>1. 参照阿里云CDN HTTPDNS方式；客户端请求服务URL:umc.danuoyi.alicdn.com xxx，参数是客户端ip地址和待解析的域名；然后返回多个ip地址，客户端轮训这些ip地址。
2. 如果把边缘节点比作小卖部，那数据中心就是超级市场，里面商品应有尽有，是所有子节点的父集。</div>2018-07-03</li><br/><li><img src="" width="30px"><span>米兰的小铁匠</span> 👍（23） 💬（1）<div>我的理解是 CDN 只是节点，网络传输只能走公网的线路。文章中说走 dns 专用线路，难道是像运营商一样自建电缆？希望老师解惑。</div>2018-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/49/d7690979.jpg" width="30px"><span>tommyCmd</span> 👍（9） 💬（4）<div>根据ip地址，怎么判断服务器的远近呢？</div>2018-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/34/0508d9e4.jpg" width="30px"><span>u</span> 👍（8） 💬（0）<div>专栏前15讲偏基础，后面的偏架构，后面的内容虽然工作中不一定接触的到，但里面的架构思想值得总结学习！超哥厉害！👍🏻👍🏻👍🏻</div>2018-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（6） 💬（2）<div>老师，DNS的作用相当于客户端找到最近最合适DNS运营商，而CDN相当于DNS运营商找到最合适的服务器获取内容。可以这样理解吗？</div>2018-08-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/wYPdGBibR1FJWWMzFzYBy4tNTd22rMgtlYTgR7wuicFLQjiaozuRWM2VSMFxPYjVdkLJLGvMav2icH3icgz07hmDsDw/132" width="30px"><span>dayspring</span> 👍（4） 💬（1）<div>超哥，请问一下cdn的权威dns服务器为什么还需要配置cname指向全局负载均衡器的域名呢？</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fc/d7/b102034a.jpg" width="30px"><span>do it</span> 👍（4） 💬（0）<div>个人小结
CDN(content delivery network)内容分发网络：分为边缘节点、区域节点、中心节点，数据缓存在离用户最近的位置。
CDN最擅长的是缓存静态数据，还可以缓存流媒体数据，这时需要注意使用防盗链(refer机制，时间戳防盗链)。也支持动态数据的缓存，一种是边缘计算的生鲜超市模式，另一种是链路优化的冷链运输模式。</div>2019-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/22/e8/8e154de6.jpg" width="30px"><span>圆嗝嗝</span> 👍（4） 💬（1）<div>客户端发送一个HTTP请求给HTTPDNS，HTTPDNS返回含有请求内容的CDN服务器的IP地址。
与基于DNS进行负载均衡相比，少了DNS先递归查询CDN负载均衡服务器IP地址再通过CDN负载均衡服务器获取CDN服务器IP地址两个步骤。</div>2019-05-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（4） 💬（0）<div>数据中心里面是一排排大机柜</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（3） 💬（0）<div>今日学习笔记：

什么是CDN?

CDN 内容分发网络，content delivery network，用于加快客户端的数据访问速度。


CDN如何加快数据访问速度?

边缘节点-&gt;区域节点-&gt;中心节点，类似于多级Cache的设计，CDN 负载均衡器会根据 用户IP，所在运营商，访问内容，当前服务器负载情况 等因素选择一台合适边缘节点的地址供客户端进行访问。


流媒体CDN的特点？

a. 音视频流数据量比较大，一般会将热点数据从中心节点主动推送到边缘节点进行缓存，以减少被动回源对中心服务器造成的压力。
b. 流媒体CDN支持对音视频流进行预处理，比如视频的标清，高清，蓝光，视频会被处理为不同码率，以便适应不同带宽，或者对视频进行分片处理，加载时只加载用户当前访问分片以加快访问速度。
c. 流媒体CDN需要注意防盗链，一般在http报头中添加 referer 字段指明访问来自哪里，在通信时服务器端需要根据加解密算法验证访问方是否可靠，也需要验证访问是否已过期。


CDN 如何加快动态数据的访问？

a. 将数据计算放在边缘节点，边缘节点定期从中心节点同步数据
b. 计算仍放在中心节点，但是访问路径进行优化</div>2019-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/09/42/1f762b72.jpg" width="30px"><span>Hurt</span> 👍（3） 💬（0）<div>认真的思考了 但又的确实是自己底子薄 不过会反复的学习</div>2018-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（2） 💬（0）<div>1.必然可以,同样是请求了DNS服务器,不过是放在了本地客户端去请求,而不是委托本地DNS服务器去请求,只要到了解析服务器上,依然可以走CDN的全局负载均衡器
2.数据中心应该是缓存了大量数据的服务器集群吧
</div>2020-05-08</li><br/><li><img src="" width="30px"><span>Geek_f0bd6b</span> 👍（2） 💬（0）<div>冷链运输模式，离源近的节点和离客户近的节点之间的链路是怎么实现优化成“专线”的，如果还是承载在公网上，那他们之间的路径本身不就应该是最优的了吗？请教老师解惑，谢谢！</div>2020-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/f1/8b06801a.jpg" width="30px"><span>哇哈哈</span> 👍（2） 💬（2）<div>其实我还是没有理解 cdn 和 dns 的区别，dns 能帮找到最近的服务器，在这些最近的服务器上做静态资源存储不就可以吗？为什么还要分发到 cdn？我个人的理解是，打个比方，可能web.com 的服务器因为资源问题不会部署到每个城市，例如只在一些大区域部署，例如华东部署一个集群华南区域部署一个集群，但是 cdn 因为基本只有存储逻辑，资源开销比服务集群小，所以可以铺开部署到下一层深入到城市级别，例如上海，广州，这样 cdn 比 web.com 的集群更接近用户，所以这就是 cdn 能存在的意义？
</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/8e/0a546871.jpg" width="30px"><span>凡凡</span> 👍（2） 💬（0）<div>1.需要客户端增加httpdns的sdk包，通过一次http请求完成最近节点的获取，然后请求cdn节点获取数据。相较于dns方式，少了一次cname域名的获取过程，少了dns域名的解析过程，而且能避免dns的偶尔失效问题。不过，现在主流的cdn似是采用的dns方式，比如阿里云和七牛云。2.到了服务地址之后，一般会有防火墙，nat，负载均衡器，网关，rpc等参与请求处理。</div>2018-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/2b/22/441c4e51.jpg" width="30px"><span>逐書寄年</span> 👍（1） 💬（0）<div>在思考動態CDN的緩存時，想著想著覺得「生鮮超市」跟「冷鏈運輸」這兩種模式好像比喻得怪怪的呀！
生鮮超市內也可以買到剛宰殺完冰鮮的魚，而且不就是靠冷鏈運輸到離家近的那超市嗎？或許我太關注比喻本身了，不過這反倒讓我有點無法搞懂邊緣計算跟路徑優化的核心區別</div>2023-01-25</li><br/>
</ul>