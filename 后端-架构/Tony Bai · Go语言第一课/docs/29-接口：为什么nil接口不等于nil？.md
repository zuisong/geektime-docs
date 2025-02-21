你好，我是Tony Bai。

上一讲我们学习了Go接口的基础知识与设计惯例，知道Go接口是构建Go应用骨架的重要元素。从语言设计角度来看，Go语言的接口（interface）和并发（concurrency）原语是我最喜欢的两类Go语言语法元素。Go语言核心团队的技术负责人Russ Cox也曾说过这样一句话：“**如果要从Go语言中挑选出一个特性放入其他语言，我会选择接口**”，这句话足以说明接口这一语法特性在这位Go语言大神心目中的地位。

为什么接口在Go中有这么高的地位呢？这是因为**接口是Go这门静态语言中唯一“动静兼备”的语法特性**。而且，接口“动静兼备”的特性给Go带来了强大的表达能力，但同时也给Go语言初学者带来了不少困惑。要想真正解决这些困惑，我们必须深入到Go运行时层面，看看Go语言在运行时是如何表示接口类型的。在这一讲中，我就带着你一起深入到接口类型的运行时表示层面看看。

好，在解惑之前，我们先来看看接口的静态与动态特性，看看“动静皆备”到底是什么意思。

## 接口的静态特性与动态特性

接口的**静态特性**体现在**接口类型变量具有静态类型**，比如 `var err error` 中变量err的静态类型为error。拥有静态类型，那就意味着编译器会在编译阶段对所有接口类型变量的赋值操作进行类型检查，编译器会检查右值的类型是否实现了该接口方法集合中的所有方法。如果不满足，就会报错：
<div><strong>精选留言（27）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（23） 💬（1）<div>思考题有2 种方法：
1）returnsError() 函数不返回 error 非空接口类型，而是直接返回结构体指针 *MyError（明确的类型，阻止自动装箱）；
2）不要直接 err != nil 这样判断，而是使用类型断言来判断：
if e, ok := err.(*MyError); ok &amp;&amp; e != nil {
    fmt.Printf(&quot;error occur: %+v\n&quot;, e)
    return
}

PS：Go 的“接口”在编程中需要特别注意，必须搞清楚接口类型变量在运行时的表示，以避免踩坑！！！</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/53/a8/abc96f70.jpg" width="30px"><span>return</span> 👍（18） 💬（1）<div>老师讲的太好， 这一篇 知识密度相当大啊， 
就这一篇就值专栏的价格了。
感谢老师如此用心的输出。</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/66/ac631a36.jpg" width="30px"><span>Geralt</span> 👍（16） 💬（3）<div>修改方法:
1. 把returnsError()里面p的类型改为error
2. 删除p，直接return &amp;ErrBad或者nil</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/d9/00870178.jpg" width="30px"><span>Slowdive</span> 👍（12） 💬（1）<div>老师， 请问这里发生装箱了吗？ 返回类型是error， 是一个接口， p是*MyError， p的方法列表覆盖了error这个接口， 所以是可以赋值给error类型的变量。 
这个过程发生了隐式转换，赋值给接口类型，做装箱创建iface， 
p != nil就成了 (&amp;tab, 0x0) != (0x0, 0x0)

func returnsError() error {    
    var p *MyError = nil    
    if bad() {
        p = &amp;ErrBad
    }
    return p
}

这样理解对吗？</div>2022-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（10） 💬（2）<div>原来装箱是这样：将任意类型赋值给一个接口类型变量就是装箱操作。
接口类型的装箱实际就是创建一个 eface 或 iface 的过程</div>2022-01-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/GJXKh8OG00U5ial64plAIibbIuwkzhPc8uYic9Hibl8SbqvhnS2JImHgCD4JGvTktiaVnCjHQWbA5wicaxRUN5aTEWnQ/132" width="30px"><span>Geek_a6104e</span> 👍（7） 💬（1）<div>eif: (0x10b38c0,0x10e9b30)
err: (0x10eb690,0x10e9b30)
eif = err: true
eface: {_type:0x10b38c0 data:0x10e9b30}
   _type: {size:8 ptrdata:0 hash:1156555957 tflag:15 align:8 fieldAlign:8 kind:2 equal:0x10032e0 gcdata:0x10e9a60 str:4946 ptrToThis:58496}
   data: bad error

