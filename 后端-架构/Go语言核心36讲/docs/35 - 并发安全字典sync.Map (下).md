你好，我是郝林，今天我们继续来分享并发安全字典sync.Map的内容。

我们在上一篇文章中谈到了，由于并发安全字典提供的方法涉及的键和值的类型都是`interface{}`，所以我们在调用这些方法的时候，往往还需要对键和值的实际类型进行检查。

这里大致有两个方案。我们上一篇文章中提到了第一种方案，在编码时就完全确定键和值的类型，然后利用Go语言的编译器帮我们做检查。

这样做很方便，不是吗？不过，虽然方便，但是却让这样的字典类型缺少了一些灵活性。

如果我们还需要一个键类型为`uint32`并发安全字典的话，那就不得不再如法炮制地写一遍代码了。因此，在需求多样化之后，工作量反而更大，甚至会产生很多雷同的代码。

## 知识扩展

## 问题1：怎样保证并发安全字典中的键和值的类型正确性？（方案二）

那么，如果我们既想保持`sync.Map`类型原有的灵活性，又想约束键和值的类型，那么应该怎样做呢？这就涉及了第二个方案。

**在第二种方案中，我们封装的结构体类型的所有方法，都可以与`sync.Map`类型的方法完全一致（包括方法名称和方法签名）。**

不过，在这些方法中，我们就需要添加一些做类型检查的代码了。另外，这样并发安全字典的键类型和值类型，必须在初始化的时候就完全确定。并且，这种情况下，我们必须先要保证键的类型是可比较的。
<div><strong>精选留言（29）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/83/4b/0e96fcae.jpg" width="30px"><span>sky</span> 👍（12） 💬（2）<div>郝大 go方面能推荐下比较成熟的微服务框架吗</div>2018-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/91/17/89c3d249.jpg" width="30px"><span>下雨天</span> 👍（7） 💬（1）<div>老师好，关于：sync.Map在存储键值对的时候，只要只读字典中已存有这个键，并且该键值对未被标记为“已删除”，就会把新值存到里面并直接返回，这种情况下也不需要用到锁。这句话，只读map里面的值可以被替换的话，为什么不需要加锁？不会 有读写冲突吗？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（5） 💬（2）<div>这个设计很巧妙，在自己的开发中可以借鉴这种思想。有个问题请问老师：
“脏字典中的键值对集合总是完全的”，而“read 和 dirty 互换之后 dirty 会置空”，那么重建的意思是不是这样的：在下一次访问 read 的时候，将 read 中的键值对全部复制到 dirty 中?</div>2020-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ce/07/15a91f75.jpg" width="30px"><span>渺小de尘埃</span> 👍（3） 💬（1）<div>当一个结构体里的字段是sync.map类型的，怎么json序列化呢？</div>2018-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/18/ac/4d68ba46.jpg" width="30px"><span>金时</span> 👍（2） 💬（1）<div>&#47;&#47; The read field itself is always safe to load, but must only be stored with mu held.
老师，源代码里对read变量注释时说read 在store时，需要加锁，没懂这是为什么？</div>2021-07-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8c/e2/48f4e4fa.jpg" width="30px"><span>mkii</span> 👍（2） 💬（3）<div>老师，看到源码中Store的时候有个疑惑。如果read中存在此key对应的vlaue，则tryStore替换read的value。这里如果在dirty给read并将dirty置为nil的时候不会丢失新数据吗？</div>2021-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/07/ba/c80fac39.jpg" width="30px"><span>夜来寒雨晓来风</span> 👍（2） 💬（1）<div>关于文中提到的“键值对应该被删除，但却仍然存在于只读字典”，什么时候会出现这种情形呢？对于sync.Map的删除机制看的不是很明白，希望能解答一下，谢谢~</div>2021-01-07</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKdiaUiaCYQe9tibemaNU5ya7RrU3MYcSGEIG7zF27u0ZDnZs5lYxPb7KPrAsj3bibM79QIOnPXAatfIw/132" width="30px"><span>Geek_a8be59</span> 👍（2） 💬（2）<div>看了一下源码有地方不理解，有劳解答一下 
第一：Store、Load等方法都会执行两次m.read.Load().(readOnly)，去判断两次  这样做的目的是什么？</div>2020-07-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ca/e3/7e860739.jpg" width="30px"><span>一介农夫</span> 👍（1） 💬（1）<div>1.18后可以用泛型实现了</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/ef/030e6d27.jpg" width="30px"><span>xl000</span> 👍（1） 💬（1）<div>老师，read、dirty交换和访问read这两个操作，难道不需要保护read变量吗</div>2021-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/96/dd/1620a744.jpg" width="30px"><span>simple_孙</span> 👍（1） 💬（2）<div>更新时只修改只读map，不会造成数据不一致吗，后面应该会定期同步到脏map里吧？</div>2021-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep0Cb1HGLBTD57I53ZLsIBnvN3YkJOTkibWyibPoCUM5cbnhqDicm1aKWTUFeI7SEd8REnibfZVWeM3BQ/132" width="30px"><span>Mr.zhou</span> 👍（0） 💬（1）<div>sync.Map在存储键值对的时候，只要只读字典中已存有这个键，并且该键值对未被标记为“已删除”，就会把新值存到里面并直接返回，这种情况下也不需要用到锁。

