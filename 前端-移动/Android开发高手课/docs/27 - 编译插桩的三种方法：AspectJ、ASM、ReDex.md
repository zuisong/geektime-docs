只要简单回顾一下前面课程的内容你就会发现，在启动耗时分析、网络监控、耗电监控中已经不止一次用到编译插桩的技术了。那什么是编译插桩呢？顾名思义，所谓的编译插桩就是在代码编译期间修改已有的代码或者生成新代码。

![](https://static001.geekbang.org/resource/image/be/75/be872dd6d12ab22879fbec9414fb2d75.png?wh=1920%2A296)

如上图所示，请你回忆一下Java代码的编译流程，思考一下插桩究竟是在编译流程中的哪一步工作？除了我们之前使用的一些场景，它还有哪些常见的应用场景？在实际工作中，我们应该怎样更好地使用它？现在都有哪些常用的编译插桩方法？今天我们一起来解决这些问题。

## 编译插桩的基础知识

不知道你有没有注意到，在编译期间修改和生成代码其实是很常见的行为，无论是Dagger、ButterKnife这些APT（Annotation Processing Tool）注解生成框架，还是新兴的Kotlin语言[编译器](https://github.com/JetBrains/kotlin/tree/v1.2.30/compiler/backend/src/org/jetbrains/kotlin/codegen)，它们都用到了编译插桩的技术。

下面我们一起来看看还有哪些场景会用到编译插桩技术。

**1. 编译插桩的应用场景**

编译插桩技术非常有趣，同样也很有价值，掌握它之后，可以完成一些其他技术很难实现或无法完成的任务。学会这项技术以后，我们就可以随心所欲地操控代码，满足不同场景的需求。

- **代码生成**。除了Dagger、ButterKnife这些常用的注解生成框架，Protocol Buffers、数据库ORM框架也都会在编译过程生成代码。代码生成隔离了复杂的内部实现，让开发更加简单高效，而且也减少了手工重复的劳动量，降低了出错的可能性。
- **代码监控**。除了网络监控和耗电监控，我们可以利用编译插桩技术实现各种各样的性能监控。为什么不直接在源码中实现监控功能呢？首先我们不一定有第三方SDK的源码，其次某些调用点可能会非常分散，例如想监控代码中所有new Thread()调用，通过源码的方式并不那么容易实现。
- **代码修改**。我们在这个场景拥有无限的发挥空间，例如某些第三方SDK库没有源码，我们可以给它内部的一个崩溃函数增加try catch，或者说替换它的图片库等。我们也可以通过代码修改实现无痕埋点，就像网易的[HubbleData](https://neyoufan.github.io/2017/07/11/android/%E7%BD%91%E6%98%93HubbleData%E4%B9%8BAndroid%E6%97%A0%E5%9F%8B%E7%82%B9%E5%AE%9E%E8%B7%B5/)、51信用卡的[埋点实践](https://mp.weixin.qq.com/s/P95ATtgT2pgx4bSLCAzi3Q)。
- **代码分析**。上一期我讲到持续集成，里面的自定义代码检查就可以使用编译插桩技术实现。例如检查代码中的new Thread()调用、检查代码中的一些敏感权限使用等。事实上，Findbugs这些第三方的代码检查工具也同样使用的是编译插桩技术实现。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/61/ab/83506e34.jpg" width="30px"><span>Eateeer</span> 👍（23） 💬（1）<div>看到这篇文章表示非常激动，这段时间自己也在尝试了解和使用编译插桩的相关技术，编译插桩涉及的东西很多，特别是 ASM 与 Transform 结合后产生的一些列化学反应，比如无埋点、增量编译、Instant Run 等，感觉像是打开了一个新世界的大门。

给大家安利一个 IntelliJ 插件 - ASM Bytecode Outline，可以用来帮助编写字节码。

再次感谢绍文大大的精彩文章！
</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4a/ab/5d8a478f.jpg" width="30px"><span>su</span> 👍（5） 💬（1）<div>这篇含金量是目前整个专栏最好的，谢谢</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/e9/072b33b9.jpg" width="30px"><span>splm</span> 👍（2） 💬（1）<div>嗯很不错啊。之前一直对插桩只有印象，但具体做什么还是不了解，但今天看了这篇文章，受益匪浅。原来插桩的技术，自己之前就用过了。

这个是自己之前利用APT和JavaPoet写的一个开发工具，大家可以交流探讨一下。
https:&#47;&#47;github.com&#47;splm&#47;WeBase
也希望大家能多点几个星。</div>2019-03-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/33/51/9073faa5.jpg" width="30px"><span>seven</span> 👍（1） 💬（1）<div>文哥牛逼！这篇至少要看个十几遍~玩溜asm估计要练习个几个月了
</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/70/8f/419240e4.jpg" width="30px"><span>itismelzp</span> 👍（0） 💬（3）<div>非常棒！但是我有个问题，就是asm插桩后的class行号就变了吧，这样堆栈信息就对不上了。。。</div>2019-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/f0/dfd29eeb.jpg" width="30px"><span>孫小逗</span> 👍（0） 💬（2）<div>请问，AS3.1.3，安装ASM Bytecode Outline后，没有显示字节码是什么情况？</div>2019-03-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erxia5dpTeXMHR1e4ibicyRkS6fAuxarFicFZ3kwlrosFszjazFDJaRrrAiaH9hX0ia45xTKE6GetKIrgqg/132" width="30px"><span>X</span> 👍（0） 💬（1）<div>请问Systrace在Windows上是不是不支持，我试过在Mac上可以用的，但是Windows上就报错，Google了下好像很多人反馈这个但是没有解决方案！</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/50/12/74d414d4.jpg" width="30px"><span>LD</span> 👍（0） 💬（1）<div>另外一个字节码处理工具javaasist也不错哦
使用比asm简单，达到的效果和asm一致(直接插入代码，不像aspectj需要生成包装函数)</div>2019-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/88/8e/6f6c7539.jpg" width="30px"><span>王大大</span> 👍（8） 💬（0）<div>推荐一个简单轻量的asm框架lancet，https:&#47;&#47;github.com&#47;eleme&#47;lancet，通过这个库实现业务代码的动态监测</div>2019-03-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/25/29/0f71c179.jpg" width="30px"><span>l晟睿致远</span> 👍（3） 💬（0）<div>这两天扣了一下asm操作字节码，把onMethodExit方法改了一下，如果time大于设定的时间就使用error级别打印。做为练习发出来共勉。内容较长分三段发，一、
protected void onMethodExit(int opcode) {

            int stringBuilderIndex = newLocal(Type.getType(&quot;java&#47;lang&#47;StringBuilder&quot;));

            mv.visitMethodInsn(INVOKESTATIC, &quot;java&#47;lang&#47;System&quot;, &quot;currentTimeMillis&quot;, &quot;()J&quot;, false);
            mv.visitVarInsn(LLOAD, timeLocalIndex);&#47;&#47;把变量压入栈
            mv.visitInsn(LSUB);&#47;&#47;执行long 类型减法  上面的减下面 ，此处的值在栈顶
            mv.visitVarInsn(LSTORE, timeLocalIndex);&#47;&#47;因为后面要用到这个值所以先将其保存到本地变量表中
            mv.visitVarInsn(LLOAD,timeLocalIndex);&#47;&#47;压入栈
            mv.visitLdcInsn(100L);&#47;&#47;压入100入栈 作为比较，如果执行时间大于100毫秒使用ERROR打印 否使用debug

            mv.visitInsn(LCMP);&#47;&#47;执行long类型比较指令
            Label l1 = new Label();

            mv.visitJumpInsn(Opcodes.IFLE,l1); &#47;&#47;弹出上面压入的两个long 比较,此时栈空,到label1
            &#47;&#47;if 比较成立执行
             mv.visitTypeInsn(Opcodes.NEW, &quot;java&#47;lang&#47;StringBuilder&quot;);
            mv.visitInsn(Opcodes.DUP);
            mv.visitMethodInsn(Opcodes.INVOKESPECIAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;&lt;init&gt;&quot;, &quot;()V&quot;, false);
            mv.visitVarInsn(Opcodes.ASTORE, stringBuilderIndex);&#47;&#47;需要将栈顶的 stringbuilder 保存起来否则后面找不到了
            mv.visitVarInsn(Opcodes.ALOAD, stringBuilderIndex);
            mv.visitLdcInsn(className + &quot;.&quot; + methodName + &quot; time:&quot;);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;append&quot;, &quot;(Ljava&#47;lang&#47;String;)Ljava&#47;lang&#47;StringBuilder;&quot;, false);
            mv.visitInsn(Opcodes.POP);
            mv.visitVarInsn(Opcodes.ALOAD, stringBuilderIndex);
            mv.visitVarInsn(Opcodes.LLOAD, timeLocalIndex);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;append&quot;, &quot;(J)Ljava&#47;lang&#47;StringBuilder;&quot;, false);
            mv.visitInsn(Opcodes.POP);
    </div>2020-05-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI3jSpV7VvK6NaUH6X1LNYWGsQdFSTu4SwTZ0nQlSYGTOY2FrDCcMic9qFXnu2ZGR88hBlUQK28Whg/132" width="30px"><span>古月弓虽1993</span> 👍（3） 💬（0）<div>如果build.gradle配置的变体buildType类型配置：shrinkResources true minifyEnabled true。第7期的练习是没法正常插桩的。因为代码里要hook的任务是写死的task名称：transformClassesWithDexBuilderFor。而在这种情况下需要hook的任务名是类似这样的：transformClassesAndResourcesWithR8For</div>2020-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4b/07/2fc0cdf8.jpg" width="30px"><span>。ZQN</span> 👍（2） 💬（0）<div>做了一个可视化埋点系统</div>2019-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/7e/bb/947c329a.jpg" width="30px"><span>程序员小跃</span> 👍（1） 💬（0）<div>文章只是敲门砖，还得看看虚拟机，以及课后的这些链接，Android高手之路，任重道远</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/25/29/0f71c179.jpg" width="30px"><span>l晟睿致远</span> 👍（0） 💬（0）<div>三、
   mv.visitInsn(Opcodes.POP);
            mv.visitLdcInsn(&quot;Geek&quot;);
            mv.visitVarInsn(Opcodes.ALOAD, stringBuilderIndex);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;toString&quot;, &quot;()Ljava&#47;lang&#47;String;&quot;, false);
            mv.visitMethodInsn(Opcodes.INVOKESTATIC, &quot;android&#47;util&#47;Log&quot;, &quot;d&quot;, &quot;(Ljava&#47;lang&#47;String;Ljava&#47;lang&#47;String;)I&quot;, false);&#47;&#47;注意： Log.d 方法是有返回值的，需要 pop 出去
            mv.visitInsn(Opcodes.POP);&#47;&#47;插入字节码后要保证栈的清洁，不影响原来的逻辑，否则就会产生异常，也会对其他框架处理字节码造成影响

            &#47;&#47;执行内容结束
            mv.visitLabel(l2); &#47;&#47;label2起始
            mv.visitFrame(Opcodes.F_SAME,2,null,0,null);&#47;&#47;访问当前帧状态
            mv.visitInsn(Opcodes.RETURN);&#47;&#47;返回
            mv.visitMaxs(2, 2);&#47;&#47;设置局部表量表和操作数栈大小
            mv.visitEnd();&#47;&#47;访问结束
        }</div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/25/29/0f71c179.jpg" width="30px"><span>l晟睿致远</span> 👍（0） 💬（0）<div>二、
        mv.visitLdcInsn(&quot;Geek&quot;);
            mv.visitVarInsn(Opcodes.ALOAD, stringBuilderIndex);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;toString&quot;, &quot;()Ljava&#47;lang&#47;String;&quot;, false);
            mv.visitMethodInsn(Opcodes.INVOKESTATIC, &quot;android&#47;util&#47;Log&quot;, &quot;e&quot;, &quot;(Ljava&#47;lang&#47;String;Ljava&#47;lang&#47;String;)I&quot;, false);&#47;&#47;注意： Log.d 方法是有返回值的，需要 pop 出去
            mv.visitInsn(Opcodes.POP);&#47;&#47;插入字节码后要保证栈的清洁，不影响原来的逻辑，否则就会产生异常，也会对其他框架处理字节码造成影响

            &#47;&#47;条件成立执行结束
            Label l2 = new Label(); &#47;&#47;声明label
            mv.visitJumpInsn(Opcodes.GOTO,l2); &#47;&#47;跳转关联label2

            mv.visitLabel(l1);&#47;&#47;label1起始
            &#47;&#47;上面条件不成立走这里

            mv.visitTypeInsn(Opcodes.NEW, &quot;java&#47;lang&#47;StringBuilder&quot;);
            mv.visitInsn(Opcodes.DUP);
            mv.visitMethodInsn(Opcodes.INVOKESPECIAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;&lt;init&gt;&quot;, &quot;()V&quot;, false);
            mv.visitVarInsn(Opcodes.ASTORE, stringBuilderIndex);&#47;&#47;需要将栈顶的 stringbuilder 保存起来否则后面找不到了
            mv.visitVarInsn(Opcodes.ALOAD, stringBuilderIndex);
            mv.visitLdcInsn(className + &quot;.&quot; + methodName + &quot; time:&quot;);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;append&quot;, &quot;(Ljava&#47;lang&#47;String;)Ljava&#47;lang&#47;StringBuilder;&quot;, false);
            mv.visitInsn(Opcodes.POP);
            mv.visitVarInsn(Opcodes.ALOAD, stringBuilderIndex);
            mv.visitVarInsn(Opcodes.LLOAD, timeLocalIndex);
            mv.visitMethodInsn(Opcodes.INVOKEVIRTUAL, &quot;java&#47;lang&#47;StringBuilder&quot;, &quot;append&quot;, &quot;(J)Ljava&#47;lang&#47;StringBuilder;&quot;, false);
         </div>2020-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/68/01/abb7bfe3.jpg" width="30px"><span>向着光亮那方</span> 👍（0） 💬（0）<div>对于这里的插桩，在覆盖率统计上，都是可以用吧？离线插桩</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/bc/dd/c9413f59.jpg" width="30px"><span>铿然</span> 👍（0） 💬（0）<div>ByteBuddy封装度很高，使用最简单，比javaassist好用很多。</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/8e/24/2e6500d2.jpg" width="30px"><span>廉颇未老 尚能饭</span> 👍（0） 💬（0）<div>我最近使用asm访问方法的注解，怎么都不能访问到呀，刚入门不久，有那个大佬指教一下呀。AnnotationVisitor</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bb/dc/ecc6f3ad.jpg" width="30px"><span>Geek_28d7fe</span> 👍（0） 💬（0）<div>感谢分享，在github上的demo很专业，不是单纯的演示。感恩专业、用心</div>2019-07-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/30/27/61b31300.jpg" width="30px"><span>李剑昆</span> 👍（0） 💬（0）<div>https:&#47;&#47;github.com&#47;lijiankun24&#47;Koala ASM 版本的 hugo ^_^。还有个问题想请教一下，使用插桩实现增量编译有什么思路或者方向吗？</div>2019-07-17</li><br/>
</ul>