你好，我是陈皓，网名左耳朵耗子。

这节课，我们来讨论一下Functional Options这个编程模式。这是一个函数式编程的应用案例，编程技巧也很好，是目前Go语言中最流行的一种编程模式。

但是，在正式讨论这个模式之前，我们先来看看要解决什么样的问题。

## 配置选项问题

在编程中，我们经常需要对一个对象（或是业务实体）进行相关的配置。比如下面这个业务实体（注意，这只是一个示例）：

```
type Server struct {
    Addr     string
    Port     int
    Protocol string
    Timeout  time.Duration
    MaxConns int
    TLS      *tls.Config
}
```

在这个 `Server` 对象中，我们可以看到：

- 要有侦听的IP地址 `Addr` 和端口号 `Port` ，这两个配置选项是必填的（当然，IP地址和端口号都可以有默认值，不过这里我们用于举例，所以是没有默认值，而且不能为空，需要是必填的）。
- 然后，还有协议 `Protocol` 、 `Timeout` 和`MaxConns` 字段，这几个字段是不能为空的，但是有默认值的，比如，协议是TCP，超时`30`秒 和 最大链接数`1024`个。
- 还有一个 `TLS` ，这个是安全链接，需要配置相关的证书和私钥。这个是可以为空的。

所以，针对这样的配置，我们需要有多种不同的创建不同配置 `Server` 的函数签名，如下所示：

```
func NewDefaultServer(addr string, port int) (*Server, error) {
  return &Server{addr, port, "tcp", 30 * time.Second, 100, nil}, nil
}

func NewTLSServer(addr string, port int, tls *tls.Config) (*Server, error) {
  return &Server{addr, port, "tcp", 30 * time.Second, 100, tls}, nil
}

func NewServerWithTimeout(addr string, port int, timeout time.Duration) (*Server, error) {
  return &Server{addr, port, "tcp", timeout, 100, nil}, nil
}

func NewTLSServerWithMaxConnAndTimeout(addr string, port int, maxconns int, timeout time.Duration, tls *tls.Config) (*Server, error) {
  return &Server{addr, port, "tcp", 30 * time.Second, maxconns, tls}, nil
}
```

因为Go语言不支持重载函数，所以，你得用不同的函数名来应对不同的配置选项。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/18/cf/0d/a173e2b8.jpg" width="30px"><span>汪辉</span> 👍（9） 💬（0）<div>之前看到mq的初始化可选配置的时候有用到Functional Options这个模式，没想到在这里找到源头了。</div>2021-01-19</li><br/><li><img src="" width="30px"><span>Geek_a754be</span> 👍（7） 💬（1）<div>之前在公司自研的微服务框架里面看到大规模使用，原来有个学名叫Functional Options</div>2021-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c1/57/27de274f.jpg" width="30px"><span>萧</span> 👍（3） 💬（0）<div>太强了，受益匪浅</div>2021-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/a7/0f/08e6d763.jpg" width="30px"><span>后青春期的Keats</span> 👍（0） 💬（0）<div>雅，太雅了
必要参数放在入参列表，非必要参数以函数式编程可变参的形式传入。</div>2024-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/84/db/bbee2b27.jpg" width="30px"><span>紫陌桑田</span> 👍（0） 💬（0）<div>各种初始化对象时用的特别多，相比于 builder 模式，省了不少代码，而且更为优雅</div>2024-07-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/I38GzuHkWp6ViaevIesgGXccBmcSuvldhsqCicicZrJUWewmibKFuNGicyIKZAPdAH9HfOpZGmke9s8TnjXzp3mNDlQ/132" width="30px"><span>Geek_sevn</span> 👍（0） 💬（0）<div>如沐春风</div>2023-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d4/5e/b8bfa75d.jpg" width="30px"><span>辰星</span> 👍（0） 💬（0）<div>太强了</div>2022-12-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/4d/81c44f45.jpg" width="30px"><span>拉欧</span> 👍（0） 💬（0）<div>option 意味选项，本身就有函数的意思</div>2022-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/d9/02/c4e2d7e8.jpg" width="30px"><span>Geek_Huahui</span> 👍（0） 💬（0）<div>真的牛逼</div>2022-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/99/33/1981b0cc.jpg" width="30px"><span>今年也没有猫</span> 👍（0） 💬（0）<div>简单理解  就是一种闭包的组织形式。</div>2022-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/b1/81/13f23d1e.jpg" width="30px"><span>方勇(gopher)</span> 👍（0） 💬（0）<div>确实很多中间件的传参都这么设计，有时候可能要考虑，函数放在client端，还是server端</div>2021-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/a6/9f/3c60fffd.jpg" width="30px"><span>青阳</span> 👍（0） 💬（0）<div>和函数科里化是一回事吗</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/51/88/232fe847.jpg" width="30px"><span>图个啥呢</span> 👍（0） 💬（0）<div>厉害了！</div>2021-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cd/77/b2ab5d44.jpg" width="30px"><span>👻 小二</span> 👍（0） 💬（0）<div>这种接口也很友好， 就是苦了作者

