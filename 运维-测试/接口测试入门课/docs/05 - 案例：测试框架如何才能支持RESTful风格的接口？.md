你好，我是陈磊。

在前面的课程中，我们一起学习了如何把流程化的测试脚本，一步一步抽象成你自己的测试框架。无论你用的是什么编程语言，封装和抽象自己的测试框架都会让你的接口测试任务事半功倍。

我相信你在平时生活或工作中，一定会接触到各式各样的软件系统，而现在的软件系统和5年前相比，最大差别就在于结构不同。

在我读大学的时候，绝大部分系统还都是用一个Tomcat来搞定的；但现在的系统更加复杂，它们已经无法只用一个Web中间件独立对外提供服务，它们之间都也是通过相互调用来完成业务逻辑的，这里面既包含了服务端和服务端的调用，也包含了前端和服务端的调用，这就催生了RESTful风格的HTTP接口。

所以，这节课我就来和你讲讲，如何让你的测试框架完美支持RESTful风格的接口测试。这里我希望你能不断强化封装测试框架的三个流程，不断为自己的接口测试框架添砖加瓦。

不过，我不会将RESTful的规则一条一条念给你听，我想让你知道的重点是作为测试工程师，你要学会从测试工程师的角度观察RESTful接口，要学会怎么分析和验证这类接口，这也是今天我们今天这节课的主要内容。

## RESTful风格接口关我什么事？

看到这里，你是不是一脸困惑：**RESTful是一个接口的封装风格，和我们测试人员有什么关系呢？**
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1b/c2/00/5d59b46c.jpg" width="30px"><span>我</span> 👍（25） 💬（1）<div>万能螺丝刀柄比喻restful接口，家具拆装必须序列化和反序列化，很好理解。</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cd/cd/3b4aadf8.jpg" width="30px"><span>Leo</span> 👍（4） 💬（3）<div>老师，有没有推荐的测试平台，支持web方式展示测试用例，用例的执行是调用背后开发的代码，支持定义测试集，支持多个测试环境，生成测试报告，提供restful接口集成CI流水线等？</div>2020-02-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIuRNfbtL5Skq3m4JW9CZv3dyicUibPXbrS0mugoVbXDB0nicdbaQuxBicGxVPf5jIeOCbzYwiccInhV9w/132" width="30px"><span>AllWin</span> 👍（4） 💬（2）<div>银行业中有些单个接口就有几百个参数，这几百个参数也不是都有联系的，会按场景分成很多参数组合，请问这样的设计是什么风格，我不理解银行为什么会有这样高复杂度的接口设计</div>2020-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b0/30/1343b0c3.jpg" width="30px"><span>沛野</span> 👍（4） 💬（1）<div>RESTful 风格的 HTTP 接口是什么意思呀？ 还有什么其他的接口么？这个是按什么分类的呀</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/3d/58/377289a8.jpg" width="30px"><span>陈磊@Criss</span> 👍（4） 💬（1）<div>序列化是指把对象转换为字节序列的过程，而反序列化是指把字节序列恢复为对象的过程。</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/39/a4c2154b.jpg" width="30px"><span>小昭</span> 👍（0） 💬（1）<div>百度了一下RESTful风格HTTP协议接口的详细介绍，发现自己之前对HTTP协议的接口的认知就是RESTful风格的……

