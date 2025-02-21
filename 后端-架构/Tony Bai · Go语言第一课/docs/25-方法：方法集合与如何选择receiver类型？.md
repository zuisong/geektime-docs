你好，我是Tony Bai。

在上一节中我们开启了Go方法的学习，了解了Go语言中方法的组成、声明和实质。可以说，我们已经正式入门Go方法了。

入门Go方法后，和函数一样，我们要考虑如何进行方法设计的问题。由于在Go语言中，**方法本质上就是函数**，所以我们之前讲解的、关于函数设计的内容对方法也同样适用，比如错误处理设计、针对异常的处理策略、使用defer提升简洁性，等等。

但关于Go方法中独有的receiver组成部分，却没有现成的、可供我们参考的内容。而据我了解，初学者在学习Go方法时，最头疼的一个问题恰恰就是**如何选择receiver参数的类型**。

那么，在这一讲中，我们就来学习一下不同receiver参数类型对Go方法的影响，以及我们选择receiver参数类型时的一些经验原则。

## receiver参数类型对Go方法的影响

要想为receiver参数选出合理的类型，我们先要了解不同的receiver参数类型会对Go方法产生怎样的影响。在上一节课中，我们分析了Go方法的本质，得出了“Go方法实质上是**以方法的receiver参数作为第一个参数的普通函数**”的结论。

对于函数参数类型对函数的影响，我们是很熟悉的。那么我们能不能将方法等价转换为对应的函数，再通过分析receiver参数类型对函数的影响，从而间接得出它对Go方法的影响呢？
<div><strong>精选留言（28）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aQmhiahazRFUA4W3r1hdxxreSB5Pl54IwAJ8bwN6j02lzicydWAfPFbWx1LSFtzXH8MkI0jUKjlpUtmQBoZ4kReA/132" width="30px"><span>Geek_99b47c</span> 👍（83） 💬（4）<div>S 类型 和 *S 类型都没有包含方法，因为type S T 定义了一个新类型。
但是如果用 type S = T 则S和*S类型都包含两个方法。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/26/27/eba94899.jpg" width="30px"><span>罗杰</span> 👍（26） 💬（9）<div>其实相比 Rust，Go 的糖更少，而且时而多，时而少，让开发者会很困惑，甚至前后矛盾。*T 和 T调用方法时编译器互相转换，哇，真贴心，真舒服。但是方法集合，又被 Go 反手打了一巴掌。的确解决了 C 语言的诸多问题，但对比 Rust 的一些处理方案，的确会让人不爽。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/1e/18/9d1f1439.jpg" width="30px"><span>liaomars</span> 👍（14） 💬（5）<div>老师：
如果 T 类型需要实现某个接口，那我们就要使用 T 作为 receiver 参数的类型，来满足接口类型方法集合中的所有方法。
这段描述感觉不对，根据上面举的例子来说，应该是使用 *T 作为 receiver参数的类型，来满足接口类型方法集合中的所有方法。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5c/da/0a8bc27b.jpg" width="30px"><span>文经</span> 👍（4） 💬（1）<div>白老师，这课有两个疑问：
1. 当函数传递T类型的参数时，编译有办法判断对T类型是否有修改吗？如果没有修改的话，是否可以把参数转化为类似常量指针的方式引用，例如传递一个数组，如果没对数组修改 ，完全可以只传递一个指针。
2. 对于receiver选择的原则三：对T类型的限制比 *T 类型多，是不是因为有些时候一个T类型的对象无法获取它的地址，例如const 对象，但是一个T的指针类型，总是可以转换为 T类型的对象。</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（4） 💬（2）<div>老师，dumpMethodSet 函数只能统计导出方法的，有没有办法把非导出方法的也统计出来？</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（3） 💬（5）<div>如果因为 T 类型需要实现某一接口而使用 T 作为 receiver 参数的类型，那如果我想把在方法里对 t 的修改反映到原 T 类型实例上，何做到呢？</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/b0/6e/921cb700.jpg" width="30px"><span>在下宝龙、</span> 👍（3） 💬（1）<div>S类型和*S类型都是 空方法，因为S是新的类型，它不能调用T的方法，必须显示转换之后才可以调用，所以本身的S或*S类型都不具有任何的方法</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cb/8f/e7e9fa10.jpg" width="30px"><span>靠近我，温暖你</span> 👍（2） 💬（1）<div>S 类型 和 *S 类型都没有包含方法，因为type S T 定义了一个新类型。
但是如果用 type S = T 则S和*S类型都包含两个方法。</div>2023-01-29</li><br/><li><img src="" width="30px"><span>111</span> 👍（1） 💬（1）<div>测试一下

import (
	&quot;fmt&quot;
	&quot;reflect&quot;
)

type T struct{}

func (T) M1() {}
func (T) M2() {}

type S T

