你好，我是刘歧。

我们日常看电视剧，录视频时，最常见的就是MP4格式了。你有没有想过，MP4格式为什么使用得这么广泛呢？

因为MP4标准非常灵活，可扩展性比较好，有很多常见的格式是基于MP4做了一些扩展，然后被应用到比较广的范围，比如CMAF、DASH、HLS。而且MP4的参考标准是一个开放的标准，我们通常以编号为ISO-14496-12来查找标准文档。因为MP4的使用范围比较广，我们在[第3节课](https://time.geekbang.org/column/article/544986)的时候，也着重讲了MP4封装容器格式，你可以回顾一下。

![图片](https://static001.geekbang.org/resource/image/68/6b/689b8f155c2ed9yy6dbb007fa474586b.png?wh=1920x1083 "MP4扩展出来的格式")

基于MP4的重要地位，我这节课来给你讲一讲，如何用FFmpeg、GPAC等工具生成与解析MP4。

尽管FFmpeg的目标是自己不去创造标准，但是难免会有一些工具或者用户会根据自己的臆测做一些定制或者修改，导致与我们公认的标准出现一些偏差。为了让MP4的标准性更好地得到验证，我们通常会选择使用多种工具，所以这节课除了给你介绍FFmpeg对MP4的mux与demux（封装与解封装）之外，我还会介绍一些其他的MP4相关的工具，例如MP4Box、Shaka- Packager。

在我们使用FFmpeg做音视频处理的时候，经常会使用FFmpeg生成MP4文件，或者使用FFmpeg输入MP4文件然后转换成其他格式。这里我们就先来了解一下FFmpeg对MP4都有哪些能力支持。这就需要用到[上节课](https://time.geekbang.org/column/article/548420)的知识了，你可以停下来先想一下我们应该怎么在FFmpeg中查找自己想要的帮助信息。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师几个问题：
Q1：FFmpeg能够生成MP4文件吗？
文中提高用GPAC等工具MP4文件，请问FFmpeg能生成MP4文件吗？

Q2：怎么通过查帮助来解决一个具体问题？
问题：我买了老师的《FFmpeg从入门到精通》，操作第二章的一个例子时遇到问题：
ffplay -debug vis_mb_type -window_title &quot;show vis_mb_type&quot; -ss 30 -t 20 -autoexit cas.mp4

Undefined constant or missing &#39;(&#39; in &#39;vis_mb_type&#39;
[aac @ 00000237ca4cff80] Unable to parse option value &quot;vis_mb_type&quot;
[aac @ 00000237ca4cff80] Error setting option debug to value vis_mb_type.

首先这个问题怎么解决？ 其次，我用的最新的5.1版本，书上用的似乎是3.X版本，感觉应该是版本不同导致的。我尝试了查帮助来解决，但没有成功。 请问：怎么从帮助中查vis_mb_type的用法？ 


Q3：FFmpeg，老师用的时候版本是多少？
我用的是最新的5.1版本，执行ffmpeg -h muxer=mp4后，显示：Default video codec: mpeg4，
缺省视频编码是mpeg4，不是h264。

Q4：moov 与 mdat 的前后位置关系，对播放有什么影响？

Q5：能否提供可执行的mp4info，以及GPAC和Shaka-Packager？
我从官网下载了mp4info,解压后是“MP4Info-0.3.3.gem”，无法执行。老师如果有可执行的mp4info，能否提供一个下载地址？还有GPAC和Shaka-Packager等工具，能否放到一个地方供下载？ （这个有点难为老师，抱歉，不方便的话可以忽略这个问题；我的工作和音视频无关，平时工作忙，每天只能抽出部分时间看专栏，实在没有时间）</div>2022-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/4b/1b/e3b3bcff.jpg" width="30px"><span>jcy</span> 👍（1） 💬（0）<div>简单解答思考题：

加密视频
ffmpeg -i test.mkv -vcodec copy -acodec copy -t 5 -encryption_scheme cenc-aes-ctr -encryption_key 76a6c65c5ea762046bd749a2e632ccbb -encryption_kid a7e61c373e219033c21091fa607bf3b8 test.mp4

解密播放：
ffplay SampleVideo_1280x720_1mb_encrypted.mp4 -decryption_key 76a6c65c5ea762046bd749a2e632ccbb</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b2/c5/6ae0be56.jpg" width="30px"><span>木偶人King</span> 👍（0） 💬（0）<div>打卡</div>2023-07-05</li><br/>
</ul>