你好，我是朱涛。这节课，我们来学习Kotlin的面向对象编程：类、接口、继承、嵌套，以及Kotlin独有的数据类和密封类。

面向对象（Object Oriented）是软件开发方法，也是计算机界应用最广的一种编程范式。它是把程序的“数据”和“方法”作为一个整体来看待，将其抽象成了一个具体的模型，从而更贴近事物的自然运行模式。它的特点是简单易懂，符合人类的思维模式。

在“面向对象”的概念上，虽然Kotlin和Java之间有一定的语法差异，但底层的思想是没有变的。比如Java和Kotlin当中，都有类、接口、继承、嵌套、枚举的概念，唯一区别就在于这些概念在两种语言中的具体语法不同。**我们需要做的，仅仅只是为我们脑海里已经熟知的概念，再增加一种语法规则而已。**

而如果你没有Java基础也没关系，今天这节课要学习的内容，几乎是所有编程语言都需要掌握的概念。在掌握了Kotlin面向对象的编程思想后，如果你再去学习其他编程语言，你也照样可以快速迁移这些知识点。

当然，Kotlin作为一门新的语言，它也创造了一些新的东西，比如数据类、密封类、密封接口等。这些Kotlin的新概念，会是我们需要着重学习的对象。**实际上，也正是因为Kotlin的这些独有概念，使得它形成了一种独特的编程风格和编程思想。**
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/33/ea/373d8e6b.jpg" width="30px"><span>夜班同志</span> 👍（28） 💬（3）<div>应该说明下 密封类是子类固定，枚举是对象固定 吧</div>2022-01-19</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Iofqk26ibmjFxAZKRibgUmwc9p5RDDArr9Jt0NTrwTKOhtPTuuia77OxOwyEUpeqp2fvU5HPpY8sK0vBejJNA3ib3w/132" width="30px"><span>夜月</span> 👍（13） 💬（4）<div>接口的属性：
1.不能设置初始值
2.val可以重写get,var的get和set都不能重写
</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（9） 💬（2）<div>Kotlin 的继承是默认封闭的，这样岂不是要经常修改基础类吗？特别是对于那些开源库来说</div>2022-01-14</li><br/><li><img src="" width="30px"><span>Geek_70c6da</span> 👍（8） 💬（1）<div>请教老师，kotlin对象的深拷贝有什么优雅的写法吗</div>2021-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/77/8b/343fa432.jpg" width="30px"><span>初升的太阳</span> 👍（8） 💬（5）<div>由于我们的密封类只有这三种情况，所以我们的 when 表达式不需要 else 分支。可以看到，这样的代码风格，既实现了类似枚举类的逻辑完备性，还完美实现了数据结构的封装。

没看出来和枚举的区别</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/ed/9cc44242.jpg" width="30px"><span>JakePrim</span> 👍（5） 💬（3）<div>密封类不是很理解，为什么密封类的内部 要使用data class 呢？如何正确的定义密封类？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/45/a7/da9b2d2b.jpg" width="30px"><span>百炼钢</span> 👍（4） 💬（7）<div>密封类的设计目的没太明白，可能我对java的枚举理解不深，导致老师用枚举来解释密封类，让我更糊涂了…    自问：密封类设计目的是为了辅助 when 表达式的使用吗？按文中的例子也可以用继承来实现，那么密封类的作用就是简化代码吗？</div>2022-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/71/c1/cbc55e06.jpg" width="30px"><span>白乾涛</span> 👍（4） 💬（1）<div>val (name, age) = tom

这里的顺序是和构造方法里面的一致呢
还是不需要一致，只需要变量名一样呢</div>2022-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/06/e5/51ef9735.jpg" width="30px"><span>A Lonely Cat</span> 👍（3） 💬（1）<div>相应地，如果想在 Kotlin 当中定义一个普通的内部类，我们需要在嵌套类的前面加上 inner 关键字。

