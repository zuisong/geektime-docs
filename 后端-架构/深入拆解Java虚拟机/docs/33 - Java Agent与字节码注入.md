关于Java agent，大家可能都听过大名鼎鼎的`premain`方法。顾名思义，这个方法指的就是在`main`方法之前执行的方法。

```
package org.example;

public class MyAgent {
  public static void premain(String args) {
    System.out.println("premain");
  }
}
```

我在上面这段代码中定义了一个`premain`方法。这里需要注意的是，Java虚拟机所能识别的`premain`方法接收的是字符串类型的参数，而并非类似于`main`方法的字符串数组。

为了能够以Java agent的方式运行该`premain`方法，我们需要将其打包成jar包，并在其中的MANIFEST.MF配置文件中，指定所谓的`Premain-class`。具体的命令如下所示：

```
# 注意第一条命令会向manifest.txt文件写入两行数据，其中包括一行空行
$ echo 'Premain-Class: org.example.MyAgent
' > manifest.txt
$ jar cvmf manifest.txt myagent.jar org/
$ java -javaagent:myagent.jar HelloWorld
premain
Hello, World
```

除了在命令行中指定Java agent之外，我们还可以通过Attach API远程加载。具体用法如下面的代码所示：

```
import java.io.IOException;

import com.sun.tools.attach.*;

public class AttachTest {
  public static void main(String[] args)
      throws AttachNotSupportedException, IOException, AgentLoadException, AgentInitializationException {
    if (args.length <= 1) {
      System.out.println("Usage: java AttachTest <PID> /PATH/TO/AGENT.jar");
      return;
    }
    VirtualMachine vm = VirtualMachine.attach(args[0]);
    vm.loadAgent(args[1]);
  }
}

```

使用Attach API远程加载的Java agent不会再先于`main`方法执行，这取决于另一虚拟机调用Attach API的时机。并且，它运行的也不再是`premain`方法，而是名为`agentmain`的方法。

```
public class MyAgent { 
  public static void agentmain(String args) {
    System.out.println("agentmain");
  }
}
```

相应的，我们需要更新jar包中的manifest文件，使其包含`Agent-Class`的配置，例如`Agent-Class: org.example.MyAgent`。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/07/8c/0d886dcc.jpg" width="30px"><span>蚂蚁内推+v</span> 👍（13） 💬（1）<div>用attach的方式注入字节码的时候遇到了99线升高的性能问题，看一些资料说 class redefinition 的时候会阻塞线程。请问能详细讲下吗？</div>2018-11-19</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（4） 💬（1）<div>我看到了jvmti可以回调异常事件，但是java.lang.instrument包下没有处理这个事件的，只能在load时回调，处理异常究竟是怎么做的？</div>2018-10-06</li><br/><li><img src="" width="30px"><span>Scott</span> 👍（4） 💬（1）<div>出方法时需要注入的字节码除了返回，还有几种情况，如果没有catch块，就拦截throw，如果有，但是catch块里面可能有很多层，只是遍历inst应该是不可以的</div>2018-10-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（28） 💬（1）<div>阅过留痕

1：Java agent 是啥玩意？
      这个概念老师没有详细讲解，我的理解是Java语言的一个特性，这个特性能够实现Java字节码的注入

2：Java字节码的注入有什么用处呢？
在平时编程几乎没有使用到这方面的功能，应该是在一些框架的设计的时候才使用吧！比如：专栏中提到的面相切面编程。

3：Java agent 本质上是通过 c agent 来实现的，那 c agent 本质上是怎么实现的呢？
C agent是一个事件驱动的工具实现接口，通常我们会在 C agent 加载后的入口方案 Agent_OnLoad处注册各个事件的钩子方法。当Java虚拟机触发了这些事件时，便会调用对应的钩子方法

4：留个话头
      写代码实现某些功能，我的理解有三个时间段
      第一个：源码阶段，最常用的，也是编程的主要活动时间
      第二个：字节码阶段，有些功能可能会在加载字节码时修改或者添加某些字节码，某些框架做的事情
      第三个：运行阶段，某些工具，在程序运行时修改代码，实现运行时功能分支的控制</div>2018-10-13</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEI0ia2Dz6NRBNZIwOLbIDJQZ5dRrhMVKj8JKic3Qibh7M8Uz1Sf1akuOJSSyHUQnrbZ0OmtmRm9yGvCw/132" width="30px"><span>feng</span> 👍（10） 💬（1）<div>第一个实验做的不严谨，第一，木有定义HelloWord类，第二，没有执行编译操作，不知道是有意为之，还是不小心把步骤漏掉了</div>2018-10-07</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLz3icr3mGs5ib8FbSPQZ2ic3ib90mHkd1btQrmGacZjJxfYXrerIdaTxglKyCicFzLcEAb6deC2cWjE5Q/132" width="30px"><span>the geek</span> 👍（7） 💬（0）<div>大概说一下我自己的理解(望老师指正):
