你好，我是刘歧。

前面两节课我们学习了AVFormat、AVIO、dict和opt操作接口，做容器格式封装与解封装问题不大，但是如果要涉及音视频的编解码的话，就需要用到AVCodec部分的接口了。

AVCodec是存储编解码器信息的结构体，当我们使用编解码器的时候会用到AVCodec，而FFmpeg除了AVCodec结构体之外，还有一个AVCodecContext，是FFmpeg内部流程中处理编解码时，用来记录和存储上下文的结构体。关于AVCodecContext这个结构体的参数，如果你学习[第7节课FFmpeg常用参数](https://time.geekbang.org/column/article/548420)的时候，仔细阅读过帮助信息的话，那AVCodecContext这个结构体对你来说应该很好理解。

## AVCodec 接口

在使用FFmpeg的编解码器之前，首先需要找到编解码器。

```plain
const AVCodec *avcodec_find_decoder(enum AVCodecID id);
const AVCodec *avcodec_find_decoder_by_name(const char *name);
const AVCodec *avcodec_find_encoder(enum AVCodecID id);
const AVCodec *avcodec_find_encoder_by_name(const char *name);
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：安装后不能查看codec的parser吗？
文中有这样一句话“如果你想要知道哪些 codec 有 parser 的话，可以在编译 FFmpeg 代码那一步就通过.&#47;configure --list-parsers 来查看”。 我安装的时候没有做过和“configure --list-parsers”有关的操作，那么，现在能够查看codec的parser吗？
Q2：FFmpeg能除去水印吗？
FFmpeg可以给视频加上水印，那可以做相反的操作吗？即去除水印。
Q3：FFmpeg支持“变速”、“变调”吗？</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e9/bb/58135c8e.jpg" width="30px"><span>长江</span> 👍（0） 💬（1）<div>解码预读大小。可以设置成0吗？这样塞进去一帧，就解码一帧，不用缓存</div>2024-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（2） 💬（0）<div>查看了 example&#47;filtering_video.c 下的源码

ffmpeg 滤镜链主要用到的
结构体有：AVFilter，AVFilterInOut
接口有：avfilter_graph_create_filter，avfilter_graph_config，av_buffersrc_add_frame_flags，av_buffersink_get_frame


</div>2022-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-30</li><br/>
</ul>