你好，我是陈航。

在上一篇文章中，我从工程架构与工作模式两个层面，与你介绍了设计Flutter混合框架需要关注的基本设计原则，即确定分工边界。

在工程架构维度，由于Flutter模块作为原生工程的一个业务依赖，其运行环境是由原生工程提供的，因此我们需要将它们各自抽象为对应技术栈的依赖管理方式，以分层依赖的方式确定二者的边界。

而在工作模式维度，考虑到Flutter模块开发是原生开发的上游，因此我们只需要从其构建产物的过程入手，抽象出开发过程中的关键节点和高频节点，以命令行的形式进行统一管理。构建产物是Flutter模块的输出，同时也是原生工程的输入，一旦产物完成构建，我们就可以接入原生开发的工作流了。

可以看到，在Flutter混合框架中，Flutter模块与原生工程是相互依存、互利共赢的关系：

- Flutter跨平台开发效率高，渲染性能和多端体验一致性好，因此在分工上主要专注于实现应用层的独立业务（页面）的渲染闭环；
- 而原生开发稳定性高，精细化控制力强，底层基础能力丰富，因此在分工上主要专注于提供整体应用架构，为Flutter模块提供稳定的运行环境及对应的基础能力支持。

那么，在原生工程中为Flutter模块提供基础能力支撑的过程中，面对跨技术栈的依赖管理，我们该遵循何种原则呢？对于Flutter模块及其依赖的原生插件们，我们又该如何以标准的原生工程依赖形式进行组件封装呢？
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1e/1f/e3c13f29.jpg" width="30px"><span>天空</span> 👍（1） 💬（1）<div>依赖插件为git时能声明分支或者tag版本什么的吗？</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/84/76ca98cc.jpg" width="30px"><span>天空</span> 👍（0） 💬（1）<div>flutter module中.android 是自动生成的， 打包aar有什么意义？  一个flutter project可以打成aar 集成到原生工程里面吗？</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a2/19/3f71c4e8.jpg" width="30px"><span>Element</span> 👍（0） 💬（1）<div>老师好, 模块工程依赖插件配置这块: flutter_plugin_network:
    git:
      url: https:&#47;&#47;github.com&#47;cyndibaby905&#47;44_flutter_plugin_network.git
平时开发就需要将插件上传到github然后这样配置依赖吗? 能不能直接在本地依赖插件?</div>2019-10-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ca/7b/03407725.jpg" width="30px"><span>学会〆忘记</span> 👍（1） 💬（0）<div>老师你好，我想问下iOS工程中的App.framework和类似fluttertoast，只能从Flutter工程里面拷贝出来吗？有没有好一点的方法，因为我iOS工程已经是组件化了，我现在把Flutter当成了其中一个子组件</div>2020-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0c/05/3e2b8688.jpg" width="30px"><span>时光念你</span> 👍（1） 💬（0）<div>拿iOS来说吧，定义一个单例plugin，每次flutter调用native，都去调用单例plugin，flutter的arguments参数会传递一个map对象，包含methodName和自定义的arguments。iOS端利用runtime，通过注册机制，将methodName和某一个class进行关系绑定，存入单例plugin对象内部。当flutter调用native，iOS端就会初始化一个对应的class实例对象并把参数和resultBlock传递给它，当该对象执行完毕之后，调用resultBlock把结果回传给flutter。</div>2019-12-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq6LGLtCCNoIZ9jUJ0uBmedrVrdgZy2wXficALJPGtPpFagbJicb3CWesvXqfzsVYMLemiaJDRqyLRqA/132" width="30px"><span>Geek_Javy</span> 👍（0） 💬（0）<div>混编的项目编译很慢啊，目前我的android项目编译一次十分钟有没有方法可以优化一下？</div>2021-06-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er6ADlY3IFt3Rs1aVDyrTO2BiaV8wiabypPwbXhbPcyqicCvnTV9lUYHULVqUab7ww4taX5QbmFyatLQ/132" width="30px"><span>Geek_cc0a3b</span> 👍（0） 💬（0）<div>这种架构应该是由三个项目：native、flutter module、flutter plugin，如何debug呢，比如从native层debug到flutter plugin，没成功。</div>2021-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/55/ff/1489d0fb.jpg" width="30px"><span>肖</span> 👍（0） 💬（0）<div>flutter 调用腾讯Tim  发送视频，原生怎么把进度传回给flutter的每一个message呢？请老师指教</div>2020-05-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/66/2e/527b73c9.jpg" width="30px"><span>骑着🚀看银河</span> 👍（0） 💬（0）<div>老师你好，有flutter完整实践一个App的经验吗，一个小的项目也可以，但是需要把常见的功能搞定，或者推荐一个这样的案例学习也可以</div>2020-05-06</li><br/>
</ul>