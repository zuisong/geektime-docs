前不久在写代码的时候，我不小心踩到一个可变长参数的坑。你或许已经猜到了，它正是可变长参数方法的重载造成的。（注：官方文档建议避免重载可变长参数方法，见\[1]的最后一段。）

我把踩坑的过程放在了文稿里，你可以点击查看。

```
void invoke(Object obj, Object... args) { ... }
void invoke(String s, Object obj, Object... args) { ... }

invoke(null, 1);    // 调用第二个invoke方法
invoke(null, 1, 2); // 调用第二个invoke方法
invoke(null, new Object[]{1}); // 只有手动绕开可变长参数的语法糖，
                               // 才能调用第一个invoke方法

```

当时情况是这样子的，某个API定义了两个同名的重载方法。其中，第一个接收一个Object，以及声明为Object…的变长参数；而第二个则接收一个String、一个Object，以及声明为Object…的变长参数。

这里我想调用第一个方法，传入的参数为(null, 1)。也就是说，声明为Object的形式参数所对应的实际参数为null，而变长参数则对应1。

通常来说，之所以不提倡可变长参数方法的重载，是因为Java编译器可能无法决定应该调用哪个目标方法。

在这种情况下，编译器会报错，并且提示这个方法调用有二义性。然而，Java编译器直接将我的方法调用识别为调用第二个方法，这究竟是为什么呢？

带着这个问题，我们来看一看Java虚拟机是怎么识别目标方法的。

## 重载与重写

在Java程序里，如果同一个类中出现多个名字相同，并且参数类型相同的方法，那么它无法通过编译。也就是说，在正常情况下，如果我们想要在同一个类中定义名字相同的方法，那么它们的参数类型必须不同。这些方法之间的关系，我们称之为重载。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/d9/055e5383.jpg" width="30px"><span>Thomas</span> 👍（41） 💬（10）<div>看明白了......这篇真好</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/12/da/a3ea305f.jpg" width="30px"><span>jiaobuchongจุ๊บ</span> 👍（47） 💬（2）<div>参考老师最后的例子，写了博客总结了一下：https:&#47;&#47;blog.csdn.net&#47;jiaobuchong&#47;article&#47;details&#47;83722193，欢迎拍砖。</div>2018-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（7） 💬（1）<div>Merchant类中actionPrice方法返回值类型为Number
NaiveMerchant类中actionPrice方法返回值类型为Double

NaiveMerchant类生成的字节码中有两个参数类型相同返回值类型不同的actionPrice方法
 Method actionPrice:(DLCustomer;)Ljava&#47;lang&#47;Double;
 Method actionPrice:(DLCustomer;)Ljava&#47;lang&#47;Number; &#47;&#47; 桥接到返回值为double的方法 flags: ACC_PUBLIC, ACC_BRIDGE, ACC_SYNTHETIC

 方法返回值不同为何也要产生桥接方法呢？ 为了保证重写语义？

不知为何javac在编译

NaiveMerchant naiveMerchant = new NaiveMerchant();
Number number = naiveMerchant.actionPrice(1d, null) &#47;&#47; 特意要求Number类型的返回值(方法描述符)

时，总invokevirtual到Method NaiveMerchant.actionPrice:(DLCustomer;)Ljava&#47;lang&#47;Double，这又是为什么呢？

附jdk版本
java version &quot;1.8.0_172&quot;
Java(TM) SE Runtime Environment (build 1.8.0_172-b11)
GraalVM 1.0.0-rc5 (build 25.71-b01-internal-jvmci-0.46, mixed mode)


