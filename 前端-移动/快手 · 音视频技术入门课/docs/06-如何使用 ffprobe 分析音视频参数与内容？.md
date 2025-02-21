你好，我是刘歧。

[上一节课](https://time.geekbang.org/column/article/546485)我们学习了如何使用FFmpeg和OBS做直播推流，当时我给你留了一个思考题，怎么确认播放的流是我们自己推的那个直播流呢？想回答这个问题，就需要用到我们今天要学习的这个视频信息分析神器——ffprobe。它是FFmpeg提供的一个工具，能够用来分析音视频容器格式、音视频流信息、音视频包以及音视频帧等信息，在我们做音视频转码、故障分析时，这个工具能提供很大的帮助。

下面，我们就来看看怎么使用ffprobe来分析音视频相关信息。

## 音视频容器格式分析

当我们拿到一个视频文件、一个视频直播URL链接时，通常的操作是播放，或者是分析其音视频容器格式的信息。播放操作比较简单，这里就不说了，如果想要分析音视频容器格式的信息，我们应该怎么做呢？

其实使用**ffprobe的-show\_format**参数就能得到对应的信息了，我们看一下输出的内容。

```plain
[FORMAT]
filename=/Users/liuqi/Movies/Test/ToS-4k-1920.mov
nb_streams=2
nb_programs=0
format_name=mov,mp4,m4a,3gp,3g2,mj2
format_long_name=QuickTime / MOV
start_time=0.000000
duration=734.167000
size=738876331
bit_rate=8051316
probe_score=100
TAG:major_brand=qt
TAG:minor_version=512
TAG:compatible_brands=qt
TAG:encoder=Lavf54.29.104
[/FORMAT]
```
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（6） 💬（1）<div>请教老师姐问题：
Q1：像素不是一个点吗？怎么会是矩形？
文中有这样一句话：“肯定有一个因素，就是像素点不是矩形的，不是 1 比 1 的单个像素点。这就产生了 Pixel Aspect Ratio（PAR）像素宽高比”。我以前一直认为像素就是一个点，难道实际上像素是按矩形处理的吗？
Q2：文中最后一个图，关于H.264的，视频文件中是同时存在Video Packet和Video Frame吗？或者说，Video Packet和Video Frame只存在一种，图中两个都列出来只是为了说明？
Q3：YUV格式能用来实际显示吗？ 我的理解是：YUV不能用来显示，需要转换为RGB才能显示。
Q4：01讲中，YUV420的图中，Y4个字节，U和V各一个字节。总共6个字节。这六个字节表示几个像素？我认为是表示4个像素，不是6个像素。
Q5：YUV420格式，V是0，为什么还会有一个字节？按道理是0个字节啊。</div>2022-08-06</li><br/><li><img src="" width="30px"><span>Geek_c9cd4c</span> 👍（1） 💬（1）<div>PPS 、SPS、VPS、SEI能介绍一下吗</div>2023-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c6/1f/7431e82e.jpg" width="30px"><span>askxionghu</span> 👍（1） 💬（1）<div>ffprobe 的 -show_formats改为-show_format</div>2022-08-05</li><br/><li><img src="" width="30px"><span>Geek_c9cd4c</span> 👍（0） 💬（1）<div>I帧不是keyframe吗</div>2023-02-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HWfgYFkH80yh2yCWEAK430aZ1e9BbvQI4DN9q8ib4Czc8DTHeWmmIuep74wBIRGARhJd6eY6Tpt3QUSpAicDIHNw/132" width="30px"><span>Geek_e2e4e9</span> 👍（0） 💬（1）<div>“因为分辨率是 1920x800 的，所以我们可以简单地称之为 1080p”这句话有问题，1080p应该是1920x1080的分辨率</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（0） 💬（1）<div>这个得分通常用来确定使用哪个容器模块来解析这个 probe 文件 
这里 这个 probe 文件 是不是应该是 这个 mov 文件？</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ec/f4/3c569056.jpg" width="30px"><span>西格玛</span> 👍（0） 💬（1）<div>老师你好，经过做实验我发现和您的描述有点出入：
ffprobe -show_frames -of xml xxx.mp4这个结果里面的pkt_pts和pkt_pts_time是不按照顺序的，但是
ffprobe -show_packets -of xml  xxx.mp4的pts是按照顺序的</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（0） 💬（0）<div>分片转码主要是根据video流特性进行分片转码，分片以gop作为划分点</div>2022-09-20</li><br/>
</ul>