你好，我是康杨。

通过上节课的学习相信你对 ThreadLocal 已经有了深刻的理解，但是在复杂的现实业务场景中，单靠ThreadLocal 所能解决的问题是有限的，我们需要通过了解ThreadLocal家族的其他成员，以及ThreadLocal 在实际场景中的各种应用，来进一步提升ThreadLocal的战斗力，帮你在现实中解决更加棘手的问题。

接下来就让我们进入ThreadLocal的江湖，首先出场的就是ThreadLocal家族的4个成员。

## ThreadLocal家族

通过上节课的学习，我们知道ThreadLocal是在JDK 1.2中引入的，解决了一个线程中多个方法间信息传递的问题。在生产环境中，为了提升系统的性能，充分发挥多核CPU的优势，我们经常通过增加线程或者异步的方式来更好地发挥底层硬件的性能。

### **InheritableThreadLocal**

在这种情况下，就自然引出了**父子线程**的问题，也就是如何优雅地把父线程的信息传递给子线程，这显然超出了ThreadLocal的能力范围。所以在JDK 1.3 中，JVM 引入了**InheritableThreadLocal**，在创建子线程时将父线程的变量副本复制到子线程中，实现子线程继承父线程的变量副本，从而有效解决父子线程之间参数传递的问题，实现了跨线程的变量传递。
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>那其实threadlocal也没有解决内存泄露的问题，那key设置成弱引用好像也没有太大的作用？请问老师，这么设计可以解决什么问题呢</div>2023-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（0）<div>请教老师两个问题：
Q1：ThreadLocal是用于线程不同方法之间信息传递吗？我感觉这个说法有问题啊。
Q2：ThreadLocal用于父子线程数据传递，只是创建的时候传递一次吗？创建完毕以后还有数据传递吗？</div>2023-10-30</li><br/>
</ul>