</div>2018-08-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/ff/295bcf2c.jpg" width="30px"><span>vimfun</span> 👍（6） 💬（1）<div>老师，public final 或 public static final 的方法，是不是在 虚拟机中解析为静态绑定的</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/58/8c8897c8.jpg" width="30px"><span>杨春鹏</span> 👍（4） 💬（3）<div>老师，关于方法调用的字节码指令中的invokespecial:调用实现接口的默认方法。
我测试了一下，发现子类中调用实现接口的默认方法还是使用的invokeinrerface。
</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/6a/ab1cf396.jpg" width="30px"><span>小兵</span> 👍（2） 💬（2）<div>invokespecial：用于调用私有实例方法、构造器，以...和所实现接口的默认方法。
这里所实现接口的默认方法具体是指什么？
</div>2018-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fe/37/ba1bebc0.jpg" width="30px"><span>王侦</span> 👍（2） 💬（1）<div>老师，最后那个例子能不能重新整理一下？说明一下操作步骤。不知道怎么操作！是写在一个文件还是多个文件？而且编译时报两个错误：一个是VIP要有一个类，一个是NaiveMerchant报错？</div>2018-10-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6c/28/a1f9f0ad.jpg" width="30px"><span>陈树义</span> 👍（2） 💬（1）<div>文章开头的例子，我在JDK8环境下写了个例子测试，发现貌似和文中所说的不一致。  不知道是不是因为JDK版本问题，还是我例子有问题？  </div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e7/b1/5c63be67.jpg" width="30px"><span>易水寒</span> 👍（1） 💬（1）<div>给下面某人解释一个问题，final[3][4]指的是参考下面的链接3，4链接，论文当中引用了别人的东西都这么写</div>2018-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/27/48/f793d74d.jpg" width="30px"><span>Go Ashton</span> 👍（1） 💬（2）<div>如果没有找到，在 C 所直接实现或间接实现的接口中搜索” 能否有个例子，什么是直接实现？什么是间接实现？ 可能我知道这是什么，但叫法不同</div>2018-09-18</li><br/><li><img src="" width="30px"><span>preston</span> 👍（1） 💬（1）<div>请问子类可以调用父类的静态方法是什么意思？我有点不太明白。</div>2018-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fd/fc/0a9ec89f.jpg" width="30px"><span>陈勇明</span> 👍（1） 💬（1）<div>如果这两个方法都是静态的，那么子类中的方法隐藏了父类中的方法，这里的隐藏是什么意思？父类的方法调用不到了吗？类C及子类C1都有静态方法m,那么C.m()与C.m()，以及这两个类的实例调用该方法应该都互不影响吧</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/12/87/765a5366.jpg" width="30px"><span>Eric</span> 👍（0） 💬（1）<div>每节课布置的题都没有讲解，让人很困扰。</div>2018-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/43/38/72feb2e0.jpg" width="30px"><span>哇！怎么这么大个</span> 👍（0） 💬（1）<div>”Java 虚拟机识别方法的方式略有不同，除了方法名和参数类型之外，它还会考虑返回类型。”
如果JAVA虚拟机考虑到了返回类型，那么是否可以定义同名类且同名方法相同参数不同返回类型的方法（实际上在ide中会报错，那JAVA虚拟机是出于怎么样的考虑会将返回类型也加入到方法描述符中去）</div>2018-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/85/d0/56602a43.jpg" width="30px"><span>灵活工作</span> 👍（0） 💬（1）<div>这篇文章的课后习题，一个是class merchant一个是class merchant&lt;T extends Merchant&gt;,把这段代码写在一个文件里面会报编译错误，请问老师怎么解决</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/22/aa/c7725dd8.jpg" width="30px"><span>Ennis LM</span> 👍（0） 💬（1）<div>并且，如果目标方法在间接实现的接口中，则需满足 C 与该接口之间没有其他符合条件的目标方法。如果有多个符合条件的目标方法，则任意返回其中一个。

请问C 与该接口之间有其他符合条件的目标方法是什么情况，这里我看不太懂</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/22/aa/c7725dd8.jpg" width="30px"><span>Ennis LM</span> 👍（0） 💬（1）<div>如果这两个方法都是静态的，那么子类中的方法隐藏了父类中的方法。如果这两个方法都不是静态的，且都不是私有的，那么子类的方法重写了父类中的方法。

那如果两个方法不是“都是静态的”，也不是“都不是静态的，且都不是私有的”，这样会是什么情况呢，隐藏？重写？还是都不是</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/ca/1a1e190a.jpg" width="30px"><span>Nu11PointerEx</span> 👍（0） 💬（1）<div>&quot;对于 Java 语言中重写而 Java 虚拟机中非重写的情况&quot;
这种是什么样的情况？</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/00/70/13b33785.jpg" width="30px"><span>蒙奇·D·淡抹🎈</span> 👍（0） 💬（1）<div>开头的坑，我也遇见过，我的例子是：
public void method(String str){
    ...
}
public void method(Object obj){
    ...
}