```go
package main

import (
	&quot;crypto&#47;tls&quot;
	&quot;time&quot;
)

type Option struct {
	Timeout *time.Duration
	TLS     *tls.Config
}

func (option *Option) SetTimeOut(timeout time.Duration) *Option {
	option.Timeout = &amp;timeout
	return option
}

func (option *Option) SetTLS(tls *tls.Config) *Option {
	option.TLS = tls
	return option
}

func MergeOptions(options ...*Option) *Option {

	&#47;&#47;把option合并起来
	return nil
}

type Server struct {
	Addr    string
	Port    int
	Timeout time.Duration
	TLS     *tls.Config
}

func NewOptions() *Option {
	return new(Option)
}
func NewServer(addr string, port int, options ...*Option) (*Server, error) {

	srv := Server{
		Addr:    addr,
		Port:    port,
		Timeout: 30 * time.Second,
		TLS:     nil,
	}

	op := MergeOptions(options...)

	if op.Timeout != nil {
		srv.Timeout = *op.Timeout
	}

	if op.TLS != nil {
		srv.TLS = op.TLS
	}

	&#47;&#47;...
	return &amp;srv, nil
}
func main() {
	_, _ = NewServer(&quot;127.0.0.1&quot;, 80)
	_, _ = NewServer(&quot;127.0.0.1&quot;, 80, NewOptions().SetTimeOut(100))
	_, _ = NewServer(&quot;127.0.0.1&quot;, 80, NewOptions().SetTimeOut(100).SetTLS(nil))
}

```</div>2021-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8d/ff/986ffb41.jpg" width="30px"><span>轻飘飘过</span> 👍（0） 💬（0）<div>对比js的...解构和函数式编程的compose?</div>2021-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/69/d9/343b7a5f.jpg" width="30px"><span>astrosta</span> 👍（0） 💬（0）<div>用了很久，才知道叫Functional Options</div>2021-04-24</li><br/><li><img src="" width="30px"><span>Geek_450b7e</span> 👍（0） 💬（0）<div>优秀，学到了</div>2021-04-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f6/12/19914d72.jpg" width="30px"><span>Eirture</span> 👍（0） 💬（0）<div>在 Kubernetes 源代码中学过这一招，原来是叫 Functional Options，有了名字更容易记住和传播 👍</div>2021-04-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/be/1f/57c88dd1.jpg" width="30px"><span>小丢👣</span> 👍（0） 💬（0）<div>豁然开朗，respect</div>2021-03-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7f/da/73778db7.jpg" width="30px"><span>侯鹏₁₈₆₁₄₀₉₂₄₁₉</span> 👍（0） 💬（0）<div>非常棒👍🏻</div>2021-02-08</li><br/>
</ul>