老师的这句话，让我有这个疑问？那写入的时候，只读map写了，那dirty map要不要同步写入？写入dirty map要不要加锁？</div>2023-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/20/bf/7c053186.jpg" width="30px"><span>Ronin</span> 👍（0） 💬（1）<div>老师，我读了好几遍，还是不明白为什么要检查键值对的类型，这不是强制整个字典的key都为一个类型，整个字典的value都为一个类型了，而实际上原先的字典的键值对类型是可以多样化的存储，像这样：
var m sync.Map
m.Store(&quot;test&quot;, 18)
m.Store(18, &quot;test&quot;)
而不是只能：
m.Store(1, &quot;a&quot;)
m.Store(2, &quot;b&quot;)
就算要检查，应该是检查键的实际类型不能是函数类型、字典类型和切片类型
还望老师解惑下~谢谢</div>2022-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/12/15558f28.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>郝大，map的键值对的删除为什么要先置为nil再置为unpunged呢，直接置为unpunged不行吗？而且真正删除一个键值对要经过delete-&gt;dirtyLocked-&gt;missLocked三个步骤才能删除</div>2022-10-11</li><br/><li><img src="" width="30px"><span>Geek_f0ae52</span> 👍（0） 💬（1）<div>func (e *entry) load() (value interface{}, ok bool) {
	p := atomic.LoadPointer(&amp;e.p)
	if p == nil || p == expunged {
		return nil, false
	}
	return *(*interface{})(p), true
}
(*interface{})(p)   这句话的意思是把p转换成interface类型的指针吗？</div>2022-04-01</li><br/><li><img src="" width="30px"><span>Geek_f0ae52</span> 👍（0） 💬（1）<div>老师，我看源码里(*interface{})(p)，这句话的意思是把p</div>2022-04-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（1）<div>当dirty重建时候旧数据量比较大，在锁保护下，这样完全拷贝是不是会很影响性能？这种情况有什么好的解决方案吗</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/bb/225e70a6.jpg" width="30px"><span>hunterlodge</span> 👍（0） 💬（1）<div>“脏字典中的键值对集合总是完全的”
郝大，在dirty被置位nil的以后，它很长时间应该都不是完全的啊，为什么说总是完全的呢？</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/89/23/73569bd7.jpg" width="30px"><span>xj_zh</span> 👍（0） 💬（1）<div>看了大半天的源码，终于读懂了。</div>2020-09-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ac/95/9b3e3859.jpg" width="30px"><span>Timo</span> 👍（56） 💬（1）<div>做个sync.Map优化点的小总结：
1. 空间换时间。 通过冗余的两个数据结构(read、dirty),实现加锁对性能的影响
2. 使用只读数据(read)，避免读写冲突。
3. 动态调整，miss次数多了之后，将dirty数据提升为read
4. 延迟删除。 删除一个键值只是打标记，只有在提升dirty的时候才清理删除的数据
5. 优先从read读取、更新、删除，因为对read的读取不需要锁</div>2019-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/64/05/6989dce6.jpg" width="30px"><span>我来也</span> 👍（6） 💬（0）<div>最近几天,golang升级到了1.15后,sync.Map又`火`了一把.
我又来温习了下本篇文章,也看了下对应的源码,
对sync.Map的印象又深刻了点.