method(null);一直调用的是string参数的方法</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/d9/055e5383.jpg" width="30px"><span>Thomas</span> 👍（0） 💬（1）<div>老师～接口与接口实现是怎么联系的？</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/81/2c31cf79.jpg" width="30px"><span>永烁星光</span> 👍（201） 💬（11）<div>写的有点晦涩难懂，看了好几遍，还是有点迷糊</div>2018-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/d6/c9/08a62ac7.jpg" width="30px"><span>胡小榕</span> 👍（117） 💬（7）<div>请不要用中文定义类&#47;变量，有强迫症</div>2018-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（47） 💬（4）<div>1:方法重载
方法名相同、方法参数类型不同（其中包括参数的个数、类型、次序，三者之中只要有一个不同就行）。以前的理解方法重载是在一个类内，今天读后感觉类间有继承关系也是存在方法重载的，需要验证一下？

2:方法重写
方法名相同、方法参数类型相同、方法返回值相同，类之间有继承关系，便构成方法重写。
这个概念和之前一样，不过老师强调了父类中的方法是飞私有、非静态的，这个有待验证一下？

3:JVM定位目标方法的关键是类名+方法名+方法参数类型+方法返回值类型，于是就出现了两种JVM找目标方法的方式，静态绑定、动态绑定

4:静态绑定
在解析时JVM便知道该调用那个目标方法

5:动态绑定
在运行时JVM需要根据对应的类类型来具体定位应该调用那个目标方法。对于方法重写，对应的类会拥有一个方法表（一个二维数组表，给方法标上序号，重写的方法序号一致）

听了几遍，也看了几遍，感觉对具体细节还是不清楚，比如：
1:静态绑定具体咋实现的？
2:方法表在那里？啥时候创建的？咋和具体的类关联起来的呢？
可能篇幅有限啊！总体老师讲的很好，有些细节没讲到，我的感觉！</div>2018-07-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/58/c5248989.jpg" width="30px"><span>...</span> 👍（16） 💬（0）<div>没完全理解，上来开头没有好的引入。</div>2019-01-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ff/d1/28adb620.jpg" width="30px"><span>蒙奇•D•273°</span> 👍（12） 💬（2）<div>没完全理解。有个问题，接口符号指向接口方法，但是接口是没有实现的，他的实现在其实现类里面，我理解最终应该指向接口的实现类</div>2018-08-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/a1/65/44853770.jpg" width="30px"><span>Hi Young</span> 👍（11） 💬（0）<div>从一个没有了解过jvm的读者角度看，这篇文章的行文组织没有简单的明确的讲清楚，最初看的一头雾水，看了两遍再+额外查找其他资料+自己写读书笔记才理解。
建议开头时候准确的回答出全部的调用过程，其中涉猎的未知的领域或概念，可以逐步的在后续展开，这样对于初学者来说更友好</div>2020-01-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fb/a7/12c90699.jpg" width="30px"><span>Askerlve</span> 👍（10） 💬（0）<div>任督二脉就靠这个系列打通了～🤑</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（9） 💬（2）<div>需要看三遍</div>2018-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/39/38/4c962666.jpg" width="30px"><span>小贝_No_7</span> 👍（8） 💬（5）<div>如果这两个方法都是静态的，那么子类中的方法隐藏了父类中的方法。

这句没太明白，这个(隐藏)是否有更深一层的意义？</div>2018-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4a/6f/e36b3908.jpg" width="30px"><span>xzy</span> 👍（7） 💬（2）<div>符号引用转实际引用时，对于非接口符号引用的第三条，在该类及父类中没有找到目标方法，便会在其直接和间接实现的接口中查找。如果存在多个符合条件的方法，并不会随机选择一个，而是优先选择拥有最具体实现的默认方法的接口，即如果 B 继承了 A，那么 B 就比 A 更加具体。代码如下：
 interface A {
	default void hello() {
		System.out.println(&quot;Hello form A&quot;);
	}
}
interface B extends A {
	default void hello() {
		System.out.println(&quot;Hello from B&quot;);
	}
}
public class C implements A,B {
	public static void main(String[] args) {
		new C().hello();   &#47;&#47;输出 Hello from B
	}
}

在 java 里如果无法判断谁更具体，则需要在 C 里面显示的覆盖 hello（）方法。</div>2018-10-10</li><br/>
</ul>