你好，我是郝林，今天我们继续来聊聊panic函数、recover函数以及defer语句的内容。

我在前一篇文章提到过这样一个说法，panic之中可以包含一个值，用于简要解释引发此panic的原因。

如果一个panic是我们在无意间引发的，那么其中的值只能由Go语言运行时系统给定。但是，当我们使用`panic`函数有意地引发一个panic的时候，却可以自行指定其包含的值。我们今天的第一个问题就是针对后一种情况提出的。

## 知识扩展

### 问题 1：怎样让panic包含一个值，以及应该让它包含什么样的值？

这其实很简单，在调用`panic`函数时，把某个值作为参数传给该函数就可以了。由于`panic`函数的唯一一个参数是空接口（也就是`interface{}`）类型的，所以从语法上讲，它可以接受任何类型的值。

但是，我们最好传入`error`类型的错误值，或者其他的可以被有效序列化的值。这里的“有效序列化”指的是，可以更易读地去表示形式转换。

还记得吗？对于`fmt`包下的各种打印函数来说，`error`类型值的`Error`方法与其他类型值的`String`方法是等价的，它们的唯一结果都是`string`类型的。

我们在通过占位符`%s`打印这些值的时候，它们的字符串表示形式分别都是这两种方法产出的。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/32/09/669e21db.jpg" width="30px"><span>wesleydeng</span> 👍（95） 💬（9）<div>从语言设计上，不使用try-catch而是用defer-recover有什么优势？c++和java作为先驱都使用try-catch，也比较清晰，为什么go作为新语言却要发明一个这样的新语法？有何设计上的考量？</div>2019-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/63/8c/8e803651.jpg" width="30px"><span>凌惜沫</span> 👍（23） 💬（3）<div>如果defer中引发panic，那么在该段defer函数之前，需要另外一个defer来捕获该panic，并且代码中最后一个panic会被抛弃，由defer中的panic来成为最后的异常返回。</div>2019-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6a/89/3cac9f83.jpg" width="30px"><span>小龙虾</span> 👍（17） 💬（2）<div>我感觉还是go的这种设计好用，它会强迫开发者区别对待错误和异常，并做出不同的处理。相比try{}catch，我在开发中经常看到开发者把大段大段的代码或者整个处理写到try{}中，这本身就是对try{}catch的乱用</div>2019-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/60/ec/11cf22de.jpg" width="30px"><span>名:海东</span> 👍（4） 💬（3）<div>&#47;&#47;测试场景1
func Test()  {
	defer func() {
		if errRecover := recover(); errRecover != nil {
			fmt.Println(&quot;recover2...&quot;)
		}
		fmt.Println(&quot;no recover2...&quot;)
	}()
	defer func() {
		test01()  &#47;&#47; test01()方法在defer func(){}中执行
	}()
	b := 0
	a := 1 &#47; b
	fmt.Println(a)
	return
}

func test01() {
	if e := recover(); e != nil {
		fmt.Println(&quot;recover...&quot;)
	} else {
		fmt.Println(&quot;no recover...&quot;)
	}
	fmt.Println(&quot;defer exe...&quot;)
}

func main() {
	Test()
}
&#47;&#47;输出：
no recover...
defer exe...
recover2...
no recover2...

&#47;&#47;测试场景2
func Test()  {
	defer func() {
		if errRecover := recover(); errRecover != nil {
			fmt.Println(&quot;recover2...&quot;)
		}
		fmt.Println(&quot;no recover2...&quot;)
	}()
	defer test01()  &#47;&#47;test01()直接放到defer后面 
	b := 0
	a := 1 &#47; b
	fmt.Println(a)
	return
}

func test01() {
	if e := recover(); e != nil {
		fmt.Println(&quot;recover...&quot;)
	} else {
		fmt.Println(&quot;no recover...&quot;)
	}
	fmt.Println(&quot;defer exe...&quot;)
}

func main() {
	Test()
}
&#47;&#47;输出：
recover...
defer exe...
no recover2...

我的问题是：为什么场景1中出现panic没有在defer func() {
		test01()
	}()中被recover，而在defer func() {
		if errRecover := recover(); errRecover != nil {
			fmt.Println(&quot;recover2...&quot;)
		}
		fmt.Println(&quot;no recover2...&quot;)
	}()中被recover。
