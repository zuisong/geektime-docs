你好，我是展晓凯。今天我们一起学习使用移动平台的硬件编码器编码AAC。

上一节课，我们学习了AAC编码格式，还用FFmpeg书写了一个AAC编码工具类，这节课我们一起学习一下如何使用平台自身提供的硬件编码方法来给音频编码。因为两个平台的硬件编码器编码出来的是裸的ES流，如果要保存为可播放的AAC，还需要自己加上ADTS的头。

## Android平台的硬件编码器MediaCodec

我们先来看如何使用Android平台提供的MediaCodec来编码AAC。MediaCodec是Android系统提供的硬件编码器，它可以利用设备的硬件来完成编码，大大提升了编码的效率，并且可以节省CPU，让你的App运行起来更加流畅。

但使用MediaCodec编码对Android系统是有要求的，必须是4.1以上的系统，Android的版本代号在Jelly\_Bean以上。而且因为Android设备的碎片化太严重，所以兼容性方面不如软件编码好，你可以根据自己的实际情况决定是否使用Android平台的硬件编码能力。

下面我们来看MediaCodec使用方法。类似于软件编码提供的三个接口方法，这里也提供三个接口方法，分别完成初始化、编码数据和销毁编码器操作。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（2） 💬（1）<div>请教老师几个问题啊：
Q1：AAC可以通过硬件编码，也可以通过硬件解码吗？
Q2：硬件编码只能对于AAC吗？可以用于其他类型的音频文件吗？ 比如mp3。
Q3：MediaCodec对应的硬件设备叫什么啊？ 就是一个专门的编解码芯片吗？可以查询手机是否有硬件编解码芯片吗？
Q4：inputBuffer和outputBuffers是MediaCodec内部维护的吧。那外部是否可以控制buffer的数量和大小？（即，上层应用是否可以控制？）
Q5：codec.queueInputBuffer(bufferIndex,0,len,time,0), 这行代码功能是什么？把时间值填入音频文件吗？ 如果是填入时间值的话，能播放出来吗？
Q6：安卓平台的代码中，编码部分，哪一行代码是编码的？
按道理，应该有一句类似 encode()的代码，但是没有看到这样的代码。难道是把数据放到buffer以后自动编码吗？
Q7：安卓平台编码部分，哪一项表明是AAC编码啊？
文中列出的代码中， 似乎没有看到哪一项标志是AAC啊。（也许是没有看到）
Q8：编码以后怎么还要放回到待编码填充队列？
文中有一句“需要我们自己添加上 ADTS 头部，然后写文件，最后把这个 outputBuffer 放回待编码填充队列里面去”， 已经完成编码了啊，怎么还需要这个操作？
Q9：iOS代码，老师用OC还是swift编码？
Q10：讲硬件编码，怎么会用软件编码？
本讲是说明硬件编码的，但文中iOS部分有一句“编码的实现方式使用兼容性更好的软件编码方式 kAppleSoftwareAudioCodecManufacturer”，怎么又用到软件编码了？</div>2022-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/73/9b/67a38926.jpg" width="30px"><span>keepgoing</span> 👍（0） 💬（2）<div>老师请教一下，kAudioFormatFlagIsPacked是表示交错存储吗，跟其对应的平面存储请问是kAudioFormatFlagIsNonInterleaved吗。如果把输入输出对调一下换成解码场景，参数设置是不是就反过来了，但同样要考虑交错和平铺两种数据格式对吧</div>2022-12-18</li><br/>
</ul>