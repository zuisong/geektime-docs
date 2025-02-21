你好，我是蔡元楠。

今天我要与你分享的主题是“Pipeline I/O: Beam数据中转的设计模式”。

在前面的章节中，我们一起学习了如何使用PCollection来抽象封装数据，如何使用Transform来封装我们的数据处理逻辑，以及Beam是如何将数据处理高度抽象成为Pipeline来表达的，就如下图所示。

![](https://static001.geekbang.org/resource/image/a5/94/a56f824d0dc8b3c1a777595b42c4b294.jpg?wh=1994%2A1302)

讲到现在，你有没有发现我们还缺少了两样东西没有讲？没错，那就是最初的输入数据集和结果数据集。那么我们最初的输入数据集是如何得到的？在经过了多步骤的Transforms之后得到的结果数据集又是如何输出到目的地址的呢？

事实上在Beam里，我们可以用Beam的Pipeline I/O来实现这两个操作。今天我就来具体讲讲Beam的Pipeline I/O。

### 读取数据集

一个输入数据集的读取通常是通过Read Transform来完成的。Read Transform从外部源(External Source)中读取数据，这个外部源可以是本地机器上的文件，可以是数据库中的数据，也可以是云存储上面的文件对象，甚至可以是数据流上的消息数据。

Read Transform的返回值是一个PCollection，这个PCollection就可以作为输入数据集，应用在各种Transform上。Beam数据流水线对于用户什么时候去调用Read Transform是没有限制的，我们可以在数据流水线的最开始调用它，当然也可以在经过了N个步骤的Transforms后再调用它来读取另外的输入数据集。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（3） 💬（0）<div>自定义输入输出能个代码示例吗？按时间分区以parquet格式写入hdfs，代码要怎么写？</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/3c/8bb9e8b4.jpg" width="30px"><span>Mr.Tree</span> 👍（0） 💬（0）<div>之前讲PCollection不会写磁盘，读取操作时，会将读取的结果全部存入到一个PCollection里面，如果返回的数据很巨大，或者说读取的数据是无边界的，该如何处理？</div>2023-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/3d/93aa82b6.jpg" width="30px"><span>Junjie.M</span> 👍（0） 💬（1）<div>一个pipeline可以有多个input和output吗</div>2020-04-11</li><br/>
</ul>