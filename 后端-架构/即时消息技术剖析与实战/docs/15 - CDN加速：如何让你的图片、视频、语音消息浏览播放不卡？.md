你好，我是袁武林。

[上一讲](https://time.geekbang.org/column/article/141456)，我从即时消息场景中多媒体消息的上传环节出发，介绍了业界常用的几种提升用户上传体验的优化手段。

那么这节课，我会从播放的角度出发，带你了解在浏览和播放图片、视频、语音等多媒体消息时，如何避免灰图和卡顿的问题，以及在节省流量方面，业界都有哪些比较常见的优化策略。

## CDN加速

提升用户浏览图片和播放视频体验的一个有效办法就是：让用户离资源更近。

比如说，北京的用户可以从北京的机房下载图片，而广东的用户可以从广东的节点机房来下载图片，这样让用户和资源实现物理位置上的相邻，以此降低远程访问的耗时，提升下载性能。

业界常用的一种手段，就是通过CDN（Content Delivery Network，内容分发网络）对图片和音视频进行加速，来提升用户播放体验。

所谓的CDN加速技术，就是将客户端上传的图片、音视频发布到多个分布在各地的CDN节点的服务器上，当有用户需要访问这些图片和音视频时，能够通过DNS负载均衡技术，根据用户来源就近访问CDN节点中缓存的图片和音视频消息，如果CDN节点中没有需要的资源，会先从源站同步到当前节点上，再返回给用户。

CDN下载时的访问链路你可以参考下图：  
![](https://static001.geekbang.org/resource/image/52/ea/52ed63773e6c489a1d55668cb74cf1ea.png?wh=600%2A400)

通过这种资源冗余的方式，既能显著提高用户访问的响应速度，也能有效缓解服务器访问量过大带来的对源存储服务的读写压力和带宽压力。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8d/6c/0c2a26c7.jpg" width="30px"><span>clip</span> 👍（14） 💬（1）<div>给资源设置带有过期时间的访问 token，服务端经过鉴权后向 CDN 服务申请对应资源的访问 token 然后给客户端下发带有访问 token 的资源链接，客户端用这个带有 token 的链接才能在有限时间向 CDN 获取资源。如果资源链接过期可以通过上面的方式重新获取。</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（9） 💬（1）<div>现在CDN都支持鉴权吧，也就是边缘计算。用户在源站登录后，拿到一个token，让CDN检查这个token是否正确。</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（2） 💬（1）<div>存储文件夹设置权限？</div>2019-09-30</li><br/><li><img src="" width="30px"><span>Geek_e986e3</span> 👍（1） 💬（1）<div>老师想问问 cdn多图片这种怎么保证权限呢？我能想到的类似mp4视频。做一个定制版的图片浏览。还有别的更优雅的方式吗？</div>2019-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/1b/4b397b80.jpg" width="30px"><span>蛮野</span> 👍（0） 💬（1）<div>前一篇提到图片视频这类资源会通过文件传输通道与业务消息通道分开，减少传输次数，理论上业务层没有收到图片的数据流，如果要从服务端长连接推送缩略图，业务服务器需要先下载缩略图才能进行推送吧？</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/08/3dc76043.jpg" width="30px"><span>钢</span> 👍（0） 💬（1）<div>传输加密：hls,rc4, 图片压缩优化：WebP,渐进式JPEG, 视频编码优化：H.265，多媒体技术层出不穷，老师有这方面的书籍推荐吗</div>2019-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0c/32/351ac6ab.jpg" width="30px"><span>Gangan</span> 👍（1） 💬（0）<div>腾讯鱼翅：http:&#47;&#47;www.52im.net&#47;thread-675-1-1.html</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/e4/39/a06ade33.jpg" width="30px"><span>极客雷</span> 👍（0） 💬（0）<div>听说过微信C2C CDN吗</div>2021-05-30</li><br/><li><img src="" width="30px"><span>tm1234</span> 👍（0） 💬（0）<div>请问老师预加载是通过长链接通道进行的吗？</div>2020-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e1/08/3dc76043.jpg" width="30px"><span>钢</span> 👍（0） 💬（0）<div>第三方访问，用oauth,普通的访问，用session或cookie和token</div>2019-09-30</li><br/>
</ul>