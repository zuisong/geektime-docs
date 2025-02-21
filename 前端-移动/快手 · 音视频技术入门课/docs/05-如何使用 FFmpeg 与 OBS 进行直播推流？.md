你好，我是刘歧。

前面四节课，我们介绍了音视频与直播相关的基础知识，那么接下来我们就要进入实战阶段了。学完这个部分，音视频处理的常用工具怎么用，你就能心中有数了。

前面我们虽然了解了什么是直播，直播服务器可以用到哪些开源项目。但直播推流到底怎么实现并没有详细展开，所以这节课我们重点讲讲怎么基于FFmpeg推直播流。如果你的业务场景用FFmpeg不太方便，我还提供了另一个方法——桌面工具OBS推流。相信学完之后，你就能轻松搞定推流。

首先，我们做直播推流的前提是要有直播服务器接收直播流，所以需要我们自己建设一个流媒体服务器。我们可以根据上一节课提到的开源直播服务器的[官方文档](https://github.com/ossrs/srs/wiki/v5_CN_Home)部署直播服务器，也可以挖掘自己当前使用的直播服务平台的服务器接收直播流。为了方便演示，我使用快手的直播云服务来接收我推的直播流。界面如下：

![图片](https://static001.geekbang.org/resource/image/d4/0f/d478c987355cff9dc4f1a7fc849b930f.png?wh=2634x1616)

## FFmpeg推流

通常，推流服务器的管理界面会提供一个收流的RTMP服务器地址，还会提供一个直播流的流名称，也叫串流密钥。例如推流的RTMP服务器地址是rtmp://publish.x.com/live，串流密钥是stream，那么最后组成的推流地址就是rtmp://publish.x.com/live/stream。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/HWfgYFkH80yh2yCWEAK430aZ1e9BbvQI4DN9q8ib4Czc8DTHeWmmIuep74wBIRGARhJd6eY6Tpt3QUSpAicDIHNw/132" width="30px"><span>Geek_e2e4e9</span> 👍（3） 💬（2）<div>ffmpeg安装太费劲了，分享个靠谱的文档：https:&#47;&#47;www.jianshu.com&#47;p&#47;663267e13769</div>2022-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e7/a9/b09e3701.jpg" width="30px"><span>村口大发</span> 👍（1） 💬（1）<div>请教一下老师，按照上面说的，试了一下ffmpeg推流，不过一直错误，难道是我参数有误？信息如下：xxx@xxx-MB4 FFmpeg % ffmpeg -re -f  -i &#47;Users&#47;allenchen&#47;workspace&#47;FFmpeg&#47;output.flv lavfi -i testsrc=s=1280x720:r=25 -pix_fmt yuv420p -vcodec libx264 -f flv rtmp:&#47;&#47;open-push.voip.yximgs.com&#47;gifshow&#47;kwai_actL_ol_act_9934790925_strL_origin?sign=633d0143-c210c0d7d91c2c1849c18bbeeac98244&amp;ks_fix_ts
输出内容：
[4] 32198
zsh: no matches found: rtmp:&#47;&#47;open-push.voip.yximgs.com&#47;gifshow&#47;kwai_actL_ol_act_9934790925_strL_origin?sign=633d0143-c210c0d7d91c2c1849c18bbeeac98244
[4]    exit 1     ffmpeg -re -f -i &#47;Users&#47;allenchen&#47;workspace&#47;FFmpeg&#47;output.flv lavfi -i      -
zsh: command not found: ks_fix_ts</div>2022-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（1）<div>老师，请问抖音，B站等平台提供的Pc直播工具，算是类似OBS的推流工具吗？</div>2023-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b1/55/249c3abd.jpg" width="30px"><span>包美丽</span> 👍（0） 💬（1）<div>成功了！</div>2022-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/c0/64/e6539baf.jpg" width="30px"><span>Geek_3b601e</span> 👍（0） 💬（1）<div>大师兄 答案是什么，直播的过程中怎么看分辨率和帧率</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d5/43/2af09681.jpg" width="30px"><span>晓风残月</span> 👍（0） 💬（1）<div>老师，我想做个远程控制Android平板，Android录屏用H264编码，服务器做转发（NAT穿越局限太大），但服务器只有5M带宽，还跑着别的项目，同一时刻最多有一个设备远程连接,您觉得我用什么传输协议好一些？RTMP还是RTSP或者是其他？麻烦告知一下</div>2022-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师一个问题：
Q1：我对于“FFmpeg推流操作步骤”的理解是： Step1：手机上安装快手APP，创建一个直播间，该直播间会有文中提到的收流地址，Step2：在PC机上安装FFmpeg，安装后采用命令行来推送视频到直播间的收流地址。 我的理解是否对？</div>2022-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/e7/a9/b09e3701.jpg" width="30px"><span>村口大发</span> 👍（1） 💬（0）<div>补充下上面推流失败的后续，经老师的指出，对推流命令中的目标地址url必须加上双引号，加上双引号之后还是报错，后来发现有参数的顺序错了，最终执行OK的命令如下：

ffmpeg -re -i &#47;Users&#47;allenchen&#47;workspace&#47;FFmpeg&#47;output.flv -f lavfi -i testsrc=s=1280x720:r=25 -pix_fmt yuv420p -vcodec libx264 -f flv &quot;rtmp:&#47;&#47;open-push.voip.yximgs.com&#47;gifshow&#47;kwai_actL_ol_act_9934790925_strL_origin?sign=633d0143-c210c0d7d91c2c1849c18bbeeac98244&amp;ks_fix_tsb&quot;

希望对其他同学有帮助</div>2022-08-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6OV33jHia3U9LYlZEx2HrpsELeh3KMlqFiaKpSAaaZeBttXRAVvDXUgcufpqJ60bJWGYGNpT7752w/132" width="30px"><span>dog_brother</span> 👍（1） 💬（0）<div>之前基于nginx搭建过直播服务器</div>2022-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/41/4d/f6d6d13a.jpg" width="30px"><span>啊良梓是我</span> 👍（0） 💬（2）<div>云直播仅对媒体政务号和企业认证账号开放，其他账号请使用直播伴侣或快手App开播，并遵守快手直播规范</div>2023-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/45/60/abb7bfe3.jpg" width="30px"><span>徐溪越</span> 👍（0） 💬（0）<div>ffplay -i
</div>2022-08-21</li><br/>
</ul>