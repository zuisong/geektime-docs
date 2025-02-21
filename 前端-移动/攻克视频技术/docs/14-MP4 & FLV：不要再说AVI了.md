你好，我是李江。

前面我们花了很长的时间学习了视频编码和视频传输弱网对抗的知识点。从今天开始我们来学习几个视频封装和播放的知识点。我们先来学习一下什么是音视频封装。之后我们再学习如何做音视频同步。

其实相比视频编码和传输，音视频封装应该是非常简单的知识点了。而且我们前面还学习过RTP打包，RTP打包音视频数据其实一定程度上也可以算是一种封装。我们今天再介绍两种常用的封装，一种是FLV，一种是MP4，相信你对这两种文件一点儿也不陌生。

音视频封装其实就是将一帧帧视频和音频数据按照对应封装的标准有组织地存放在一个文件里面，并且再存放一些额外的基础信息，比如说分辨率、采样率等信息。那到底怎么组织这些基础信息还有音视频数据呢？我们接下来先看看FLV是怎么做的。

## FLV

FLV是一种非常常见的音视频封装，尤其是在流媒体场景中经常用到。FLV封装也是比较简单的封装格式，它是由一个个Tag组成的。Tag又分为视频Tag、音频Tag和Script Tag，分别用来存放视频数据、音频数据和MetaData数据。

下图就是FLV的总体结构图：

![图片](https://static001.geekbang.org/resource/image/38/c0/38cc18a2a824e2001ae4d38818e691c0.jpeg?wh=1920x1080)

其总体格式图如下：

![](https://static001.geekbang.org/resource/image/d9/00/d9e526be063eb8382535caa585d9f600.jpeg?wh=1552x1190)

### FLV Header

其中，FLV Header占用9个字节。前3个字节是文件的标识，固定是FLV。之后的1个字节表示版本。在之后的1个字节中的第6位表示是否存在音频数据，第8位表示是否存在视频数据，其他位都为0。最后的4个字节表示从文件开头到FLV Body开始的长度，一般就是等于9。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/37/5a/16cb9009.jpg" width="30px"><span>裕鹏</span> 👍（1） 💬（1）<div>请问，如果有sei帧，那是保存在和sps pps同一个位置吗？
</div>2022-08-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erCsjMVpe5IvFIbnHOHUDR9vOa6TyJZs3La4iaP2ujficLwZfhibXR209O65fxicUIMMPxfD084Ngb1hw/132" width="30px"><span>何祖坚</span> 👍（0） 💬（1）<div>总体格式图中 tag header 只展示了10个字节， 但实际有11个字节。还有个字节哪去了呢？</div>2022-09-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erwtNpjvg3LElFyWtatwmtaticiatj1RUAe9bt14vYOGyHCicwxhRJjZibZhibsyXpffkuC2mrPIh6kbMg/132" width="30px"><span>Geek_6b760c</span> 👍（0） 💬（2）<div>想问一下老师，flv的一个视频tag还有mp4的一个sample是对应一个帧还是对应一个NALU呢</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（4）<div>不是太明白这些视频格式flv&#47;avi&#47;mpeg&#47;rmvb等跟前面谈到的视频编码和传输控制有什么关系？希望老师能够解答一下。</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/88/cc/e1ba2379.jpg" width="30px"><span>一身龙骨</span> 👍（0） 💬（1）<div>因为flv结构简单稳定，所以更适合流媒体</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/89/ed/79fb5c71.jpg" width="30px"><span>陈诚</span> 👍（0） 💬（1）<div>请问一下：mp4文件中，sps，pps只是存储一组吗？后续来的sps，pps直接丢弃，还是sps，pps也可以存储多组？ </div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/80/99/abe64707.jpg" width="30px"><span>翻山越岭</span> 👍（6） 💬（0）<div>1)flv,mpeg和rmvb文件可以任意大小，不需要通过索引分包，任意位置可以直接解析分包  2)mp4，avi一定要依赖索引表才行，开始就要固定好位置，如果索引表在尾部，就没办法解析</div>2021-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/1f/a58f27de.jpg" width="30px"><span>罗瑞一</span> 👍（1） 💬（1）<div>sample是什么，我还是没太理解，和frame 有什么关系。另外视频元数据在哪呀
</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/e3/0a094b50.jpg" width="30px"><span>Wales</span> 👍（0） 💬（0）<div>思考题：
FLV格式的①音视频数据和②解码必要信息是均匀分布的，在时间和空间上颗粒度都很小，对于实时生成的音视频数据，以流的方式传输和解码，实时性好。

而MP4格式的音视频数据和解码必要信息是分开存放的，时空颗粒度很大，不方便以流的形式传输和实时解码。</div>2022-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/83/4a/3e08427e.jpg" width="30px"><span>药师</span> 👍（0） 💬（0）<div>老师 标题“MP4 &amp; FLV：不要再说AVI了”文中没有呼应呢</div>2022-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/24/33/bcf37f50.jpg" width="30px"><span>阿甘</span> 👍（0） 💬（0）<div>FLV的Script Tag的Data里面有vedio&#47;audio codec id表示音视频的编码类型，为什么音视频的Tag Data还需要重复音视频的编码类型呢？</div>2022-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/d7/c7/f3e783e8.jpg" width="30px"><span>Max(Deguang)</span> 👍（0） 💬（0）<div>现在是不是fmp4在流媒体用的比较多？</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/20/abb7bfe3.jpg" width="30px"><span>Geek_wad2tx</span> 👍（0） 💬（0）<div>MP4中stbl box中是视频编解码信息，mdat box中的音视频裸数据，只要拿到整个MP4文件，才能完整解码播放</div>2021-12-22</li><br/>
</ul>