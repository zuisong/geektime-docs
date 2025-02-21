你好，我是展晓凯。今天我们来一起学习Android平台视频画面的采集。

[上一节课](https://time.geekbang.org/column/article/556012)我们一起学习了iOS平台的视频画面采集，Android平台的采集相对来讲会更复杂一些，因为我们整个系统的核心部分都是在Native层构建的，所以这就会涉及JNI层的一些转换操作。不过不用担心，我会带着你一步步构建起整个系统。

## 权限配置

要想使用Android平台提供的摄像头，必须在配置文件里添加权限要求。

```plain
<uses-permission android:name="android.permission.CAMERA" />
```

Android 6.0及以上的系统，需要动态申请权限。

```plain
if (ContextCompat.checkSelfPermission(MainActivity.this, android.Manifest.permission.CAMERA)!= PackageManager.PERMISSION_GRANTED){
  //没有权限就在这里申请 
  ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, CAMERA_OK); 
}else { 
  //说明已经获取到摄像头权限了 
}
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/64/52a5863b.jpg" width="30px"><span>大土豆</span> 👍（0） 💬（1）<div>老师可以加个微信，或者公众号可以关注吗？😄</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/eb/19/19e706a5.jpg" width="30px"><span>cc</span> 👍（0） 💬（1）<div>老师，我看文章中，你说纹理坐标是从左下角开始的，但是在Android坐标原点好像是左上角</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师两个问题：
Q1：老师用的AS是什么版本？
我目前安装了两个版本，一个是AS3.5，另外一个是AS2021(免安装版本)。如果我的版本和老师的不同，可能会出很多问题。最好保持AS版本一样，避免不必要的问题。

Q2：FFmpeg具有“编辑”音频的能力吗？ 
在win10下，我做过这样的操作，一个3分钟的长音频，一个5秒的短音频，用FFmpeg可以将两个音频合成为一个音频，播放时，前五秒钟，同时听到两个音频的声音，五秒之后，只有长音频的声音。进一步地，通过设置参数，可以让短音频重复播放，合成后的效果是：在长音频文件的播放过程中，短音频文件不停地重复播放，同时听到两个音频文件的声音。
这算是“音频”编辑的能力吗？
在win10下面可以合成声音，在移动端也能实现“音频合成”的功能吗？</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/44/5e/a882dc64.jpg" width="30px"><span>北国风光</span> 👍（0） 💬（0）<div>请问项目整体代码在哪里？</div>2023-04-27</li><br/>
</ul>