这下面的代码有误，IDE 会报错，我猜朱老师是想写下面这段代码吧
 init {
        println(name)
        foo()
  }</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/c5/95b97dfa.jpg" width="30px"><span>郑峰</span> 👍（2） 💬（1）<div>You can declare properties in interfaces. A property declared in an interface can either be abstract or provide implementations for accessors. Properties declared in interfaces can&#39;t have backing fields, and therefore accessors declared in interfaces can&#39;t reference them.</div>2022-01-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a4/ee/cffd8ee6.jpg" width="30px"><span>魏全运</span> 👍（2） 💬（1）<div>接口成员属性实际编译时都会转成方法，所以如果是Java继承该接口必须实现getter(val 属性)和setter(var 属性)，而如果实现类是kotlin 的则必须定义接口属性为成员变量且添加override 关键字，kotlin的语法糖自动实现了接口属性的getter 和setter 方法。总体使用起来还是很麻烦的，没理解什么场景会需要这样用。</div>2022-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/f2/c7/c5855ff3.jpg" width="30px"><span>l-zesong</span> 👍（2） 💬（1）<div>copy函数是深克隆吗？</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ee/f4/27a5080a.jpg" width="30px"><span>7Promise</span> 👍（2） 💬（2）<div>接口的属性不可以重写setter方法</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/50/c9/1bec2c98.jpg" width="30px"><span>Barry</span> 👍（1） 💬（2）<div>class Person(val name: String, var age: Int) {
     val isAdult 
        get() = age &gt;= 18
}
-----------
age是可变的，在age从17变到18过程中，isAdult就从false变成true了。而isAdult这里用val修饰，是不是用错了，而应该用var修饰？</div>2022-02-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/25/3c/b28426b8.jpg" width="30px"><span>阿白</span> 👍（1） 💬（1）<div>open class Person() { 
    abstract fun walk()
}
文档中这一处示例错了，抽象方法只能定义在抽象类里</div>2022-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/ea/94/77a8acdf.jpg" width="30px"><span>Hongyi Yan</span> 👍（1） 💬（2）<div>kotlin接口的属性也是静态的吧</div>2022-01-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Iofqk26ibmjFxAZKRibgUmwc9p5RDDArr9Jt0NTrwTKOhtPTuuia77OxOwyEUpeqp2fvU5HPpY8sK0vBejJNA3ib3w/132" width="30px"><span>夜月</span> 👍（1） 💬（1）<div>感觉正常的抽象类也能实现那个when的逻辑，就是要多写一个else而已，不知道理解对不对。</div>2022-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1b/fa/44a3e48a.jpg" width="30px"><span>张国庆</span> 👍（1） 💬（1）<div>请教老师，kotlin作用域函数嵌套引起圈复杂度过高有什么好的解决方法么？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c7/5c/94cb3a1a.jpg" width="30px"><span>$Kotlin</span> 👍（0） 💬（1）<div>棒棒棒，昨天刚催更，今天就有了～</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/36/61/54/31a8d7e6.jpg" width="30px"><span>anmi</span> 👍（0） 💬（0）<div>诚然，枚举类的同一个枚举对象的引用是相同的，但是我们使用密封类是图它引用不一样吗？
一个密封类子类有限，我们通过有限的数量来限制它。一个密封类子类可以创建多个对象的话，引用的确不一样，但我们根本不是根据密封类的引用不同来使用它的吧？我们不是根据密封类子类类型来判断吗？
我不明白为什么要这样引出密封类。太奇怪了。</div>2023-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/75/bc/89d88775.jpg" width="30px"><span>Calvin</span> 👍（0） 💬（0）<div>这kotlin的数据类是不是对应的java新出的record记录类？封闭类java也有了！</div>2023-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6c/6f/f378f206.jpg" width="30px"><span>你个叛徒</span> 👍（0） 💬（0）<div>入门 Kotlin 很容易，精通 Kotlin 很难，确实新的语法和编程模式的增多会大大增加程序的设计，就像C++一样内容巨多。</div>2023-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/13/c5/791d0f5e.jpg" width="30px"><span>大列巴</span> 👍（0） 💬（0）<div>那密闭类是否存在继承，接口实现的能力，如果可以，其子类是否具备父类的特性。</div>2023-03-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/35/be/c9/791d0f5e.jpg" width="30px"><span>学不动</span> 👍（0） 💬（0）<div>val (name, age) = tom
按照文档的写法去实现，编译器直接提示错误，kotlin版本是1.3.72  是因为版本的差异导致的吗</div>2023-02-13</li><br/>
</ul>