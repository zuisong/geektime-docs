你好，我是康杨。

Java 作为一门面向对象的编程语言，在近年来也逐步拥抱了函数式编程。在 JDK 8 中，引入了 Lambda 表达式和 Stream API，为 Java 开发者提供了更简洁、更易读的编写方式。今天我们来详细聊聊JDK 对函数式编程的支持，以及 JDK 中的各种函数式接口，并通过丰富的场景案例和实践，让你轻松掌握 Java 的函数式编程。

## JDK 函数式接口

函数式接口是Java 8引入的一种新特性，它有点像一种“超级接口”，因为它只有一个抽象方法，但却可以以Lambda表达式的形式被实例化和执行。在JDK中，Function、Predicate和Consumer是最常用的函数式接口。在开发过程中，有时候可能我们需要的功能在JDK中并没有现成的实现，但是借助于函数式接口，我们就可以很方便地自定义自己需要的功能。

首先，我们来看看**Function接口**。在我们的日常生活里也有类似的例子，比如能够把苹果转变为苹果汁的机器，其实就是一个Function，它把一个输入转变为一个输出。在Function接口中，有一个主要的方法，就是apply，它可以把输入的东西转变成输出的东西。例如，我们可以实现一个Function，把字符串变成整数。这个Function就像一个黑盒子，你给它一个字符串，它就会给你一个整数。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（1） 💬（0）<div>能不能加餐讲下java新版本的虚拟线程呢。</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（1）<div>请教老师问题：
Q1：案例1中，Function类型的square怎么没有apply？
Function接口只有一个方法apply，怎么定义的square没有apply?
Q2：案例2中，Predict类型的hasEvenLength怎么没有test?
Predict接口只有一个方法test，怎么定义的hasEvenLength没有test?</div>2023-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/59/af/d2107a67.jpg" width="30px"><span>二九幂加八</span> 👍（0） 💬（0）<div>老师，Stream API处理数据会不会造成OOM？如果会出现OOM的情况，应该如何处理这种情况？</div>2023-11-06</li><br/>
</ul>