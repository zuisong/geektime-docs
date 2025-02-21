你好，我是孙鹏飞。

专栏上一期，绍文讲了编译插桩的三种方法：AspectJ、ASM、ReDex，以及它们的应用场景。学完以后你是不是有些动心，想赶快把它们应用到实际工作中去。但我也还了解到，不少同学其实接触插桩并不多，在工作中更是很少使用。由于这项技术太重要了，可以实现很多功能，所以我还是希望你通过理论 + 实践的方式尽可能掌握它。因此今天我给你安排了一期“强化训练”，希望你可以趁热打铁，保持学习的连贯性，把上一期的理论知识，应用到今天插桩的练习上。

为了尽量降低上手的难度，我尽量给出详细的操作步骤，相信你只要照着做，并结合专栏上期内容的学习，你一定可以掌握插桩的精髓。

## ASM插桩强化练习

![](https://static001.geekbang.org/resource/image/e2/07/e2f777c2fb2ed535be7367643e43c307.png?wh=1204%2A1026)

在上一期里，Eateeer同学留言说得非常好，提到了一个工具，我也在使用这个工具帮助自己理解ASM。安装“ASM Bytecode Outline”也非常简单，只需要在Android Studio中的Plugin搜索即可。

![](https://static001.geekbang.org/resource/image/7a/47/7ad456d5f6d5054d6259f66a41cb6047.png?wh=1610%2A412)

ASM Bytecode Outline插件可以快速展示当前编辑类的字节码表示，也可以展示出生成这个类的ASM代码，你可以在Android Studio源码编译框内右键选择“Show Bytecode Outline“来查看，反编译后的字节码在右侧展示。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/2d/93/1a4c40fe.jpg" width="30px"><span>唯鹿</span> 👍（31） 💬（1）<div>感谢老师的认可与鼓励，我会继续坚持学习与分享！🙏</div>2019-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/68/49/418a9486.jpg" width="30px"><span>Neil</span> 👍（2） 💬（4）<div>这个插件是不是在AS3.3上失效了啊</div>2019-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/52/7b/49f88f67.jpg" width="30px"><span>Geek_p7uia1</span> 👍（1） 💬（2）<div>请问在写Transform的过程中，如何debug代码呢？初期对ASM不熟悉，在写的过程中如果能debug最好了</div>2019-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/7f/fb/49507baa.jpg" width="30px"><span>blithe</span> 👍（0） 💬（1）<div>为什么是使用发射的方式，替换了transformClassesWithDexBuilderForDebug，而不是直接在plugin中直接加入进去一个</div>2019-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/88/8e/6f6c7539.jpg" width="30px"><span>王大大</span> 👍（0） 💬（1）<div>@splm 我的方法是在本地建repo，然后在项目中classpath引进去，然后在apply进去，但是修改了代码调试需要重新uploadArchives，就很麻烦，有什么好的调试办法吗</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/e9/072b33b9.jpg" width="30px"><span>splm</span> 👍（0） 💬（1）<div>如果不上传maven的话，本地工程使用，提示找不到插件类，这个是什么问题？</div>2019-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/85/2a/53461450.jpg" width="30px"><span>杨泉</span> 👍（3） 💬（0）<div>如何运行Demo
ASMSample项目先注释掉
&#47;&#47; apply plugin: &#39;com.geektime.asm-plugin&#39;
&#47;&#47; classpath (&quot;com.geektime.asm:asm-gradle-plugin:1.0&quot;) { changing = true }`
编译和发布asm-gradle-plugin 到本地maven
.&#47;gradlew buildAndPublishToLocalMaven
还原第1步注释掉的插件依赖，即可运行Demo
.&#47;gradlew installDebug
我的，还要修改以下3点，才能编译通过：
1 把项目的改为 distributionUrl=https:&#47;&#47;services.gradle.org&#47;distributions&#47;gradle-5.6.4-all.zip
2 项目的 buildscript{ dependencies { classpath &#39;com.android.tools.build:gradle:3.6.1&#39; } }
3 asm-gradle-plugin module中的
dependencies {
compile &#39;com.android.tools.build:gradle:3.6.1&#39; &#47;&#47;从2.1.0改为3.6.1，否则com.android.build.gradle.internal.pipeline和com.android.build.api.transform包找不到
}</div>2020-05-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/3b/83/a5327123.jpg" width="30px"><span>ysnows</span> 👍（0） 💬（0）<div>https:&#47;&#47;plugins.jetbrains.com&#47;plugin&#47;14860-asm-bytecode-viewer-support-kotlin 大家也可以用这个插件，ASM Bytecode Outline已经不更新了</div>2022-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fd/aa/3353a9b0.jpg" width="30px"><span>haizhiyun</span> 👍（0） 💬（0）<div>你好，asm 如何在一个方法的调用后面插入一个方法 ，并获取这个方法的所有参数，实现类似  aspectJ @After(&quot;call(...)&quot;)  或者 @Around(&quot;call(...)&quot;)的功能 </div>2019-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/e9/072b33b9.jpg" width="30px"><span>splm</span> 👍（0） 💬（0）<div>Could not find implementation class for plugin error when using Gradle 4.1+。
有遇到这个问题的朋友，可以肯定是找不到类，第一要看插件的properties文件命名和里面的内容指向，命名是用来apply的，内容是用来找到对应插件类，要明确这个关系。第二，要仔细groovy文件是否有后缀。我之前就是粗心连续的回车，导致忘记给文件家后缀，一直报这个恶心的错误。</div>2019-03-26</li><br/>
</ul>