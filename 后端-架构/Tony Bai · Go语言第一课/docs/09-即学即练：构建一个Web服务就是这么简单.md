你好，我是Tony Bai。

在入门篇前面的几节课中，我们已经从Go开发环境的安装，一路讲到了Go包的初始化次序与Go入口函数。讲解这些，不仅仅是因为它们是你学习Go语言的基础，同时我也想为你建立“手勤”的意识打好基础。

作为Go语言学习的“过来人”，学到这个阶段，我深知你心里都在跃跃欲试，想将前面学到的知识综合运用起来，实现一个属于自己的Go程序。但到目前为止，我们还没有开始Go基础语法的系统学习，你肯定会有一种“无米下炊”的感觉。

不用担心，我在这节课安排了一个实战小项目。在这个小项目里，我希望你不要困在各种语法里，而是先跟着我““照猫画虎”地写一遍、跑一次，感受Go项目的结构，体会Go语言的魅力。

## 预热：最简单的HTTP服务

在想选择以什么类型的项目的时候，我还颇费了一番脑筋。我查阅了[Go官方用户2020调查报告](https://go.dev/blog/survey2020-results)，找到Go应用最广泛的领域调查结果图，如下所示：

![图片](https://static001.geekbang.org/resource/image/9a/91/9ab73568ef659d75a313f3394a811491.png?wh=1194x1158)

我们看到，Go应用的前4个领域中，有两个都是Web服务相关的。一个是排在第一位的API/RPC服务，另一个是排在第四位的Web服务（返回html页面）。考虑到后续你把Go应用于Web服务领域的机会比较大，所以，在这节课我们就选择一个Web服务项目作为实战小项目。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2b/92/af/ad02ae4b.jpg" width="30px"><span>扣剑书生</span> 👍（26） 💬（2）<div>store.go提供了 图书 和 接口的模板
factory 用于生产 接口实例
memstore.go 用于具体实现一个接口实例，实现其方法，并把样例发送到工厂
server.go 用于把路由和接口的方法对接起来</div>2021-11-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/8b/7c/fe7b1bf7.jpg" width="30px"><span>尧九之阳</span> 👍（11） 💬（2）<div>Go现在有流行的web服务器框架么？</div>2021-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/fe/f8/3e8de9b1.jpg" width="30px"><span>猫饼</span> 👍（9） 💬（2）<div>我果然还是太菜了 我开始看不懂了</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/59/21/d2efde18.jpg" width="30px"><span>布凡</span> 👍（8） 💬（4）<div>终于实验成功：
以下几个点需注意：
1、项目应放到 gopath货goroot相关的目录下，否则本地包的引用会报错，报错信息如下：&quot;could not import errors (cannot find package &quot;errors&quot; in any of c:\go\src\errors (from $GOROOT)...)&quot;
2、如果是复制的代码应该注意文件格式，可能报错&quot;package main: read unexpected NUL in input&quot;</div>2021-11-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/49/4e/8798cd01.jpg" width="30px"><span>顷</span> 👍（7） 💬（2）<div>老师的这个示例，麻雀虽小，五脏俱全。不过main.go里有一点疑问：http.Server.Shutdown(ctx)被调用后，http.Server.ListenAndServe()方法马上会返回error吧，按照实例代码里的写法，接收到中断信号后，马上调用Shutdown方法，此时errChan会返回ErrServerClosed，select逻辑走完，main方法就退出了，而go的http包里示意了我们需要确保shutdown调用后，整个代码不能马上退出，请老师解惑。。</div>2022-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/52/66/3e4d4846.jpg" width="30px"><span>includestdio.h</span> 👍（5） 💬（2）<div>作为基本0基础学go，这一节完全没看懂-，- 把后面的基础篇看完回来再试试吧</div>2022-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/a4/e481ae48.jpg" width="30px"><span>lesserror</span> 👍（5） 💬（5）<div>感谢 Tony Bai 老师这样由浅入深，并且尽可能贴近实战的讲解。

有以下困惑，麻烦解忧。

1. 对于一个module中，相同的包名，go内部是根据文件位置的不同，加以区分的吧？ 例如：bookstore&#47;store 和 bookstore&#47;internal&#47;store 这两个 package 同名，但是文件的路径不同，所以并不会有什么问题。如果在同一个package中，导入另一个同名的package，最佳实践是取个别名，我的理解没错吧？

2. 另外在 memstore.go 中的 包导入语句中： factory &quot;bookstore&#47;store&#47;factory&quot;，这个 默认使用的是factory名字，不需要再另起名字为factory吧？

3. 这门课中的知识和你在另外的一个平台的《改善Go语言编程质量的50个有效实践》的内容重合度大吗？ 精力有限，如果重合度大，就专心看这个就好了。

4. 这门课会讲讲Go写RPC服务方面的知识吗？ 这个在生产中挺常用的。</div>2021-11-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e9/dc/cc05ebc7.jpg" width="30px"><span>小明</span> 👍（4） 💬（3）<div>能在gitee 上也放一份吗？github现在已经没那么友好了
</div>2022-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/e6/c67f12bd.jpg" width="30px"><span>左耳朵东</span> 👍（4） 💬（3）<div>server&#47;server.go 文件中 select 那里，第二个 case 的意思是定时 1 秒后就会触发，从而执行后面的 return，为什么服务没有终止一直在运行呢？麻烦老师解答一下</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/3f/2ce014e7.jpg" width="30px"><span>snow</span> 👍（4） 💬（1）<div>我看这里使用了mux包，我只用过gin包，请问这两个老师更喜欢哪个？以及这里选择mux的原因。</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/22/86/3fe860c9.jpg" width="30px"><span>邰洋一</span> 👍（4） 💬（2）<div>老师，采用Restful规范，更新一条图书条目  http方法采用PUT，当然post也是可以的，put book&#47;id，是我太限定自己了吗？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6d/cf/ec335526.jpg" width="30px"><span>jc9090kkk</span> 👍（4） 💬（5）<div>这节课的项目内容理解起来不困难，但是对于实际的生产项目而言，尤其是对第三方的中间件有依赖的前提下，大都会针对的将配置单独存储为配置文件以方便维护，我想问下老师go项目针对配置文件有什么最佳实践方式吗? 我自己本地写了一个小项目，用的是以下方式来配置MySQL连接的，我总觉得不太优雅，大多项目会根据开发环境的不同选取不同的配置文件作为配置项加载，但是如果通过硬编码的方式添加进去会让项目变得很奇怪。。。

package config

&#47;&#47; GetDBConfig 数据库配置
func GetDBConfig() map[string]string {
	&#47;&#47; 初始化数据库配置map
	dbConfig := make(map[string]string)

	dbConfig[&quot;DB_HOST&quot;] = &quot;127.0.0.1&quot;
	dbConfig[&quot;DB_PORT&quot;] = &quot;3306&quot;
	dbConfig[&quot;DB_NAME&quot;] = &quot;test&quot;
	dbConfig[&quot;DB_USER&quot;] = &quot;root&quot;
	dbConfig[&quot;DB_PWD&quot;] = &quot;123456&quot;
	dbConfig[&quot;DB_CHARSET&quot;] = &quot;utf8&quot;

	&#47;&#47; 连接池最大连接数
	dbConfig[&quot;DB_MAX_OPEN_CONNECTS&quot;] = &quot;20&quot;
	&#47;&#47; 连接池最大空闲数
	dbConfig[&quot;DB_MAX_IDLE_CONNECTS&quot;] = &quot;10&quot;
	&#47;&#47; 连接池链接最长生命周期
	dbConfig[&quot;DB_MAX_LIFETIME_CONNECTS&quot;] = &quot;7200&quot;

	return dbConfig
}</div>2021-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e9/7b/4e0ede2a.jpg" width="30px"><span>莫名四下里</span> 👍（3） 💬（3）<div>Tony Bai 老师
$ go build bookstore&#47;cmd&#47;bookstore&#47;        
package bookstore&#47;cmd&#47;bookstore is not in GOROOT (&#47;usr&#47;local&#47;go&#47;src&#47;bookstore&#47;cmd&#47;bookstore)
无法构建   

配置 GOROOT=&quot;&#47;usr&#47;local&#47;go&quot;
报错  &#47;usr&#47;local&#47;go&#47;src&#47;bookstore&#47;cmd&#47;bookstore</div>2021-11-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIqhXd8JapYK3q6EQzSC6brm7EPqwEe2vCKjOO0FibzAgc1svqtAvVe6HMN8oUiaXZTFtxWJuM36nlA/132" width="30px"><span>xsgzh</span> 👍（3） 💬（3）<div>老师请教个文件
store&#47;memstore.go文件中第29 - 30行，直接赋值不可以么，ms.books[book.id] = book?
	nBook := *book
	ms.books[book.Id] = &amp;nBook
</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/e9/dc/cc05ebc7.jpg" width="30px"><span>小明</span> 👍（2） 💬（1）<div>看了两遍代码，能跑起来，但是只吃透了百分之三十，好着急啊  memstore.go   没看懂</div>2022-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/f1/ce10759d.jpg" width="30px"><span>wei 丶</span> 👍（2） 💬（2）<div>老师这一行代码使用time.after如果err发生了不会产生内存泄漏了? https:&#47;&#47;github.com&#47;bigwhite&#47;publication&#47;blob&#47;master&#47;column&#47;timegeek&#47;go-first-course&#47;09&#47;bookstore&#47;server&#47;server.go#L49</div>2022-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/42/3f/cb0d8a8d.jpg" width="30px"><span>Geek_zkg</span> 👍（2） 💬（1）<div>我是mac环境，按照老师上面的步骤走下来，在go build bookstore&#47;cmd&#47;bookstore的时候
报错package bookstore&#47;cmd&#47;bookstore is not in GOROOT (&#47;usr&#47;local&#47;go&#47;src&#47;bookstore&#47;cmd&#47;bookstore)
我已经设置了GO111MODULE=&quot;on&quot;
用goland开发的
想请老师帮忙解决一下</div>2022-05-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erD8CwHKGGIia1HwRBxy5GxMLTfGGzOeLjrmZ6ich9Ng7bbPia89iaSibbldnV4uiaKNXFcO2vQ3ztibCrDw/132" width="30px"><span>Williamleelol</span> 👍（2） 💬（2）<div>你好老师，
Get(string) (Book, error) &#47;&#47; 获取某图书信息 
GetAll() ([]Book, error) &#47;&#47; 获取所有图书信息
这两个方法的返回值为什么不是*Book呢？查询出来的结果应该是Book的实例了，返回值类型是Book会发生Copy么？</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/38/5c/c6a4e7f0.jpg" width="30px"><span>宝宝</span> 👍（2） 💬（1）<div>main.go方法的23-27行已经有捕获err退出了，为什么main.go的34-26行还要再监听一遍呢？</div>2022-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/14/57cb7926.jpg" width="30px"><span>ShawnWu</span> 👍（2） 💬（1）<div>providersMu.RLock()
我的goland里面报错啊，没有这个方法呢</div>2022-03-23</li><br/><li><img src="" width="30px"><span>601073891</span> 👍（2） 💬（2）<div>大大你好，这次遇到这样一个问题：
    这次的代码在linux下能成功的运行，但是在window下虽然能成功构建出可执行文件，也能成功执行，
D:\Goproject\src\entity\class\bookstore\cmd\bookstore&gt;bookstore.exe
2022&#47;03&#47;17 23:10:49 web server start ok
但在本机通过curl 访问时却有这样一个报错：
C:\Users\user&gt;curl -X POST -H &quot;Content-Type:application&#47;json&quot; -d &#39;{&quot;id&quot;: &quot;978-7-111-55842-2&quot;, &quot;name&quot;: &quot;The Go Programming Language&quot;, &quot;authors&quot;:[&quot;Alan A.A.Donovan&quot;, &quot;Brian W. Kergnighan&quot;],&quot;press&quot;: &quot;Pearson Education&quot;}&#39; 192.168.1.7:8080&#47;book
curl: (6) Could not resolve host: 978-7-111-55842-2,
curl: (3) URL using bad&#47;illegal format or missing URL
curl: (3) URL using bad&#47;illegal format or missing URL
curl: (3) bad range in URL position 10:
authors:[Alan A.A.Donovan,

不同系统下的go版本都是1.17，全部默认使用go module，我百度了一下，有说是URL格式的问题，但没有很对应，看了评论您也在windows上能成功执行，所以有这个疑问，您知道这会是怎么回事吗？
</div>2022-03-17</li><br/><li><img src="" width="30px"><span>Geek_73c432</span> 👍（1） 💬（1）<div>net&#47;http 包有一个叫 Server 的结构体，*Server 类型的方法 Shutdown 方法的最后部分我看懂了

timer := time.NewTimer(nextPollInterval())
defer timer.Stop()
for {
  if srv.closeIdleConns() {
    return lnerr
  }
  select {
  case &lt;-ctx.Done():
    return ctx.Err()
  case &lt;-timer.C:
    timer.Reset(nextPollInterval())
  }
}

但是官网的例子（https:&#47;&#47;pkg.go.dev&#47;context@go1.20.4#WithTimeout）我还是没看懂

const shortDuration = time.Second * 1

func slowOperationWithTimeout(ctx context.Context) {
	ctx, cancel := context.WithTimeout(ctx, shortDuration)
	defer cancel()
	timer := time.NewTimer(time.Second * 5)
	defer timer.Stop()
	select {
	case &lt;-timer.C:
		fmt.Println(&quot;timeout&quot;)
	case &lt;-ctx.Done():
		fmt.Println(ctx.Err())
	}
}

func main() {
	slowOperationWithTimeout(context.Background())
}

老师能否说一下 context.WithTimeout 的用法和使用场景？</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7b/03/03583011.jpg" width="30px"><span>天天有吃的</span> 👍（1） 💬（1）<div>这门课除了这个项目，后面还有其余的项目吗？gin会不会讲一下？</div>2023-04-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/6d/a4ff33bb.jpg" width="30px"><span>Lee</span> 👍（1） 💬（2）<div>package bootstore&#47;internal&#47;store is not in GOROOT (&#47;usr&#47;local&#47;go&#47;src&#47;bootstore&#47;internal&#47;store)

已经是GO111MODULE=&quot;on&quot; 但是还提示这个错误
</div>2023-03-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/32/45/b2/24dee83c.jpg" width="30px"><span>Ppppppp</span> 👍（1） 💬（1）<div>这篇读了好几天，有两个问题。
1. 对于读写锁的选型，这一块儿没怎么接触过，有什么讲究吗？
2. 基于1，如果有讲究，能提供一些学习方向吗？比如说对于不同的模式，以及用法。
</div>2023-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/0b/c8/15f055d3.jpg" width="30px"><span>图灵机</span> 👍（1） 💬（1）<div>要素太多， 脑子炸了....</div>2023-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/0a/23/c26f4e50.jpg" width="30px"><span>Sunrise</span> 👍（1） 💬（1）<div>还有一点不太明白，望老师解答，
server.go 中 
case &lt;-time.After(time.Second):
return errChan, nil
这块的作用是啥
</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/0a/23/c26f4e50.jpg" width="30px"><span>Sunrise</span> 👍（1） 💬（1）<div>memstore Create 方法中：
 nBook := *book
ms.books[book.Id] = &amp;nBook
为啥要这样赋值，直接 ms.books[book.Id] = book 不可以吗</div>2022-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a1/6d/a4ff33bb.jpg" width="30px"><span>Lee</span> 👍（1） 💬（2）<div>package bookstore&#47;cmd&#47;bookstore is not in GOROOT (&#47;usr&#47;local&#47;go&#47;src&#47;bookstore&#47;cmd&#47;bookstore) </div>2022-10-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2d/7d/9d/ced762c5.jpg" width="30px"><span>Beng吓咔啦咔</span> 👍（1） 💬（1）<div>Tony Bai 老师，能讲下如何调试go工程代码吗？我用vscode一直不能调试，照网上的办法设置了也没能行，不晓得具体问题出在哪</div>2022-10-13</li><br/>
</ul>