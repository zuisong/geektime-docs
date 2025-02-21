在上两篇文章中，我主要为你讲解了与`go`语句、goroutine和Go语言调度器有关的知识和技法。

内容很多，你不用急于完全消化，可以在编程实践过程中逐步理解和感悟，争取夯实它们。

* * *

现在，让我们暂时走下神坛，回归民间。我今天要讲的`if`语句、`for`语句和`switch`语句都属于Go语言的基本流程控制语句。它们的语法看起来很朴素，但实际上也会有一些使用技巧和注意事项。我在本篇文章中会以一系列面试题为线索，为你讲述它们的用法。

那么，**今天的问题是：使用携带`range`子句的`for`语句时需要注意哪些细节？** 这是一个比较笼统的问题。我还是通过编程题来讲解吧。

> 本问题中的代码都被放在了命令源码文件demo41.go的`main`函数中的。为了专注问题本身，本篇文章中展示的编程题会省略掉一部分代码包声明语句、代码包导入语句和`main`函数本身的声明部分。

```
numbers1 := []int{1, 2, 3, 4, 5, 6}
for i := range numbers1 {
	if i == 3 {
		numbers1[i] |= i
	}
}
fmt.Println(numbers1)
```

我先声明了一个元素类型为`int`的切片类型的变量`numbers1`，在该切片中有6个元素值，分别是从`1`到`6`的整数。我用一条携带`range`子句的`for`语句去迭代`numbers1`变量中的所有元素值。

在这条`for`语句中，只有一个迭代变量`i`。我在每次迭代时，都会先去判断`i`的值是否等于`3`，如果结果为`true`，那么就让`numbers1`的第`i`个元素值与`i`本身做按位或的操作，再把操作结果作为`numbers1`的新的第`i`个元素值。最后我会打印出`numbers1`的值。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/fb/44/8b2600fd.jpg" width="30px"><span>咖啡色的羊驼</span> 👍（29） 💬（1）<div>好久没留言了，

1.断言判断value.(type)
2.if的判断的域和后面跟着的花括号里头的域。和函数雷同，参数和花括号里头的域同一个</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/f9/caf27bd3.jpg" width="30px"><span>大王叫我来巡山</span> 👍（17） 💬（2）<div>了解这些只能证明您对这个语言足够的了解，但是实际中谁会写这么蛋疼的代码呢，这一篇通篇其实说明的还是go语言中关于类型转换的内容</div>2019-09-09</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJAWUhO0xSjD6wbGScY5WOujAE94vNYWlWmsVdibb0IWbXzSSNXJHp0lqfWVq8ZicKBsEY1EuAWArew/132" width="30px"><span>Felix</span> 👍（9） 💬（1）<div>关于数组变切片那个地方。我理解如下：切片自己不拥有任何数据，它只是底层数组的一种表示，对切片的任何操作都会被反映到底层数组中去。 
package main

import &quot;fmt&quot;

func main() {

	numbers3 := []int{1, 2, 3, 4, 5, 6}
	maxIndex3 := len(numbers2) - 1 &#47;&#47;6-1= 5
	for i, e := range numbers3 {  &#47;&#47; 0:1 1:2 2:3 3:4 4:5 5:6
		if i == maxIndex3 {   &#47;&#47; 5
			numbers3[0] += e  &#47;&#47; 0,7
		} else {
			numbers3[i+1] += e  &#47;&#47; 1:3
		}
		&#47;&#47; 0:1 1:(1+2)3 2:3 3:4 4:5 5:6
		&#47;&#47; 0:1 1:3 2:(3+3)6 3:4 4:5 5:6
		&#47;&#47; 0:1 1:3 2:6 3:(6+4)10 4:5 5:6
		&#47;&#47; 0:1 1:3 2:6 3:10 4:(10+5)15 5:6
		&#47;&#47; 0:1 1:3 2:6 3:10 4:15 5:(15+6)21
		&#47;&#47; 0:(21+1)22 1:3 2:6 3:10 4:15 5:21
		&#47;&#47; 22 3 6 10 15 21
	}
	fmt.Println(numbers3)
}</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a6/87/e802a33e.jpg" width="30px"><span>Dr.Li</span> 👍（8） 💬（2）<div>感觉go的语法有点变态啊</div>2018-09-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GBU53SA3W8GNRAwZIicc3gTEc0nSvfPJw7iboAMicjicmP6egDcibib28DkUfTYOjMd31DIznmofdRZrpIXvmXvjV1PQ/132" width="30px"><span>博博</span> 👍（6） 💬（1）<div>老师遇到一个问题，希望能帮忙解答下！
您在文章中说range表达式的结果值是会被复制的，那么是所有的都会被复制么？ 我看了资料，发现字典和通道类型好像没有发生复制！

