你好，我是刘歧。

学到这里，不知道你有没有发现一个事情：从开始到现在，我们讲得最多的就是FFmpeg的命令行工具和参数，很少讲到界面操作。其实在做视频转码时，大多数人除了经常用FFmpeg之外，还会用一些免费的带界面的转码工具，这节课我除了会教你如何使用FFmpeg转码之外，还会给你介绍一个非常好用的本地化转码工具Handbrake。

## 如何使用FFmpeg转码？

在我们专栏开篇的基础部分，我给你讲过音视频相关的图像色彩、编解码、封装（Mux）与解封装（Demux）的基本原理。[第7节课](https://time.geekbang.org/column/article/548420)，我又给你讲了如何高效地使用FFmpeg帮助信息和文档。在前面这些内容的基础上，我们来学以致用，讲一讲怎么用FFmpeg转码。

首先我们需要确定我们在转码的时候输出文件的应用场景。假如你是希望传到快手这样的内容发布平台，那么我们是需要转换成平台要求的转码规格的。既然要转码，就需要先看一下自己电脑系统的环境是否支持这一操作，比如使用CPU做转码，电脑会不会变得很慢，如果电脑上有GPU，使用GPU转码的话，CPU理所当然地会空出来，这样就不会影响我们继续使用电脑做其他的事情了。

我们先来了解一下怎么使用CPU做转码。

### 用 CPU 转码
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（1）<div>PC和手机还不太一样，PC的音视频硬件是集成在GPU中的，而手机就不一样了，是分开的。手机上职责还挺清楚的，CPU解封装，音视频专用器件硬解码，再给GPU进行渲染和图像处理（OpenGL部分）</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：需要安装libx264吗？
文中有这样一句“使用命令行 ffmpeg -h encoder=libx264 查看”。
执行命令： ffmpeg -h encoder=libx264
输出：Codec &#39;libx264&#39; is not recognized by FFmpeg.
提示没有libx264。 

用这个命令：ffmpeg -encoders | grep H.264
输出：V..... h264_v4l2m2m
请问：“h264_v4l2m2m”和libx264是什么关系？需要安装libx264吗？（需要的话，怎么安装？）
Q2: 转码用CPU还GPU，是由谁决定的？
是用户在ffmpeg的命令里指定吗？ 还是由ffmeg自动决定？
Q3：“转码”是把一个视频文件的编码从原来的编码方式转换为另外一种编码方式，比如，原来是A编码，转换为B编码。 对吗？
Q4:：本文讲的是视频转码，请问有音频转码吗？</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9f/f6/7431e82e.jpg" width="30px"><span>xueerfei007</span> 👍（0） 💬（2）<div>老师您好，我最近在使用ffmpeg编码工业相机sdk提供的raw帧数据。目前编码后，视频的时间与原始视频流对不上，编码长度比录制时长多了一倍。猜测可能与pts&#47;dts的设置有关。这个需要如何设置，或者有什么方法定位到问题的具体原因？</div>2023-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/65/fa4437d7.jpg" width="30px"><span>Wonderfulpeng</span> 👍（0） 💬（1）<div>老师的课非常精彩，看了这节课我想请教的问题如下：
针对，“设置视频编码流为 CloseGOP，关键帧间隔的 -g 设置成 fps 的一半即可，fps 需要使用参数 -r:v 来设置，例如设置 -r:v 为 30，就是 30 fps”，那想问下：
1、OPENGOP如何设置呢？
2、网上说H265编码GOP只是OPENGOP，是否正确？
3、GOP设置对于视频编码压缩的影响？哪里能参考到相关最好的说明？
</div>2022-10-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（0） 💬（0）<div>尝试回答一下思考题：
ffmpeg -i input.mkv -x264opts &quot;bframes=2:b-adapt=0&quot; -r:v 30 -g 60 -sc_threshold 0 -vf &quot;scale=1280:720&quot; output.mkv</div>2022-09-02</li><br/>
</ul>