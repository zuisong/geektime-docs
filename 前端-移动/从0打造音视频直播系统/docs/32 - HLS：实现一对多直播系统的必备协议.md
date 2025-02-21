在[上一篇文章](https://time.geekbang.org/column/article/140181)中 ，我们对 RTMP 协议和 HLS 协议的优势与劣势进行了比较。从比较的结果我们可以看出，RTMP作为传统的直播传输技术在实时性方面要比 HLS 好很多，所以它还是有一定优势的。

不过，随着Chrome浏览器宣布不再对Flash 插件提供支持、Adobe 公司停止对 RTMP 协议更新以及苹果公司声称 iOS 上不允许使用 RTMP 协议等一系列事件的发生，我们可以断定 RTMP 协议已失去了未来。

而 HLS 协议则恰恰相反，它在未来会有更广阔的应用前景。我们可以通过以下几点来得到这个结论：

- HLS 是苹果开发的协议，苹果产品原生支持此协议；
- HLS 是基于 HTTP 的，可以不受防火墙限制，所以它的连通性会更好；
- HLS 还能根据客户的网络带宽情况进行自适应码率的调整，这对于很多用户来说是非常有吸引力的。

基于以上原因，我们有必要从HLS 直播架构、FFmpeg 生成 HLS 切片、HLS m3u8 格式和HLS TS 格式这四个方面对 HLS 协议的细节做一下介绍。

## HLS 直播架构

下面我们来看一下 HLS 直播系统的架构图，如下所示：

![](https://static001.geekbang.org/resource/image/c8/7a/c824a7d2fc85aa9583e10bc0dbff407a.png?wh=1142%2A800)

HLS直播架构图

我们在[上一篇文章](https://time.geekbang.org/column/article/140181)中讲过，传统直播系统大致分为三部分：直播客户端、信令服务和CDN网络，使用HLS 协议也是如此。只不过在我们这里为了简化流程，去掉了信令服务系统。
<div><strong>精选留言（15）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/39/24/963178c4.jpg" width="30px"><span>rrbbt</span> 👍（5） 💬（1）<div>博主，您好，“而服务端的 HLS 切片则是由 CDN 网络完成的，你只需要向 CDN 网络推流就可以了”，hls切片的功能是在cdn中完成的？阿里云的cdn自带这种功能？还是说cdn中可以上传自己的服务，自己写hls切片？没搞过这个，希望帮忙解答一下。</div>2019-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/21/99/ed7d9dc1.jpg" width="30px"><span>priapus</span> 👍（4） 💬（1）<div>其实怎么说呢，这个课程我最关心的还是hls，因为点播技术感觉比直播技术更有未来~</div>2020-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/8b/e97e5d3d.jpg" width="30px"><span>willxiao</span> 👍（3） 💬（2）<div>请问如果是直播中间进入，怎么确定该从哪个 ts 文件开始播放？是不是有什么 timestamp 可以用于比对，然后获取当前时间戳和之后的 ts 文件？</div>2021-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1d/70/0869ede3.jpg" width="30px"><span>绿水</span> 👍（3） 💬（1）<div>我们接入HLS，网站用的是https，但是HLS是http的，结果获取流的时候，浏览器（chrome）就报mixed-content错误，虽然可以通过设置浏览器的安全级别来解决，但有没有更加通用的解决方法？</div>2020-06-15</li><br/><li><img src="" width="30px"><span>Geek_b37496</span> 👍（2） 💬（2）<div>有些m3u8是带key的，那么调用sdk解key播放ts文件的原理是怎么样的呢？</div>2019-10-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6d/b9/6d6d3a9a.jpg" width="30px"><span>花盆</span> 👍（1） 💬（1）<div>HLS需要切片，存储，推送到边缘节点，这个过程的延时对于直播教育类的场景，10~20多秒的延时是无法忍受的，而RTMP协议对于网络要求比较高，在百万场景下让学生不卡不延迟是这个场景核心要去解决的问题。特别在这次公益课期间，大量的CDN的节点被各大直播平台控制，比较小的在线教育公司没法被很好的调度。</div>2020-04-15</li><br/><li><img src="" width="30px"><span>pysn</span> 👍（1） 💬（1）<div>hls推流端也是采用rtmp协议吗？</div>2020-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/2d/e6548e48.jpg" width="30px"><span>tokamak</span> 👍（1） 💬（1）<div>思考题回答：因为高清TS数据包为204字节，标清TS数据包为188字节。当一个媒体数据流小于5个TS包时，这个媒体数据流的长度不可能同时被204和188同时整除。
      不太确定，是这样吗？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（3） 💬（0）<div>固定字节应该是为了便于管理，否则切的时候肯定长度波动，这样可能不便于播放端识别</div>2019-12-17</li><br/><li><img src="" width="30px"><span>Geek_974707</span> 👍（2） 💬（0）<div>老师请问m3u8文件是动态更新的吗？直播中生成的ts文件怎么放入m3u8里呢？</div>2022-04-08</li><br/><li><img src="" width="30px"><span>Geek_6d49f5</span> 👍（2） 💬（0）<div>老师，纯音频直播流要用什么来搞</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/27/b4/df65c0f7.jpg" width="30px"><span>| ~浑蛋~</span> 👍（0） 💬（0）<div>一个ts文件是不是包含多个ts数据流？m3u8和dash的区别是什么，孰优孰劣呢？</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/dd/6851e7cc.jpg" width="30px"><span>白小菜</span> 👍（0） 💬（0）<div>Hls做直播，观看者与直播者的延迟越来越大，这咋处理啊</div>2022-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（0）<div>Convert 服务器是属于CDN还是直播业务的某个服务器？这里是CDN推流是怎么推的？怎么知道推送到哪个CDN节点？没有推送到位的CDN节点是不是还需要回源？这个回源地址是什么？</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/df/e0eb437e.jpg" width="30px"><span>无痕</span> 👍（0） 💬（0）<div>Ts 文件，播放器可以加速播放吗</div>2021-07-07</li><br/>
</ul>