&#47;&#47; Lower a for range over a map.
&#47;&#47; The loop we generate:
&#47;&#47;   var hiter map_iteration_struct
&#47;&#47;   for mapiterinit(type, range, &amp;hiter); hiter.key != nil; mapiternext(&amp;hiter) {
&#47;&#47;           index_temp = *hiter.key
&#47;&#47;           value_temp = *hiter.val
&#47;&#47;           index = index_temp
&#47;&#47;           value = value_temp
&#47;&#47;           original body
&#47;&#47;   }
很是疑惑，希望能得到指点！谢谢</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a4/76/585dc6b3.jpg" width="30px"><span>hiyanxu</span> 👍（5） 💬（3）<div>老师，我想问一下，range的副本，是说k、v是副本，还是被迭代的数组是副本？
我自己测试在for的里面和外面数组地址是一样的</div>2018-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/34/67/06a7f9be.jpg" width="30px"><span>while (1)等;</span> 👍（3） 💬（1）<div>文中说“被迭代的对象是range表达式结果值的副本而不是原值。”，那被迭代的对象是切片时，可以理解为指针的副本吗？也就是指针和指针的副本指向同一地址？</div>2021-05-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/22/c0/177d6750.jpg" width="30px"><span>Rico</span> 👍（2） 💬（2）<div>在类型switch语句中，我们怎样对被判断类型的那个值做相应的类型转换？
------val.(type)

在if语句中，初始化子句声明的变量的作用域是什么？
-------变量作用域为if语句{}内部的范围
</div>2021-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/71/e5/bcdc382a.jpg" width="30px"><span>My dream</span> 👍（2） 💬（1）<div>Go1.11已经正式发布，最大的一个亮点是增加了对WebAssembly的实验性支持。老师要讲一下不？我们都不懂这个有什么意义</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/24/a2/d61e4e28.jpg" width="30px"><span>jack</span> 👍（0） 💬（1）<div>        index := 0
	var mu sync.Mutex
	fp := func(i int, fn func()) {
		for {
			mu.Lock()
			if index == i {
				fn()
				index++
				mu.Unlock()
				break
			}
			mu.Unlock()
			time.Sleep(time.Nanosecond)
		}
	}
	for i := 0; i &lt; 10; i++ {
		go func(i int) {
			fn := func() {
				fmt.Println(i)
			}
			fp(i, fn)
		}(i)
	}
	&#47;&#47; 这里就简单点了，不用 sync.WaitGroup 等那些结束了
	time.Sleep(time.Second)</div>2022-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/94/12/15558f28.jpg" width="30px"><span>Jason</span> 👍（0） 💬（1）<div>老师，我在Go编译器源码的statements.cc里找到了range的原型，其实是对数组本身做了整体拷贝，后面的循环都是基于这个副本。我想问问老师，为什么range表达式要去做拷贝呢，明明代价更高了。还是说go设计range的初衷就是读取，真要修改就使用传统的for循环，期待老师的回答
