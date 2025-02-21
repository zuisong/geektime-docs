你好，我是蔡元楠。

专栏上线已经一个月了，在这里我要先感谢大家的留言，留言的对答可以使我们互有补益。

这段时间，我发现留言中的很多问题都很有价值，希望你也可以看到。所以，我根据已发布的文章中的思考题，从留言中摘录了一些典型的、常见的问题做出答疑集锦，最终成为了今天你看到的“特别福利篇”。

## “[开篇词](https://time.geekbang.org/column/article/90067)”问题精选

问题一：学习大规模数据处理需要有什么基础？

![](https://static001.geekbang.org/resource/image/a6/05/a6b4f451fde7e70d80649889d4d9b005.jpg?wh=1057%2A1453)

这是一个很好的问题，虽然专栏已经更新了一个月，我还是要把这个开篇词中的提问放进来。就像你看到的那样，有好几位读者都问了类似的问题。

其实在最开始做专栏的内容设计时，我并没有对读者的知识背景作任何假设。

所以，即使是一些基础的技术概念，我也会举例解释一下（如果你已经会了可能会觉得啰嗦，这时候就需要你照顾一下其他同学了）。如果你有一些语言的编程经验（任何语言都可以）的话，看文章的理解速度会快一点。文章中会有一些示例代码，是用Python编写的。

但是在设计类型的案例中，我不觉得它对读者有特别的技术要求。

希望你在后面的阅读中提出建议，告诉我有哪些地方我讲得不够清楚，或者解释的过多，我会适当调整内容。

问题二：小型公司程序员学习大规模数据处理的意义？

![](https://static001.geekbang.org/resource/image/76/8c/763eefc53ce0e3c4ce07240328c8358c.jpg?wh=1125%2A890)  
这个问题问得很好。以客观条件来看，韩程的说法没有问题。
<div><strong>精选留言（6）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c5/1d/1a301635.jpg" width="30px"><span>火星人</span> 👍（3） 💬（1）<div>老师，请以你专家级的视角，推荐5篇将来可能影响大数据发展趋势的论文吧！</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/dd/41614582.jpg" width="30px"><span>HomeyLiu</span> 👍（10） 💬（0）<div>数据均匀分片的核心是 哈希函数的设计。
如果你数据结构和算法不错的话，我觉得这是一个很简单的问题。
通过hashFunchiton（key）函数，输入key，输出hash值。

哈希函数设计的特点：
1》输入的key一样，得到的hash值肯定一样
2》输入的key不一样，得到的hash值可能一样，也就是hash冲突。
这个是评判一个哈希函数的好坏的重要标准。
冲突概率大的哈希函数肯定会引起严重的数据倾斜。极端的例子，
所有的key的hash值都一样，都跑到一个桶里面去了。

所以衡量一个哈希函数的好坏：
1》冲突要小。（例如用素数，还有模拟10进制，弄个26进制，abc可以编码为 0×26的0次方+1×26+2×26的2次方）
2》计算要快。常用位运算。
3》key哪怕很小的变动，输出的hash值差距越大越好。

有很多很经典的hash算法。

但是如果key一样hash值肯定一样。
所有key重复的数据很多的话，哈希函数是解决不了问题的。
必须对key进行组合，只要 组合后的key的重复的比率 不要
比 哈希冲突的概率 大太多就行。

</div>2019-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1a/f9/180f347a.jpg" width="30px"><span>朱同学</span> 👍（4） 💬（0）<div>刚入行时，师傅曾指导我，hash可以做随机，但是不能做key，因为不同平台hash算法可能是不一样的，类似需求推荐使用md5。</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/af/27/76489618.jpg" width="30px"><span>sunsweet</span> 👍（2） 💬（0）<div>但是比特币交易平台就是实时的，那是怎么实现呢</div>2019-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0f/71/9273e8a4.jpg" width="30px"><span>时间是最真的答案</span> 👍（2） 💬（0）<div>感觉不是做大数据领域的同学，读这个专栏还是比较吃力的。专栏设计知识的很广，提升了大家的认识，但不懂大数据相关技术，没法实践，比如spark不懂如何部署，然后用自己所熟悉的需要去实践</div>2019-05-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/ee/9d/3266d88b.jpg" width="30px"><span>listen</span> 👍（0） 💬（1）<div>老师你好，我们是做学生学习情况的，现在要做实时，就是一节课的信息，是一个大json，1-10+M，其中嵌套多个json，由于各个子json的耦合性太强没办法分离，使用kafka的话一条数据太大了，数据是在OSS上，现在是先拉取到hdfs，
现在是发现3中方法，
1、java put到hdfs时，mq发送位置信息，sparkstreaming订阅，根据位置拉取
2、put 到hbase,sparkstreaming 扫描
3、使用sparkstreaming的textFileStream算子监控路径
三种方法没种都有很大的缺陷，老师能指点一下吗</div>2019-05-21</li><br/>
</ul>