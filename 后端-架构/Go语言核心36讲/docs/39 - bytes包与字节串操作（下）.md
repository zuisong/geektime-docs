你好，我是郝林，今天我们继续分享bytes包与字节串操作的相关内容。

在上一篇文章中，我们分享了`bytes.Buffer`中已读计数的大致功用，并围绕着这个问题做了解析，下面我们来进行相关的知识扩展。

## 知识扩展

### 问题 1：`bytes.Buffer`的扩容策略是怎样的？

`Buffer`值既可以被手动扩容，也可以进行自动扩容。并且，这两种扩容方式的策略是基本一致的。所以，除非我们完全确定后续内容所需的字节数，否则让`Buffer`值自动去扩容就好了。

在扩容的时候，`Buffer`值中相应的代码（以下简称扩容代码）会**先判断内容容器的剩余容量**，是否可以满足调用方的要求，或者是否足够容纳新的内容。

**如果可以，那么扩容代码会在当前的内容容器之上，进行长度扩充。**

更具体地说，如果内容容器的容量与其长度的差，大于或等于另需的字节数，那么扩容代码就会通过切片操作对原有的内容容器的长度进行扩充，就像下面这样：

```
b.buf = b.buf[:length+need]
```

**反之，如果内容容器的剩余容量不够了，那么扩容代码可能就会用新的内容容器去替代原有的内容容器，从而实现扩容。**

不过，这里还有一步优化。

**如果当前内容容器的容量的一半，仍然大于或等于其现有长度（即未读字节数）再加上另需的字节数的和**，即：
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/53/063f9d17.jpg" width="30px"><span>moonfox</span> 👍（1） 💬（3）<div>文章中说：“如果当前内容容器的容量的一半，仍然大于或等于其现有长度再加上另需的字节数的和，cap(b.buf)&#47;2 &gt;= len(b.buf)+need”。

如果是这样的话，那说明还有很多的未使用的空间，起码有一半，那就不用扩容，直接追加就可以了。所以这里的代码是错的，源码(1.16.2)中是 n &lt;= c&#47;2-m ，即cap(b.buf) &gt;= b.Len() + need，也就是未读字节长度 + 另需的字节数 小于等于容量的一半时，才会把未读字节copy到buf的头部，只有在未读字节较少的时候，才发生copy，如果有太多的未读字节，就不copy到头部了(费时)</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（1） 💬（1）<div>老师，Buffer的Write，WriteString方法返回一个int，一个err，int是参数长度，err永远是nil，感觉这个返回没啥用啊。这么设计是为了实现某些接口么？</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（1） 💬（1）<div>请问老师，用 bytes.Buffer 而不用字节切片是因为它有计数器和一些方法使得操作更方便，还有高效的扩容策略么。这么说对么？</div>2020-01-07</li><br/><li><img src="" width="30px"><span>窗外</span> 👍（1） 💬（4）<div>老师你好，为什么我本地的src&#47;runtime包下的stringtoslicebyte方法里面tmpBuf的默认长度是32。
所以文中例子，输出的容量是32</div>2019-08-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/7P4wtgRQt1l0YQlVOtiaUKey2AFZqQCAcABzdCNTP0JR027tkhVkRYgj1iaYF8OlqsE8j6A6icsAvYHIAX8E31WNg/132" width="30px"><span>killer</span> 👍（0） 💬（1）<div>2023年了都，大佬还在看评论吗？写了4年go了总感觉差点意思，最近把郝大佬的文章翻出来每篇仔细阅读、做笔记、看源码，另外也在团队给大家分享golang的学习之路特别充实；

对stringtoslicebyte做了debug，没想到cap为8是这么来的

func stringtoslicebyte(buf *tmpBuf, s string) []byte {
	var b []byte
	if buf != nil &amp;&amp; len(s) &lt;= len(buf) {
		*buf = tmpBuf{}
		b = buf[:len(s)]
	} else {
		b = rawbyteslice(len(s))&#47;&#47; bytes.Buffer 初始化 buf 为空，需要调用 rawbyteslice 初始化 slice
	}
	copy(b, s)
	return b
}