场景2使用defer test01 的写法后就可以被recover。</div>2020-07-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c6/73/abb7bfe3.jpg" width="30px"><span>疯琴</span> 👍（4） 💬（1）<div>试验了一下在 goroutine 里面 panic，其他的 goroutine（比如main）是 recover()不到的：

func main() {
	fmt.Println(&quot;start&quot;)
	defer func() {
		if p := recover(); p != nil {
			fmt.Println(p)
		}
	}()
	var wg sync.WaitGroup
	wg.Add(1)
	go func() {
		defer func() {
		    wg.Done()
		}()
		panic(errors.New(&quot;panic in goroutine&quot;))

	}()
	wg.Wait()
}</div>2019-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/9a/7f/781f89ab.jpg" width="30px"><span>Zz~</span> 👍（3） 💬（2）<div>老师，您好，我想问一下，如果在main函数里调用一个我自定义的panic方法，recover可以恢复；但是如果我将自定义的panic方法改为go mypanic这样，recover就不能恢复。这是什么原因呢？下面是我实验的代码


==============可以恢复的==============
package main

import (
	&quot;errors&quot;
	&quot;fmt&quot;
)

func myRecover() {
	if err := recover(); err != nil {
		fmt.Printf(&quot;panic is %s&quot;, err)
	}
}

func myPanic() {
	panic(errors.New(&quot;自定义异常&quot;))
}

func main() {
	defer myRecover()
	myPanic()
}


=================不可以恢复的==============
package main

import (
	&quot;errors&quot;
	&quot;fmt&quot;
	&quot;time&quot;
)

func myRecover() {
	if err := recover(); err != nil {
		fmt.Printf(&quot;panic is %s&quot;, err)
	}
}

func myPanic() {
	panic(errors.New(&quot;自定义异常&quot;))
}

func main() {
	defer myRecover()
	go myPanic()
	time.Sleep(time.Second * 5)
}
</div>2021-01-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/21/0e/b2c7469c.jpg" width="30px"><span>翼江亭赋</span> 👍（3） 💬（3）<div>iava世界里曾经try catch满天飞，现在还能看到不少这种代码，但逐渐大家认同了在去掉这种代码。

因为大部分catch住异常以后只是打个log再重新throw，这个交给框架代码在最外层catch住以后统一处理即可。非框架代码极少需要处理异常。

go世界里，err guard满天飞，但大部分的处理也是层层上传。但做不到不用，因为不像try那样去掉catch后会自动往上传递，不检查err的话就丢失了，所以这种代码去不掉。只能继续满天飞。

底层实现其实都是setjmp，主要的区别之一我认为是go设计者认为java异常的性能代价大。</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（3） 💬（1）<div>可以 defer 有点类似java中的final语句，里面还可以抛出异常。这样的好处是，我们捕获panic之后，可以对起内容进行查看，如果不是我们关注的panic那么可以继续抛出去</div>2018-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/aa/30/acc91f01.jpg" width="30px"><span>honnkyou</span> 👍（2） 💬（2）<div>「延迟到什么时候呢？这要延迟到该语句所在的函数即将执行结束的那一刻，无论结束执行的原因是什么。」
以该节课中代码为例的话是要吃到main函数快结束时执行是吗？执行defer函数。</div>2019-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5f/5d/63010e32.jpg" width="30px"><span>有匪君子</span> 👍（2） 💬（1）<div>这个问题就引发了另一个问题。defer可以在同一个函数中嵌套使用吗？感觉这两个问题答案应该一致</div>2018-10-01</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJSmAhbvPia1msvk91m5rQLTpicY85f2moFMCcAibictL3OeiaaVREadpHN2O3FwicmylwiclTUJJa1peS1Q/132" width="30px"><span>张sir</span> 👍（1） 💬（1）<div>您好，请问defer函数压𣏾的时候，为什么把当时的入参也放入𣏾中呢
```
func test() {
	var a, b = 1, 1
	defer func(flag int) {
		fmt.Println(flag)
	}(a + b)

	a = 2
	b = 2

}

```

