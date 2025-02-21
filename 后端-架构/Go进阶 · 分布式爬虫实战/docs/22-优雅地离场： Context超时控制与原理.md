你好，我是郑建勋。

在Go语言的圈子里有一句名言：

> **Never start a goroutine without knowing how it will stop。**

意思是，如果你不知道协程如何退出，就不要使用它。

如果想要正确并优雅地退出协程，首先必须正确理解和使用 Context 标准库。Context是使用非常频繁的库，在实际的项目开发中，有大量第三方包的API（例如 Redis Client、MongoDB Client、标准库中涉及到网络调用的API）的第一个参数都是Context。

```plain
// net/http
func (r *Request) WithContext(ctx context.Context) *Request
// sql
func (db *DB) BeginTx(ctx context.Context, opts *TxOptions) (*Tx, error)
// net
func (d *Dialer) DialContext(ctx context.Context, network, address string) (Conn, error)
```

那么Context的作用是什么？应该如何去使用它？Context的最佳实践又是怎样的？让我们带着这些疑问开始这节课的学习。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJw1XoOvKHBmyvGpxyoWibq7FYj6blWe0cUKJCqUFPHF1jmkxdBe6icTVC0nTYYPIP2ggx3UodKsLibQ/132" width="30px"><span>Geek_7ba156</span> 👍（12） 💬（0）<div>老师课程后面会有websocket相关的爬虫设计吗？毕竟网站数据也不只是restfulapi，现在很多数据都是wss了。对于wss的控制，keepalive，我觉得也很需要了解，gorilla自带的keepalive不是特别好用，如果有比较好的项目也可推荐下</div>2022-11-29</li><br/>
</ul>