1. Agent就是一个调用JVMTI函数的一个程序。
2. JVMTI能够提供的函数能够获得JVM的运行信息，还可以修改JVM的运行态。
3. JVMTI能够修改JVM运行态是因为JVM已经在运行流程中埋下了钩子函数，JVMTI中的函数可以传递具体逻辑给钩子函数。
4. JVMTI函数是C语言实现的JNI方法。
5. 通过Instrumentation我们可以用Java语言调用大部分JVMTI函数。
6. JVM在启动时会加载Agent 入口函数Agent_OnLoad,我们可以在此函数中注册Agent。
7. JVM在运行中可以通过Agent_OnAttach函数来加载Agent,我们可以在此函数中注册Agent。
8. B虚拟机调用attach方法attach到A虚拟机后，可以将Agent程序作为参数调用A虚拟机的Agent_OnAttach函数。
9. premain方法中的程序逻辑会被注册到Agent_OnLoad函数中。
10. agentmain方法中的程序逻辑会被注册到Agent_OnAttach函数中。
11. 在premain或agentmain方法中的拿到的Instrumentation引用，可以理解成拿到了JVMTI的引用(大部分函数)。

以上全是个人抽象理解，不是具体实现。</div>2020-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（3） 💬（0）<div>把老师给的程序都跑了一篇，发现想要彻底搞懂，还需要多学习，C&#47;C++的知识不能丢了，因为HotSpot JVM 的源码基本上都是用它来实现的。
不过跑了一下代码，最起码可以表面上搞懂了像Lombok，AOP这些都是如何实现的。</div>2019-11-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/99/af/d29273e2.jpg" width="30px"><span>饭粒</span> 👍（1） 💬（0）<div>profiler 示例，文中省略了 HelloWorld.java 和编译提及下更好。
# cat HelloWorld.java 

public class HelloWorld {

    public static void main(String[] args) {
        System.out.println(&quot;Hello World!&quot;);
        HelloWorld w = new HelloWorld();
    }
}

# java -javaagent:myagent.jar -cp $CLASS_PATH:.&#47;asm-7.0-beta.jar:.&#47;asm-tree-7.0-beta.jar HelloWorld
Hello World!
HelloWorld: 1</div>2019-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/3a/97/c4493e91.jpg" width="30px"><span>一缕阳光</span> 👍（1） 💬（0）<div>实习的时候有幸做过一个利用Instrumentation实现自动打点和性能监控的项目。受益匪浅啊  哈哈哈哈  ，不得不说里面坑还是挺多的</div>2019-07-07</li><br/><li><img src="" width="30px"><span>奇奇</span> 👍（1） 💬（1）<div>ASM7 GETSTATIC这些常量是哪里来的？</div>2019-04-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d4/54/7263deb2.jpg" width="30px"><span>吃饭</span> 👍（0） 💬（0）<div>一直不理解java的debug是怎么实现的</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/2e/c1/3b9844cd.jpg" width="30px"><span>房艳</span> 👍（0） 💬（0）<div>https:&#47;&#47;www.jianshu.com&#47;p&#47;b72f66da679f 可参考</div>2021-02-02</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEI0ia2Dz6NRBNZIwOLbIDJQZ5dRrhMVKj8JKic3Qibh7M8Uz1Sf1akuOJSSyHUQnrbZ0OmtmRm9yGvCw/132" width="30px"><span>feng</span> 👍（0） 💬（0）<div>还有个问题想请教下，每次启动的时候都会打印如下信息，objc[2614]: Class JavaLaunchHelper is implemented in both &#47;Library&#47;Java&#47;JavaVirtualMachines&#47;jdk1.8.0_31.jdk&#47;Contents&#47;Home&#47;bin&#47;java (0x102f6f4c0) and &#47;Library&#47;Java&#47;JavaVirtualMachines&#47;jdk1.8.0_31.jdk&#47;Contents&#47;Home&#47;jre&#47;lib&#47;libinstrument.dylib (0x104f384e0). One of the two will be used. Which one is undefined.

请问怎么可以消除，谢谢</div>2018-10-07</li><br/>
</ul>