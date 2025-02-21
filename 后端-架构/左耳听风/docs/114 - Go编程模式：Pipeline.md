你好，我是陈皓，网名左耳朵耗子。

这节课，我着重介绍一下Go编程中的Pipeline模式。对于Pipeline，用过Unix/Linux命令行的人都不会陌生，**它是一种把各种命令拼接起来完成一个更强功能的技术方法**。

现在的流式处理、函数式编程、应用网关对微服务进行简单的API编排，其实都是受Pipeline这种技术方式的影响。Pipeline可以很容易地把代码按单一职责的原则拆分成多个高内聚低耦合的小模块，然后轻松地把它们拼装起来，去完成比较复杂的功能。

## HTTP 处理

这种Pipeline的模式，我在[上节课](https://time.geekbang.org/column/article/332608)中有过一个示例，我们再复习一下。

上节课，我们有很多 `WithServerHead()` 、`WithBasicAuth()` 、`WithDebugLog()`这样的小功能代码，在需要实现某个HTTP API 的时候，我们就可以很轻松地把它们组织起来。

原来的代码是下面这个样子：

```
http.HandleFunc("/v1/hello", WithServerHeader(WithAuthCookie(hello)))
http.HandleFunc("/v2/hello", WithServerHeader(WithBasicAuth(hello)))
http.HandleFunc("/v3/hello", WithServerHeader(WithBasicAuth(WithDebugLog(hello))))
```

通过一个代理函数：

```
type HttpHandlerDecorator func(http.HandlerFunc) http.HandlerFunc
func Handler(h http.HandlerFunc, decors ...HttpHandlerDecorator) http.HandlerFunc {
    for i := range decors {
        d := decors[len(decors)-1-i] // iterate in reverse
        h = d(h)
    }
    return h
}
```

我们就可以移除不断的嵌套，像下面这样使用了：

```
http.HandleFunc("/v4/hello", Handler(hello,
                WithServerHeader, WithBasicAuth, WithDebugLog))
```

## Channel 管理

当然，如果你要写出一个[泛型的Pipeline框架](https://coolshell.cn/articles/17929.html#%E6%B3%9B%E5%9E%8B%E7%9A%84%E4%BF%AE%E9%A5%B0%E5%99%A8)并不容易，可以使用[Go Generation](https://coolshell.cn/articles/21179.html)实现，但是，我们别忘了，Go语言最具特色的 Go Routine 和 Channel 这两个神器完全可以用来构造这种编程。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/hNVMG2tFVzXzCYibhvOZ8wVBHicg5nicu0FSQdx0ItFZIoLSMC7AAbNL0fbPOuiaLqTsOkKe6BDKl6lcIXYH5vuRHg/132" width="30px"><span>Geek_Fantasy</span> 👍（5） 💬（0）<div>判断一个数是否是质数的方法可以优化一下。只需要枚举到value的平方根就可以，可以把复杂度从O(n)降到O(sqrt(n))。</div>2021-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/36/2e/376a3551.jpg" width="30px"><span>ano</span> 👍（0） 💬（0）<div>merge 中的  wg.Wait() 为什么必须要放到一个单独的 goroutine 中呢？</div>2022-09-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLAHCRt6dBUDTFX4EotyV5NDbYiaUXH109SOdRprLky1PUc9jm2K7QvoCpkZuCyqMCNSogUpdFzMJw/132" width="30px"><span>Geek_ce6971</span> 👍（0） 💬（0）<div>pipeline 最后返回 &lt;- chan  类型，就像 java stream编程的输出流</div>2022-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（0） 💬（0）<div>Pipeline使用场景还是很多的，在做任务发布的时候会经常用到</div>2021-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/f1/12/7dac30d6.jpg" width="30px"><span>你为啥那么牛</span> 👍（0） 💬（1）<div>没看明白 你是怎么分组的</div>2021-08-16</li><br/>
</ul>