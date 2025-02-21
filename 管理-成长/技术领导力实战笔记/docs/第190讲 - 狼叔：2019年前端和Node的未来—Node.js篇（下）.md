你好，我是阿里巴巴前端技术专家狼叔，今天是咱们大前端趋势系列的最后一篇文章，我将主要分享一些Node.js的新特性，以及我对大前端、Node.js未来的一点看法，但在开始之前，我想先聊一聊Serverless这个当下很火，同时未来可期的技术。

### Serverless

简单地说，Serverless = FAAS + BaaS ，服务如果被认为是Serverless的，它必须无需显式地配置，并能自动调整扩缩容以及根据使用情况进行计费。云function是当今无Serverless计算中的通用元素，并引领着云的简化和通用编程模型发展的方向。2015年亚马逊推出了一项名为AWS Lambda服务的新选项。Node.js领域TJ大神去创业，开发了[http://apex.run](http://apex.run/)。目前，各大厂都在Serverless上发力，比如Google、AWS、微软，阿里云等。

![](https://static001.geekbang.org/resource/image/4b/72/4bb32cc24f1581b7158859b4f5906e72.png?wh=1606%2A334)

这里不得不提一下Eventloop，Node.js成也Eventloop，败也Eventloop，本身Eventloop是黑盒，开发将什么样的代码放进去你是很难全部覆盖的，偶尔会出现Eventloop阻塞的情况，排查起来极为痛苦。

而利用Serverless，可以有效的防止Eventloop阻塞。比如加密，加密是常见场景，但本身的执行效率非常慢。如果加解密和你的其他任务放到一起，很容易导致Eventloop阻塞。
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/56/ee/3b774739.jpg" width="30px"><span>Fei</span> 👍（1） 💬（0）<div>Hey 狼叔，lowjs的link有点问题，有时间可以fix下。</div>2019-08-28</li><br/>
</ul>