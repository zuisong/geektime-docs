你好，我是刘歧。

[上一节课](https://time.geekbang.org/column/article/551256)我们了解了AVFormat中的API接口的功能，从实际操作经验看，这些接口是可以满足大多数音视频的mux与demux，或者说remux场景的。但是除此之外，在日常使用API开发应用的时候，我们还会遇到需要从自己定义的内存或文件中读写数据，然后套用在AVFormat中的场景。遇到这种场景的时候我们应该怎么办呢？使用AVIO就可以做到。

## AVIO

我们先来认识一下AVIO。AVIO部分常见的接口看上去比较多，主要是为了方便读、写内容时做一些字节对齐与大小端定义的操作，了解了它内在的结构之后，你就会觉得清晰多了。下面我们来一一讲解一下。

当你想知道一个URL字符串是什么协议的时候，通过**avio\_find\_protocol\_name接口**就能得到协议的名称，例如http、rtmp、rtsp等。

```plain
const char *avio_find_protocol_name(const char *url);
```

**avio\_alloc\_context接口**主要用来申请AVIOContext句柄，并且可以在申请的时候注册read\_packet、write\_packet与seek回调，然后可以将AVIOContext句柄挂载到AVFormatContext的pb上面。挂载完成后，在操作AVFormatContext的read\_packet、write\_packet、seek的时候，会调用这里注册过的回调接口，注册的时候如果把回调接口设置成NULL（空），就会使用AVIOContext子模块默认的流程。这里申请的AVIOContext可以通过**avio\_context\_free**来释放。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（3） 💬（1）<div>AVPacket 是属于AVCodec
AVPacket 一般用来存储解码前的数据，AVFormat一般用来存储解码后的数据，
通过 avcodec_send_packet 送入avpacket ,  通过 avcodec_receive_frame 进行解码，送出avformat</div>2022-09-30</li><br/><li><img src="" width="30px"><span>geek</span> 👍（0） 💬（1）<div>还有个问题

avio_alloc_context 接口主要用来申请 AVIOContext 句柄，并且可以在申请的时候注册 read_packet、write_packet 与 seek 回调，然后可以将 AVIOContext 句柄挂载到 AVFormatContext 的 pb 上面。

这个pb是什么？</div>2022-08-19</li><br/><li><img src="" width="30px"><span>geek</span> 👍（0） 💬（1）<div>请教老师
AVDictionary是可以自定些自己的信息写到文件里？而AVOption却不可以？还是都可以？比如我想在mp4文件中加些个人信息。</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：static av_always_inline int64_t avio_tell(AVIOContext *s)，av_always_inline 什么意思？
Q2：有基于FFmpeg的开源应用吗？有的话麻烦推荐一下啊。
Q3：快手APP，音视频处理是采用FFmpeg吗？
Q4：我刚接触FFmpeg，印象中FFmpeg可以用在手机上。那么，除了移动端外，还有哪些应用场景？</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/13/0b/14670105.jpg" width="30px"><span>欢仔</span> 👍（0） 💬（0）<div>双屏，不同dpi，屏幕位置随意。当我在副屏幕上截区域录屏，然后传的是wpf 控件在屏幕上的顶点坐标,但是录出来的区域不对，查了一下，说是副屏会按照主屏幕的dpi计算，不知道有没有接口是接收这样的参数</div>2023-07-18</li><br/>
</ul>