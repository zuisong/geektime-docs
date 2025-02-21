你好，我是石川。

说到HTTP你可能并不陌生，但是你真的确定你对它有所了解吗？或者你可能会觉得了解它对前端开发没什么用。但实际上，对HTTP的理解可以帮助我们更好地制定前端应用层性能优化的策略。

所以今天，我们就来看看不同的HTTP版本。对于HTTP/1的不足之处，我们能做哪些优化；对于HTTP/2的优点，我们如何加以利用；对于HTTP/3，我们又可以有哪些期望。下面，我们就先从HTTP的前世今生开始说起吧。

## HTTP/1.0

HTTP最早的版本是1991年由万维网之父蒂姆·伯纳斯-李（Tim Berners-Lee）定义的，这个HTTP/0.9的版本起初只有[一页纸](https://www.w3.org/Protocols/HTTP/AsImplemented.html)一行字的描述。HTTP/0.9仅支持GET方法，仅允许客户端从服务器检索HTML文档，甚至都不支持任何其他文件格式或信息的上传。

之后的HTTP/1是从1992年开始草拟到1996年定版的，这个版本的协议就包含了更多的我们如今耳熟能详的元素和功能，比如我们常用的headers、errors、redirect都是在这个版本中出现了。但是它仍然有几个核心问题：一是没有办法让连接在不同请求间保持打开；二是没有对虚拟服务器的支持，也就是说在同一个IP上没有办法搭建多个网站；三是缺乏缓存的选项。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/a4nwicfbEpwqfm8En9iapFqGoOpVg0p0N4ZjIFAdWQMiaxT0JT9OpYrM5ud1OliaLAUhhiaHDjY8mxmNfSbgBNAAGTQ/132" width="30px"><span>sqnv_geek</span> 👍（0） 💬（1）<div>协议这方面是不是更需要网络基础硬件设备的支持？</div>2023-01-20</li><br/>
</ul>