&#47;&#47; Arrange to do a loop appropriate for the type.  We will produce
&#47;&#47;   for INIT ; COND ; POST {
&#47;&#47;           ITER_INIT
&#47;&#47;           INDEX = INDEX_TEMP
&#47;&#47;           VALUE = VALUE_TEMP &#47;&#47; If there is a value
&#47;&#47;           original statements
&#47;&#47;   }
针对数组
&#47;&#47; The loop we generate:
&#47;&#47;   len_temp := len(range)
&#47;&#47;   range_temp := range
&#47;&#47;   for index_temp = 0; index_temp &lt; len_temp; index_temp++ {
&#47;&#47;           value_temp = range_temp[index_temp]
&#47;&#47;           index = index_temp
&#47;&#47;           value = value_temp
&#47;&#47;           original body
&#47;&#47;   }</div>2022-05-24</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erNhKGpqicibpQO3tYvl9vwiatvBzn27ut9y5lZ8hPgofPCFC24HX3ko7LW5mNWJficgJncBCGKpGL2jw/132" width="30px"><span>Geek_1ed70f</span> 👍（0） 💬（1）<div>按位或

有错别字  += 写成了  |=</div>2019-02-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIu1n1DhUGGKTjelrQaLYOSVK2rsFeia0G8ASTIftib5PTOx4pTqdnfwb0NiaEFGRgS661nINyZx9sUg/132" width="30px"><span>Zzz</span> 👍（24） 💬（0）<div>个人理解： for .. range ..  实际上可以认为是方法调用的语法糖，range后面的变量就是方法参数，对于数组类型的变量，传入的参数是数组的副本，更新的是原数组的元素，取的是副本数组的元素；对于切片类型的变量，传入的参数是切片的副本，但是它指向的底层数组与原切片相同，所以取的元素和更新的元素都是同一个数组的元素。</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/84/6c/effc3a5a.jpg" width="30px"><span>澎湃哥</span> 👍（15） 💬（0）<div>好像还没有人回答数组变切片的问题，贴一下运行结果吧：
i:0, e:1
i:1, e:3
i:2, e:6
i:3, e:10
i:4, e:15
i:5, e:21
[22 3 6 10 15 21]

每次循环打印了一个索引和值，看起来 range 切片的话，是会每次取 slice[i] 的值，但是应该还是发生了拷贝，不能通过 e 直接修改原值。</div>2018-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9b/a8/6a391c66.jpg" width="30px"><span>geraltlaush</span> 👍（8） 💬（1）<div>val.(type)需要提前将类型转换成interface{},一楼的留言有点问题</div>2018-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（6） 💬（1）<div>第一个问题，在类型switch语句中，如何对被判断类型的那个值做类型转换，尝试在 switch 语句中重新定义了一个 uint8 类型的变量和被判断类型的值做加法操作，一共尝试了三种方法，发现需要使用 type assertion 才可以，强转或者直接相加都会出错。

转换语句是：val.(uint8)

完整验证代码：

val := interface{}(byte(1))
switch t := val.(type) {
case uint8:
	var c uint8 = 2

	&#47;&#47;use type assertion
	fmt.Println(c + val.(uint8))

	&#47;&#47;invalid operation: c + val (mismatched types uint8 and interface {})
	&#47;&#47;fmt.Println(c + val)

	&#47;&#47;cannot convert val (type interface {}) to type uint8: need type assertion
	&#47;&#47;fmt.Println(c + uint8(val))

default:
	fmt.Printf(&quot;unsupported type: %T&quot;, t)
}

第二个问题，在if语句中，初始化子句声明的变量的作用域是在该if语句之内，if语句之外使用该变量会提示 “undefined”。

验证代码：

m := make(map[int]bool)
if _, ok := m[1]; ok {
	fmt.Printf(&quot;exist: %v\n&quot;, ok)
} else {
	fmt.Printf(&quot;not exist: %v\n&quot;, ok)
}

&#47;&#47;fmt.Println(ok)  &#47;&#47;报错，提示 undefined: ok</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/87/64/3882d90d.jpg" width="30px"><span>yandongxiao</span> 👍（4） 💬（1）<div>咖啡色的羊驼的答案貌似是错误的吧？
1. 在类型switch语句中，t := value6.(type)；匹配到哪个case表达式，t就会是哪种具体的数据类型；
2. 在if语句中，子句声明的变量的作用域  比 随后的花括号内的变量的的作用域  更大
	if a := 10; a &gt; 0 {
		a := 20
		println(a)
	}
