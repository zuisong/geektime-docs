我在上两篇文章中，详细地讲述了Go语言中的错误处理，并从两个视角为你总结了错误类型、错误值的处理技巧和设计方式。

在本篇，我要给你展示Go语言的另外一种错误处理方式。不过，严格来说，它处理的不是错误，而是异常，并且是一种在我们意料之外的程序异常。

## 前导知识：运行时恐慌panic

这种程序异常被叫做panic，我把它翻译为运行时恐慌。其中的“恐慌”二字是由panic直译过来的，而之所以前面又加上了“运行时”三个字，是因为这种异常只会在程序运行的时候被抛出来。

我们举个具体的例子来看看。

比如说，一个Go程序里有一个切片，它的长度是5，也就是说该切片中的元素值的索引分别为`0`、`1`、`2`、`3`、`4`，但是，我在程序里却想通过索引`5`访问其中的元素值，显而易见，这样的访问是不正确的。

Go程序，确切地说是程序内嵌的Go语言运行时系统，会在执行到这行代码的时候抛出一个“index out of range”的panic，用以提示你索引越界了。

当然了，这不仅仅是个提示。当panic被抛出之后，如果我们没有在程序里添加任何保护措施的话，程序（或者说代表它的那个进程）就会在打印出panic的详细情况（以下简称panic详情）之后，终止运行。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/dc/07195a63.jpg" width="30px"><span>锋</span> 👍（20） 💬（8）<div>老师，你好，我有一个疑问，请教一下，谢谢~
Go在设计的时候没有设计try...catch...finally这样的方式来捕获异常。
我在网上查很多人用panic、defer和recover组合来实现异常的捕获，甚至很多都将这个二次封装之后作为一个库来进行使用。
我的疑问是，从Go的设计角度为什么要这么做？是出于什么样的目的，还是他俩之间有什么优劣？
非常感谢~，烦请解答。</div>2020-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/60/c2/6d50bfdf.jpg" width="30px"><span>唐丹</span> 👍（12） 💬（5）<div>郝大，你好，我在golang 8中通过recover处理panic时发现，必须在引发panic的当前协程就处理掉，否则待其传递到父协程直至main方法中，都不能通过recover成功处理掉了，程序会因此结束。请问这样设计的原因是什么？那么协程是通过panic中记录的协程id来区分是不是在当前协程引发的panic的吗？另外，这样的话，我们应用程序中每一个通过go新起的协程都应该在开始的地方recover，否则即使父协程有recover也不能阻止程序因为一个意外的panic而挂掉？盼望解答，谢谢🙏</div>2018-09-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLia2EwyyEVs3tWRnMlqaAG7R7HvlW4vGvxthKsicgsCEeXO1qL7mMy6GAzgdkSKcH3c70Qa2hY3JLw/132" width="30px"><span>沐夜星光</span> 👍（4） 💬（2）<div>“控制权如此一级一级地沿着调用栈的反方向传播至顶端，也就是我们编写的最外层函数那里”。最外层函数是go函数，也就说当panic触发，通过其所在的goroutine，将控制权转移给运行时系统时，是不一定经过main函数的吗？另外老师能不能讲讲，go是怎么回收一个进程的，怎么处理运行中的goroutine以及涉及的资源。</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（2） 💬（4）<div>初学go都会吐槽说没有 try catch , 应该不止我一个</div>2021-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/02/ff/569d5904.jpg" width="30px"><span>阿俊</span> 👍（0） 💬（2）<div>请问老师 曾经我也是JAVA程序员 以前做JAVA项目 那时候遇到 例如 编写业务代码 “用户名称”不符合某种条件 业务逻辑代码会写throws 包含错误信息的自定义业务Exception 然后最终做一个try catch 然后catch到业务excption提取其中的message反馈给最终结果；如果在go项目开发中遇到类似问题，是不是可以通过的手动触发panic， 再在最终出口的地方，通过defer结合recover全局捕获相关panic并提取信息反馈给客户端也防止因此整个application崩掉，这种方式是否可取？ 想听听老师的观点，感谢~</div>2023-09-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PeibZXsEcwic1zvrAQpDlnNlPxZvmAtIZ6XCenC8NaPbVVfCk7PXgAYzb8icqrYlb9cJd82hia9FYTicxqSdgyCEP4w/132" width="30px"><span>Geek_37a441</span> 👍（0） 💬（4）<div>老师，你好，我想问下，panic触发的时机，比如指令执行过程中，在什么时候会调用到相关的panic，比如数组越界是什么时候调用runtime.panicIndex，是有个额外的线程不断检测有异常了吗？</div>2020-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/21/b8/aca814dd.jpg" width="30px"><span>江山如画</span> 👍（37） 💬（3）<div>一个函数如果要把 panic 转化为error类型值，并将其结果返回给调用方，可以考虑把 defer 语句封装到一个匿名函数之中，下面是实验的一个例子，所用函数是一个除法函数，当除数为0的时候会抛出 panic并捕获。

