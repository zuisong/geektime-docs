你好，我是郑建勋。

这节课，我们来学习分析Go程序的利器：pprof和trace。

## pprof及其使用方法

先来看pprof。pprof用于对指标或特征的分析（Profiling）。借助pprof，我们能够定位程序中的错误（内存泄漏、race 冲突、协程泄漏），也能对程序进行优化（例如 CPU 利用率不足等问题）。

Go 语言运行时的指标并不对外暴露，而是由标准库 net/http/pprof 和 runtime/pprof 来与外界交互。其中， runtime/pprof需要嵌入到代码进行调用，而net/http/pprof 提供了一种通过 HTTP 获取样本特征数据的便利方式。而要对特征文件进行分析，就得依赖谷歌推出的分析工具pprof了。这个工具在 Go 安装时就存在，可以用go tool pprof执行。

要用 pprof 进行特征分析需要执行两个步骤：**收集样本和分析样本。**

收集样本有两种方式。一种是引用 net/http/pprof，并在程序中开启 HTTP 服务器，net/http/pprof 会在初始化 init 函数时注册路由。

```plain
import _ "net/http/pprof"
if err := http.ListenAndServe(":6060", nil); err != nil {
	log.Fatal(err)
}
```
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/7f/d3/b5896293.jpg" width="30px"><span>Realm</span> 👍（1） 💬（0）<div>思考题：
单次执行占用很高的cpu和内存的函数，不一定是瓶颈。

调用非常频繁的函数，并且每次需要分配内存或者造成软中断，也可能形成瓶颈。</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/79/2b/365055c3.jpg" width="30px"><span>公共账号</span> 👍（0） 💬（0）<div>pprof  top后为什么会有负数出现</div>2024-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3e/9a/c37a43f0.jpg" width="30px"><span>加油</span> 👍（0） 💬（0）<div>火焰图 : 框越长、颜色越深，代表当前函数占用 CPU 的时间越久。
——————
这句话有问题哈，框越长，代表当前函数占用CPU的时间越久。但是和颜色无关，火焰图的颜色是随机的暖色调。</div>2023-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/00/618b20da.jpg" width="30px"><span>徐海浪</span> 👍（0） 💬（0）<div>内存分配多和CPU耗时长，只能说明这个函数占用的资源多，还需要结合执行次数分析，计算平均每次执行时间和内存分配的情况。</div>2023-01-17</li><br/>
</ul>