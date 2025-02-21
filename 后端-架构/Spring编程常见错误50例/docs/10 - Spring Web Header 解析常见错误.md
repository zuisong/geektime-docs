你好，我是傅健，这节课我们来聊聊 Spring Web 开发中 Header 相关的常见错误案例。

在上节课，我们梳理了 URL 相关错误。实际上，对于一个 HTTP 请求而言，URL 固然重要，但是为了便于用户使用，URL 的长度有限，所能携带的信息也因此受到了制约。

如果想提供更多的信息，Header 往往是不二之举。不言而喻，Header 是介于 URL 和 Body 之外的第二大重要组成，它提供了更多的信息以及围绕这些信息的相关能力，例如Content-Type指定了我们的请求或者响应的内容类型，便于我们去做解码。虽然 Spring 对于 Header 的解析，大体流程和 URL 相同，但是 Header 本身具有自己的特点。例如，Header 不像 URL 只能出现在请求中。所以，Header 处理相关的错误和 URL 又不尽相同。接下来我们看看具体的案例。

## 案例 1：接受 Header 使用错 Map 类型

在 Spring 中解析 Header 时，我们在多数场合中是直接按需解析的。例如，我们想使用一个名为myHeaderName的 Header，我们会书写代码如下：

```
@RequestMapping(path = "/hi", method = RequestMethod.GET)
public String hi(@RequestHeader("myHeaderName") String name){
   //省略 body 处理
};
```

定义一个参数，标记上@RequestHeader，指定要解析的 Header 名即可。但是假设我们需要解析的 Header 很多时，按照上面的方式很明显会使得参数越来越多。在这种情况下，我们一般都会使用 Map 去把所有的 Header 都接收到，然后直接对 Map 进行处理。于是我们可能会写出下面的代码：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/6b/e9/7620ae7e.jpg" width="30px"><span>雨落～紫竹</span> 👍（3） 💬（0）<div>这章所有问题都是不规范导致的</div>2022-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/ea/7d/37977a99.jpg" width="30px"><span>天天向上</span> 👍（0） 💬（0）<div>请教下什么情况下需要修改content type</div>2022-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/16/e0/7abad3cc.jpg" width="30px"><span>星期八</span> 👍（0） 💬（0）<div>案例3中“决定用哪一种 MediaType 返回” header有值，为什么会走到下面去选择MediaType#TEXT_PLAIN？</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6c/67/07bcc58f.jpg" width="30px"><span>虹炎</span> 👍（0） 💬（4）<div>案例2说：1. 存取 Map 的 Header 是没有忽略大小写的 然后给出了源码：
private void findNext() {
    next=null;
    for(; pos&lt; size; pos++ ) {
        next=headers.getName( pos ).toString();
        for( int j=0; j&lt;pos ; j++ ) {
            if( headers.getName( j ).equalsIgnoreCase( next )) {
                &#47;&#47; duplicate.
                next=null;
                break;
            }
        }
        if( next!=null ) {
            &#47;&#47; it&#39;s not a duplicate
            break;
        }
    }
    &#47;&#47; next time findNext is called it will try the
    &#47;&#47; next element
    pos++;
}
然后说：返回结果并没有针对 Header 的名称做任何大小写忽略或转化工作。没看懂。其他小伙伴看懂了吗？

这里说的返回结果指什么？ if( headers.getName( j ).equalsIgnoreCase( next ))  这行代码不是忽略了大小写了吗？

</div>2021-05-16</li><br/>
</ul>