func rawbyteslice(size int) (b []byte) {
	cap := roundupsize(uintptr(size))&#47;&#47; roundupsize 计算容量，重点关注这里
	p := mallocgc(cap, nil, false)&#47;&#47; 分配内存
	if cap != uintptr(size) {
		memclrNoHeapPointers(add(p, uintptr(size)), cap-uintptr(size))
	}

	*(*slice)(unsafe.Pointer(&amp;b)) = slice{p, size, int(cap)}
	return
}


&#47;&#47; Returns size of the memory block that mallocgc will allocate if you ask for the size.
func roundupsize(size uintptr) uintptr {
	if size &lt; _MaxSmallSize {
		if size &lt;= smallSizeMax-8 {		&#47;&#47; 以大佬例子为例：contents := &quot;ab&quot; buffer1 := bytes.NewBufferString(contents)，size长度为2，肯定小于smallSizeMax-8
			return uintptr(class_to_size[size_to_class8[divRoundUp(size, smallSizeDiv)]]) &#47;&#47; divRoundUp 函数算出来 为1， size_to_class8[1]=1;class_to_size[1]=8返回的uintptr为8，这里做了一个约定类似于查表
		} else {
			return uintptr(class_to_size[size_to_class128[divRoundUp(size-smallSizeMax, largeSizeDiv)]])
		}
	}
	if size+_PageSize &lt; size {
		return size
	}
	return alignUp(size, _PageSize)
}


&#47;&#47; 这里算出来是1
func divRoundUp(n, a uintptr) uintptr {
	&#47;&#47; a is generally a power of two. This will get inlined and
	&#47;&#47; the compiler will optimize the division.
	return (n + a - 1) &#47; a  &#47;&#47; (8+2-1)&#47; 8=1
}</div>2023-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c5/5c/04be6fb7.jpg" width="30px"><span>costaLong</span> 👍（0） 💬（1）<div>	contents := &quot;ab&quot;
	buffer1 := bytes.NewBufferString(contents)
	fmt.Printf(&quot;The capacity of new buffer with content %q: %d\n&quot;, contents, buffer1.Cap()) &#47;&#47; 内容容器的容量：8
单独执行这段代码输出的结果是：The capacity of new buffer with content &quot;ab&quot;: 32
 请问是原因呢</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/23/1c/d5c164df.jpg" width="30px"><span>rename</span> 👍（0） 💬（2）<div>如果当前内容容器的容量的一半，仍然大于或等于其现有长度再加上所需的字节数的和，即：cap(b.buf)&#47;2 &gt;= len(b.buf)+need
这边len(b.buf)用b.Len()似乎更准确？才是获取未读部分的实际长度</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b1/0f/e81a93ed.jpg" width="30px"><span>嘎嘎</span> 👍（0） 💬（1）<div>源码里给了推荐的构建方法
&#47;&#47; To build strings more efficiently, see the strings.Builder type.
func (b *Buffer) String() string {
	if b == nil {
		&#47;&#47; Special case, useful in debugging.
		return &quot;&lt;nil&gt;&quot;
	}
	return string(b.buf[b.off:])
}</div>2019-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/b2/74519a7c.jpg" width="30px"><span>失了智的沫雨</span> 👍（34） 💬（3）<div>如果只看strings.Builder 和bytes.Buffer的String方法的话，strings.Builder 更高效一些。
我们可以直接查看两个String方法的源代码，其中strings.Builder String方法中
*(*string)(unsafe.Pointer(&amp;b.buf))  是直接取得buf的地址然后转换成string返回。
而bytes.Buffer的String方法是   string(b.buf[b.off:])
 对buf 进行切片操作,我认为这比直接取址要花费更多的时间。
测试函数:
func BenchmarkStrings(b *testing.B) {
	str := strings.Builder{}&#47;bytes.Buffer{}
	str.WriteString(&quot;test&quot;)
	for i := 0; i &lt; b.N; i++ {
		str.String()
	}
}
结果为
BenchmarkStrings-8   	2000000000	         0.66 ns&#47;op
BenchmarkBuffer-8    	300000000	         5.64 ns&#47;op
所以strings.Builder的String方法更高效</div>2018-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/80/8759e4c1.jpg" width="30px"><span>🐻</span> 👍（7） 💬（0）<div>https:&#47;&#47;github.com&#47;golang&#47;go&#47;blob&#47;master&#47;src&#47;strings&#47;builder_test.go#L319-L366