iface: {tab:0x10eb690 data:0x10e9b30}
   itab: {inter:0x10b5e20 _type:0x10b38c0 hash:1156555957 _:[0 0 0 0] fun:[17454976]}
     inter: {typ:{size:16 ptrdata:16 hash:235953867 tflag:7 align:8 fieldAlign:8 kind:20 equal:0x10034c0 gcdata:0x10d2418 str:3666 ptrToThis:26848} pkgpath:{bytes:&lt;nil&gt;} mhdr:[{name:2592 ityp:43520}]}
     _type: {size:8 ptrdata:0 hash:1156555957 tflag:15 align:8 fieldAlign:8 kind:2 equal:0x10032e0 gcdata:0x10e9a60 str:4946 ptrToThis:58496}
     fun: [0x10a5780(17454976),]
   data: bad error 请问为什么data会是bad error不应该是5吗</div>2022-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（6） 💬（1）<div>Go 指针这块，感觉可以单独抽出一讲来讲下，并且结合unsafe 讲解，不知道大白老师能否满足大家的愿望呢？😂</div>2022-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/16/48/01567df1.jpg" width="30px"><span>郑泽洲</span> 👍（5） 💬（3）<div>请教老师，接口类型装箱过程为什么普遍要把原来的值复制一份到data？（除了staticuint64s等特例）直接用原来的值不行吗，还能提升点性能</div>2022-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b0/6e/921cb700.jpg" width="30px"><span>在下宝龙、</span> 👍（5） 💬（3）<div>老师您好，在   eif2 = 17 这个操作后，输出后的data  ,0xc00007ef48 和0x10eb3d0 不相等呀，为甚么说他们是一样的
eif1: (0x10ac580,0xc00007ef48)
eif2: (0x10ac580,0x10eb3d0)</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（3） 💬（2）<div>大白老师的这一节干货很多，读的意犹未尽。有几个疑惑点，麻烦老师解忧。

1. 文中类似：“_type” 这种命名，前面加下划线，这种有什么含义呢？

2. 文中关于打印两类接口内部详细信息的代码中，运用了大量的 * 还有 &amp; 再加上  unsafe.Pointer 的使用，看起来会非常困惑，希望老师后面能讲一讲Go的指针吧。刚从动态语言转过来，确实应该好好理解一下。不然后面写出来的代码一定会有很多潜在的风险。</div>2021-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（2） 💬（1）<div>tony bai 老师，翻看评论留言中，发现有一处你是这样写的：

var a int = 6
var i interface{} = a
i.(int) = 7

通过前面的知识，i.(int)  是类型断言，通常是 v，ok := i.(int)，这里的 i.(int) = 7 该怎么理解呢？</div>2023-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（2） 💬（2）<div>白老师我将 returnsErro()改为如下的方式,
func returnsError() error {
	var p MyError
	return p
}
然后在main()中使用
err := returnsError()
if err != nil {
	fmt.Printf(&quot;error :%+v\n&quot;, err)  &#47;&#47; 输出: error :%!v(PANIC=Error method: runtime error: invalid memory address or nil pointer dereferenc
}

如果在MyError 显式实现 error的Error()函数, 就不会报错了, 即:
func (MyError) Error() string {
	return &quot;bad things happend&quot;
}

我用 dumpItabOfIface(unsafe.Pointer(&amp;err)) 查看一下输出, 发现不管是否显式实现 MyError 中的 Error(),
tab.fun 字段都是有值的，因此就很疑惑为什么显式实现了 Error()就不会报错呢？ 麻烦白老师帮我解惑一下，谢谢~~</div>2022-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/87/5f/6bf8b74a.jpg" width="30px"><span>Kepler</span> 👍（2） 💬（1）<div>这篇有点高强度对抗啊</div>2022-03-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（2） 💬（1）<div>虽然是Go语言第一课，但这一部分讲得很深入，而且很厉害的一点是，把难以理解的技术细节隐藏的刚刚好，这一篇要再看几遍。白老师真是讲课的高手啊👍👍</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/59/28/943709cb.jpg" width="30px"><span>Witt</span> 👍（2） 💬（2）<div>返回 *MyError 而不是 error</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/64/8a/bc8cb43c.jpg" width="30px"><span>路边的猪</span> 👍（1） 💬（2）<div>var err error
err = errors.New(&quot;error1&quot;)
fmt.Printf(&quot;%T\n&quot;, err)  &#47;&#47; *errors.errorString

