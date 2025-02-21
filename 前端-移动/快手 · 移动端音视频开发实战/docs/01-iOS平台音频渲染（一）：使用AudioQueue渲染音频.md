你好，我是展晓凯。

记得在开篇的时候我说过，我们最后的目标之一就是要实现一个视频播放器项目。而想要实现这个项目，需要我们先掌握音频渲染、视频渲染以及音视频同步等知识。所以今天我们就来迈出第一步——音频的渲染。

音频渲染相关的技术框架比较多，平台不同，需要用到的技术框架也不同。这节课我们就先来看一下iOS平台都有哪些音频框架可供我们选择，以及怎么在iOS平台做音频渲染。

我们先看一下图1，iOS平台的音频框架，里面比较高层次的音频框架有Media Player、AV Foundation、OpenAL和Audio Toolbox（AudioQueue），这些框架都封装了AudioUnit，然后提供了更高层次的、功能更精简、职责更加单一的API接口。这里你先简单地了解一下这些音频框架之间的关系，以及AudioUnit在整个音频体系中的作用，下节课我会给你详细地讲解AudioUnit框架。

![](https://static001.geekbang.org/resource/image/42/7f/429c932f1b5fed302fa262bff76yy87f.png?wh=1744x704 "图1 iOS平台的音频框架（图片来自苹果官网）")

如果我们想要低开销地实现录制或播放音频的功能，就需要用到iOS音频框架中一个非常重要的接口——**AudioQueue**，**它是实现录制与播放功能最简单的API接口**，作为开发者的我们无需知道太多内部细节，就可以简单地完成播放PCM数据的功能，可以说是非常方便了。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（2）<div>播放原始的PCM，优势是不言而喻的，音频轨道解码之后的PCM数据，可以给FFmpeg的音频滤镜做进一步各种效果的处理，还可以接入soundtouch做变速和变调的处理，然后处理过的PCM再给audioqueue播放，各个流程都可以定制。</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（1） 💬（1）<div>展老师，对于AudioStreamBasicDescription的参数设置，文章中有三个不明白的地方，想请教一下老师：假设我现在需要播放的音频格式为44100采样, 2声道，交错存放，float类型数据，每个包有1024个采样的PCM数据
1. mFramesPerPacket为什么一般是1呢，怎么理解这里的Frame？如果设置成1是不是可以理解为这里的一个frame也就是输入的一个包的整体数据，也就是我上述情况里 1024个采样 * 2通道 * sizeof(float)的大小
2. 如果在1成立的基础上，看见接下来两个参数mBytesPerFrame和mBytesPerPacket在样例代码中是对应同一个变量bytesPerSample；bytesPerSample的计算规则是不是可以用44100 * 2 * 1024 * sizeof(float)来计算 （如果非交错存储就不乘以2）
3. 请问有什么情况mFramesPerPacket这个值设置为非1呢
感谢老师有空时帮忙解答，刚接触音视频不久，常常为参数问题所困顿，所以问题稍微有点细，如果有一些理解错误的地方拜托老师多多指正，谢谢展老师</div>2022-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/3d/ae41c2b3.jpg" width="30px"><span>data</span> 👍（1） 💬（2）<div>是否案例都有demo可以跑一跑😌</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6b/3d/ae41c2b3.jpg" width="30px"><span>data</span> 👍（0） 💬（1）<div>老师,我想咨询一下 我使用 AudioQueue 来录音,然后封装成rtp包进行发送,里面 有个时间戳 timestamp,我没找到 里面有方法可以获取到这个时间戳的?

 int32_t t = ((float)timestamp.value &#47; timestamp.timescale) * 1000;
 if(start_t == 0) start_t = t;
 header.ts = t - start_t;

</div>2022-08-03</li><br/>
</ul>