func divide(a, b int) (res int, err error) {
	func() {
		defer func() {
			if rec := recover(); rec != nil {
				err = fmt.Errorf(&quot;%s&quot;, rec)
			}
		}()
		res = a &#47; b
	}()
	return
}

func main() {
	res, err := divide(1, 0)
	fmt.Println(res, err) &#47;&#47; 0 runtime error: integer divide by zero

	res, err = divide(2, 1)
	fmt.Println(res, err) &#47;&#47; 2 &lt;nil&gt;
}
</div>2018-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/8f/4caf7f03.jpg" width="30px"><span>Bang</span> 👍（14） 💬（0）<div>先使用go中的类似try catch这样的语句，将异常捕获的异常转为相应的错误error就可以了</div>2018-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/99/c9/a7c77746.jpg" width="30px"><span>冰激凌的眼泪</span> 👍（4） 💬（0）<div>panic时，会捕获异常及异常上下文（函数名+文件行）
类似看作有一个异常上下文列表，始于异常触发处，沿着函数调用逆向展开，每一级append自己的异常上下文，直至goroutine入口函数，最终被runtime捕获
最终异常信息被打印，异常上下文列表被顺序打印，程序退出</div>2018-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ea/80/8759e4c1.jpg" width="30px"><span>🐻</span> 👍（2） 💬（0）<div>https:&#47;&#47;gist.github.com&#47;bwangelme&#47;9ce1c606ba9f69c72f82722adf1402e1</div>2019-03-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/45/31/53910b61.jpg" width="30px"><span>A 凡</span> 👍（2） 💬（0）<div>之前自己学习时候的一些模糊点更加清晰了，支持！</div>2018-10-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e8/55/63189817.jpg" width="30px"><span>MClink</span> 👍（0） 💬（0）<div>这个看起来比较简单
func main() {
	res, err := divide(1, 0)
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println(res)
}

func divide(a, b int) (res int, err error) {
	defer func() {
		if r := recover(); r != nil {
			err = fmt.Errorf(&quot;omg, panic ! err:%v&quot;, r)
			return
		}
	}()
	res = a &#47; b
	return
}</div>2022-07-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erpYZalYvFGcBs7zZvYwaQAZwTLiaw0mycJ4PdYpP3VxAYkAtyIRHhjSOrOK0yESaPpgEbVQUwf6LA/132" width="30px"><span>Harlan</span> 👍（0） 💬（0）<div>go这种满屏幕都是 判断 err!=nil 这种没有意义的代码  代码侵入性极强  也不优雅</div>2021-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/df/1e/cea897e8.jpg" width="30px"><span>传说中的成大大</span> 👍（0） 💬（0）<div>今日总结
今天主要是讲了panic运行时恐慌，一般发生在运行时
同样也可以自己调用内置的panic来主动引起恐慌 一般用来自己调试程序异常等等
主要掌握panic的执行过程 
首先从某一行引起了panic 然后返回到其调用函数 这样一级一级的返回 直到最顶层也即main函数中 最后把控制权交给了go运行时状态，最后程序奔溃 进程退出
panic的信息一般也在这个返回过程中不断的完善
panic: runtime error: index out of range &#47;&#47;错误信息
&#47;&#47;以下是调用堆栈
goroutine 1 [running]:
main.caller2()
        &#47;home&#47;ubuntu&#47;geek_go&#47;Golang_Puzzlers&#47;src&#47;puzzlers&#47;article19&#47;q1&#47;demo48.go:22 +0x91
main.caller1()
        &#47;home&#47;ubuntu&#47;geek_go&#47;Golang_Puzzlers&#47;src&#47;puzzlers&#47;article19&#47;q1&#47;demo48.go:15 +0x66
main.main()
        &#47;home&#47;ubuntu&#47;geek_go&#47;Golang_Puzzlers&#47;src&#47;puzzlers&#47;article19&#47;q1&#47;demo48.go:9 +0x66
exit status 2
关于思考题 我也先想了一下 我们捕获异常并将错误信息封装到一个error当中最后返回这个err
后来又去翻了解答 好像就是这个 样子的</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/20/27/a6932fbe.jpg" width="30px"><span>虢國技醬</span> 👍（0） 💬（0）<div>打卡</div>2019-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5d/f8/62a8b90d.jpg" width="30px"><span>melody_future</span> 👍（0） 💬（0）<div>panic、recover 有点像try、、catch。这样应该会好理解很多</div>2018-12-25</li><br/>
</ul>