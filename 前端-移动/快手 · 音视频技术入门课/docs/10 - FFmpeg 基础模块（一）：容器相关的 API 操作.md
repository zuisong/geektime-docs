你好，我是刘歧。

学到这里，相信你对音视频的基本工作原理和基本操作已经有了一定的认识，并且能够通过命令行、参考标准文档等工具独立完成一些音视频工作了。课程到现在开始渐入佳境，我们要从工具用户逐渐转变成API用户了。毕竟还有很多工作是FFmpeg命令行操作起来不太方便的，比如直播连麦的动态画面拼接、连麦PK结束后画面比例变化等。

从这节课开始，我们会逐步分析作为API用户我们需要了解的FFmpeg中的重要模块，比如AVFormat模块、AVcodec模块、AVfilter模块、swscale模块、swresample模块。

在具体讲解如何使用FFmpeg的API之前，为了方便你查看API对应的代码，首先我会介绍一下FFmpeg的代码结构目录，我建议你先从[FFmpeg的官方代码库](https://ffmpeg.org/download.html)下载一份代码。

```plain
git clone git://source.ffmpeg.org/ffmpeg.git 
```

从目录中可以看到，FFmpeg目录中包含了FFmpeg库代码目录、构建工程目录、自测子系统目录等，具体内容如下：

![图片](https://static001.geekbang.org/resource/image/8a/bd/8af20d33c9b1d3144dddf25cbfafe5bd.png?wh=1626x1140)

现在你知道FFmpeg的源代码目录中都包含了哪些内容，在之后使用FFmpeg的API做开发遇到问题时，就可以通过查看源代码来了解更多、更详细的内部实现了。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（3） 💬（1）<div>请教老师几个问题：
Q1：FFmpeg框架有渲染音频的能力吗？比如要实现“混音”功能，即在一个音频上叠加另外一个音频，混音后能同时听到两个声音。Ffmpeg是否支持开发“混音”功能？（安卓系统上搜到了几个音频编辑的APP，APP的其中一个功能是“音频合并”。我这里说的“混音”差不多就是“音频合并”）。
Q2：切片是什么意思？是若干帧的组合吗？或者是从视频或音频文件中截取一小段？
Q3：partition、切片、宏块有什么区别？
Q4：”side data”是什么意思？</div>2022-08-16</li><br/><li><img src="" width="30px"><span>Geek_a54b66</span> 👍（1） 💬（1）<div>windows 的 ffmpeg 要通过源代码编译，还是官网直接下编译好的，如果要编译怎么编译，而且开发环境怎么搭建</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/84/c5/99ca891a.jpg" width="30px"><span>Sky丶蓝调</span> 👍（0） 💬（0）<div>在FFmpeg的API中，可以使用av_opt_set()函数来设置movflags参数，从而实现将MP4的moov移动到文件头部的功能。具体步骤如下：

首先需要获取AVFormatContext，可以使用avformat_alloc_output_context2()函数创建一个输出上下文。
设置输出格式和输出文件路径，可以使用avformat_new_stream()函数新建一个流。
使用av_opt_set()函数设置movflags参数，将其设置为&quot;faststart&quot;。
调用avformat_write_header()函数写入文件头。
循环调用av_interleaved_write_frame()函数将AVPacket输出到文件中。
调用av_write_trailer()函数输出文件尾。
需要注意的是，如果使用avformat_write_header()函数写入文件头之前没有设置movflags参数，那么moov将会被放在文件的尾部。如果在调用avformat_write_header()函数之后再设置movflags参数，那么设置将不起作用。因此，必须在调用avformat_write_header()函数之前设置movflags参数。

AVFormatContext *out_ctx;
AVOutputFormat *out_fmt;
AVStream *out_stream;
AVCodecContext *codec_ctx;
AVCodec *codec;
AVPacket packet;

avformat_alloc_output_context2(&amp;out_ctx, NULL, &quot;mp4&quot;, &quot;output.mp4&quot;);
out_fmt = out_ctx-&gt;oformat;

out_stream = avformat_new_stream(out_ctx, NULL);
codec_ctx = out_stream-&gt;codec;

codec = avcodec_find_encoder(codec_ctx-&gt;codec_id);
avcodec_open2(codec_ctx, codec, NULL);

av_opt_set(out_ctx-&gt;priv_data, &quot;movflags&quot;, &quot;faststart&quot;, 0);

avformat_write_header(out_ctx, NULL);

while (&#47;* 读取AVPacket *&#47;) {
    av_interleaved_write_frame(out_ctx, &amp;packet);
}

av_write_trailer(out_ctx);
</div>2023-04-01</li><br/>
</ul>