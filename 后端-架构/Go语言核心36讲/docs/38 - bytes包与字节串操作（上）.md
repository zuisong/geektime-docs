我相信，经过上一次的学习，你已经对`strings.Builder`和`strings.Reader`这两个类型足够熟悉了。

我上次还建议你去自行查阅`strings`代码包中的其他程序实体。如果你认真去看了，那么肯定会对我们今天要讨论的`bytes`代码包，有种似曾相识的感觉。

## 前导内容： `bytes.Buffer`基础知识

`strings`包和`bytes`包可以说是一对孪生兄弟，它们在API方面非常的相似。单从它们提供的函数的数量和功能上讲，差别可以说是微乎其微。

**只不过，`strings`包主要面向的是Unicode字符和经过UTF-8编码的字符串，而`bytes`包面对的则主要是字节和字节切片。**

我今天会主要讲`bytes`包中最有特色的类型`Buffer`。顾名思义，`bytes.Buffer`类型的用途主要是作为字节序列的缓冲区。

与`strings.Builder`类型一样，`bytes.Buffer`也是开箱即用的。

但不同的是，`strings.Builder`只能拼接和导出字符串，而`bytes.Buffer`不但可以拼接、截断其中的字节序列，以各种形式导出其中的内容，还可以顺序地读取其中的子序列。

可以说，`bytes.Buffer`是集读、写功能于一身的数据类型。当然了，这些也基本上都是作为一个缓冲区应该拥有的功能。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/a5/67/bf286335.jpg" width="30px"><span>AllenGFLiu</span> 👍（6） 💬（3）<div>赫老師多次闡明源碼的重要性，但源碼內容的量確實不小。
不知道老師能不能給個閱讀源碼的路徑？</div>2021-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（3） 💬（1）<div>花了2小时，一遍啃源码，一遍对照文章,一边自己写测试用例，一边搞官方包自己实现的用例。。。绝了，啃津津有味，不知不觉都天黑了</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（2）<div>郝林老师，以下问题，麻烦回答一下：

1.  「bytes.Buffer」 为什么不提供一个 Buffer值的已读计数值的获取方法呢？

2.  文中说： “在我们剖析了所有的相关方法之后，可以这样来总结：在已读计数代表的索引之前的那些内容，永远都是已经被读过的，它们几乎没有机会再次被读取”。我理解的是： 唯一有机会获取到这些内容的机会是 「UnreadByte」和 「UnreadRune」这两个方法吗？

3. 文中说：“这些已读内容所在的内存空间可能会被存入新的内容。这一般都是由于重置或者扩充内容容器导致的”。 已读的内容不是已经 复制给另外的变量返回给调用方了吗？为什么还会被被存入新的内容呢？没理解这句话的想表达的意思。</div>2021-08-24</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKOM6tVLSiciaQeQst0g3iboWO74ibicicVAia9qno0X6cf65pEKLgdKkUdcpCWpjAB5e6semrFrruiaGQWhg/132" width="30px"><span>NoTryNoSuccess</span> 👍（2） 💬（1）<div>坚持到这里了，给自己点赞！</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（1） 💬（2）<div>无法直接得到一个Buffer值的已读计数？？
	n, _ := buffer1.Read(p1)
这个 n 不就是已读取的字节数吗？

老师还说 buffer1的Len方法返回的也是内容容器中未被读取部分的长度，我认为是错的，buffer1的Len方法返回就是 buffer1 内的长度，只要读取了，就不会存在 buffer1 里面了，难道不是吗？ 难道 buffer1 中还保留有已读取的字节吗？如果我错了，请老师给段代码证明下，buffer1 已读取的字节仍然可再次读取。 </div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/30/3c/0668d6ae.jpg" width="30px"><span>盘胧</span> 👍（1） 💬（1）<div>学习源码以及使用的过程，按照作者写这个标准库的时候的思路：库函数 &gt; 结构定义 &gt; 结构函数
举例学习strings包：
1. 先熟悉外部库函数：go doc strings|grep &quot;^func&quot;
2. 熟悉对应的结构定义：go doc strings|grep &quot;^type&quot;|grep &quot;struct&quot;
3. 接下来就应该学习对应的内部结构的函数了 go doc strings.Builder|grep &quot;^func&quot;
可以使用思维导图，顺着函数的调用去看，把过程记录下来</div>2021-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/8c/e4/ad3e7c39.jpg" width="30px"><span>L.</span> 👍（1） 💬（1）<div>老师同学们好，请问一下大家手头有能够辅助阅读源码的书籍或者资料吗，有的包下边的源码实在是理解不了，有的是不理解整体逻辑，有的是不理解某一行的写法等等(小白求助</div>2020-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/4c/2cefec07.jpg" width="30px"><span>静水流深</span> 👍（25） 💬（3）<div>一图胜千言</div>2019-08-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/KFgDEHIEpnSjjGClCeqmKYJsSOQo40BMHRTtNYrWyQP9WypAjTToplVND944one2pkEyH5Oib4m4wUOJ9xBEIZQ/132" width="30px"><span>sket</span> 👍（4） 💬（1）<div>原来read把从缓冲区读的字节放到p1里面了，让我这个小白纠结了好半天</div>2019-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（1）<div>我去阅读了源码 发现重要的不止是 off 我暂且叫他偏移量 还有一个重要的字段lastRead 标识上一次是否是成功读取 和读了多少个字节 所以UnreadRune方法应该还是可以正常使用吧(不包含ReadRune的情况) 毕竟底层是b.off -= int(b.lastRead) </div>2020-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（1） 💬（0）<div>老师 请教下👇
golang如何实验solidity中的require和assert函数功能啊 试着写了下 没啥思路 求老师指点 谢谢</div>2018-11-08</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/iaXcnYOjwO39gSSyo0CprNeLxx6OF80KqPz69ErJKmibMSxn5YeM4VGD6ATBnUR045ibsYjQGlAAQo5r3iaTPydTbA/132" width="30px"><span>docker131313</span> 👍（0） 💬（0）<div>坚持学习</div>2024-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/78/c7/083a3a0b.jpg" width="30px"><span>新世界</span> 👍（0） 💬（0）<div>每天坚持刷，讲的很不错</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/f2/ba/aad606a6.jpg" width="30px"><span>爱如少年</span> 👍（0） 💬（0）<div>我个人觉得老师讲的内容很不错，融入了他的经验和精华，但你觉得这种叙事方式我个人觉得还是不太适合新手的。</div>2021-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（1）<div>二刷
注意点：
String和Bytes方法不会更新内部计数器off</div>2019-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/80/a0533acb.jpg" width="30px"><span>勇.Max</span> 👍（0） 💬（0）<div>老师，请教下👇
golang中如何实现类似solidity中的require(用来判断输入的参数是否符合某些条件)和assert(不只是对类型的断言)呢？
试着写了下，没思路，求老师指教。非常感谢</div>2018-11-08</li><br/>
</ul>