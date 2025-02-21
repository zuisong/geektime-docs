到目前为止，我们已经一起陆陆续续地学完了Go语言中那些最重要也最有特色的概念、语法和编程方式。我对于它们非常喜爱，简直可以用如数家珍来形容了。

在开始今天的内容之前，我先来做一个简单的总结。

## Go语言经典知识总结

基于混合线程的并发编程模型自然不必多说。

在**数据类型**方面有：

- 基于底层数组的切片；
- 用来传递数据的通道；
- 作为一等类型的函数；
- 可实现面向对象的结构体；
- 能无侵入实现的接口等。

在**语法**方面有：

- 异步编程神器`go`语句；
- 函数的最后关卡`defer`语句；
- 可做类型判断的`switch`语句；
- 多通道操作利器`select`语句；
- 非常有特色的异常处理函数`panic`和`recover`。

除了这些，我们还一起讨论了**测试Go程序**的主要方式。这涉及了Go语言自带的程序测试套件，相关的概念和工具包括：

- 独立的测试源码文件；
- 三种功用不同的测试函数；
- 专用的`testing`代码包；
- 功能强大的`go test`命令。

另外，就在前不久，我还为你深入讲解了Go语言提供的那些**同步工具**。它们也是Go语言并发编程工具箱中不可或缺的一部分。这包括了：

- 经典的互斥锁；
- 读写锁；
- 条件变量；
- 原子操作。

以及**Go语言特有的一些数据类型**，即：

- 单次执行小助手`sync.Once`；
- 临时对象池`sync.Pool`；
- 帮助我们实现多goroutine协作流程的`sync.WaitGroup`、`context.Context`；
- 一种高效的并发安全字典`sync.Map`。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/d8/425e1b0a.jpg" width="30px"><span>小虾米</span> 👍（7） 💬（4）<div>这篇文章把unicode和utf8区分的不是很清楚，正如上面有个网友说的rune切变16进制输出是字符的unicode的码点，而byte切片输出的才是utf8的编码</div>2018-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（6） 💬（1）<div>郝林老师，请问一下：“基于混合线程的并发编程模型”。这句话该怎么理解呢？</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/80/8759e4c1.jpg" width="30px"><span>🐻</span> 👍（4） 💬（1）<div>+ isrunesingle.go

```go
package show_rune_length

func isSingleCharA(c rune) bool {
	return int32(c) &lt; 128
}

func isSingleCharB(c rune) bool {
	data := []byte(string(c))
	return len(data) == 1
}

func isSingleCharC(c rune) bool {
	data := string(c) + &quot; &quot;

	for i, _ := range data {
		if i == 0 {
			continue
		}

		if i == 1 {
			return true
		} else {
			return false
		}
	}

	return false
}
```

+ isrunesingle_test.go

