你好，我是LMOS。

在上一节课中，我们通过对IO Cache的学习，知道了IO Cache缓存了IO设备的数据，这些数据经过IO 调度器送给块层，进而发送给IO设备。

今天我们再往下一层探索，以Linux为例，看看Linux是如何管理多个IO外设的。我们先从例子出发，了解一下设备在Linux中的与众不同，然后看看设备分类及接口，分析一下应用开发人员应该如何使用它们，最后我会带你一起实现一个设备加深理解。

这节课的配套代码，你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson32)下载。话不多说，我们开始吧。

### 文件和外设的关系

用几十行代码在Linux上读写一个文件，我们都很熟悉吧。若是不熟悉，百度、谷歌都可以让我们熟悉。

我们今天要写的这个小例子就是从读取一个文件开始的。想要读取文件，首先得知道文件在哪里，也就是需要知道文件路径名，知道了文件路径名，再进行“三步走”就可以：打开它、读取它、关闭它。一句话，open、read、close一气呵成。

那么这个文件是什么呢，路径名如下所示：

```plain
"/dev/input/event3"
```

看了路径名，我们知道enent3文件在根目录下dev目录的input目录之下。从名称上看，这好像与设备、输入、事件有关系，我这里先卖个关子，看完后面的讲解，你自然就知道答案了。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（2）<div>读写一个设备文件，运行不起来，一直阻塞在这行：ret = read(fd, &amp;in, sizeof(struct input_event));</div>2022-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请问：对于一个驱动程序，Linux是在&#47;dev目录下面创建一个文件来与之对应吗？</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>dev下面有net文件夹和network_latency和network_throughput字符设备
预估网络文件信息存储在内存上，上述文件构成设备登记函数！</div>2022-10-15</li><br/>
</ul>