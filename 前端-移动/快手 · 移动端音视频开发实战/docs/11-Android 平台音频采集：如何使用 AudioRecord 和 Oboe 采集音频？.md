你好，我是展晓凯。今天我们来一起学习Android平台的音频采集。

视频播放器是将一个视频文件通过解封装、解码、渲染等工作，让用户可以听到声音、看到画面，而视频录制器恰恰是一个逆向的过程，是将麦克风采集到的声音、摄像头采集到的画面通过编码、封装，最终得到一个视频文件。所以整个项目的前置知识包括音视频的采集、编码还有音视频同步等，上一节课我们一起学习了iOS平台的音频采集方法，这节课我们就一起来看Android平台给我们提供了哪些音频采集的方法吧。

## Android平台的音频采集技术选型

![图片](https://static001.geekbang.org/resource/image/f0/eb/f02ac0c612eyyeceebbc56898fc894eb.png?wh=1920x670)

### SDK层提供的采集方法

Android SDK 提供了两套音频采集的API接口，分别是MediaRecorder 和 AudioRecord。前者是一个端到端的API，它可以直接把手机麦克风录入的音频数据进行编码压缩（如AMR、MP3等）并存储成文件；而后者则更底层一些，可以让开发者更加灵活地控制麦克风采集到的PCM数据。

如果想简单地做一个录音机，并且录制出一个音频文件，首选肯定是MediaRecorder，而如果需要对音频做进一步的算法处理，或者需要采用第三方的编码库进行编码压缩，那么就需要使用AudioRecord了。我们的视频录制器场景显然更适合选用第二种方式，使用AudioRecord来采集音频。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：SDK层的MediaRecorder是对AudioRecord的封装吗？
Q2：NDK层的AAudio是基于OpenSL ES吗？（或者说，AAudio是对OpenSL ES的封装吗）
Q3：SDK层的方法，都是基于NDK层的方法吗？ 比如SDK层的MediaRecorder是基于NDK层的AAudio或OpenSL ES。
Q4：默认的麦克风等于主麦克风吗?
Q5：AEC是什么意思？
文中有一句“在 VOIP 场景下如果使用硬件 AEC 的话”，其中的AEC什么意思？
Q6：单声道采集，转换为立体声，也是伪立体声吧。是把单声道的数据拷贝一份变成另外一个声道吗？
Q7：read函数的数组类型，需要根据audioFormat来确定吧。如果audioFormat是8位，应该用byte[],
        如果audioFormat是16位，则应该用short[]，是这样吗？

Q8：播放PCM的命令中，哪一项是表示PCM？
ffplay -f s16le  -sample_rate 44100  -channels 1 -i vocal.pcm，s16le表示什么意思？表示PCM吗？
Q9：PCM转WAV的命令中，哪一项是表示WAV？
ffmpeg -f s16le -sample_rate 44100 -channels 1 -i vocal.pcm -acodec pcm_s16le vocal.wav，哪一项是表示wav？pcm_s16se吗？
Q10：用两种采集方法，是播放器项目会同时采用这两种吗？
选取了 SDK 层的 AudioRecord 和 Native 层的 Oboe 采集音频的方法，只是为了分别说明这两种方法吗？
还是说播放器项目会同时采用这两种方法来采集音频？（同时用两种，好像没有道理）</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9a/64/63fd724b.jpg" width="30px"><span>一日</span> 👍（0） 💬（0）<div>手机熄屏后还可以录制吗？</div>2024-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e9/01/6e6d80d1.jpg" width="30px"><span>Loy</span> 👍（0） 💬（0）<div>老师，你好。低延时耳返需要底层特殊定制吗？</div>2023-04-06</li><br/>
</ul>