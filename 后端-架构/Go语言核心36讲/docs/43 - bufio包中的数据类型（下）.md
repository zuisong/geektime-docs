你好，我是郝林，我今天继续分享bufio包中的数据类型。

在上一篇文章中，我提到了`bufio`包中的数据类型主要有`Reader`、`Scanner`、`Writer`和`ReadWriter`。并着重讲到了`bufio.Reader`类型与`bufio.Writer`类型，今天，我们继续专注`bufio.Reader`的内容来进行学习。

## 知识扩展

### 问题 ：`bufio.Reader`类型读取方法有哪些不同？

`bufio.Reader`类型拥有很多用于读取数据的指针方法，**这里面有4个方法可以作为不同读取流程的代表，它们是：`Peek`、`Read`、`ReadSlice`和`ReadBytes`。**

**`Reader`值的`Peek`方法**的功能是：读取并返回其缓冲区中的`n`个未读字节，并且它会从已读计数代表的索引位置开始读。

在缓冲区未被填满，并且其中的未读字节的数量小于`n`的时候，该方法就会调用`fill`方法，以启动缓冲区填充流程。但是，如果它发现上次填充缓冲区的时候有错误，那就不会再次填充。

如果调用方给定的`n`比缓冲区的长度还要大，或者缓冲区中未读字节的数量小于`n`，那么`Peek`方法就会把“所有未读字节组成的序列”作为第一个结果值返回。

同时，它通常还把“`bufio.ErrBufferFull`变量的值（以下简称缓冲区已满的错误）”  
作为第二个结果值返回，用来表示：虽然缓冲区被压缩和填满了，但是仍然满足不了要求。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（3） 💬（1）<div>郝老师，我通过阅读这部分的源代码感受到源代码作者的用心良苦，以及对 I&#47;O 读写控制的精细。我的疑问时：对于方法返回值的用途，以及在设计 API 时，特别是方法的返回值都有哪些需要注意的地方。</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/17/96/a10524f5.jpg" width="30px"><span>蓬蒿</span> 👍（2） 💬（1）<div>“ ReadSlice方法会先在其缓冲区的未读部分中寻找分隔符。如果未能找到，并且缓冲区未满，那么该方法会先通过调用fill方法对缓冲区进行填充，然后再次寻找，如此往复。”  虽然通过后续内容了解了ReadSlice方法只填满一次缓冲区，但是这里上下文中的 “如此反复” 一词容易让人产生和readbyte功能一样的误解。</div>2019-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>请教一个读代码是遇到的疑问，collectFragments方法中fullBuffers并没有提前声明，这样也可添加buff吗吗，另外注释中说这种方式可以减少调用时的内存开销和数据拷贝，是指这里分片拷贝后一次填充到一个切片中返回，就不用外部调用者自己去组装的意思吗</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/79/803537db.jpg" width="30px"><span>慢动作</span> 👍（0） 💬（3）<div>这几节感觉直接看api或源码就好，没有什么印象深刻的地方</div>2021-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/fb/ffa57759.jpg" width="30px"><span>xyz</span> 👍（20） 💬（1）<div>慢慢追上了（不过有些内容学的比较粗略……），感觉郝林老师的这个系列，特别是后面的内容更适合作为一个了解常用库的索引存在，有在实际工作中碰到了问题再来参考会更好理解。</div>2018-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/43/e2/a1ff289c.jpg" width="30px"><span>wang jl</span> 👍（16） 💬（1）<div>我就想看bufio.Scanner才买的这个教程😓结果是思考题</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/53/063f9d17.jpg" width="30px"><span>moonfox</span> 👍（6） 💬（0）<div>可以把 io.Reader 或 strings.NewReader 想像成一个实际的存在于硬盘之上的文件IO对象，你要对这个文件进行读写操作，感觉这样比较生动具体，可以更好的理解bufio包的功能用途，bufio包可以有效的降低系统IO的读写次数，从而提高了程序的性能。 XD</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f7/83/7fa4bd45.jpg" width="30px"><span>趣学车</span> 👍（6） 💬（0）<div>bufio.Scanner 通过一个分隔函数，循环读取底层读取器中的内容，每次读取一段，使用Scanner.Scan() 读取， 通过Scanner.Text() 或 Scanner.Bytes() 获取读到的内容</div>2020-11-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/37/92/961ba560.jpg" width="30px"><span>授人以🐟，不如授人以渔</span> 👍（3） 💬（0）<div>「bufio.Reader类型的 Peek 方法有一个鲜明的特点，那就是：即使它读取了缓冲区中的数据，也不会更改已读计数的值。」这里需要说明的是 Peek 方法可能会修改 b.r 和 b.w 的值，但是对于 Peek 方法来说，其含义是并非是一种“真实”的读取，意味着接下来再用 ReadByte 还能读取到相同的数据。比如用下面的示例程序可以验证：

func main() {
	buf := bytes.NewBufferString(&quot;abcd&quot;)
	reader := bufio.NewReader(buf)

	slice, err := reader.Peek(4)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf(&quot;%v.\n&quot;, slice)

	value, err := reader.ReadByte()
	fmt.Printf(&quot;%v.\n&quot;, value)
}</div>2021-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/e1/0f4d90ff.jpg" width="30px"><span>乖，摸摸头</span> 👍（3） 💬（0）<div>好吧，看了源码， writer2.ReadFrom 只有缓冲区为0才会跨过缓冲区</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5e/4f/56ad818d.jpg" width="30px"><span>张剑</span> 👍（3） 💬（0）<div>先学一遍 有个整体的分类和粗略了解 以后有用到还可回来找到</div>2019-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（0）<div>大家一定要看看老师写的示例代码，写的非常用心了。</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/97/e1/0f4d90ff.jpg" width="30px"><span>乖，摸摸头</span> 👍（0） 💬（0）<div>basicWriter3 := &amp;strings.Builder{}
reader2 := strings.NewReader(&quot;1234456789&quot;)
writer2 := bufio.NewWriterSize(basicWriter3,3)
writer2.WriteString(&quot;abcd&quot;)
&#47;&#47;此时缓冲区中还有数据 d, basicWriter3的数据为 ”abc“
writer2.ReadFrom(reader2) &#47;&#47;这一步不经过缓冲区
&#47;&#47;basicWriter3.String()  数据理论上就应该是 abc123456789
&#47;&#47;实际我打印出来的数据为 abcd1234567
writer2.Flush()
&#47;&#47;应该是  abc123456789d 才对，但是实际打印出来并不是这样的

</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/aa/eb4c37db.jpg" width="30px"><span>John</span> 👍（0） 💬（0）<div>打卡</div>2019-09-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/90/02/ba6c8c73.jpg" width="30px"><span>jimmy</span> 👍（0） 💬（0）<div>坚持，加油</div>2019-08-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/44/fc/1ca9c88c.jpg" width="30px"><span>曾春云</span> 👍（0） 💬（0）<div>每天坚持一课</div>2019-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/06/4f/de1e5a54.jpg" width="30px"><span>Zero</span> 👍（0） 💬（0）<div>坚持</div>2019-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-03-13</li><br/>
</ul>