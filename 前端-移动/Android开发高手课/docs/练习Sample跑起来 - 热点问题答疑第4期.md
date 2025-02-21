你好，我是孙鹏飞。今天我们回到专栏第7期和第8期，来看看课后练习Sample的运行需要注意哪些问题。另外我结合同学们留言的疑问，也来谈谈文件顺序对I/O的影响，以及关于Linux学习我的一些方法和建议。

[专栏第7期](http://time.geekbang.org/column/article/73651)的Sample借助于systrace工具，通过字节码处理框架对函数插桩来获取方法执行的trace。这个Sample实现相当完整，你在日常工作也可以使用它。

这个Sample使用起来虽然非常简单，但其内部的实现相对来说是比较复杂的。它的实现涉及Gradle Transform、Task实现、增量处理、ASM字节码处理、mapping文件使用，以及systrace工具的使用等。

对于Gradle来说，我们应该比较熟悉，它是Android平台下的构建工具。对于平时使用来说，我们大多时候只需要关注Android Gradle Plugin的一些参数配置就可以实现很多功能了，官方文档已经提供了很详细的参数设置[说明](https://developer.android.com/studio/build/?hl=zh-cn)。对于一些需要侵入打包流程的操作，就需要我们实现自己的Task或者Transform代码来完成，比如处理Class和JAR包、对资源做一些处理等。

Gradle学习的困难更多来自于Android Gradle Plugin对Gradle做的一些封装扩展，而这部分Google并没有提供很完善的文档，并且每个版本都有一些接口上的变动。对于这部分内容的学习，我主要是去阅读别人实现的Gradle工具代码和[Android Gradle Plugin代码](https://android.googlesource.com/platform/tools/base/+/studio-3.2.1/build-system/)。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erxia5dpTeXMHR1e4ibicyRkS6fAuxarFicFZ3kwlrosFszjazFDJaRrrAiaH9hX0ia45xTKE6GetKIrgqg/132" width="30px"><span>X</span> 👍（2） 💬（3）<div>文中有个笔误:“SampleApp 中其 p 的 e.systrace.TraceTag&quot; 这句话我推测应该是&quot;com.sample.systrace.TraceTag&quot;，同学们移植时要确保TraceTag的路径为com.sample.systrace.TraceTag，否则会报NoClassDefFoundError的。

</div>2019-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/53/af/0e3ddb1d.jpg" width="30px"><span>SunnyBird</span> 👍（1） 💬（0）<div>很棒 谢谢老师</div>2019-01-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJrYx98EACOUVZWTIMMfvsNwMEgm8GNicvpuRIGmqd1VCqJp7LBGh08xWMVicphlliaaDcxlBc5iaP4TA/132" width="30px"><span>yuanyuan</span> 👍（0） 💬（0）<div>生成的trace html显示
activityStart(Did Not Finish)
com.sample.systrace.MainActivity.onCreate.(Landroid.os.Bundle;)V(Did Not Finish)，
实际上onCreate早运行完成了，感觉Trace一直卡在onCreate()，我自己手动插桩就是正常的，请问这是什么原因？

</div>2020-02-08</li><br/>
</ul>