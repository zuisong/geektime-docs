你好，我是刘歧。

通过前面13节课的学习，我们对FFmpeg整体的使用和架构已经有了一定的了解。接下来，我们一起来探索一下FFmpeg社区的“玩法”，了解一下FFmpeg常用的交流工具、反馈bug和贡献代码的渠道，以及定制专属板块的方法。这个部分，我会分成两讲给你介绍。这节课我们先来学习一下如何在FFmpeg中定制一个专属于自己的模块。定制模块的作用有很多，比如可以通过定制自己的私有格式，防止别人播放自己的视频。

在FFmpeg中添加模块，需要深入了解源代码架构。但FFmpeg源代码太多，我们需要找到一个突破口深入进去。下面，我们一步一步来解决这些问题。

首先，我们下载官方的源代码库，基于5.0分支做一个新分支kwai，作为我们源码的基础。

```plain
$ git clone git://source.ffmpeg.org/ffmpeg.git     # 下载源代码
$ cd ffmpeg                                        # 进入源代码主目录
$ git checkout remotes/origin/release/5.0          # 切换到5.0分支
Note: switching to 'remotes/origin/release/5.0'.

$ git checkout -b kwai                             # 开一个新分支，起名叫kwai
Switched to a new branch 'kwai'
```
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（1）<div>这种私有文件格式的玩法，确实很多😄，微信的语音文件是silkv3格式，和标准格式有点差别是文件最前面加了一个字节的点号“.” ，导致其他播放器都打不开，也不知道是图个啥。</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：查看FFmpeg源码，linux下一般用什么软件？ Win10下一般用什么软件？（win10下用sourceInsight吗？）

Q2：添加文件封装格式之后，编译失败
“添加文件封装格式”之前的操作都是成功的。
从“添加文件封装格式”开始，我的操作是：
1  打开kwaienc.c:  vi kwaienc.c
2 将“添加文件封装格式”下面五个小步骤中每一个小步骤的代码都
  拷贝到kwaienc.c中（原样拷贝，没有修改），
3 打开kwaidec.c，加入下面两句：
#include &quot;avformat.h&quot;
const AVInputFormat  ff_kwai_demuxer;

然后编译： make -j4
报错：&#47;usr&#47;bin&#47;ld: libavformat&#47;libavformat.a(allformats.o):(.data.rel.ro+0xa40): undefined reference to `ff_kwai_demuxer&#39;

请问错误原因是什么？ 怎么修改？</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/16/bca904d6.jpg" width="30px"><span>青晨昊天</span> 👍（1） 💬（0）<div>请问老师，关于自定义filter的编写，有哪些教程</div>2022-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（0） 💬（1）<div>写音视频数据 部分里的函数开头部分：
static int kwai_write_packet(AVFormatContext *s, AVPacket *pkt) { 
&#47;&#47; kwaiMuxContext *mov = s-&gt;priv_data; 
uint32_t size = pkt-&gt;size; &#47;&#47; 获取数据大小 
if (!pkt) { 
    return 1; 
}
...

这里应该在函数开头先判断指针是否为空 if (!pkt) 然后再取 pkt-&gt;size</div>2022-09-20</li><br/>
</ul>