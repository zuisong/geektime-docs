你好，我是微扰君。

不知不觉，已经到工程实战篇的最后一讲了，在这个章节中，我们一起学习了很多工程中常用的算法，如果你从事后端开发，应该或多或少有些接触，比如在Redis、Kafka、ZooKeeper等常用中间件里就经常出现，理解它们的核心思想，能给你的工作带来很大的帮助。

今天，我们最后来聊一聊大部分Web开发工程师都会用到的后端Web框架中的算法。

### 路由匹配

Web框架的作用，我们都知道，主要就是封装Web服务，整合网络相关的通用逻辑，一般来说也就是帮助HTTP服务建立网络连接、解析HTTP头、错误恢复等等；另外，大部分框架可能也会提供一些拦截器或者middleware，帮助我们处理一些每个请求可能都需要进行的操作，比如鉴权、获取用户信息。

但是所有Web框架，无论设计得多么不同，必不可少的能力就是路由匹配。

因为我们的Web服务通常会对外暴露许多不同的API，而区分这些API的标识，主要就是用户请求 API的URL。所以，**一个好用的Web框架，要能尽可能快地解析请求URL并映射到不同API 的处理逻辑，也就是我们常说的“路由匹配”**。

以Golang中常用的Web框架Gin为例，如果用户想注册一套遵循RESTful风格的接口，只需要像这样，写一下注册每个路由所对应的handler方法就完成了：
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/bb/abb7bfe3.jpg" width="30px"><span>csyangchsh</span> 👍（1） 💬（1）<div>radix trie</div>2022-03-13</li><br/><li><img src="" width="30px"><span>Paul Shan</span> 👍（0） 💬（1）<div>前缀树的空间浪费可以用hashmap来优化，key对应的字母，value对应下一层的指针。这种方案在节点数量多的时候反而要浪费更大的空间，因为hashmap需要一定的空余空间，而且key之间的顺序信息也丢失了。</div>2022-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（1） 💬（1）<div>请教老师一个问题：
Q1：如果是中文，字符集怎么处理？
文中例子是英文，字符集确定而且很小。但如果是中文，字符集太大了，怎么处理？</div>2022-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/98/ae/532f7282.jpg" width="30px"><span>nbsp;</span> 👍（0） 💬（0）<div>前缀树里字母是路径不是节点</div>2022-05-16</li><br/>
</ul>