你好，我是展晓凯。

上节课我们学习了iOS平台的音频框架的第一部分，深入了解了AVAudioSession以及AudioQueue的使用方法，同时也学习了iOS音频格式的表示方法，就是ASBD。其中重点学习了AudioQueue渲染音频的方法。AudioQueue这个API其实是介于AVPlayer/AVAudioPlayer与Audio Unit之间的一个音频渲染框架。如果我们想对音频有更高层次的控制，而AudioQueue满足不了我们的开发需求的时候，我们应该使用哪个音频框架呢？

![图片](https://static001.geekbang.org/resource/image/53/9a/5398e87e2955052a62f9dc5accc1b89a.png?wh=1744x704 "图1 iOS平台的音频框架（图片来自苹果官网）")

没错，就是AudioUnit。作为iOS最底层的音频框架，AudioUnit是音视频开发者必须要掌握的内容。我们在开发音频相关产品的时候，如果对音频有更高程度的控制、性能以及灵活性需求，或者想使用一些特殊功能（比如回声消除、实时耳返）的时候，就可以直接使用AudioUnit这一层的API，这些接口是面向C语言的。

随着iOS的API不断升级，AudioUnit还逐渐演变出了AUGraph与AVAudioEngine框架，它们可以为你的App融入更强大的音频多媒体能力。

正如苹果官方文档中描述的，AudioUnit提供了快速的音频模块化处理功能，如果是在以下场景中，更适合使用AudioUnit，而不是高层次的音频框架。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（3） 💬（2）<div>iOS Api就是花样多，这个Graph类似FFmpeg的滤镜graph，抽象了一部分的音频处理。Android Api就原始多了，解码出来的PCM，自己去处理吧，不提供任何Api，连重采样都没有。</div>2022-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（1） 💬（2）<div>老师这一讲的内容非常详细，对iOS audio unit的使用有了很详细的了解，其中还是有几个问题想确认希望老师有空时帮忙解答，十分感谢：

1. 示例代码中给audio unit扬声器播放的场景设置ASBD代码是：
AudioUnitSetProperty( remoteIOUnit,kAudioUnitProperty_StreamFormat, 
kAudioUnitScope_Output, 1, &amp;asbd, sizeof(asbd));
这里的element 是1，请问是不是应该改成element为0；另外asbd需要给element的0的output和input scope都设置一下吗？

2. 老师在文中给出的将remote i&#47;o audio unit element 0 与扬声器进行连接使用的key是 kAudioOutputUnitProperty_EnableIO，这个key的本质是一个开关，是不是可以理解remote i&#47;o audio unit 的 element 0 output 和 element 1 input 本身已经与扬声器&#47;麦克风连接了，我们使用时只需要将kAudioOutputUnitProperty_EnableIO的值设置为1，即启动了这个连接？

3. 在问题2的基础上，请问该如何将 element 0 的 input 和 element 1 的 output 连接起来。
如果想实现老师文中提到的从麦克风中采集音频后使用扬声器播放的场景，element 0 需要数据时可以通过预先设置的call back 方法感知到，需要调用什么接口才能从 element 1 中获取采集到的数据呢，这块没有特别想明白，想请老师提示下细节，感谢！

学了老师的课确实对 audio unit 有了更多好奇的地方，上面是一些困惑，希望老师有空时能帮忙解答，非常感谢！如果有一些理解错误或者鱼唇的地方，请老师多多包涵</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（1） 💬（1）<div>问一下，如何需要提供很复杂、很强大的音频功能，使用 AUGraph 是否比使用 AVAudioEngine 有更大地灵活性</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/45/74/7a82eebb.jpg" width="30px"><span>Ins</span> 👍（0） 💬（1）<div>老师能否补一下音频技术的历史发展，比如一些标准、频谱、编码之类的，讲一下音频的一些底层逻辑。</div>2022-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（0） 💬（1）<div>
AURenderCallbackStruct renderProc;
renderProc.inputProc = &amp;inputAvailableCallback;
renderProc.inputProcRefCon = (__bridge void *)self;
AUGraphSetNodeInputCallback(mGraph, ioNode, 0, &amp;finalRenderProc);

这里的 finalRenderProc 应该是 renderProc 吧</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/b9/70/fd0ab6b9.jpg" width="30px"><span>好好浩浩</span> 👍（0） 💬（1）<div>有基于Android的吗？</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>老师的课很好，很有价值；刚发现这个专栏，赶紧追赶，终于赶上了进度。
请教老师一个问题：
开篇词中老师提到“我所在的团队开发并维护了唱鸭、鲸鸣、虾米音乐等产品。当时我们将弹唱的实时耳返做到了业界最佳并独创了音乐弹幕的交互形式”，

请问：具有“音乐弹幕”功能的APP的完整名字叫什么？ 我想下载一个。知道APP名字后我可以根据名字从应用市场上搜。</div>2022-07-28</li><br/>
</ul>