使用过音视频会议或在线教育等实时互动软件的同学都知道，在打开摄像头（Camera）或麦克风（Micphone）的时候，首先要对其进行检测，检测的内容包括：

- 电脑/手机上都有那些音视频设备？
- 我们选中的音视频设备是否可用？

以手机为例，它一般会包括前置摄像头和后置摄像头。我们可以根据自己的需要，选择打开不同的摄像头。当然，手机上不单有多个摄像头，麦克风的种类就更多了， 如：

- 系统内置麦克
- 外插的耳机
- 蓝牙耳机
- ……

以上这些设备，我们都可以通过手动或自动的方式打开它们。

那么，WebRTC是否提供了相关的接口，以便我们查询自己机子上都有哪些音视频设备呢？答案是肯定的。

下面我们就来看看如何使用浏览器下 WebRTC API 来显示我们的音视频设备吧。

## WebRTC处理过程

在正式讲解之前，咱们先回顾一下WebRTC 的整体处理过程图，以便让你清楚地知道咱们这篇文章在整个处理过程中的位置。

![](https://static001.geekbang.org/resource/image/e9/1c/e9a2fd3adee1568e4171addce5b64a1c.png?wh=1142%2A571)

WebRTC 1对1音视频实时通话过程示意图

上面这幅图与第一篇文章中的图几乎是一模一样的。其差别在于，我将图中两个**音视频设备检测模块**置红了。

这样，我们本文所讲的内容在整个 WebRTC 处理过程中的位置就一目了然了！

## 音视频设备的基本原理

既然说到音视频设备，那么我们再顺便介绍一下音视频设备的基本工作原理，对于这些设备工作原理的了解，会为你后续学习音视频相关知识提供很大的帮助。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/87/62/f99b5b05.jpg" width="30px"><span>曙光</span> 👍（6） 💬（1）<div>1 我测试的结果没有videooutput(显示器不算么？)
2 default和communications 有啥区别？如何显示它们的id信息？
3 ()是lable,老师说需要HTTPS才能看到，有其他方法么？
谷歌浏览器，测试结果如下：
audioinput:(): id = default
audioinput:(): id = communications
audioinput:(): id = 101a8.....
videoinput:(): id = f9b4.....
audiooutput:(): id = default
audiooutput:(): id = communications
audiooutput:(): id = 71b3....</div>2019-07-29</li><br/><li><img src="" width="30px"><span>宇宙之王</span> 👍（4） 💬（2）<div>请问老师，我用的自己生成的证书https和阿里云的ECS主机（CentOS系统），用第一讲和第三讲，第四讲（后面还没试）的代码可以正常获取摄像头的图像，采集视频，并实现保存下载视频功能，但是这一讲的代码我获取label也是为空，是不是还有什么别的限制，最关键的是本地运行也获取不到，是什么原因呢？谢谢老师！</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/90/d0/48037ba6.jpg" width="30px"><span>李跃爱学习</span> 👍（3） 💬（4）<div>老师音频采样率解释得很清楚，可是采样大小没有深入解释，能否补充一下，不同采样大小意味着什么差别？</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/a7/6ef32187.jpg" width="30px"><span>Keep-Moving</span> 👍（3） 💬（2）<div>想问一下，后续的实例代码也都是js语言的吗？</div>2019-07-18</li><br/><li><img src="" width="30px"><span>Geek_a6a976</span> 👍（2） 💬（1）<div>作业：
应该可以用上一节课讲的MediaStreamConstraints中的MediaTrackConstraints设置要读取的deviceId, groupId来选择要获取的设备的stream。
想问老师，设备掉线后，是否有类似onchange事件来异步通知</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/38/6d/4efc1bea.jpg" width="30px"><span>在水一方</span> 👍（2） 💬（1）<div>移动端（安卓，iOS）有没有一种浏览器，能完美支持webrtc？</div>2020-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（2） 💬（1）<div>我这通过 navigator.mediaDevices.enumerateDevices() 获取到的设备列表想请教下老师：
1: 对于每个设备 还有个 groupId ，这个字段是干什么用的？ 每一组的设备还有特殊的含义吗？
2: 获取的设备分为 InputDeviceInfo 和 MediaDeviceInfo ，这里 InputDeviceInfo 是指输入设备信息，那么MediaDeviceInfo（下面的kind:都是 &quot;audiooutput&quot; 没有 videooutput）是指输出的设备信息吗？</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/a1/2857f15d.jpg" width="30px"><span>chong-de.fang</span> 👍（1） 💬（1）<div>请问在本地，用域名的方式可以获取到设备信息，但是label值为空，这是什么问题？</div>2020-01-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/33/31/8db0ff30.jpg" width="30px"><span>月光伴奏</span> 👍（1） 💬（1）<div>我本地测试不用https也能拿到lable 哈哈</div>2019-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3a/d6/485590bd.jpg" width="30px"><span>赵健</span> 👍（1） 💬（3）<div>需要注意的是，出于安全原因，除非用户已被授予访问媒体设备的权限，否则 label 字段始终为空 --- 老师，您好，不太明白何为用户已被授予访问媒体设备的权限？比如，第一节课里面的电脑的摄像头已经被打开了，这个还不算有访问设备的权限吗？</div>2019-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/62/78/6e7642a3.jpg" width="30px"><span>王蓬勃</span> 👍（0） 💬（0）<div>好像都没有显示 
enmurateDevices is support
client.js:17 devicesInfos: [object InputDeviceInfo],[object InputDeviceInfo],[object MediaDeviceInfo]
client.js:18 devicesInfos: undefined
client.js:19 devicesInfos: undefined
client.js:22 audioinput: label = : id = : groupId = 
client.js:22 videoinput: label = : id = : groupId = 
client.js:22 audiooutput: label = : id = : groupId = </div>2024-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/62/78/6e7642a3.jpg" width="30px"><span>王蓬勃</span> 👍（0） 💬（0）<div>enmurateDevices is support
client.js:17 devicesInfos: [object InputDeviceInfo],[object InputDeviceInfo],[object MediaDeviceInfo]
client.js:18 devicesInfos: undefined
client.js:19 devicesInfos: undefined
client.js:22 audioinput: label = : id = : groupId = 
client.js:22 videoinput: label = : id = : groupId = 
client.js:22 audiooutput: label = : id = : groupId = </div>2024-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/64/39/2d8a2d69.jpg" width="30px"><span>.</span> 👍（0） 💬（0）<div>app端监听插拔耳机失败，但pc端可以，这个地方有特别之处吗</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/64/39/2d8a2d69.jpg" width="30px"><span>.</span> 👍（0） 💬（0）<div>在pc端插拔耳机可以监听到，但在手机端却检测不到。这个有什么好办法吗？</div>2022-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/14/57cb7926.jpg" width="30px"><span>ShawnWu</span> 👍（0） 💬（0）<div>好像插拔设备，不会自动切换，我们自己实现的切换</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/58/31205087.jpg" width="30px"><span>恋着歌</span> 👍（1） 💬（1）<div>deviceID 切换，通过观察 enumerateDevices() 返回的数据，目的是要向 default 切换。对目标设备信息做一次拷贝，修改 deviceId 为 default，修改 label 加上前缀“默认 - ”。不知道老师的题目是不是这样解答？</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/73/f5/6f11f003.jpg" width="30px"><span>loong</span> 👍（0） 💬（1）<div>老师好，deviceId为空是什么原因？ 有3个kind显示，也有groupId。看你这个才接触js，对这个代码运行和要搭建的环境还不熟悉。我是直接点开html文件在浏览器中打开运行的，是否这样就可以？不用管https什么的？</div>2020-04-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erxJYxzce3mZpuZFJNyTAvCibzLUTYbZepaBPNd7ichZgkMeibkQLmNzeb63zda1iaKJ6aIewUTA517hQ/132" width="30px"><span>Geek_6jxh2r</span> 👍（0） 💬（1）<div>webrtc在移动web的兼容性如何解决呢</div>2020-03-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIQYc8seCHrRfJicqCWDfUap4jdHWnJ39ezlpvIY5sbwZP8ze9lFE572hzeNEY07nHWVjaR0QLjgyw/132" width="30px"><span>Geek_5a0689</span> 👍（0） 💬（2）<div>老师，咨询一下，我获取到的label都是空，我不晓得如何设置https，调用getusermedia是直接将第一讲的js代码复制到第二讲的开源代码中么？</div>2020-03-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/dQZH4oEsCUjunqCIs4ls8iaAFsgzc7lQVFtgUd6RicKt3DSpANXAQCsLfU5MmgcRwJl1L9kdr3H5L5QM1BqMxPlg/132" width="30px"><span>随风的小猪</span> 👍（0） 💬（1）<div>老师，https访问是在html中配置的么？</div>2020-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4b/02/ee837c4b.jpg" width="30px"><span>子非鱼焉知鱼之乐</span> 👍（0） 💬（1）<div>老师 android ios是怎么实现音视频呢</div>2019-12-20</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJoNVHqRL5iatEoMgfFAaGFZxD8ic6CicxKI9Facp4bzAkNMAfaduSENlPOafs6dOGawibhNv3V9lVowQ/132" width="30px"><span>SherwinFeng</span> 👍（0） 💬（4）<div>小白的基本思路是这样的：
通过enumerateDevices（）遍历所有的输入输出设备列表，如果当前设备的id和想要访问的设备id一致，就通过某个函数使用它。</div>2019-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/fd/4cc7212e.jpg" width="30px"><span>style</span> 👍（0） 💬（2）<div>老师我打印了下devices信息，有两点不明白
kind=audioinput label= id=default
kind=audioinput label= id=communications
kind=audioinput label= id=afab9796f6f60aa5d0a7c6604619ccbf452e5abfbf33a7adf76839f480ae3a14
kind=audiooutput label= id=default
kind=audiooutput label= id=communications
kind=audiooutput label= id=8e2cdf7151acd5c488d56bb1b397dcf23063d4cdf7a3a39b3a9c723090073c6b
 kind=audiooutput label= id=d1c85beda42b8586f603e24335eec7e430d88320a91a99c4eee3d2eecedd581c
1，我把电脑上的耳机，麦都拔下来了，但还是输入和输出设备
2，我也授权访问麦克风了，但是我打印的label始终为空</div>2019-08-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3b/71/b7094a80.jpg" width="30px"><span>Sunsmile</span> 👍（0） 💬（2）<div>老师，js可以实现音量柱吗？怎样获取音量柱数据的呢？</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/d2/d7a200d5.jpg" width="30px"><span>小鸟淫太</span> 👍（0） 💬（1）<div>我也是 mac 环境，我以为接入耳机后id也会发生变化。把label打出来就看到label变了。。
老师我还有个问题，Safari只有两个，分别是 内建麦克风 和 FaceTime 高清摄像头（内建）。没看到有audioOutput，是权限问题吗？</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/07/d2/d7a200d5.jpg" width="30px"><span>小鸟淫太</span> 👍（0） 💬（1）<div>老师好，我想问一下这个列表里的 audioOutput 有耳机吗？我接入耳机和拔掉耳机打印出来的设备数量没有变化。</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/64/7e39a739.jpg" width="30px"><span>麦晓杰alwaysu</span> 👍（0） 💬（1）<div>学习打卡！！</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/21/a33cc944.jpg" width="30px"><span>熊出没</span> 👍（0） 💬（1）<div>怎么把这里面的代码用起来 JS还是太陌生了</div>2019-07-20</li><br/><li><img src="" width="30px"><span>tommy_zhang</span> 👍（0） 💬（1）<div>怎么实现摄像头的关闭操作？</div>2019-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/46/58/31205087.jpg" width="30px"><span>恋着歌</span> 👍（0） 💬（1）<div>在调用 getUserMedia 的时候，可以通过 MediaStreamConstraints 参数可以指定采集设备的deviceId。但是这样只能切换输入设备。</div>2019-07-18</li><br/>
</ul>