老师总能找到生活中的例子来讲一些晦涩的概念，厉害厉害</div>2021-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e9/34/83025564.jpg" width="30px"><span>-_-</span> 👍（0） 💬（2）<div>使用json格式的数据，post请求的参数要改为json=xxx吗，还是data=json格式的数据也可。
如果是用json=是要再写一个post方法吧</div>2020-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/2f/f4/2dede51a.jpg" width="30px"><span>小老鼠</span> 👍（0） 💬（1）<div>RestFul中的delete、put.…等用的就是http协议中的delete、put⋯方法吧？</div>2020-04-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/c3/6c/d24a23a7.jpg" width="30px"><span>彦鋆</span> 👍（0） 💬（1）<div>老师，rest风格的接口我们在设计测试用例和断言的时候预期返回要和接口返回的内容完全一样还是判断返回值中的某些重要的key-value一样就行了？</div>2020-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/95/bd/20ec9f4c.jpg" width="30px"><span>深瞳</span> 👍（0） 💬（1）<div>思路有了，但是需要填充的内容还需要大量的学习</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/96/d5/23fecf33.jpg" width="30px"><span>Hy</span> 👍（0） 💬（1）<div>最后delete函数的注解好像有问题，if params is not None，后面提示用Put方法，另外如果delete方法没参数请问为什么写成了res = requests.put(url)，请老师赐教</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/da/f1/bf74a792.jpg" width="30px"><span>Map</span> 👍（0） 💬（2）<div>老师这个框架源码有项目地址可以下载么
</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d1/d3/5dfc36c0.jpg" width="30px"><span>王德发</span> 👍（0） 💬（1）<div>老师，这个python的测试框架，怎么做的切换环境，比如说，我现在有三个环境测试、仿真、预发布，不同的环境数据库、redis等这些配置都不一样，如何在测试框架运行的时候能动态切换不同的配置文件呢？比如像java里，可以用maven的插件来做。</div>2020-02-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJJXlflPMj9Ct9ia5G8ia51YZpdAuvSokWZoJlXPpk0rkwVrRQ1LzZIlNMBqRaTibAH09JBIeEysDwLQ/132" width="30px"><span>Geek_f644f9</span> 👍（0） 💬（1）<div>复制代码段存在语法错误，不能识别is not
</div>2020-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/65/4e4e376e.jpg" width="30px"><span>Angela</span> 👍（0） 💬（1）<div>还比如 socket、udp TCP 接口与restful接口有啥区别</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/65/4e4e376e.jpg" width="30px"><span>Angela</span> 👍（0） 💬（1）<div>还是不太懂 restful Api 和http API的关系和区别 能再详述一下么</div>2020-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a4/6a/7e7bf408.jpg" width="30px"><span>张胜坡</span> 👍（0） 💬（1）<div>可以写一个测试的实例吗？参数是data或者json 格式，如何在测试框架中怎么兼容？</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c1/14/659c8ca2.jpg" width="30px"><span>7F</span> 👍（0） 💬（2）<div>这里的风格是指入参全部定义成json格式？然后不需要在代码中在去写入参了么？</div>2020-02-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4e/fe/838a5835.jpg" width="30px"><span>Watermelon</span> 👍（3） 💬（0）<div>还是不懂RESTful风格接口跟普通HTTP接口有什么区别。。。传输数据的话，普通接口也用json传啊</div>2021-01-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（2） 💬（1）<div>过，迭代抽象封装。</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4c/b5/fcede1a9.jpg" width="30px"><span>IT小村</span> 👍（1） 💬（0）<div>restful其实就是更好区分接口方法的用途</div>2022-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/dc/33/a68c6b26.jpg" width="30px"><span>捷后愚生</span> 👍（1） 💬（0）<div>RESTful 风格 HTTP 接口的产生
简单系统可以使用单体结构，用一个 Tomcat 来做中间件就可搞定。随着系统急剧扩大，已经无法只用一个 Web 中间件独立对外提供服务，它们之间都也是通过相互调用来完成业务逻辑的，这里面既包含了服务端和服务端的调用，也包含了前端和服务端的调用，这就催生了 RESTful 风格的 HTTP 接口。


RESTful 风格 HTTP 接口的特点
每一个接口只面向一种特定的资源，而不需要关心其他接口的处理方式，接口简单、轻便。
ESTful 风格接口同样是一种 HTTP 协议的接口，而主要是以 JSON 格式来进行数据交换，且不只会使用get、post方法，还会使用put、detele方法。


封装可以测试RESTful风格接口地测试框架
引入JSON库，拼凑参数已经无法满足需求，需要使用 JSON 字符串和代码对象实体的转换，也就是序列化和反序列化。
加入 Delete 和 Put 方法的支持。
</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/77/92/65f2b654.jpg" width="30px"><span>Chaos</span> 👍（0） 💬（0）<div>https:&#47;&#47;www.xinzhiweike.com&#47;wenda&#47;1630979493140646</div>2022-04-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/43/2e/2a5d0f3e.jpg" width="30px"><span>Past</span> 👍（0） 💬（0）<div>原文：商家把衣柜拆成各个零件、然后打包的这个过程就是“序列化”，在代码中，就是将一些程序对象转换成 JSON 等格式的字符串的过程。接下来，你用这些零件再重新组装成一个衣柜，这个过程就是“反序列化”，在代码中，就是 JSON 等格式的字符串转换成程序的对象的过程。

序列化和反序列化的例子挺有意思的，和Modrem调制解调器原理有点类似，调制(数字信号--&gt;模拟信号)和解调原理(模拟信号--&gt;数字信号)，同时也让我想起了老师一个搞笑的解释，把整条萝卜切割成小块处理，是处理调制的过程，那么解调原理是再把小块小块的萝卜组合成完整的萝卜，保持原特性。
</div>2020-03-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/etbNBmR5PEicra7jbaV9pRsCaibXZ3ichB6JicMOnYowP65W5QMKb8Zicud19jicmEGAGh8ylwDXoYM3SHVU6hf6dFpQ/132" width="30px"><span>roychris</span> 👍（0） 💬（0）<div>序列化和反序列化的具体例子后面有例子讲解吗？</div>2020-02-10</li><br/>
</ul>