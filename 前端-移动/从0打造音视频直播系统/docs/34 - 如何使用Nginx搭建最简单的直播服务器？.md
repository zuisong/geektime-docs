在前面三篇文章中，我们介绍了传统直播系统架构、HLS协议、RTMP协议相关的知识，那今天我们就来具体实操一下，根据前面所学到的知识搭建出一套最简单的音视频直播系统。

今天我们要搭建的这套直播系统相较于[《31 | 一对多直播系统RTMP/HLS，你该选哪个？》](https://time.geekbang.org/column/article/140181)一文中介绍的直播系统要简单得多。该系统不包括客户端、没有 CDN分发，只包括最基本的推流、转发及拉流功能。虽然它简单了一点，但麻雀虽小五脏俱全，通过这样一个实战操作，我们就可以将前面讲解的理论与实际结合到一起了。

当然，作为一个直播系统来说，客户端是必不可少的。但由于时间和篇幅的原因，我们只能借助一些现成的或者开源的客户端对我们的直播系统进行测试了，所以客户端的界面可能会简陋一些。也正因为如此，我才没有将它们算作咱们这个直播实验平台之中。

实际上，我们完全可以以这个直播系统实验平台为原型，逐步地将一些功能添加进去，这样很快就可以构建出一套商业可用的传统直播系统了。

## 直播系统架构

在正式开始实战之前，我们先来简要介绍一下这个直播系统的架构，如下图所示：

![](https://static001.geekbang.org/resource/image/68/e3/68f233981343fca6aac7557baa79b1e3.png?wh=1142%2A713)

最简单的直播系统

这个直播架构非常简单，由两部分组成，即**媒体服务器**和**客户端**。

媒体服务器有两个功能：

- 推流功能，可以让客户端通过 RTMP 协议将音视频流推送到媒体服务器上；
- 拉流功能，可以让客户端从媒体服务器上拉取 RTMP/HLS 流。
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/fb/2d/e6548e48.jpg" width="30px"><span>tokamak</span> 👍（7） 💬（4）<div>开源RTMP流媒体服务器：SRS，github地址：https:&#47;&#47;github.com&#47;ossrs&#47;srs</div>2019-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（3） 💬（1）<div>用nginx或者SRS搭建的这种流媒体服务器只能用于传统直播。 而第25讲里面提到的那4中SFU架构的流媒体服务器用于实时直播？ 一般商用的实时直播或者传统直播是在开源软件上改的吗？ 还是厂商自己实现的？</div>2020-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/58/95/c1d937f6.jpg" width="30px"><span>庄忠惠</span> 👍（3） 💬（3）<div>老师，我们现在用nginx搭了个流媒体服务器，但是发现移动端和pc端延迟时间会差10秒以上，这个有办法缩短延迟时间吗</div>2020-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（3） 💬（1）<div>用nginx的模块和用srs有什么区别呢，是不是可以理解为srs用了部分nginx的功能同时加了很多流媒体方面的处理功能，更专用？</div>2019-12-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJw0VnT9fk33w0Kgic1udf85TmuzBhibIzic188HIlhJ5SLMnVuM8ia9GDpLTia5k2zy0EoXgCj9ibYzvZA/132" width="30px"><span>tiga</span> 👍（3） 💬（2）<div>老师为什么没介绍 HLS 相关的内容呢？比如如何推拉流进行测试等等</div>2019-10-17</li><br/><li><img src="" width="30px"><span>Lion</span> 👍（2） 💬（1）<div>老师请教下，medooze流媒体服务器和SRS这类流媒体服务器有什么差异？据说srs&#47;nginx性能很强能支持几千路视频，可以作为SFU架构中的流媒体服务器吗？</div>2020-08-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（1） 💬（1）<div>老师，最后的播放用的rtmp地址和ffmpeg推给nginx的地址一样，好像没有nginx服务器什么事？</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3c/8a/900ca88a.jpg" width="30px"><span>神经旷野舞者</span> 👍（1） 💬（2）<div>实时查看摄像头功能，是在摄像头这边切成hls然后响应推送快，还是有响应后推rtmp到服务器再切速度快呢</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4d/c0/89a4194e.jpg" width="30px"><span>贯通</span> 👍（0） 💬（1）<div>web端，rtmp推流基于flash，然而浏览器又不支持flash。在web端还有什么好的推流工具么？</div>2020-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f6/80/85ec2c2a.jpg" width="30px"><span>连瑞龙</span> 👍（0） 💬（1）<div>编译nginx前，.&#47;configure的时候报缺pcre和zlib库。需要，sudo apt install libpcre3 libpcre3-dev zlib1g-dev </div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/8c/ce36a2d0.jpg" width="30px"><span>爱看书的蜗牛</span> 👍（0） 💬（1）<div>nginx生成Mackfile那一步，Makefile没有内容呢</div>2020-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0d/a0/c97ce2fe.jpg" width="30px"><span>coco</span> 👍（0） 💬（1）<div>老师，请教一下：
推流到rtmp服务器经常会中断：
环境：
1. Mac系统
2. ffmpeg4.2.2版本
```shell
ffmpeg \
    -re \
    -stream_loop -1 \
    -i https:&#47;&#47;oss.com&#47;live&#47;20191228.mp4 \
    -c copy \
    -f flv &quot;rtmp:&#47;&#47;localhost:1935&#47;live&#47;test99&quot;
```</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ce/ce/53392e44.jpg" width="30px"><span>BingoJ</span> 👍（0） 💬（0）<div>老师，如果要基于浏览器打开网页就可以进行直播，是不是只能用webrtc了啊，因为用户方不一定安装ffmpeg这些推流工具</div>2023-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cd/df/c520d418.jpg" width="30px"><span>董俊俊</span> 👍（0） 💬（0）<div>老师，最后直播的是视频文件，如何直播摄像头的内容啊？</div>2022-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d0/ce/a81126ea.jpg" width="30px"><span>代先生。</span> 👍（0） 💬（0）<div>编译好的 nginx-rtmp 有需要的自取,https:&#47;&#47;gitee.com&#47;daixingdeng_admin&#47;windows-rtmp-server。https:&#47;&#47;gitee.com&#47;daixingdeng_admin&#47;nginx-http-flv-module</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/d0/ce/a81126ea.jpg" width="30px"><span>代先生。</span> 👍（0） 💬（0）<div>ZLMediaKit不是首选吗</div>2022-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1b/de/e63da460.jpg" width="30px"><span>仰泳鱼</span> 👍（0） 💬（0）<div>请问老师两问题（一）webrtc的客户通能直接推流到ngnix&#47;srs这样的 流媒体服务器吗？ 还是说webrtc先推到mediasoup， meidiasoup再推给srs。
（二）能指导下娱乐直播（类似斗鱼）中加连麦功能（webrtc）的框架设计吗</div>2021-10-08</li><br/>
</ul>