你好，我是王昊天。

在上节课中，我们重点学习了sqlmap中一个非常重要的算法——页面相似度算法。相信你对页面相似度这个概念会有更加清晰的认知，不但知道它是什么含义，而且知道它是如何计算出来的。解决了这个大难点之后，我在上节课的结尾提出了一个空连接检测功能，有了它，sqlmap就可以大大提高执行效率。完成了检测，sqlmap就进入到实际的SQL注入测试阶段了。

在SQL注入测试阶段，系统首先会检测有哪些注入点，然后对这些注入点逐一发送合适的payload，检测注入是否成功。如果注入成功，那么系统会将注入点存储下来，最后对它们进行输出。

这节课，我们就来正式学习sqlmap的SQL注入测试过程。

## 注入点检测

在SQL正式注入测试之前，sqlmap会对每个目标的参数进行过滤。将那些非动态的，不存在注入可能的参数剔除掉，留下可能的注入点。这样sqlmap仅需要对这些可能的注入点进行正式的注入测试即可。

### 动态参数检测

我们首先来看sqlmap是如何检测动态参数的。这部分代码依旧在start函数中，紧接着空连接检测出现。

```python
# sqlmap首先对所有可用于注入测试的参数进行简单的优先级排序。
   parameters = list(conf.parameters.keys())
# 定义测试列表的顺序。（从后到前）
   orderList = (PLACE.CUSTOM_POST, PLACE.CUSTOM_HEADER, PLACE.URI, PLACE.POST, PLACE.GET)
# 对测试参数排好序之后，系统开始对参数进行过滤操作。
   proceed = True
   for place in parameters:
       skip = # ...
       if skip:
           continue
       if place not in conf.paramDict:
           continue
       paramDict = conf.paramDict[place]
       paramType = conf.method if conf.method not in (None, HTTPMETHOD.GET, HTTPMETHOD.POST) else place
# ...
       for parameter, value in paramDict.items():
           if not proceed:
               break
# 经过过滤，将该参数加入到测试过的参数中，防止重复测试。
           kb.testedParams.add(paramKey)
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/34/df/64e3d533.jpg" width="30px"><span>leslie</span> 👍（1） 💬（0）<div>应当会是在算法效率和资源使用方面，python被人诟病最多的就是资源消耗。</div>2022-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>秀</div>2023-03-15</li><br/>
</ul>