这个输出的２不是４的理论论据是什么呢</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/fb/9d232a7a.jpg" width="30px"><span>Pana</span> 👍（1） 💬（1）<div>在defer 中 recover 了panic ，是否还能让函数返回错误呢</div>2020-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/74/a7/e609ca59.jpg" width="30px"><span>大雄</span> 👍（0） 💬（1）<div>是否可以理解，我们一般自己返回的error都是可以预见的业务异常（例如：手机号码格式不正确等），可以灵活判断。
panic则是意料外的，但不需要终止进程，所以需要要recover恢复</div>2022-10-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKELX1Rd1vmLRWibHib8P95NA87F4zcj8GrHKYQL2RcLDVnxNy1ia2geTWgW6L2pWn2kazrPNZMRVrIg/132" width="30px"><span>jxs1211</span> 👍（0） 💬（2）<div>如果	s5 := s1[5]引发panic，可以在函数退出前通过defer语句中recover捕获并处理，哪是否有办法让函数继续执行完引发panic时后面哪些代码，像其他语言用try catch一样，能继续向下执行完整个函数的代码，还是说go的设计并不是如此，一定要在引发异常处立即返回
func caller2() (err error) {
	defer func() {
		p := recover()
		if p != nil {
			err = fmt.Errorf(&quot;error: %s\n&quot;, p)
		}
	}()
	fmt.Println(&quot;Enter function caller2.&quot;)
	s1 := []int{1, 2, 3, 4, 5}
	s5 := s1[5]
	_ = s5
	fmt.Println(&quot;Exit function caller2.&quot;)
	return err
}</div>2021-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/fb/3eb917f1.jpg" width="30px"><span>爱学习的好孩子</span> 👍（0） 💬（1）<div>看不懂，defer函数和defer语句是什么关系？</div>2021-11-06</li><br/><li><img src="" width="30px"><span>tuxknight</span> 👍（0） 💬（1）<div>假如一个函数里面会有多个 panic，怎么能够只对某些 panic 进行 recover 呢？</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/0b/d4/39763233.jpg" width="30px"><span>Tianz</span> 👍（0） 💬（1）<div>皮友们，所有在 runtime 时导致程序终止（除了响应外部终止信号），都是 panic 吗？还真是有已经正确添加了 defer &amp; recover 机制但程序还是被终止了，所有像郝大上一篇回答说的有些 panic 是不可恢复的，蛋是都有哪些呢？</div>2020-06-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/49/31/6d5728ac.jpg" width="30px"><span>LUO JINGYUAN</span> 👍（0） 💬（2）<div>想问一下老师，队列和栈是不是两个不同的概念。因为之前看别的材料说队列（queue）和栈（stack）是不同的类型的数据结构。主要区分点是队列是FIFO，而栈是FILO。所以在看defer函数那段，感觉有点迷惑。所以希望老师讲解一下。</div>2020-05-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GBU53SA3W8GNRAwZIicc3gTEc0nSvfPJw7iboAMicjicmP6egDcibib28DkUfTYOjMd31DIznmofdRZrpIXvmXvjV1PQ/132" width="30px"><span>博博</span> 👍（0） 💬（1）<div>老师，最近遇到一个defer的问题，想请教一下！
defer在声明的时候会把函数和它的参数求值后拷贝一份先入栈，如果这个参数是值，那么在真正执行的时候不会改变，如果这个参数是引用，那在真正执行前如果改变了它的话，最终defer执行时的参数应该是改变后的！但是切片这种引用类型的参数，为什么没办法改变呢，而如果是一个指针的话就会被改变？
希望能得到您的解答，谢谢了！！！</div>2019-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（43） 💬（1）<div>defer其实是预调用，产生一个函数对象，压栈保存，函数退出时依次取出执行</div>2018-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a9/90/0c5ed3d9.jpg" width="30px"><span>颇忒妥</span> 👍（9） 💬（3）<div>作者想把概念给我们讲清楚，但是我总觉着看着费劲。为啥？因为作者太啰嗦了。比如：
defer函数调用的执行顺序与它们分别所属的defer语句的出现顺序（更严谨地说，是执行顺序）完全相反。
改成这样就简单多了：defer函数的调用顺序与其defer语句执行顺序相反。
还有：当一个函数即将结束执行时，其中的写在最下边的defer函数调用会最先执行，其次是写在它上边、与它的距离最近的那个defer函数调用，以此类推，最上边的defer函数调用会最后一个执行。
改成：当一个函数即将执行结束时，最下面的defer函数先执行，然后是倒数第二个，以此类推。</div>2020-02-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/KFgDEHIEpnSjjGClCeqmKYJsSOQo40BMHRTtNYrWyQP9WypAjTToplVND944one2pkEyH5Oib4m4wUOJ9xBEIZQ/132" width="30px"><span>sket</span> 👍（8） 💬（1）<div>感觉还是try{}catch这种异常处理好用</div>2018-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/27/fc/b8d83d56.jpg" width="30px"><span>Geek_e68th4</span> 👍（6） 💬（0）<div>Go 语言会把它携带的defer函数及其参数值另行存储到一个队列中。