func dumpMethodSet(i interface{}) {
	dynTyp := reflect.TypeOf(i)
	if dynTyp == nil {
		fmt.Printf(&quot;there is no dynamic type\n&quot;)
		return
	}
	n := dynTyp.NumMethod()
	if n == 0 {
		fmt.Printf(&quot;%s&#39;s method set is empty!\n&quot;, dynTyp)
		return
	}
	fmt.Printf(&quot;%s&#39;s method set:\n&quot;, dynTyp)
	for j := 0; j &lt; n; j++ {
		fmt.Println(&quot;-&quot;, dynTyp.Method(j).Name)
	}
	fmt.Printf(&quot;\n&quot;)
}

func main() {
	var s S
	dumpMethodSet(s)
}
----------------------------------
S&#39;s method set is empty!
*S&#39;s method set is empty!

S 类型 和 *S 类型都没有包含方法

看来 S 是一个新类型，没有“继承”到T的方法
</div>2023-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/cb/28/21a8a29e.jpg" width="30px"><span>夏天</span> 👍（1） 💬（1）<div>方法接收者类型选择三个原则

1.如果需要修改接收者本身，传指针 *T
2.如果接受者本身较为复杂，传指针 *T，避免拷贝
3.*T 的方法集合是包含 T 的方法集合。*T 范围更大

go 文档不推荐混合使用，一般还是用 T* 吧。除非明确需要不改动 T 本身</div>2022-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2e/ca/469f7266.jpg" width="30px"><span>菠萝吹雪—Code</span> 👍（1） 💬（1）<div>思考题回答：type S T  相当于定义了一个新的类型，和T是完全不同的类型，测试结果，main.S&#39;s method set is empty!
*main.S&#39;s method set is empty!

</div>2022-08-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/66/047ee060.jpg" width="30px"><span>Return12321</span> 👍（1） 💬（1）<div>func main() {
	type S T
	var s1 S
	tool.DumpMethodSet(s1)
	tool.DumpMethodSet(&amp;s1)

	type L = T
	var l1 L
	tool.DumpMethodSet(l1)
	tool.DumpMethodSet(&amp;l1)
}

output：
main.S&#39;s method set is empty
*main.S&#39;s method set is empty
main.T&#39;s method set:
- M1
- M2

*main.T&#39;s method set:
- M1
- M2
- M3
- M4

type S T 定义了一个新类型</div>2022-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/a8/8aaf13e0.jpg" width="30px"><span>mikewoo</span> 👍（1） 💬（1）<div>S&#39;s method set is empty!
*S&#39;s method set is empty!
我的理解是type S T是定义了一个新类型。</div>2022-04-28</li><br/><li><img src="" width="30px"><span>白辉</span> 👍（1） 💬（1）<div>老师，您好，根据本节课内容有如下两个结论，那么T类型的实例可以调用receiver 为 *T 类型的方法，不能说明T类型的方法集合包含*T类型的方法吗？

1 通过这个实例，我们知道了这样一个结论：无论是 T 类型实例，还是 *T 类型实例，都既可以调用 receiver 为 T 类型的方法，也可以调用 receiver 为 *T 类型的方法。
2  Go 语言规定，*T 类型的方法集合包含所有以 *T 为 receiver 参数类型的方法，以及所有以 T 为 receiver 参数类型的方法。</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3a/68/373b90c8.jpg" width="30px"><span>River</span> 👍（1） 💬（1）<div>&quot;同理，类型为 *T 的实例 t2，它不仅可以调用 receiver 参数类型为 *T 的方法 M2，还可以调用 receiver 参数类型为 T 的方法 M1，这同样是因为 Go 编译器在背后做了转换。也就是，Go 判断 t2 的类型为 *T，与方法 M1 的 receiver 参数类型 T 不一致，就会自动将t2.M1()转换为(*t2).M1()。&quot;
老师这一段最后，（*t2）等于T类型了吗？前面（&amp;t1）等于*T类型好理解，*号对于类型和类型实例用法不一样吗？这个确实懵</div>2021-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/42/cd/09b568fc.jpg" width="30px"><span>JabariH</span> 👍（1） 💬（1）<div># go version: 1.16.5
func dumpMethodSet(i interface{}) {
    dynTyp := reflect.TypeOf(i)

    if dynTyp == nil {
        fmt.Printf(&quot;there is no dynamic type\n&quot;)
        return
    }

    n := dynTyp.NumMethod()
    if n == 0 {
        fmt.Printf(&quot;%s&#39;s method set is empty!\n&quot;, dynTyp)
        return
    }

    fmt.Printf(&quot;%s&#39;s method set:\n&quot;, dynTyp)
    for j := 0; j &lt; n; j++ {
        fmt.Println(&quot;-&quot;, dynTyp.Method(j).Name)
    }
    fmt.Printf(&quot;\n&quot;)
}

type T struct{}

func (T) M1() {}
func (T) M2() {}

func (*T) M3() {}
func (*T) M4() {}

func main() {
    var n int
    dumpMethodSet(n)
    dumpMethodSet(&amp;n)

    var t T
    dumpMethodSet(t)
    dumpMethodSet(&amp;t)
}

main()

在jupyter lab上的go kernel输出的是：
int&#39;s method set is empty!
*int&#39;s method set is empty!
struct {}&#39;s method set is empty!
*struct {}&#39;s method set is empty!

用的是go 1.16.5。</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（1） 💬（6）<div>追更老师的文章到现在，解答了我之前很多的困惑。也发现了一些新问题，希望老师抽空解答一下。

1. var t1 T   t2 := &amp;t   和  var t2 = &amp;T{} ，这两种对结构体 T 的实例化方式有什么区别呢？ 我从别的语言转到Go，就是很多时候被Go的一些奇奇怪怪的写法绕晕了。

2. &amp; 和 * 能不能 单独好好讲讲，看Go的代码，都是满屏的 &amp; 和 * ，对于动态语言的人来说，真的很难适应。

3. 文中的 NumMethod 方法，我点开方法的源码处的注释部分，这么写：“Note that NumMethod counts unexported methods only for interface types.”  这里的 unexported 代表的是未导出的意思，应该统计的是未导出的方法，但是我看文中统计了 导出方法的个数，感觉不理解。

4. 文中说：“Interface 接口类型包含了两个方法 M1 和 M2，它们的基类型都是 T。 ”  我想的是这句话表述有问题的，仅仅才接口的方法列表中，是看不出它们的基类型的呀。</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（1） 💬（4）<div>老师，go 方法可以“多实现”（“多继承”）吗？</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/28/22/ebc770dc.jpg" width="30px"><span>哈哈哈哈哈</span> 👍（1） 💬（7）<div> var t2 = &amp;T{} 中＆是什么意思？</div>2021-12-10</li><br/><li><img src="" width="30px"><span>Geek_0b92d9</span> 👍（1） 💬（1）<div>都是空方法集合。并没有定义 receiver 为 S 或者 &amp;S 的方法</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/98/4b/39908079.jpg" width="30px"><span>叶鑫</span> 👍（1） 💬（1）<div>真是太棒了</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e6/e5/b6980a7a.jpg" width="30px"><span>无双</span> 👍（1） 💬（2）<div>可以讲一下go的指针吗？</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/29/41/a413ca91.jpg" width="30px"><span>冒泡雪碧 🏈</span> 👍（0） 💬（1）<div>type S T &#47;&#47;定义一个新的类型，S和T不是同一个类型，而方法M1和M2指定的类型是T
type S=T &#47;&#47;S执行类型T的一个别名，S和T是同一个类型，S自然就拥有T的两个方法</div>2024-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/d9/ba/306ca85a.jpg" width="30px"><span>gogo</span> 👍（0） 💬（1）<div>遇事不决用指针，有问题再说
</div>2023-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/70/67/0c1359c2.jpg" width="30px"><span>qinsi</span> 👍（0） 💬（1）<div>原则三：“如果 T 类型需要实现某一接口的全部方法，那么我们就需要使用 T 作为 receiver 参数的类型来满足接口类型方法集合中的所有方法。”

似乎这是一句正确的废话？

“实际进行 Go 方法设计时，我们首先应该考虑的是原则三，即 T 类型是否要实现某一接口”。这似乎也是有问题的。假设有这样的定义：

type Interface interface {
	Get() int
	Set(n int)
}

type T struct {
	a int
}

按照原则三，T要实现Interface的话就要实现receiver为T的方法：

func (t T) Get() int {
	return t.a
}

func (t T) Set(n int) {
	t.a = n
}

但这样写没有实际意义，因为接口中Set()方法的语义隐含着要实现receiver为*T的方法。即此时需先通过原则一判断T是否要实现接口。
</div>2021-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（5） 💬（1）<div>对于 类型 T 能不能 使用 *T 的方式，取决于 T 类型是不是可寻址的，在方法集合中也体现出来了，默认 T 类型是不包含 *T 的方法的</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（4） 💬（0）<div>*T 会把修改反应到原类型实例；*T 会对性能开销有关系；T 和 *T 的方法会隐式转换；实际进行 Go 方法设计时，我们首先应该考虑的是原则三，即 T 类型是否要实现某一接口，如要实现某一接口，使用 T 作为 receiver 参数的类型，来满足接口类型方法集合中的所有方法。</div>2021-12-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/cc/70/64045bc0.jpg" width="30px"><span>人言有力</span> 👍（0） 💬（0）<div>本节讲了方法的receiver类型选择三个原则，以及方法集合的概念
0.判断一个类型是否实现一个接口的唯一原则是类型的方法集合是否包含了接口的方法集合，所以原生类型没有方法集合
1.所以首先看类型T是否要实现接口的方法，如果是则选择类型T
2.如果需要修改原类型实例或者类型的size值传递的开销过大时，选择类型*T
3.除此之外选择类型T
4.类型T的方法集合同时也是*T类型的方法集合，同时有一个语法糖——go编译器会针对T和*T类型在方法参数不满足时进行隐式转换

思考题：
其实最后得出的结果是T的方法集合是M1和M2，而S是空，说明类型嵌套没法用到底层类型的方法集合。</div>2024-05-18</li><br/>
</ul>