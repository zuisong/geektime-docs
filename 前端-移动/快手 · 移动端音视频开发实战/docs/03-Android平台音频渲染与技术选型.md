你好，我是展晓凯。

前两节课我们一起学习了iOS平台的音频渲染技术，深入地了解了AudioQueue和AudioUnit两个底层的音频框架，了解这些音频框架便于我们做技术选型，可以给我们的应用融入更强大的功能。那除了iOS平台外，Android平台的音视频开发也有着相当大的需求，所以这节课我们一起来学习Android平台的音频渲染技术。

由于Android平台的厂商与定制Rom众多，碎片化特别严重，所以系统地学习音频渲染是非常重要的。这节课我会先从音频渲染的技术选型入手，向你介绍Android系统上渲染音频方法的所有可能性，然后依次讲解常用技术选型的内部原理与使用方法。

## 技术选型及其优缺点

Android系统为开发者在SDK以及NDK层提供了多种音频渲染的方法，每一种渲染方法其实也是为不同的场景而设计的，我们必须要了解每一种方法的最佳实践是什么，这样在开发工作中才能如鱼得水地使用它们。

### SDK层的音频渲染

Android系统在SDK层（Java层提供的API）为开发者提供了3套常用的音频渲染方法，分别是：MediaPlayer、SoundPool和AudioTrack。这三个API的推荐使用场景是不同的。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/c3/eb150080.jpg" width="30px"><span>bentley</span> 👍（0） 💬（1）<div>请教教老师一个问题：文中提到AAudio在一些品牌的特殊 Rom 版本中适配性不是特别好，方便说一下是那些品牌的什么ROM吗？</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>请教老师两个问题：
Q1：具有“音乐弹幕”功能的APP叫什么？
开篇词中老师提到“我所在的团队开发并维护了唱鸭、鲸鸣、虾米音乐等产品。当时我们将弹唱的实时耳返做到了业界最佳并独创了音乐弹幕的交互形式”，
请问：具有“音乐弹幕”功能的APP的完整名字叫什么？ 我想下载一个。知道APP名字后我可以根据名字从应用市场上搜。

Q2：文中介绍的安卓自身的音频组件能实现“混音”功能吗？
SDK中有MediaPlayer、SoundPool 和 AudioTrack三种方法。Native层有OpenSL ES、AAudio，请问这些方法能实现音频的“混音”功能吗？（即：在一个音频上再叠加另外一个音频）。</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/86/73/5190bbde.jpg" width="30px"><span>苏果果</span> 👍（0） 💬（1）<div>老师讲的很详细，最近新的很需要这门技术加持😭</div>2022-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/7b/dd/d5efdcaf.jpg" width="30px"><span>逝去</span> 👍（0） 💬（0）<div>我去。我以为是视频 原来是音频</div>2023-07-28</li><br/>
</ul>