这个队列与该defer语句所属的函数是对应的，并且，它是先进后出（FILO）的，相当于一个栈


直接表达为  创建defer时“函数对象“压栈，panic触发时出栈调用   更容易理解吧</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c5/44/8ff59fc4.jpg" width="30px"><span>風華</span> 👍（3） 💬（0）<div>如果defer中引发panic，那么在该段defer函数之前，需要另外一个defer来捕获该panic，并且代码中最后一个panic会被抛弃，由defer中的panic来成为最后的异常返回。</div>2018-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/8f/4caf7f03.jpg" width="30px"><span>Bang</span> 👍（2） 💬（1）<div>请问下，按您上面说的，一个recover只能恢复所在的那个函数。那如果一个 函数中有一个goroutine函数  而这个goroutine函数触发了panic，那是只有他自己可以recover是吗，他的上级是无法recover内部的goroutine的painc是这样吗？</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（1） 💬（0）<div>今日总结 
本章主要是讲了panic和recover以及defer
panic主要是用来抛出恐慌
而recover主要用来恢复恐慌，但是recover使用即恢复 如果在此时没有恐慌产生就会返回一个nil
也正是因为recover使用即恢复的特性 所以要把recover执行在产生恐慌之后，但是panic之后的代码不会再执行所以引入defer表达式
defer表达式 主要是用来代码延迟执行 延迟到函数结束，所以一般把recover跟defer搭配 
defer的执行 没执行一次defer语句产生一个defer函数 并且将其放入一个额外的栈中 所以是个先入后出的顺序!所以defer 函数的执行顺序与其声明顺序完全相反
关于思考题:
我觉得从理论上来说 我们没必要完全人为的引起panic 但是如果是不小心引起的panic那也无法避免,同时通过测试也是可以引发panic的</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/8f/4caf7f03.jpg" width="30px"><span>Bang</span> 👍（1） 💬（0）<div>请问下，按您上面说的，一个recover只能恢复所在的那个函数。那如果一个 函数中有一个goroutine函数  而这个goroutine函数触发了panic，那是只有他自己可以recover是吗，他的上级是无法recover内部的goroutine的painc是这样吗？</div>2018-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/11/d3/dd499428.jpg" width="30px"><span>独自逛荡</span> 👍（1） 💬（0）<div>defer func(){.....1}()
defer func(){.....2}()
defer func(){.....3}()
panic(&quot;4&quot;)
我在goland里面分别选择 gc 和 gccgo编译
发现执行的顺序不同  一个是3421一个是 3214</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/c9/a7c77746.jpg" width="30px"><span>冰激凌的眼泪</span> 👍（1） 💬（0）<div>可以使用panic函数主动触发panic，参数建议传递error（实际上可以是任意类型）
可以使用recover捕获panic，如果当前没有发生panic，则返回nil，如果有则返回panic副本
defer语句有延后执行调用表达式（推荐是个函数）的作用，这里的延后指的是defer语句的调用函数即将退出的那一刻
defer语句的延后调用是先进后出（FILO）的，C++的析构也是这样的</div>2018-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cd/64/ed091686.jpg" width="30px"><span>sdliang</span> 👍（0） 💬（0）<div>且不说先不先进, 我觉得try-catch的设计是符合人的思维习惯. defer可以有其他用途, 但是它也不该摒弃try-catch. 我觉得两者都保留, 各司其职才是好的选择.</div>2024-02-02</li><br/>
</ul>