```go
package show_rune_length

import (
	&quot;testing&quot;

	&quot;github.com&#47;stretchr&#47;testify&#47;assert&quot;
)

type CharJudger func(c rune) bool

func TestIsSingleChar(t *testing.T) {

	for _, judger := range []CharJudger{
		isSingleCharA,
		isSingleCharB,
		isSingleCharC,
	} {
		assert.True(t, judger(&#39;A&#39;))
		assert.True(t, judger(rune(&#39; &#39;)))
		assert.False(t, judger(&#39;😔&#39;))
		assert.False(t, judger(&#39;爱&#39;))
	}
}
```</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/fa/a7edbc72.jpg" width="30px"><span>安排</span> 👍（3） 💬（2）<div>一个unicode字符在内存中存的是码点的值还是utf8对应的编码值？</div>2019-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/48/21/bd739446.jpg" width="30px"><span>Gryllus</span> 👍（3） 💬（1）<div>终于追上了进度</div>2018-11-02</li><br/><li><img src="" width="30px"><span>qiushye</span> 👍（2） 💬（2）<div>str := &quot;Go 爱好者 &quot;fmt.Printf(&quot;Th...

您在文章里举的这个例子在Go后面多加了空格，会让人误解成遍历字符串可以跳过空格，github代码里没问题。

</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/b2/2e9f442d.jpg" width="30px"><span>文武木子</span> 👍（1） 💬（2）<div>十六进制四个数字不是一共占用32位吗，一个字节不是8位嘛，这样不是占用4个字节吗？求大神解答</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/66/ad35bc68.jpg" width="30px"><span>党</span> 👍（1） 💬（1）<div>一个unicode字符点都是由两个字节存储，为什么在go语言中 type rune = int32 四个字节 而不是 type rune=16 两个字节啊</div>2019-07-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/9LFicnceEOlv9eNwJqjRDHbX87iaJectWs9ibgRLs8jTsDZDsvnTzUI8J1YJ1CiaNWzXiaTnkjscz4gR0wcvw3JfasoO0rg9FliaDsK8FqTQmHyNE/132" width="30px"><span>Geek_479239</span> 👍（0） 💬（1）<div>谢谢老师，这篇很有收获</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/4b/d7/f46c6dfd.jpg" width="30px"><span>William Ning</span> 👍（0） 💬（1）<div>打卡，一直不明白字符集unicode与字符编码utf-8以及其他的编码实现方式的区别，现在有些理解，但是还是需要理一理。</div>2022-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/49/86/a588c76d.jpg" width="30px"><span>杨锦</span> 👍（0） 💬（1）<div>郝老师，请教一个问题，对于一个6字节的utf8编码，怎么判断是要解码成6个宽度为1字节宽度的的还是2个3字节宽度的呢？</div>2020-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/14/e684be86.jpg" width="30px"><span>张岳文</span> 👍（0） 💬（1）<div>我认为string的底层是Unicode, 而非UTF-8。只是string转成[]byte时，string转成了utf-8的序列。。。内存中的应该统一用unicode处理，而UTF-8是为了存储和传输才进行字节转换的。</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/f9/a8f26b10.jpg" width="30px"><span>jacke</span> 👍（0） 💬（1）<div>string 底层是[]byte数组，我的疑问是：例子里面看出来，string转化为tune的时候，tune里面保存的是utf-8的代码点数据，string转化为[]byte的时候保存的是utf-8代码点对应的字节序。
上面这些转化逻辑在哪里实现的？fmt.print里面？看了fmt.print找不到,string转为[]byte的实现函数stringtoslicebyte也没看到这部分逻辑</div>2019-05-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erNhKGpqicibpQO3tYvl9vwiatvBzn27ut9y5lZ8hPgofPCFC24HX3ko7LW5mNWJficgJncBCGKpGL2jw/132" width="30px"><span>Geek_1ed70f</span> 👍（0） 💬（1）<div>您是说 一个汉字的rune值 在计算机底层会被转成utf-8编码来 给计算机读取是吗?  

比如  一个&quot;严&quot;字  unicode为20005(十进制),  utf-8编码是11100100 10111000 10100101(二进制),十进制就是14989477 ,     我们平时打印只能看到 20005  它是什么时候转成14989477的啊</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5d/f8/62a8b90d.jpg" width="30px"><span>melody_future</span> 👍（0） 💬（1）<div>有点小晕，想请问下 rune 类型在内存的表现形式是 unicde 编码值，还是utf-8 编码值，你所说的底层指的是？</div>2019-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（1）<div>打卡：
1、len函数对于字符串，得到的是字节长度
2、utf-8 我以前看到的资料是 1-6个字节的可变长编码，go如果用rune，对于超过4个字节的utf-8字符怎么处理？</div>2019-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/2d/ef3b42df.jpg" width="30px"><span>wade</span> 👍（51） 💬（5）<div>而后三个十六进制数7231、597d和8005都相对较大，它们分别表示中文字符&#39;爱&#39;、&#39;好&#39;和&#39;者&#39;。这些中文字符对应的 UTF-8 编码值，都需要使用三个字节来表达。所以，这三个数就是把对应的三个字节来表达。所以，这三个数就是把对应的三个字节的编码值，转换为整数后得到的结果。

&quot;爱好者&quot;对应的7231、597d、8005，不是UTF-8编码值，是unicode码点。unicode码点和最终计算器存储用的utf-8编码值不是一样的。转换成rune的时候rune切片每个元素存储一个unicode码点，也就是string里的一个字符转成rune切片的一个元素。string是以utf-8编码存储，byte切片也就是存储用的string用utf-8编码存储后的字节序。

unicode和utf-8的关系，可以看这个文章
http:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2007&#47;10&#47;ascii_unicode_and_utf-8.html</div>2018-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/3b/b4a47f63.jpg" width="30px"><span>only</span> 👍（23） 💬（2）<div>unicode只是给全世界的字符做了一个编码，假如世界上有100亿个字符，那么从0到100亿，有的数只占用一个字节，有的数二个有的数三个…，找到对应的编号就找到了对应的字符。unicode只给字符分配了编号，没有说怎么去存储这些字符，用1字节存不下，100字节太浪费，于是utf-8就想到了一个存储的点子，因为生活中用到的字符用4个字节应该能存下了，于是就用1到4个字节来存储这些字符，占1个字节的就用1字节存储，2字节的就用2字节存储，以此类推……，utf8要做的就是怎么去判断一个字符到底用了几个字节存储，就好比买绳子一样，有的人要两米有的人要一米，不按照尺寸剪肯定不行，具体怎么减咱们先不关心这个留给utf8去处理。存储这些编码在计算机里就是二进制。这些二进制utf8能读懂，但是计算机看来就是01没啥了不起的，8二进制放到4字节存储没毛病吧，装不满的高位大不了填充0，就是这么有钱豆浆喝一杯倒一杯，这个就是[]rune, 但是世界总有吃不饱饭的人看着闹心，那还是一个字节一个字节存吧，等需要查看字符的时候大不了再转换为rune切片，这就是[]byte</div>2020-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/c9/a7c77746.jpg" width="30px"><span>冰激凌的眼泪</span> 👍（16） 💬（0）<div>src文件编码是utf8
string是utf8编码的mb，len(string)是字节的长度
string可以转化为[]rune，unicode码，32bit的数字，当字符看，len([]rune)为字符长度
string可以转化为[]byte，utf8编码字节串，len([]byte)和len(string)是一样的
for range的时候，迭代出首字节下标和rune，首字符下标可能跳跃(视上一个字符编码长度定)</div>2018-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/c9/a7c77746.jpg" width="30px"><span>冰激凌的眼泪</span> 👍（9） 💬（0）<div>看rune大小
转成byte看长度
加个小尾巴,range看间隔
</div>2018-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a5/a3/f8bcd9dd.jpg" width="30px"><span>韡WEI</span> 👍（3） 💬（2）<div>rune怎么翻译？有道查的：神秘的记号。为什么这么命名这个类型？有没有什么故事？</div>2018-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f7/83/7fa4bd45.jpg" width="30px"><span>趣学车</span> 👍（2） 💬（0）<div>len(s) == 1 则为单字节</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/09/22/22c0c4fa.jpg" width="30px"><span>benying</span> 👍（1） 💬（0）<div>打卡,讲的挺清楚的,谢谢</div>2019-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/9d/d487c368.jpg" width="30px"><span>花见笑</span> 👍（0） 💬（0）<div>UTF-8的编码规则:
1、对于单字节的字符，字节的第一位设为0，后面七位为这个字符的Unicode码。
因此对于英文字符，UTF-8编码和ASCII码是相同的。

2、对于n字节的字符(n&gt;1)，第一个字节的前n位都设为1，第n+1位设为0，后面字节的
前两位一律设为10。剩下的没有提及的二进制位，全部为这个字符的Unicode编码。

UTF-8每次传送8位数据,并且是一种可变长的编码格式
具体来说，是怎么的可变长呢.

分为四个区间：
0x0000 0000 至 0x0000 007F:0xxxxxxx
0x0000 0080 至 0x0000 07FF:110xxxxx 10xxxxxx
0x0000 0800 至 0x0000 FFFF:1110xxxx 10xxxxxx 10xxxxxx
0x0001 0000 至 0x0010 FFFF:11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

UTF-8解码过程:

对于采用UTF-8编码的任意字符B

如果B的第一位为0，则B为ASCII码，并且B独立的表示一个字符;

如果B的前两位为1，第三位为0，则B为一个非ASCII字符，该字符由多个字节表示，
并且该字符由两个字节表示;

如果B的前三位为1，第四位为0，则B为一个非ASCII字符，该字符由多个字节表示，
并且该字符由三个字节表示;

比如汉字 “王”,它的二进制形式为: 0x0000 738B,属于第三区间,
0x0000 738B - 00000000 00000000 01110011 10001011,
第三区间的编码是 1110xxxx 10xxxxxx 10xxxxxx
把x都给替换,则最终&quot;王&quot;字对应的Unicode的编码是
11100111 10001110 10001011
转换成16进制 0xe7 0x8e 0x8b

如果B的前四位为1，第五位为0，则B为一个非ASCII字符，该字符由多个字节表示，
并且该字符由四个字节表示;</div>2022-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3b/ba/3b30dcde.jpg" width="30px"><span>窝窝头</span> 👍（0） 💬（0）<div>看它的长度或者转换类型判断</div>2022-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/56/8d/9b8a6837.jpg" width="30px"><span>Louhwz</span> 👍（0） 💬（0）<div>这章讲的很清楚，谢谢</div>2021-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/b1/97/9cbfca81.jpg" width="30px"><span>丶浮空的身体如石的❤</span> 👍（0） 💬（0）<div>豁然开朗</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/05/431d380f.jpg" width="30px"><span>拂尘</span> 👍（0） 💬（1）<div>对于utf8字节序列中的某个字节，是独立成为一个字符，还是和前字节或者后字节或者前后字节来共同组成一个字符，需要前后字节和当前字节都考虑的。考虑的点为每个字节的最高位。具体来讲，前0当0，则当前字节独立成字符；前1或0当0，则当前字节和前面一个或多个字节组成一个字符；前1或0当1，则当前字节和前后多个字节组成一个字符；当1，则当前字节和后面一个或多个字节组成一个字符。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c3/22/8520be75.jpg" width="30px"><span>1287</span> 👍（0） 💬（0）<div>这篇很赞</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/1b/5462d887.jpg" width="30px"><span>强凯</span> 👍（0） 💬（0）<div>写的真清楚，说的真明白！</div>2020-04-25</li><br/>
</ul>