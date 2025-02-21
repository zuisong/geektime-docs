你好，我是孙鹏飞。又到了答疑的时间，今天我将围绕卡顿优化这个主题，和你探讨一下专栏第6期和补充篇的两个Sample的实现。

专栏第6期的Sample完全来自于Facebook的性能分析框架[Profilo](https://github.com/facebookincubator/profilo)，主要功能是收集线上用户的atrace日志。关于atrace相信我们都比较熟悉了，平时经常使用的systrace工具就是封装了atrace命令来开启ftrace事件，并读取ftrace缓冲区生成可视化的HTML日志。这里多说一句，ftrace是Linux下常用的内核跟踪调试工具，如果你不熟悉的话可以返回第6期文稿最后查看ftrace的介绍。Android下的atrace扩展了一些自己使用的categories和tag，这个Sample获取的就是通过atrace的同步事件。

Sample的实现思路其实也很简单，有两种方案。

第一种方案：hook掉atrace写日志时的一系列方法。以Android 9.0的代码为例写入ftrace日志的代码在[trace-dev.cpp](http://androidxref.com/9.0.0_r3/xref/system/core/libcutils/trace-dev.cpp)里，由于每个版本的代码有些区别，所以需要根据系统版本做一些区分。

第二种方案：也是Sample里所使用的方案，由于所有的atrace event写入都是通过[/sys/kernel/debug/tracing/trace\_marker](http://androidxref.com/9.0.0_r3/xref/system/core/libcutils/trace-container.cpp#85)，atrace在初始化的时候会将该路径fd的值写入[atrace\_marker\_fd](http://androidxref.com/9.0.0_r3/s?defs=atrace_marker_fd&project=system)全局变量中，我们可以通过dlsym轻易获取到这个fd的值。关于trace\_maker这个文件我需要说明一下，这个文件涉及ftrace的一些内容，ftrace原来是内核的事件trace工具，并且ftrace文档的开头已经写道
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/5d/e50cf9c7.jpg" width="30px"><span>Kenneth</span> 👍（1） 💬（1）<div>请问这些知识是怎么获取到的呢？总感觉获取原声资料的渠道很受限制，感谢授人以鱼，更感谢授人以渔，感谢🙏</div>2019-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7f/fb/49507baa.jpg" width="30px"><span>blithe</span> 👍（0） 💬（0）<div>应用层开发都没接触过这些内容，大佬，你是从做什么开始接触到这些内容，并学习的</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/57/0b/8b2465d6.jpg" width="30px"><span>eyeandroid</span> 👍（0） 💬（0）<div>通过hook atrace拿到的systrace，有cpu和其它进程的信息吗？</div>2019-04-24</li><br/>
</ul>