具体的链接如下:
[踩了 Golang sync.Map 的一个坑](https:&#47;&#47;gocn.vip&#47;topics&#47;10860)
[sync: sync.Map keys will never be garbage collected](https:&#47;&#47;github.com&#47;golang&#47;go&#47;issues&#47;40999)

有兴趣的小伙伴可以去看看.</div>2020-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a7/8b/208d9e2c.jpg" width="30px"><span>Rainman</span> 👍（5） 💬（0）<div>这个脏字典让我想起了mysql的刷脏页。
给老师点赞。</div>2019-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4b/69/c02eac91.jpg" width="30px"><span>大漠胡萝卜</span> 👍（4） 💬（0）<div>sync.Map适用于读多写少的情况，如果写数据比较频繁可以参考：https:&#47;&#47;github.com&#47;orcaman&#47;concurrent-map</div>2020-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/83/f1/d6676d6b.jpg" width="30px"><span>墨水里的鱼</span> 👍（3） 💬（0）<div>如何初始化reflect.Type？reflect.TypeOf(1) reflect.TypeOf(&quot;a&quot;) 只能这样吗?</div>2018-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/54/d6/124e2e93.jpg" width="30px"><span>Calios</span> 👍（1） 💬（0）<div>个人以为是读过的这个专栏里最精彩的一篇~ 只读字典和脏字典的实现好精彩，忍不住再去细细读一下sync.Map的实现。</div>2019-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/3c/6f2a4724.jpg" width="30px"><span>唐大少在路上。。。</span> 👍（1） 💬（0）<div>班门弄斧，其实有个细节帮老师丰富一下：
两个原生map的定义为 map[interface{}]*entry
其中的entry为一个只包含一个unsafe.pointer的结构体
这里之所以value设置为指针类型，个人感觉就是为了在dirtry重建的时候直接把read里面这个entry的地址copy到dirty里面，这样当read中对entry里面的pointer执行原子替换的时候，dirty里面的值也会跟随着改变。
这样，当每次对read已有key进行更新的时候就不用单独去操作一次dirty了</div>2019-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（1） 💬（0）<div>打卡</div>2019-03-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep0Cb1HGLBTD57I53ZLsIBnvN3YkJOTkibWyibPoCUM5cbnhqDicm1aKWTUFeI7SEd8REnibfZVWeM3BQ/132" width="30px"><span>Mr.zhou</span> 👍（0） 💬（0）<div>有一个疑问。删除操作时，如果key在read中存在，但是也在dirty中存在。这个key在read中只是被标记删除，dirty中并没有被物理删除。
如果这个时候dirty转换为了read。那么原来dirty中应该被删除的元素 到底是怎么被删除的？
老师，我不知道我表述清楚没？</div>2024-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/75/551c5d6c.jpg" width="30px"><span>CrazyCodes</span> 👍（0） 💬（0）<div>关于保证并发安全字典中的键和值的类型正确性，你还能想到其他的方案吗？

现在应该可以用泛型了吧</div>2023-11-25</li><br/>
</ul>