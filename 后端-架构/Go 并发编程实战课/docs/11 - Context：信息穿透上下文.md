你好，我是鸟窝。

在这节课正式开始之前，我想先带你看一个工作中的场景。

假设有一天你进入办公室，突然同事们都围住你，然后大喊“小王小王你最帅”，此时你可能一头雾水，只能尴尬地笑笑。为啥呢？因为你缺少上下文的信息，不知道之前发生了什么。

但是，如果同事告诉你，由于你业绩突出，一天之内就把云服务化的主要架构写好了，因此被评为9月份的工作之星，总经理还特意给你发1万元的奖金，那么，你心里就很清楚了，原来同事恭喜你，是因为你的工作被表扬了，还获得了奖金。同事告诉你的这些前因后果，就是上下文信息，他把上下文传递给你，你接收后，就可以获取之前不了解的信息。

你看，上下文（Context）就是这么重要。在我们的开发场景中，上下文也是不可或缺的，缺少了它，我们就不能获取完整的程序信息。那到底啥是上下文呢？其实，这就是指，在API之间或者方法调用之间，所传递的除了业务参数之外的额外信息。

比如，服务端接收到客户端的HTTP请求之后，可以把客户端的IP地址和端口、客户端的身份信息、请求接收的时间、Trace ID等信息放入到上下文中，这个上下文可以在后端的方法调用中传递，后端的业务方法除了利用正常的参数做一些业务处理（如订单处理）之外，还可以从上下文读取到消息请求的时间、Trace ID等信息，把服务处理的时间推送到Trace服务中。Trace服务可以把同一Trace ID的不同方法的调用顺序和调用时间展示成流程图，方便跟踪。
<div><strong>精选留言（21）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/34/84/27ecfcab.jpg" width="30px"><span>江湖夜雨十年灯</span> 👍（1） 💬（1）<div>感觉context的例子太少了老师，实际中context用的场景其实最多对复杂</div>2022-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/8d/87/47d95f4a.jpg" width="30px"><span>syuan</span> 👍（1） 💬（2）<div>老师，您好。
var (
    background = new(emptyCtx)
    todo       = new(emptyCtx)
)
在实际使用中，这两个变量在什么时候执行，在引入包的时候就执行了吗？
还是在执行Background() ，TODO() 这两个函数调用的时候执行？
在一个main函数中多次调用Background() ，TODO()，background，todo变量始终是指向同一个值吗？</div>2020-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f1/f3/6a2e6977.jpg" width="30px"><span>严光</span> 👍（0） 💬（1）<div>这篇如果能多一点 demo 就好了</div>2025-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/95/dc/07195a63.jpg" width="30px"><span>锋</span> 👍（0） 💬（2）<div>老师好。
【记住，不是只有你想中途放弃，才去调用 cancel，只要你的任务正常完成了，就需要调用 cancel，这样，这个 Context 才能释放它的资源（通知它的 children 处理 cancel，从它的 parent 中把自己移除，甚至释放相关的 goroutine】
上面这一段中任务正常完成 parent来cancel不太理解，正常父主动cancel基本都属于中断操作。但是老师讲到要正常退出的时候来cancel一下，既然是正常结束，那么父应该知道子结束了才去cancel，那父子之间不是还要单独建立一个channel来进行通讯？没有get到老师的点，麻烦老师能不能举个例子</div>2020-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/8f/cf/890f82d6.jpg" width="30px"><span>那时刻</span> 👍（0） 💬（2）<div>请问老师，文中提到的 exported key 的静态类型和保守的 unexported 的类型，它们各自指的是什么类型呢？</div>2020-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d4/37/bb19dbcd.jpg" width="30px"><span>楼梯口倒立</span> 👍（30） 💬（3）<div>这个例子讲的一言难尽，还不如百度出来的</div>2021-09-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/5b/4486e4f9.jpg" width="30px"><span>虫子樱桃</span> 👍（18） 💬（2）<div>Using Context Package in GO (Golang) – Complete Guide https:&#47;&#47;golangbyexample.com&#47;using-context-in-golang-complete-guide&#47;</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b8/3c/1a294619.jpg" width="30px"><span>Panda</span> 👍（11） 💬（1）<div>Context  就像 糖葫芦中的 竹签子  </div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e1/4f/00476b4c.jpg" width="30px"><span>Remember九离</span> 👍（10） 💬（1）<div>思考题简单写了下:
```go
package main

import (
	&quot;context&quot;
	&quot;fmt&quot;
	&quot;time&quot;
)

func main() {
	parent := context.Background()
	ctx, cancel := context.WithCancel(parent)
	child := context.WithValue(ctx, &quot;name&quot;, &quot;wuqq&quot;)
	go func() {
		for {
			select {
			case &lt;-child.Done():
				fmt.Println(&quot;it&#39;s over&quot;)
				return
			default:
				res := child.Value(&quot;name&quot;)
				fmt.Println(&quot;name:&quot;, res)
				time.Sleep(1 * time.Second)
			}
		}
	}()
	go func() {
		time.Sleep(3 * time.Second)
		cancel()
	}()

	time.Sleep(5 * time.Second)
}

```
源码在：https:&#47;&#47;github.com&#47;wuqinqiang&#47;Go_Concurrency</div>2020-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/b6/5b/4486e4f9.jpg" width="30px"><span>虫子樱桃</span> 👍（10） 💬（0）<div>context其实上几个例子更好。哈哈。大家可以参考 go by Example的例子 http:&#47;&#47;play.golang.org&#47;p&#47;0_bu1o8rIBO</div>2020-11-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhZZ4YhWluhayDIDDicJXJkDe86hm2mYEpPZzYdyopt8hPbt2EMcwgZ4jzPBqFyVUEQzb3sEYXWuA/132" width="30px"><span>愤怒的显卡</span> 👍（9） 💬（1）<div>可以写几个应用的实例</div>2020-11-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/8e/f0/18720510.jpg" width="30px"><span>50%</span> 👍（8） 💬（0）<div>其实这章我觉得通过例子来吃透比较好，建议大家看看那个golangbyexample的文章</div>2020-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/ea/8269574b.jpg" width="30px"><span>缘</span> 👍（6） 💬（0）<div>context讲的比较简单，特别是goroutine怎么不断的去检查是否超时，什么阶段检查合适</div>2020-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c7/89/16437396.jpg" width="30px"><span>极客酱酱</span> 👍（0） 💬（0）<div>思考题实践