为什么说这里的 errors.New(&quot;error1&quot;) 赋值给err 是体现动态性了呢？
errors.New(&quot;error1&quot;) 能不能赋值给 err 不是也是在编译阶段就能知道了吗？</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/5f/f1/c66c8c51.jpg" width="30px"><span>吃两块云</span> 👍（1） 💬（1）<div>实在是太干了，喝了两瓶水才咽下去。</div>2023-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/6d/3c2a5143.jpg" width="30px"><span>二进制傻瓜</span> 👍（1） 💬（1）<div>木有看懂，还得多看几遍。</div>2022-11-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJ8ic8eLTo5rnqIMJicUfpkVBrOUJAW4fANicKIbHdC54O9SOdwSoeK6o8icibaUbh7ZUXAkGF9zwHqo0Q/132" width="30px"><span>ivhong</span> 👍（1） 💬（4）<div>这篇文章看了好几遍，一直在纠结文章开头的那个代码示例看不懂
func returnsError() error {    
    var p *MyError = nil    
    if bad() {
        p = &amp;ErrBad
    }
    return p
}
1）通过returnsError函数是不是可以翻译成：该函数返回的是一个实现了error变量，而这个变量具体是什么类型的不清楚。
2）为什么 使用 MyError 指针类型定义 p
3）为什么返回的是 p（一个指向实现了error接口的指针？）
4）既然接口的返回值是一个接口类型，那么只能确定使用该返回值的方法，而不是值，因为值并不确定是什么类型的，所以在使用值时必须先断言才能合理的使用其值（个人理解）。在main函数中直接使用返回值 == nil 判断，结果是不可预测的，可以是说是逻辑上是不允许的（为什么go的设计者不在编译的时候报错报错呢？这个应该可以判断的吧）。
5）于是我把函数代码简化成下面这样
func returnsError() error {
	var p MyError
	return p
}
然后在main函数中使用
err := returnsError()
if err != nil {
	fmt.Printf(&quot;error occur: %+v\n&quot;, err)
	return
}
发现 err 包含运行时错误：
error occur: %!v(PANIC=Error method: runtime error: invalid memory address or nil pointer dereference) 无效内存地址或nil指针引用
是不是因为函数返回的结果要求是error指针类型的，而函数返回的是空指针，空指针不是error类型的指针，所以报着个错呢？
6）把returnsError 再次修改
func returnsError() *MyError {
	var p *MyError
	return p
}
这样这样在main函数中就不会报错了，可以把main函数翻译成这样的人类语言对么? “通过returnsError获取 MyError类型的指针，如果这个指针不为空的话，则说明有错误返回”

7）装箱&#47;拆箱 是不是就是解决接口类型参数在传输过程中，“动态”类型的问题？



</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ce/d7/5315f6ce.jpg" width="30px"><span>不负青春不负己🤘</span> 👍（1） 💬（1）<div>mark，回头在反复读，干货太多了</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ba/ce/fd45714f.jpg" width="30px"><span>bearlu</span> 👍（1） 💬（1）<div>这次课很干。需要再学一遍</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（0） 💬（1）<div>Tony bai 老师，我在 go 1.18.3 版本中已经找不到 convT2E 和 convT2I 两个 runtime 包的函数了，老师能讲讲后来的版本中，这两个函数是被哪几个函数取代了吗？ 做了什么优化。</div>2023-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/bb/e0/c7cd5170.jpg" width="30px"><span>Bynow</span> 👍（0） 💬（1）<div>将 returnsError 返回签名更改为 *MyError </div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/44/b5/7eba5a0e.jpg" width="30px"><span>木木</span> 👍（0） 💬（1）<div>这节学到很多！</div>2022-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/2a/4e/a3f53cae.jpg" width="30px"><span>撕影</span> 👍（2） 💬（0）<div> 装箱 inerface=struct 和前面说的 i.(T) 好像一对反操作</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/00/3202bdf0.jpg" width="30px"><span>piboye</span> 👍（2） 💬（1）<div>nil error ！= nil的价值是啥，data为空，itab有类型信息的接口变量这种东西有什么具体使用场景吗？ 如果只是因为实现的原因，我觉得就是go在挖坑，典型的违背了直觉啊</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cc/70/64045bc0.jpg" width="30px"><span>人言有力</span> 👍（0） 💬（0）<div>本节通过一个接口变量赋值为nil和nil比较不相等的例子引出了接口类型运行时的细节
1、接口类型会根据空接口和非空接口采用两种不同的结构体表示（eface和iface）
2、前者记录了动态类型的类型信息（_type)还有动态类型的数值引用；后者不仅要记录接口的信息，同时还要记录（_type动态类型的结构）
3、接口类型的比较需要_type和data引用都完全一致才相等，但是要注意，如果是空接口和非空接口比较，会采用非空接口的_type变量进行比较，data字段如果是指针类型则会解指针判断，如果是非指针类型则直接比较
4、接口类型变量赋值的本质是一个装箱操作，赋值后等式右端的变量data域会进行拷贝，有性能开销，这点需要注意。

思考题：
1、通过明确的类型返回避免自动装箱
2、通过类型断言来避免直接==nil</div>2024-05-19</li><br/>
</ul>