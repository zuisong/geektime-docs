你好，我是郭屹。今天我们继续手写MiniSpring。这也是MVC内容的最后一节。

上节课，我们对HTTP请求传入的参数进行了自动绑定，并调用了目标方法。我们再看一下整个MVC的流程，现在就到最后一步了，也就是把返回数据回传给前端进行渲染。

![图片](https://static001.geekbang.org/resource/image/a5/f3/a51576e7bc6a3dba052274546f5311f3.png?wh=1660x916)

调用目标方法得到返回值之后，我们有两条路可以返回给前端。第一，返回的是简单的纯数据，第二，返回的是一个页面。

最近几年，第一种情况渐渐成为主流，也就是我们常说的“前后端分离”，后端处理完成后，只是把数据返回给前端，由前端自行渲染界面效果。比如前端用React或者Vue.js自行组织界面表达，这些前端脚本只需要从后端service拿到返回的数据就可以了。

第二种情况，由后端controller根据某种规则拿到一个页面，把数据整合进去，然后整个回传给前端浏览器，典型的技术就是JSP。这条路前些年是主流，最近几年渐渐不流行了。

我们手写MiniSpring的目的是深入理解Spring框架，剖析它的程序结构，所以作为学习的对象，这两种情况我们都会分析到。

## 处理返回数据

和绑定传入的参数相对，处理返回数据是反向的，也就是说，要从后端把方法得到的返回值（一个Java对象）按照某种字符串格式回传给前端。我们以这个@ResponseBody注解为例，来分析一下。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="" width="30px"><span>Geek3485</span> 👍（1） 💬（1）<div>老师的minitomcat源码在哪可以看到</div>2023-08-04</li><br/><li><img src="" width="30px"><span>马儿</span> 👍（0） 💬（2）<div>1.目前如果加了ResponseBody注解返回String的话返回的是String在内存中的信息，而需要的字符串值字段在这个json中也是内存中的地址值，这将导致结果不符合预期，这里应该还需要对writeValuesAsString这个函数优化一下，或者是拓展一些其他的实现。
2. 目前在InternalResourceViewResolver中写死了处理Jsp的View，可以在加一个有参构造函数，传入参数为资源类型，InternalResourceViewResolver内部维护一个资源类型和View的Map

希望老师可以抽时间加一些答疑课，对之前一些同学问到的问题在课上统一解答一下。或者是将一些mini-spring中的一些拓展点提供一个思路，比如上节课遇到的传参数不支持基本类型和自定义类型中WebDataBinder不可用的问题。谢谢老师。</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师几个问题：
Q1：本文所讲的内容，就是模仿SpringMVC，对吗？
Q2：很多信息都存在request中，那这个request对象会占用很大内存吗？对于一个用户，一般地讲，会占用多大内存？比如10M？
Q3：View这个类，是生成一个页面文件吗？还是把数据填充到已经存在的页面上？</div>2023-04-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/45/3f/e4fc2781.jpg" width="30px"><span>梦某人</span> 👍（2） 💬（0）<div>打卡成功，从理解上这节课并不难，虽然很多代码（主要是User类和一些辅助）需要参考GitHub不然无法进行。但是调整环境浪费了接近2个小时，因为访问jsp一直报404的错误，后来意识到是没在idea的Project Structe 中的 Module设置资源文件夹。。。。另外目前的返回来讲，string包装成了 ModelAndView，但是这样做在reander的时候无法辨别，导致最基础的 &#47;test反而无法访问。思考题来说，View的两个类，一个负责分析内容，一个负责渲染内容，将 ViewResolver 进行扩展就可以解决相关问题了。</div>2023-04-18</li><br/><li><img src="" width="30px"><span>Geek_b3425a</span> 👍（1） 💬（0）<div>最新版初始化的handleAdapter的时候并没有给webBindingInitialize赋值，只给了一个set方法但是没有找到调用的地方，这样有请求进来的时候不会就空指针了吗？是我漏看东西了吗</div>2023-09-14</li><br/><li><img src="" width="30px"><span>Geek_b3425a</span> 👍（0） 💬（0）<div>

有点不懂，老师仓库代码，handleMaping和handleAdapter都实现了applicationContextAware接口，类中applicationContext属性是abstractApplicationContext在getBean的时候给set进去的，不懂得是在容器启动的时候并没有这个bean相应的实体对象，并不会调用这个方法，我本地handleMapping中容器属性也是空，并没有掉set方法给他赋值</div>2023-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0b/5a/453ad411.jpg" width="30px"><span>C.</span> 👍（0） 💬（1）<div>结束结束！</div>2023-04-06</li><br/>
</ul>