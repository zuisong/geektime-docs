你好，我是展晓凯。今天我们一起来学习iOS平台的视频画面采集。

前面我们学习的音频采集与编码的方法，可以用来实现音频录制器的功能。但如果要完成视频录制器的功能我们还需要掌握视频采集与编码方面的内容，所以从今天开始我们来学习如何采集视频的画面。

采集到视频画面之后一般会给用户预览出来，这就要结合之前我们学过的[视频画面渲染](https://time.geekbang.org/column/article/545953)方面的知识，再加上视频的编码，这样就可以在用户点击录制的时候给视频画面编码并且存储到本地了。这节课我们就先来一起学习在iOS平台如何采集视频画面。

## 视频框架ELImage架构设计

在iOS平台使用Camera来采集视频画面的API接口比较简单，但要设计出一个优秀的、可扩展的架构，也不是一件容易的事情。所以这节课我会带你设计并实现出一个架构，这个架构基于摄像头采集驱动，中间可以支持视频特效处理，最终用OpenGL ES渲染到UIView上，且支持扩展插入编码节点。我们先来看一下整体的架构图。

![图片](https://static001.geekbang.org/resource/image/43/2f/43da58864042499a170ba75d96d9352f.png?wh=1694x636 "架构图")

左边第一个节点是用系统提供的Camera接口，采集出一帧内存中的图像，然后将这个图像上传到显存中成为YUV的纹理对象，最后将这个YUV格式的纹理重新渲染到一个RGBA的纹理上。接着将这个RGBA类型的纹理对象传到中间的Filters节点，这个节点内部会使用OpenGL ES来处理这个纹理对象，最后输出一个纹理对象到下面的节点。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（0） 💬（2）<div>老师有三个问题想请教一下：
1. 通过这个采集渲染框架，能否理解为摄像头采集-&gt;编辑-&gt;渲染的过程就是从摄像头中拿到原始图像，然后经过每一个节点不断渲染到显存中的一个纹理ID上，最终在显示节点上把每一层渲染好的纹理显示到目标view上？
2. 如果需要编码这个最终的图像，是需要编码节点每一帧都从显存中获取吗？
3. 老师在文中提到了每次将内存图片上传显存是一个很低效的做法，可以使用CVOpenGLESTextureCacheCreateTextureFromImage API，请问这个API的原理是什么呢，是怎么做到高效内存-&gt;显存的操作呢

感谢老师的解答，辛苦了</div>2022-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b0/2b/87aff702.jpg" width="30px"><span>一个正直的小龙猫</span> 👍（0） 💬（2）<div>请教老师一个问题：
这个是摄像头采集视频画面，如果是webrtc直播视频流呢？
想录制视频，采集直播流的视频和音频，用什么技术方案实现是最佳的？replaykit2还是ffmepg，他俩对比优缺点是什么？ 
</div>2022-08-24</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/2nM9PaEsM4XTZuqQiavicyRuibcp8n1tBpL9mFTRbeqn47dzU9eGNoicJYUOO8tUiaU6pT2D8rjmG0DlBv1eFVWZrkQ/132" width="30px"><span>Neil43</span> 👍（0） 💬（1）<div>老师你好，我在使用AVFoundation框架的AVAssetWriterinput ，追加SampleBuffer报错，关键代码：
AVAsset WriterInput *videoInput = [AVAsset WriterInput
asset WriterInput WithMediaType:AVMediaTypeVideo
outputSettings:videoSettings];
assetWriter = [[AVAssetWriter alloc] initWithURL: _URL
fileType:AVFileTypeQuickTimeMovie error: &amp;error];
[assetWriter addInput:_videolnput];
BOOL success = [videoInput appendSampleBuffer:sampleBuffer];

具体报错信息：
userInfo={
NSLocalizedFailureReason = An unknown error occurred (-12780),
NSLocalizedDescription = The operation could not be completed,
NSUnderlyingError = Error Domain=NSOSStatusErrorDomain Code=-12780
&quot;(null)”}

请问老师知道大概是什么原因吗？如果appendSampleBuffer方法报错，再调用finishWritingWithCompletionHandler方法，能正常生成视频吗？谢谢。


</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师一个问题：
Q1：AI唱歌，有能够使用的软件吗？（开源、付费的都可以）。 AI唱歌，是指用一个人的声音把一首歌完整的唱出来。比如有特朗普的一段音频（比如30s声音片段），然后软件根据这个声音片段，就可以把《好汉歌》唱出来。效果就是听众认为是特朗普唱的《好汉歌》。</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cf/e2/975f9a2a.jpg" width="30px"><span>月半木子🎊</span> 👍（0） 💬（0）<div>请问老师，这个实现如何自测是否满足需求呢，自测需要关注哪些测试点呢</div>2023-06-13</li><br/>
</ul>