你好，我是蔡元楠。

这里是“FAQ第三期：Apache Beam基础答疑”。这一期主要是针对上周结束的模块四——Apache Beam的基础知识部分进行答疑，并且做了一些补充。

如果你对文章的印象不深了，可以先点击题目返回文章复习。当然，你也可以继续在留言中提出疑问。希望我的解答对你有所帮助。

## [22 | Apache Beam的前世今生](https://time.geekbang.org/column/article/99379)

在第22讲中，我分享了Apache Beam的诞生历程。留言中渡码、coder和Milittle都分享了自己了解的技术变迁、技术诞生历史。

![unpreview](https://static001.geekbang.org/resource/image/33/cf/337b762426b35a4b4222f33f7def3dcf.jpg?wh=1125%2A1930)

![unpreview](https://static001.geekbang.org/resource/image/1e/89/1e59031e7acad0480e41ff5d80c0c889.jpg?wh=1125%2A2014)

而JohnT3e则是分享了我在文章中提到的几个论文的具体内容。他分享的论文是非常好的补充材料，也希望你有时间的话可以下载来看一看。我把链接贴在了文章里，你可以直接点击下载浏览。

[MapReduce论文](https://research.google.com/archive/mapreduce-osdi04.pdf)  
[Flumejava论文](https://research.google.com/pubs/archive/35650.pdf)  
[MillWheel论文](https://research.google.com/pubs/archive/41378.pdf)  
[Data flow Model论文](https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf%5D)

Morgan在第22讲中提问：Beam和Spark是什么关系？

![unpreview](https://static001.geekbang.org/resource/image/77/5e/772769f1de87b38363aa5aa59d22dd5e.jpg?wh=1125%2A1090)

我的回答是，Spark可以作为Beam的一个底层Runner来运行通过Beam SDK所编写的数据处理逻辑。相信在读完第23讲的内容后，Morgan会对这个概念有一个更好的认识。

## [23 | 站在Google的肩膀上学习Beam编程模型](https://time.geekbang.org/column/article/100478)
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（0） 💬（1）<div>感谢老师</div>2019-07-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLdWHFCr66TzHS2CpCkiaRaDIk3tU5sKPry16Q7ic0mZZdy8LOCYc38wOmyv5RZico7icBVeaPX8X2jcw/132" width="30px"><span>JohnT3e</span> 👍（4） 💬（0）<div>感谢老师的解答</div>2019-07-03</li><br/>
</ul>