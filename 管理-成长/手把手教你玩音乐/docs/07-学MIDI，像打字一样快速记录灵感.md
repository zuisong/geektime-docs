你好，我是邓柯，欢迎你和我一起玩音乐。

前几节课呢，我们学习了库乐队的基本操作，还学习了库乐队中一些乐器组件和演奏界面的使用。不过你在具体操作的过程中，有没有意识到一个问题，就是这些组件虽然能够帮助我们很快搭建好乐曲的段落和结构，但是，我们却没法儿对这些段落进行更细致地编辑。比如在自动弹奏出来的乐句中，修改其中某一个音的音高、节奏、力度等。

所以从这节课开始，我们就一起来学习一些库乐队进阶的编辑功能。今天我们先来讲讲 MIDI 信号的录制与编辑。我会给你演示在库乐队里输入MIDI音符的三种方法，并且还会带着你把《小星星》这首歌的主旋律录进库乐队当中。

## 什么是 MIDI ？

简单来讲，MIDI 可以理解成一种数字乐谱，它是一种包含了诸如音高、音量、节奏、时长，以及乐器、演奏技法、声音效果等各种音乐要素的控制信息。MIDI 信号本身是没有声音的，就像乐谱它本身没有声音一样，你需要为 MIDI 信号加载一个音源，它才能够发出声音。而对于同样的乐谱，你为它加载不同的音色，它听起来的声音也是不一样的。

对了，还记得我们之前提到过的红白机配乐，以及老式诺基亚功能机上的手机铃声吗？它们播放的都是 MIDI 文件。正因为当时的硬件性能差、存储空间小，所以这种 MIDI 信号+音源的方式，要比音频文件更节约空间和硬件性能。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="" width="30px"><span>Geek-chen</span> 👍（1） 💬（1）<div>更新太慢了呀</div>2021-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（1）<div>小白表示，《小星星》录完了，《后会无期》是真不行……</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/14/397145a4.jpg" width="30px"><span>谷鱼</span> 👍（0） 💬（1）<div>😃哈哈，学过一两年钢琴，还是能够看着谱子，把后会无期弹下来，哎，生疏了</div>2021-02-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJEREDDmZco6rPVgOrWqia2DcrTHibZUZ4njEgVgNriavblFkca8UVRjbwibAx4fJx8R4qYNloozrqIuA/132" width="30px"><span>happytree</span> 👍（0） 💬（1）<div>请问，garageband 库乐队，可以把不同的音轨绑定到不同的输出设备上进行播放不一样音轨的声音吗？我看网上只有介绍怎么绑定不同输入设备到不同音轨的方法，没有介绍绑定不同输出设备的方法。</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/66/44/9bbc2b4a.jpg" width="30px"><span>陈璐</span> 👍（0） 💬（0）<div>老师我想问下，如果不是C调的歌曲应该怎么设置呢？比如说G调…</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/1b/9a/009140f7.jpg" width="30px"><span>Indigo</span> 👍（0） 💬（0）<div>老师我想要给iphone做一个nokia tune，求求了</div>2021-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/54/ca/58449d0c.jpg" width="30px"><span>0.01 公分</span> 👍（0） 💬（0）<div>每天累成狗后沉浸地玩一段好开心好开心啊 🎵（以前玩游戏的时间没了hhh</div>2021-04-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoBJeMROTEialDsas1triahDZ9RKH0yDqha8495IdTaJOqnrGKQ5CCmtRIrjlLnY1p1ickicJWeJNrJng/132" width="30px"><span>SongHerz</span> 👍（0） 💬（0）<div>用触屏键盘录入后会无期的时候可以先把速度调慢，修完了再把速度调上去。MIDI键盘应该也可以，不在身边就没试。</div>2021-02-13</li><br/>
</ul>