package main

import (
	&quot;context&quot;
	&quot;fmt&quot;
	&quot;time&quot;
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	ctx1 := context.WithValue(ctx, &quot;key1&quot;, &quot;val1&quot;)
	go func() {
		defer func() { fmt.Println(&quot;goroutine exit&quot;) }()
		for {
			select {
			case &lt;-ctx1.Done():
				fmt.Println(&quot;ctx1 done&quot;)
				return
			}
		}
	}()
	cancel()
	time.Sleep(time.Millisecond)
}
</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e8/f4/40d6c39c.jpg" width="30px"><span>努力的狗狗</span> 👍（0） 💬（0）<div>只是概念，应该多举两个例子的</div>2021-11-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cf/cc/8de5007b.jpg" width="30px"><span>徐改</span> 👍（0） 💬（0）<div>func TestCascadeContext(t *testing.T) {
	type key int
	quit := false
	ctx, cancel := context.WithCancel(context.TODO())
	k := key(100)
	ctx = context.WithValue(ctx, k, 100)
	go func() {
		time.Sleep(time.Second)
		cancel()	&#47;&#47; parent context被cancel后，其子context也会被取消
	}()
	for {
		if quit {
			break
		}
		select {
		case &lt;- ctx.Done():		&#47;&#47; 子context被取消，结束循环
			quit = true
		default:
			fmt.Println(ctx.Value(k))
			time.Sleep(time.Second)
		}
	}
}</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d0/46/7f9af8de.jpg" width="30px"><span>寻</span> 👍（0） 💬（0）<div>grpc 客户端 传 backgroud类型的ctx，为什么服务端收到显示已经超时？</div>2021-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/0f/da7ed75a.jpg" width="30px"><span>芒果少侠</span> 👍（0） 💬（0）<div>思考题：
package context

import (
	&quot;context&quot;
	&quot;log&quot;
	&quot;testing&quot;
	&quot;time&quot;
)

func TestContextCancel(t *testing.T) {
	parent := context.Background()
	cancelCtx, cancelFunc := context.WithCancel(parent) &#47;&#47; parent
	valueCtx := context.WithValue(cancelCtx, &quot;key&quot;, &quot;value&quot;) &#47;&#47; child

	go func() {
		for {
			select {
			case &lt;-cancelCtx.Done(): {
				log.Printf(&quot;cancelCtx done&quot;)
				return
			}
			default:
				log.Printf(&quot;cancelCtx working&quot;)
			}
			time.Sleep(time.Millisecond * 500)
		}
	}()

	time.Sleep(time.Second)

	go func() {
		for {
			select {
			case &lt;-valueCtx.Done(): {
				log.Printf(&quot;valueCtx done&quot;)
				return
			}
			default:
				log.Printf(&quot;valueCtx working&quot;)
			}
			time.Sleep(time.Millisecond * 500)
		}
	}()


	time.Sleep(time.Second)
	&#47;&#47; cancel
	log.Printf(&quot;now start to cancel..&quot;)
	cancelFunc()

	time.Sleep(time.Second)
}
</div>2021-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/22/c8/f2892022.jpg" width="30px"><span>科科</span> 👍（0） 💬（0）<div>Done 方法返回一个 Channel 对象。在 Context 被取消时，此 Channel 会被 close，如果没被取消，可能会返回 nil。

我看了半天，到底是这个Done()方法返回nil,还是这个Channel返回nil，其实应该是Channel返回nil。

一般来说都把Done方法返回的这个Channel对象放在select里面监听，也不会直接去把Done()返回的channel关闭，既然WithConcel都返回一个函数了，就是在stop操作的时候调用cancelFunc，由这个函数去做资源的释放，关闭channel。</div>2021-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/17/11/a63acc6a.jpg" width="30px"><span>( ･᷄ὢ･᷅ )</span> 👍（0） 💬（1）<div>【记住，不是只有你想中途放弃，才去调用 cancel，只要你的任务正常完成了，就需要调用 cancel，这样，这个 Context 才能释放它的资源（通知它的 children 处理 cancel，从它的 parent 中把自己移除，甚至释放相关的 goroutine】

既然这样如果只是想做主动停止goroutine的操作，那么还不如直接使用make(chan struct{})这种情况了，而且context对子对象的遍历取消也会对性能有影响吧</div>2021-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/6e/76b4aa3d.jpg" width="30px"><span>橙子888</span> 👍（0） 💬（1）<div>打卡。</div>2020-11-04</li><br/>
</ul>