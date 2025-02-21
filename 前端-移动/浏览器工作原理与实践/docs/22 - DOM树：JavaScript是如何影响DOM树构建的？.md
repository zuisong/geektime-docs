在[上一篇文章](https://time.geekbang.org/column/article/138844)中，我们通过开发者工具中的网络面板，介绍了网络请求过程的几种**性能指标**以及对页面加载的影响。

而在渲染流水线中，后面的步骤都直接或者间接地依赖于DOM结构，所以本文我们就继续沿着网络数据流路径来**介绍DOM树是怎么生成的**。然后再基于DOM树的解析流程介绍两块内容：第一个是在解析过程中遇到JavaScript脚本，DOM解析器是如何处理的？第二个是DOM解析器是如何处理跨站点资源的？

## 什么是DOM

从网络传给渲染引擎的HTML文件字节流是无法直接被渲染引擎理解的，所以要将其转化为渲染引擎能够理解的内部结构，这个结构就是DOM。DOM提供了对HTML文档结构化的表述。在渲染引擎中，DOM有三个层面的作用。

- 从页面的视角来看，DOM是生成页面的基础数据结构。
- 从JavaScript脚本视角来看，DOM提供给JavaScript脚本操作的接口，通过这套接口，JavaScript可以对DOM结构进行访问，从而改变文档的结构、样式和内容。
- 从安全视角来看，DOM是一道安全防护线，一些不安全的内容在DOM解析阶段就被拒之门外了。

简言之，DOM是表述HTML的内部数据结构，它会将Web页面和JavaScript脚本连接起来，并过滤一些不安全的内容。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/02/81/489e1cd4.jpg" width="30px"><span>忘忧草的约定</span> 👍（11） 💬（4）<div>老师请问一下：主线程在parseHtml时，是不是没办法执行执行paint等操作、那这时候页面又是如何绘制出来的呀？</div>2019-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d6/80/07de6693.jpg" width="30px"><span>叫我大胖就好了</span> 👍（8） 💬（1）<div>我看MDN写的是defer在DOMContentLoaded 前执行</div>2019-09-26</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（2） 💬（1）<div>您好，网络进程接收到响应头之后，会根据请求头中的 content-type 字段来判断文件的类型，比如 content-type 的值是“text&#47;html”！  
这个地方应该是根据响应头判断文件类型吧？</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/94/0b22b6a2.jpg" width="30px"><span>Luke</span> 👍（127） 💬（27）<div>CSS不阻塞dom的生成。
CSS不阻塞js的加载，但是会阻塞js的执行。
js会阻塞dom的生成，也就是会阻塞页面的渲染，那么css也有可能会阻塞页面的渲染。
如果把CSS放在文档的最后面加载执行，CSS不会阻塞DOM的生成，也不会阻塞JS，但是浏览器在解析完DOM后，要花费额外时间来解析CSS，而不是在解析DOM的时候，并行解析CSS。
并且浏览器会先渲染出一个没有样式的页面，等CSS加载完后会再渲染成一个有样式的页面，页面会出现明显的闪动的现象。
所以应该把CSS放在文档的头部，尽可能的提前加载CSS；把JS放在文档的尾部，这样JS也不会阻塞页面的渲染。CSS会和JS并行解析，CSS解析也尽可能的不去阻塞JS的执行，从而使页面尽快的渲染完成。
</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（53） 💬（8）<div>会显示time.geekbang和test，JavaScript代码执行的时候第二个div还没有生成DOM节点，所以是获取不到div2的，页面会报错Uncaught TypeError: Cannot set property &#39;innerText&#39; of undefined。

另外复习了下async和defer：

async：脚本并行加载，加载完成之后立即执行，执行时机不确定，仍有可能阻塞HTML解析，执行时机在load事件派发之前

defer：脚本并行加载，等待HTML解析完成之后，按照加载顺序执行脚本，执行时机在DOMContentLoaded事件派发之前</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/07/4d/408daf20.jpg" width="30px"><span>Geek_93f234</span> 👍（20） 💬（10）<div>网络进程加载了多少数据，HTML 解析器便解析多少数据。这里有一个问题，如果是边加载边解析，那么一个标签还在网络传输过程中，浏览器还没有接受到script这个词段，那么浏览器又是怎么预加载的呢？</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/28/a9/99b74f3e.jpg" width="30px"><span>欣欣向荣的万七七</span> 👍（6） 💬（0）<div>讲得太赞了！一直以来我都只记着加载表现结果（大部分文章都并不知道细节原因，而只能从做测试得到的结果来推测）。而老师的视角则可以从运行时进行讲解 这种知识是很难得的呀～</div>2019-10-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（6） 💬（1）<div>开始看文章的时候就在想如果js获取的dom还没有解析出来，会如何处理，结果思考题就是这个。

会两行显示，一行是time.geekbang 另外一行是test。原因是script脚本执行的时候获取想不到第二个div，所以不会对后来的div有影响。

今日总结：
1. 首先介绍了什么是DOM（表述渲染引擎内部数据结构，它将Web页面和JavaScript脚本连接起来，并过滤不安全内容）、DOM树如何生成（网络进程和渲染进程建立一个流式管道，HTML解析器直接解析，不需要等待text&#47;html类型的接口 接受完毕再进行解析），第一步：通过分词器将字节流转换为Token；第二步：将Token解析为DOM节点；第三步：将DOM节点添加到DOM树中。
2. JavaScript是如何影响DOM生成的？暂停html解析，下载解析执行完毕js之后再进行html解析（如果这期间使用到了cssDom，需要等待相应css过程）。预解析线程的优化（提前加载相应js css文件）
3. 渲染引擎还有一个安全检查模块XSSAuditor用来检测词法安全的</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（4） 💬（3）<div>老师，CSSOM的生成依赖于DOM吗？</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/1c/e160955d.jpg" width="30px"><span>sky</span> 👍（3） 💬（2）<div>有个问题，网络传输过程中，传输包有可能是乱序的，如果index.html没有加载完，怎么保证传输回来的index.html字节流不是乱序的呢。这样边加载边解析不会有问题吗？</div>2021-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ee/e2/23e44221.jpg" width="30px"><span>余熙</span> 👍（3） 💬（0）<div>这是需求本身要求的: DOM 生成依赖 JS加载和执行，JS 依赖 CSS加载和解析。

DOM 生成等待 JS: 
解析到&lt;script&gt;标签时，渲染引擎判断这是一段脚本，此时 HTML 解析器就会暂停 DOM 的解析，因为接下来的 JavaScript 可能要修改当前已经生成的 DOM 结构。

JS 等待 CSS加载和解析：
JavaScript 引擎在解析 JavaScript 之前，是不知道 JavaScript 是否操纵了 CSSOM 的，所以渲染引擎在遇到 JavaScript 脚本时，不管该脚本是否操纵了 CSSOM，都会执行 CSS 文件下载，解析操作，再执行 JavaScript 脚本。</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/13/84d35588.jpg" width="30px"><span>张萌</span> 👍（3） 💬（1）<div>一个很长的 html 文档，浏览器会分段进行渲染，一般是按什么规则分段的？</div>2020-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（3） 💬（0）<div>第一行是time.geekbang，第二行不会变，仍是test。原因就是浏览器是边加载边解析html的，而且遇到js会停止dom的解析执行js，js执行完毕后再接着解析dom。上面的代码，js执行时第2个div并未被解析为dom，所以js中获取不到，js会抛出错误TypeError，但js抛出错误并未影响html的继续解析。所以，第2个div保持原来的状态被解析出来。</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1f/04/1cddf65b.jpg" width="30px"><span>不二</span> 👍（2） 💬（6）<div>老师，思考题有个疑问：首先html解析器，解析到完&lt;div&gt;1&lt;&#47;div&gt;，此时dom树里是没有&lt;div&gt;test&lt;&#47;div&gt;的，然后开始i 解析script标签，在解析过程中，发现&lt;div&gt;test&lt;&#47;div&gt;找不到，所以此时js会报错，既然此时js报错了，不会阻止后面其他dom的生成吗？为什么页面&lt;div&gt;test&lt;&#47;div&gt;还是显示了出来？求解答</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/88/73/592c8ddd.jpg" width="30px"><span>HB</span> 👍（2） 💬（2）<div>每节课都能学到东西，如果能更新快一点就好了。比如二四六改成一三五七</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/25/38/618040ad.jpg" width="30px"><span>宇宙机吴彦祖</span> 👍（1） 💬（0）<div>哇更新了</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/13/e4/3acadb90.jpg" width="30px"><span>Leon</span> 👍（1） 💬（0）<div>谷歌源码有涉及就好了
</div>2020-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/e7/d9/83d1346c.jpg" width="30px"><span>Lx</span> 👍（1） 💬（1）<div>即使js脚本设置了a sync defer，也还是会被css的文件下载阻塞吧？</div>2019-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5f/80/51269d88.jpg" width="30px"><span>Hurry</span> 👍（1） 💬（2）<div>Token 栈，遇到结束标签，但是栈顶刚好不是对应开始标签, 这种错误，解析器，如何处理？</div>2019-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1e/71/54ff7b4e.jpg" width="30px"><span>3Spiders</span> 👍（1） 💬（8）<div>针对文章中js和css加载我有一个疑问。
&lt;head&gt;
&lt;link ref=&quot;a.css&quot;&gt;
&lt;script src=&quot;b.js&quot;&gt;&lt;&#47;scripit&gt;
&lt;link ref=&quot;c.css&quot;&gt;
&lt;&#47;head&gt;
这三个资源的加载顺序是什么。按照老师文章中的意思，是先加载css文件，再加载js文件吗。
即a.css，c.css，b.js。
</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/19/69f6e2ec.jpg" width="30px"><span>王大可</span> 👍（1） 💬（0）<div>time.geekbang
test
把script标签包裹的代码放入一个js文件中，在引入该文件
1. 放入第一个div之前页面显示
1
test 
控制台报错；
2. 放入最后一个div之前页面显示
time.geekbang
time.geekbang.com ；
3.放入任何位置加入defer或async 显示
time.geekbang
time.geekbang.com </div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ec/68/06d59613.jpg" width="30px"><span>柒月</span> 👍（1） 💬（0）<div>time.geekbang
test
get了，一直以为CSS的解析不会阻塞DOM的解析呢</div>2019-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-05-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqks5UGahZtWAzZcmBkUZtibok5fGLWvpkR17PT65tjiaw4zCxntq18wKU1ia0AjITsZykxo5k0xV27w/132" width="30px"><span>俊俊大魔王</span> 👍（0） 💬（1）<div>老师，这句话怎么理解，“CSS不阻塞js的加载，但是会阻塞js的执行。”</div>2023-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（0） 💬（0）<div>思考题：

我以为给是undefined的div2赋值，会导致页面报错，导致进程崩溃，页面白屏。

实际结果是console控制台是有报错，但是解析还是继续执行了，最后div2的文本还是test。</div>2023-09-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/XPWXccJiaGnF4AZuuWnH4SQpKibwAhnRDAlnpcCwKW6JjJHFCz6ldicfC6QMiaJefyGVl8jZpYWvEJicZ2eK5qibCldA/132" width="30px"><span>周大大</span> 👍（0） 💬（0）<div>time.geekbang 
test
原因：解析到script标签时，js引擎开始工作，dom解析被暂停，但是当前dom树上只有一个div，所以第一个div内容被修改成time.geekbang，第二个div还未生成，所以通过js修改并未找到该dom，所以第二个div的文本内容还是test</div>2023-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/44/cf/a78de5f6.jpg" width="30px"><span>F.T.O</span> 👍（0） 💬（0）<div>看完文章之后，有个疑问内联的JavaScript脚本会阻塞Dom的解析，css又会阻塞内联JavaScript脚本的执行，那是不是就说明css会间接阻塞dom的解析？</div>2023-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/44/cf/a78de5f6.jpg" width="30px"><span>F.T.O</span> 👍（0） 💬（0）<div>我想问一下，渲染引擎和渲染进程是什么关系？</div>2023-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/25/da/0db2423f.jpg" width="30px"><span>编程小子</span> 👍（0） 💬（0）<div>老师 我想问一下，浏览器四次挥手断开与服务器连接的时机是什么时候呀</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/34/c1/4e4917f5.jpg" width="30px"><span>有一种踏实</span> 👍（0） 💬（0）<div>不是说现在没有 CSSOM 的概念吗？已经被重构优化成样式表？</div>2022-09-08</li><br/>
</ul>