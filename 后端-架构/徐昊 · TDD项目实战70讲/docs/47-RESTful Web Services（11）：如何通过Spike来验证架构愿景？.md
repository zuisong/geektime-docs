你好，我是徐昊。今天我们继续使用TDD的方式实现RESTful Web Services。

## 回顾架构愿景与任务列表

目前，我们的任务列表是这样的：

- RuntimeDelegate
  
  - 为MediaType提供HeaderDelegate
  - 为CacheControl提供HeaderDelegate
  - 为Cookie提供HeaderDelegates
  - 为EntityTag提供HeaderDelegate
  - 为Link提供HeaderDelegate
  - 为NewCookie提供HeaderDelegate
  - 为Date提供HeaderDelegate
  - 提供OutboundResponseBuilder
- OutboundResponseBuilder
  
  - 可按照不同的Status生成Resposne
- OutboundResponse
- ResourceDispatcher
  
  - 将Resource Method的返回值包装为Response对象
- Providers
  
  - 可获取MessageBodyWriter
  - 可获取ExceptionMapper
- Runtimes
  
  - 可获取ResourceDispatcher
  - 可获取Providers
- MessageBodyWriter
- ExceptionMapper
  
  - 需要提供默认的ExceptionMapper
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/7a/56/29877cb9.jpg" width="30px"><span>临风</span> 👍（1） 💬（0）<div>我觉得RootResource下的每个method对应的path可以以每个&#39;&#47;&#39;为分隔，一个segment为一个node，按图的方式进行保存，match的时候就可以按图的方式进行遍历，查找出满足条件的RootResource和方法。</div>2022-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bd/6a/abe84a16.jpg" width="30px"><span>范特西</span> 👍（0） 💬（0）<div>进入项目三的学习后，你有什么有意思的收获吗？

总的来说就是当我们面对一个需求时，刚开始我们可以按照一个小需求的方式去开发，代码可以快速成型并且满足需求需要。但是问题又来了，可能刚开始我们只是考虑得少，以后这个需求可能会变得非常复杂，我们怎么可以在最开始就识别到这些点，并且充分考虑如何设计我们的抽象层而不是依赖于后面一次次“大规模”重构呢？

很期待后面老师的讲解！</div>2024-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7d/b6/abdebdeb.jpg" width="30px"><span>Michael</span> 👍（0） 💬（0）<div>老师能讲一下对于Context这种设计么？比如Spring的ApplicationContext, 我们什么情况下会想到可以抽象出一个Context对象？以及为什么是Context去做实例化而不是其他的去做实例化呢？这里面有些什么考量么？</div>2022-07-08</li><br/>
</ul>