发现最后的问题，Go 的标准库中，已经给出了相关的测试代码了。</div>2019-04-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/ed/daa94663.jpg" width="30px"><span>1thinc0</span> 👍（5） 💬（0）<div>bytes.Buffer 值的 String() 方法在转换时采用了指针 *(*string)(unsafe.Pointer(&amp;b.buf))，更节省时间和内存</div>2018-11-16</li><br/><li><img src="" width="30px"><span>Geek_51aa7f</span> 👍（3） 💬（0）<div>在Byte()或者Next()结果返回的字节切片处理后才可以返回给外部函数
unreadBytes = unreadBytes[:len(unreadBytes):len(unreadBytes)]</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4a/42/b2c7dd30.jpg" width="30px"><span>骏Jero</span> 👍（3） 💬（0）<div>读了老师的两篇文章，strings.Builder更多是拼接数据和以及拼接完成后的读取使用上应该更适合。而buffer更为动态接受和读取数据时，更为高效。</div>2018-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/c4/e55fdc1c.jpg" width="30px"><span>cygnus</span> 👍（2） 💬（1）<div>```
func (b *Buffer) grow(n int) int {
        ......
	&#47;&#47; Restore b.off and len(b.buf).
	b.off = 0
	b.buf = b.buf[:m+n]
	return m

func (b *Buffer) Grow(n int) {
	if n &lt; 0 {
		panic(&quot;bytes.Buffer.Grow: negative count&quot;)
	}
	m := b.grow(n)
	b.buf = b.buf[:m]
}
```
请问下老师，bytes.Buffer里grow函数返回前做过一次切片b.buf = b.buf[:m+n]，返回后在Grow函数又做了一次切片b.buf = b.buf[:m]，这样做的目的是什么呢？感觉有点冗余</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f5/96/0cf9f3c7.jpg" width="30px"><span>Aeins</span> 👍（0） 💬（0）<div>“你可能会有疑惑，我只在这个Buffer值中放入了一个长度为2的字符串值，但为什么该值的容量却变为了8”

目前，字符串长度小于 32 的直接分配在缓冲区上，Cap 是 32，大于 32 的，再重新分配内存</div>2022-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（0） 💬（0）<div>老师讲的很透彻，需要结合源码</div>2022-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/57/41/29d1642e.jpg" width="30px"><span>Geek_cupkg6</span> 👍（0） 💬（0）<div>更具体地说，如果内容容器的容量与其长度的差，大于或等于另需的字节数，那么扩容代码就会通过切片操作对原有的内容容器的长度进行扩充。
这句话中与“其长度的差”，表述不明确，应该是已存内容长度的差。</div>2021-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4a/53/063f9d17.jpg" width="30px"><span>moonfox</span> 👍（0） 💬（0）<div>思考题: strings.Builder的实现是 return *(*string)(unsafe.Pointer(&amp;b.buf))， bytes.Buffe的实现是string(b.buf[b.off:])，显然strings.Builder的String方法更高效，它没有发生拷贝，而是直接使用(共享)了buf的内存数据(数组，长度)</div>2021-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/12/70/10faf04b.jpg" width="30px"><span>Lywane</span> 👍（0） 💬（0）<div>如果当前内容容器的容量的一半，仍然大于或等于其现有长度再加上另需的字节数的和，即：cap(b.buf)&#47;2 &gt;= len(b.buf)+need，那么，扩容代码就会复用现有的内容容器，并把容器中的未读内容拷贝到它的头部位置。这也意味着其中的已读内容，将会全部被未读内容和之后的新内容覆盖掉。

其实这一步并不会覆盖所有已读内容（copy(b.buf, b.buf[b.off:])），因为根据条件可以推出未读+剩余&lt;已读部分。所以在Grow方法的最后又截取了一下</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-03-06</li><br/>
</ul>