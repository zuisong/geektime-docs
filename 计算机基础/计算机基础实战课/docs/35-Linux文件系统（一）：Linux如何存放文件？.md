你好，我是LMOS。

上一节课，我们一起了解了什么是文件和文件系统。接下来的两节课，我们继续深入学习Linux上的一个具体的文件系统——Ext3，搞清楚了文件究竟是如何存放的。

这节课我会带你建立一个虚拟硬盘，并在上面建立一个文件系统。对照代码实例，相信你会对Ext3的结构有一个更深入的认识。课程配套代码，你可以从[这里](https://gitee.com/lmos/Geek-time-computer-foundation/tree/master/lesson35~36)下载。话不多说，我们开始吧。

## 建立虚拟硬盘

要想建立文件系统就得先有硬盘，我们直接用真正的物理硬盘非常危险，搞不好数据就会丢失。所以，这里我们选择虚拟硬盘，在这个虚拟硬盘上操作，这样怎么折腾都不会有事。

其实我们是用Linux下的一个文件来模拟硬盘的，写入硬盘的数据只是写入了这个文件中。所以建立虚拟硬盘，就相当于生成一个对应的文件。比如，我们要建立一个 100MB 的硬盘，就意味着我们要生成 100MB 的大文件。

下面我们用 Linux 下的 dd 命令（用指定大小的块拷贝一个文件，并在拷贝的同时进行指定的转换）生成 100MB 的纯二进制的文件（就是向 1～100M 字节的文件里面填充为 0 ），代码如下所示：

```plain
dd bs=512 if=/dev/zero of=hd.img count=204800

;bs:表示块大小，这里是512字节
;if：表示输入文件，/dev/zero就是Linux下专门返回0数据的设备文件，读取它就返回0
;of：表示输出文件，即我们的硬盘文件
;count：表示输出多少块
```
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/b4/fd/791d0f5e.jpg" width="30px"><span>sN0wpeak</span> 👍（0） 💬（1）<div>为什么block_size = 123</div>2022-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/c8/c8/d23a126b.jpg" width="30px"><span>南城忆潇湘</span> 👍（0） 💬（2）<div>一级间接储存块里的块号索引的储存块中不是文件数据，而是储存的指向储存块的块号，它可以储存 1024&#47;4 个块号，即可索引 1024&#47;4 个储存块。      请问：1024&#47;4这个计算公式的原理是啥</div>2022-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（1）<div>请问一下：为什么在hdisk目录下能创建出超出255个字符的目录呢？</div>2022-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/a6/ad/e65aec4c.jpg" width="30px"><span>苏流郁宓</span> 👍（0） 💬（1）<div>超级块存放在硬盘分区的第2个扇区，文中建立的硬盘不能直接打开（在home下建立hdisk，挂载这上面 单独显示硬盘），需要特殊字符设备软件。这也是真实的硬盘以二进制形式储存，日常能打开的硬盘都是在二进制基础上建立了ext4或者ntfs文件系统！
但建立能打开的文件系统硬盘，它显示的存储空间小于二进制硬盘（无字符设备软件打不开）的存储空间（假如两块硬盘一样大）
实际上硬盘的打开，读写，存储都需要cpu的配合！文件系统的基础是数学，比如画曲线只要5个点就可以确定sin x或者cos x曲线！硬盘存储系统，就是用更少的点储存更多更准确的信息，通过cpu把这些点翻译成信息或者图形！所以二进制硬盘区别于纸质的书籍储存方式，通过类似以点代线的方式（cpu翻译），存储更多的信息！包括图像视频信息！</div>2022-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请问：文件的连接数是指什么？</div>2022-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/cb/c8/ff9f3ffb.jpg" width="30px"><span>赵国辉</span> 👍（0） 💬（0）<div>mac下与losetup相对的命令是什么呢老师。</div>2023-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/7b/cbe07b5c.jpg" width="30px"><span>顾琪瑶</span> 👍（0） 💬（1）<div>老师, 有个问题不理解.
看您给的图中描述, 超级块是在快组下的, 但超级快描述的是全局信息, 为什么还需要每个快组都有超级快信息呢?
还是我理解的不对?</div>2023-01-06</li><br/>
</ul>