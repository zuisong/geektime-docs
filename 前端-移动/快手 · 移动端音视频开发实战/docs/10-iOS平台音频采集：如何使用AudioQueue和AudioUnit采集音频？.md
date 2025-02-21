你好，我是展晓凯。今天我们来一起学习iOS平台的音频采集。

iOS平台提供了多套API来采集音频，分别是AVAudioRecoder，AudioQueue以及AudioUnit。这三种方法各有优缺点，适用于不同的场景，我们一起看一下。

![图片](https://static001.geekbang.org/resource/image/76/5d/76f28e48a0bc736af8b03b26b3a0225d.png?wh=1920x587)

- AVAudioRecorder，类似于AVAudioPlayer，属于端到端的API，存在于AVFoundation框架中。当我们想指定一个路径将麦克风的声音录制下来的时候，就可以使用这一个API。优点是简单易用，缺点是无法操控中间的数据。
- AudioQueue，之前我们使用AudioQueue渲染过音频，其实AudioQueue也可以录制音频，也是对AudioUnit的封装，它允许开发者获取、操控中间的数据（按照配置的数据格式）。优点是灵活性较强，缺点是上手难度较高。
- AudioUnit，是音频最底层的API接口，之前我们使用AudioUnit渲染过音频，和AudioQueue一样，我们也可以使用它录制音频。当我们需要使用VPIO（VoiceProcessIO）等处理音频的AudioUnit、需要使用实时耳返或在低延迟场景下，必须使用这一层的API。优点是灵活性最强，缺点是上手难度更高。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（0） 💬（2）<div>老师一直没有介绍audio unit录制音频的方式，请问用audiounit来录制音频是需要给audiounit的input element设置回调，像audioqueue一样按时回调数据保存到自己的队列里，还是有特定的api可以从audio unit 的input element 中获取呢，多谢老师解答</div>2022-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（0） 💬（1）<div>1.  这个 App 是如何实现启动录音的时候音乐作品可以流畅地播放的呢？
A: 播放音乐的过程中录音是启动的。只不过塞的是空白帧，开始录制时，填充录制帧？

2. 使用蓝牙耳机的情况下，在保证录制高音质音频的同时，音乐作品如何保持声音的流畅性呢？
A: 采集用手机Mic，播放用蓝牙耳机？</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>请教老师一个问题：
Q1：关于“混音”功能，是的，这个功能有点类似于回森App的弹幕功能。其实就是一个音乐编辑的功能。音乐编辑的APP，我搜到并下载了“音乐剪辑”、“音频音乐”这两个APP，都具有“混音”、“变速”、“变调”等功能。关于“混音”功能，从实现的角度，安卓上应该怎么做？基于安卓的MediaPlayer来开发吗？ (我感觉MediaPlayer不能实现该功能，就是说没有API可以调用)。是基于OpenSL ES或AAudio来开发吗？ 也许OpenSL ES、AAudio有音频合并方面的API，调用即可。（甚至，需要采用FFmpeg来开发？）。针对安卓平台的“混音”开发，请老师从架构、技术方案层面给我一点指导，非常感谢！  （“混音”也可能只是一种叫法，或者叫“音频合并”？）</div>2022-08-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e5/bd/d6fc7a09.jpg" width="30px"><span>余生不渝</span> 👍（0） 💬（0）<div>请问audioqueue可以在后台执行开始录音采集么</div>2024-04-23</li><br/>
</ul>