反证法：如果咖啡色的羊驼说的对，上面的语句不应该编译通过才对。

关于2这个细微的差异，也适用于for i:=0; i&lt;10; i++ 语句。
在for语句中的使用匿名函数，很可能出现“loop variable capture”问题。根本原因也是i的作用域与{}中的变量的作用域是不同的。</div>2018-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/3e/692a93f7.jpg" width="30px"><span>茶底</span> 👍（3） 💬（0）<div>老师什么时候讲逃逸分析啊</div>2018-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ed/04/a63ed1e3.jpg" width="30px"><span>hua</span> 👍（2） 💬（0）<div>把总结结论放在最前面再看主体内容会容易理解得多。</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/18/918eaecf.jpg" width="30px"><span>后端进阶</span> 👍（2） 💬（0）<div>真的很喜欢go的语法与简洁的哲学</div>2018-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/97/c5/84491beb.jpg" width="30px"><span>罗峰</span> 👍（1） 💬（1）<div>Switch是匹配每个case，找到相等的那个case，包含常量类型转换，唯一值检验。select是先对多个case求值，然后随机选一个执行</div>2021-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/ff/e4/927547a9.jpg" width="30px"><span>无名无姓</span> 👍（0） 💬（0）<div>package main
import(
	&quot;fmt&quot;
)
func main() {
	arr:=[]int{1,2,3,4,5,6}
	arrlen:=len(arr)-1
	for i,e:= range arr {
		if i==arrlen{
			arr[0]+=e
		}else{
			arr[i+1]+=e
		}
	}
	fmt.Println(arr)
}
========================</div>2021-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（0） 💬（0）<div>都是坑点，一不小心在生产就是隐患</div>2021-03-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7e/05/431d380f.jpg" width="30px"><span>拂尘</span> 👍（0） 💬（0）<div>本节第一个numbers1的例子，只有一个迭代变量的range，我本来理解的是变量里就是切片的元素值，自己心算的和老师的答案还一样的，心里有点沾沾自喜的，后来发现自己理解错了😂</div>2020-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a2/b5/4dc0c109.jpg" width="30px"><span>Cyril</span> 👍（0） 💬（0）<div>这个 switch case 的用法很灵活</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（0）<div>总结 
今天主要是讲了如下内容
1. range range表达主要是返回了一个对象的副本  并且只会执行一次
2. switch 主要注意的是
   2.1 不能有结果值相同的case表达式(当然变量除外) 如果有 则会编译不通过
   2.2 fallthrough 如果某个满足条件的case语句后面有fallthrough则会执行后面一个case语句
   2.3 类型自动转换 如果switch表达式后面的是无类型的值,它不会发生自动转换类型 但是如果case后面的是无类型的值的话 会被自动转换成 switch后面的类型
   2.4 如果表达式中含有接口类型  一定要注意 接口类型的实际动态类型 是否支持判等操作 因为会绕过编译器的检查 但是在运行时引起恐慌
关于思考题
1. 通过value.(type)表达式获取类型操作
2. 整个if语句范围内</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/iajicahVUQORTadFz4gJvicaiciaxicUI3VcTDVrPOBOpCvXibtPLyjvMCaoHiaOcnuBJOpShj6eRtsrKaOXBianDiaWcxKg/132" width="30px"><span>Geek_0ed632</span> 👍（0） 💬（0）<div>个人感觉go的作用域的设置比其他语言要好</div>2020-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/09/22/22c0c4fa.jpg" width="30px"><span>benying</span> 👍（0） 💬（0）<div>学习到一些平时没注意的细节，学习老师</div>2019-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b7/f9/a8f26b10.jpg" width="30px"><span>jacke</span> 👍（0） 💬（2）<div>switch进行有限的转化不是很明白？value1里面switch的语句不能从int转换为int8、那value2里面case语句又可以从int转换为int8？还有借口转换如何判定呢？</div>2018-10-24</li><br/>
</ul>