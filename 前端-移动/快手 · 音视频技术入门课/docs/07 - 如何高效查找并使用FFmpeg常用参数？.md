你好，我是刘歧。

我们讲述直播推流的时候曾简单介绍过[FFmpeg推直播流](https://time.geekbang.org/column/article/546485)的操作，但是并不是特别全面，遇到一些问题的时候我们还是无法很好地解决。有时候，我们想要使用FFmpeg的某个功能，但不知道怎么查找，甚至可能不知道FFmpeg是否包含我们需要的能力。那么这节课我们会更全面地介绍FFmpeg中常用的参数，还有遇到问题的时候如何确认FFmpeg是否可以达到我们预期的目的。

如果你是第一次使用FFmpeg，肯定会有很多疑惑，尤其是看到命令行的一堆参数之后。所以这节课我会一步一步引导你先学会使用FFmpeg，最后让你拥有自己深度挖掘FFmpeg里面各种黑科技的能力。先吃到“鱼”，然后学会“钓鱼”，之后你就可以自己慢慢收获各种“鱼”了。

## FFmpeg 输入输出组成

FFmpeg的工作原理比较简单，它没有指定输出文件的参数。一般的工具都会带一个-o来指定输出文件，但FFmpeg不是，它不用-o指定输出，FFmpeg自己会分析命令行然后确定输出。例如我们输入这么一段命令：

```plain
ffmpeg -i i.mp4 a.mp4 -vcodec mpeg4 b.mp4
```

这段命令会输出两个文件，分别是a.mp4和b.mp4。

```plain
(base) liuqi05:xx liuqi$ ls
a.mp4 b.mp4
(base) liuqi05:xx liuqi$
```
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（1） 💬（2）<div>老师想请教一下，如果对于 -filter_complex 这种命令完全不了解其用法和作用，应该怎么通过ffmpeg -help相关的内容进行学习，感谢！</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ec/f4/3c569056.jpg" width="30px"><span>西格玛</span> 👍（0） 💬（1）<div>老师的课程内容很饱满，就是部分命令不是太准确，苦了我们初学者，比如这篇里面的&quot;视频操作部分&quot;-vr：设置视频的帧率；应该是 &quot;-r&quot;,我试了好久 “-vr”不可以的
</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/d4/cc/dfd4a7f1.jpg" width="30px"><span>Octo</span> 👍（0） 💬（1）<div>请教老师一个问题，我在用ffmpeg对mp4视频做分割后，发现很多视频播放软件无法打开分割后的视频文件，这一般是什么问题呢？
命令是：
ffmpeg -i xxx.mp4 -vcodec copy -acodec copy -ss 5 -to 25 xxx_out.mp4</div>2022-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：“做解码后再编码”是解释谁的？
文中有这句话：“来进行只转封装不转码（做解码后再编码）的操作”，括号中的“做解码后再编码”是用来解释“转码”的吧。 刚开始看，以为是解释“只转封装不转码”的。
Q2: H.264查询结果矛盾问题。
命令：ffmpeg -encoders | grep H.264
输出：
V..... h264_v4l2m2m         V4L2 mem2mem H.264 encoder wrapper (codec h264)
 V....D h264_vaapi           H.264&#47;AVC (VAAPI) (codec h264)
命令输出结果说明有H,264

但是,用命令：ffmpeg -h encoder=libx264
输出：Codec &#39;libx264&#39; is not recognized by FFmpeg.

为什么又说没有H.264? 不是矛盾吗？

Q3：FFmpeg可以应用到Android、iOS上吗？
Q4：源码目录下面没有make文件但能执行，为什么？
从官网上下载5.1源码，解压后生成ffmpeg目录，先再此目录下面执行：.&#47;configure，
“ls –al | grep make”没有make这个文件。 输入“make”，刚开始不能执行，提示没有此文件，后来又试了几次，突然就能执行了。 请问：没有make文件，怎么就能执行了？
Q5：添加meta参数信息的命令，输入文件是什么？
ffmpeg -f lavfi -i testsrc=s=176x144 -metadata title=&quot;This Is A Test&quot; -t 2 out.mp4， 这个命令中，源文件是什么？ 没有源文件的话，生成的out.mp4没有实际内容吧。</div>2022-08-08</li><br/><li><img src="" width="30px"><span>geek</span> 👍（0） 💬（1）<div>貌似本节的小结思维导图，串台了。
</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（2） 💬（1）<div>尝试回答一下思考题：
1. 先用 ffprobe -show_format test.mkv 查看视频文件的 duration，假设这里的 duration 是 22.47
2. 用如下命令生成新的视频文件 out.mkv，其在原来 test.mkv 视频文件上会叠加一个 logo，播放时，按照视频进度比例从左下角向右下角移动

    ffmpeg -re -i test.mkv -vf &quot;movie=logo.PNG[test];[in][test]overlay=x=&#39;if(gte(t,0), t*(W-w)&#47;20.47, NAN)&#39;:y=H-h [out]&quot; out.mkv</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-25</li><br/>
</ul>