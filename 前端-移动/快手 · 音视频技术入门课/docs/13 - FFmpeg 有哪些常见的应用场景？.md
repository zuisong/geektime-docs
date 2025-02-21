你好，我是刘歧。

FFmpeg API 应用部分的前两节课，我们了解了AVFormat、AVCodec以及常用的操作接口，但是现在这些知识还是“各忙各的”的状态，好像没有真正地把图像与封装格式、传输协议给串起来，形成一个完整的音视频图形图像处理的链条，可能你都没空看FFmpeg源代码目录里面提供的例子。

别急，这节课我们就一起来看一看FFmpeg源代码里面的例子，主要是不转码只转封装、转码转封装和直播推流三个场景，通过分析这三个场景案例，加深一下你对API使用的理解。

## Remuxing

在使用FFmpeg的API做开发之前，我们先来梳理一下想要做Remuxing的话都需要用到哪些结构体与模块，看一下基本的流程。

![图片](https://static001.geekbang.org/resource/image/d7/a4/d7bac673dcbfc6949d9abae5ac6bc9a4.png?wh=1310x906)

1. 打开输入文件和打开输出文件，我们可以理解为初始化操作。
2. 从输入文件中读取音视频数据包，将音视频数据包写入输出文件，我们可以把它理解为一个循环操作，直到遇到结束相关的操作信息才停止。
3. 关闭输出文件和输入文件，我们可以理解为收尾操作。

下面，我们逐步剖析一下。

初始化操作部分的代码大概会使用这些函数。

使用avformat\_open\_input、avformat\_find\_stream\_info来打开输入文件，并根据输入文件中的音视频流信息建立音视频流，也就是AVStreams。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师两个问题：
Q1：双声道合并单声道，还能听到两个声道，有什么意义？
用这个命令：ffmpeg -i input.aac -ac 1 output.aac，可以把双声道合并为单声道，但是，合并后的文件，还是能听到两个声道的声音，怎么能算是“单声道”呢？
用命令“ffmpeg -i jixiaolan_aac.aac -map_channel 0.0.0 left.aac -map_channel 0.0.1 right.aac”生成的两个文件，无论是left.aac还是right.aac ,两个耳机都能听到，为什么？

这个问题是看书《FFmpeg从入门到精通》遇到的。
Q2：文中的代码，应该是C代码。这些代码可以下载并执行吗？ （比如：从github上下载，然后编译、执行，能看到结果）。如果有一个完整的步骤，能操作成功并看到结果就更好了。</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/de/bf/259d4570.jpg" width="30px"><span>Amos</span> 👍（0） 💬（1）<div>请教老师个问题：如果将视频文件的码率下降一半，其他编码参数不变，视频文件的大小也应该下降一半吧？</div>2023-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-31</li><br/>
</ul>