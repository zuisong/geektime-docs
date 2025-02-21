Java语言有很多看起来很相似，但是用途却完全不同的语言要素，这些内容往往容易成为面试官考察你知识掌握程度的切入点。

今天，我要问你的是一个经典的Java基础题目，谈谈final、finally、 finalize有什么不同？

## 典型回答

final可以用来修饰类、方法、变量，分别有不同的意义，final修饰的class代表不可以继承扩展，final的变量是不可以修改的，而final的方法也是不可以重写的（override）。

finally则是Java保证重点代码一定要被执行的一种机制。我们可以使用try-finally或者try-catch-finally来进行类似关闭JDBC连接、保证unlock锁等动作。

finalize是基础类java.lang.Object的一个方法，它的设计目的是保证对象在被垃圾收集前完成特定资源的回收。finalize机制现在已经不推荐使用，并且在JDK 9开始被标记为deprecated。

## 考点分析

这是一个非常经典的Java基础问题，我上面的回答主要是从语法和使用实践角度出发的，其实还有很多方面可以深入探讨，面试官还可以考察你对性能、并发、对象生命周期或垃圾收集基本过程等方面的理解。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/d7/df/fc0a6709.jpg" width="30px"><span>WolvesLeader</span> 👍（177） 💬（4）<div>能不能帮我分析一哈，匿名内部累，访问局部变量时，局部变量为啥要用final来修饰吗？</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/8e/0e4bc2a9.jpg" width="30px"><span>皮卡皮卡丘</span> 👍（52） 💬（1）<div>“将 State 定义为 static，就是为了避免普通的内部类隐含着对外部对象的强引用，因为那样会使外部对象无法进入幻象可达的状态。”这个该怎么理解呢？</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0e/72/2a92a4c1.jpg" width="30px"><span>🎵Children乏</span> 👍（23） 💬（1）<div>用final修饰的class，这可以有效避免 API 使用者更改基础功能，某种程度上，这是保证平台安全的必要手段。这个地方真的很需要个例子去帮助理解。比如大家都知道String类是被final修饰不可被继承，但假如没有被final修饰，很好奇会出现什么样不安全的后果。</div>2018-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/d7/a52e390d.jpg" width="30px"><span>Pantheon</span> 👍（18） 💬（2）<div>杨老师，关于final不能修改我想请教下，代码如下，class util {
    public final Integer info = 123;
}

@Test
public void test() throws NoSuchFieldException, IllegalAccessException {
    util util = new util();
    Field field = util.getClass().getDeclaredField(&quot;info&quot;);
    field.setAccessible(true);
    field.set(util,789);
    System.out.println(field.get(util));
    System.out.println(util.info);
}
这里final修饰的被改了，如果不加accessible这句会报错，刚刚试了几个，似乎是基本数据类型改不了，封装类型都能改，请杨老师解答下我的疑惑，感谢。</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5e/bd/e28f8ce5.jpg" width="30px"><span>ls</span> 👍（13） 💬（1）<div>Java中有说：finalize 有一种用途：在 Java 中调用非 Java 代码，在非 Java 代码中若调用了C的 malloc 来分配内存，如果不调用 C 的free 函数，会导致内存泄露。所以需要在 finalize 中调用它。

面试中会有问：为什么 String 会设计成不可变？想听听老师的解释</div>2018-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1c/7d/ecbf84a8.jpg" width="30px"><span>Do</span> 👍（7） 💬（1）<div>final修饰变量参数的时候，其实理解为内存地址的绑定，这样理解是不是更直观，基本类型指向栈中，引用类型指向堆中。老师后期文章能不能说下java堆栈的区别，还有变量局部变量的生命周期，最好能附上图，加深理解。</div>2018-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/7a/5ffb9d63.jpg" width="30px"><span>张勇</span> 👍（6） 💬（1）<div>匿名内部类为什么访问外部类局部变量必须是final的？private Animator createAnimatorView(final View view, final int position) {
    MyAnimator animator = new MyAnimator();
    animator.addListener(new AnimatorListener() {
        @Override
        public void onAnimationEnd(Animator arg0) {
            Log.d(TAG, &quot;position=&quot; + position); 
        }
    });
    return animator;
}</div>2018-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/9a/e9d32750.jpg" width="30px"><span>Dee1024</span> 👍（4） 💬（1）<div>Cleaner机制没有Finalizer机制那样危险，但仍然是不可预测，也是运行缓慢，同样不能保证他们能够及时执行。所以，尽量避免使用。
正确的关闭资源的打开方式应该是，使用JDK1.7或者以上版本，里面提供的 AutoCloseable 接口，实现该接口以达目的</div>2018-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/95/6f0aad03.jpg" width="30px"><span>loveluckystar</span> 👍（4） 💬（1）<div>个人理解，finalize本身就是为了提供类似c或c++析构函数产生的，由于java中gc本身就是自动进行的，是不希望被干扰的，(就像System.gc()，并不一定起作用)所以与其费心研究如何使用这个，不如老老实实在finally中把该做的事情做了来的实惠。</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d0/63/83236814.jpg" width="30px"><span>老胡</span> 👍（3） 💬（1）<div>Cleaner机制会对jvm回收造成负担，因为gc回收的时候需要检测这个对象十分是Cleaner，然后处理。如果处理过长，十分影响gc的效率。好点方案，容器管理对象，比如spring的sopce，或者对象单利等等，gc负担是一个致命问题，所以Cleaner谨慎使用，甚至应该禁止</div>2018-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/85/bbdcf614.jpg" width="30px"><span>haoz</span> 👍（1） 💬（1）<div>List.of()方法我的jdk1.8中没有 网上也没有相关资料。是不是老师写错了呢?还望老师多多指教！</div>2018-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/ad/19cc513d.jpg" width="30px"><span>程序猿的小浣熊</span> 👍（1） 💬（1）<div>关于copy_on_write实现getter方法可以有例子吗？因为我理解的该原则是懒修改策略，但是不变类不应该不做任何修改么？希望可以解答一下。</div>2018-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/8f/7ecd4eed.jpg" width="30px"><span>FF</span> 👍（1） 💬（1）<div>请教杨老师一个异常处理的问题，我们使用 eclipse 的同学通常这样处理异常：
try{
。。。。
}catch(Exception ex){
throw ex;  &#47;&#47;这里抛出异常，
}

但方法并没有声明 throws Exception，而  eclipse  通常也能编译执行，这不是违反了基本语法了吗，为何 eclipse 里面没有任何问题的？

这是什么原因？但这样的代码在使用 IntellIj  IDEA  的同学那里是完全没法编译执行的，直接就提示语法错误了

很困惑，网上没找到相关答案，望解答，感谢！</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fc/24/7d43d807.jpg" width="30px"><span>mongo</span> 👍（1） 💬（1）<div>final修饰引用类型的话，引用值不能被修改。但是引用值指向的内容可以被修改，这样看来修饰引用类型并不是线程安全的。什么场景下会使用final修饰引用类型呢？</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/77/cc2817b9.jpg" width="30px"><span>曲水流觞TechRill</span> 👍（0） 💬（1）<div>关于匿名内部类访问局部变量必须final的原因，还有一个关键是匿名内部类的生命周期可能比外部类要长，而如果外部类已经被垃圾回收了，那内部类访问的就是一个空变量。final可以防止被回收，老师对么？</div>2018-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d6/7c/979429d8.jpg" width="30px"><span>Z</span> 👍（0） 💬（1）<div>有List.of（）方法吗我怎么找不到</div>2018-05-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/8b/11c87d4e.jpg" width="30px"><span>櫻の空</span> 👍（0） 💬（1）<div>说到final的话，现在更多的会谈到static.许多代码都会使用到static final来同时修饰一个变量(这里称为常量更合适哈)。从而可以达到一个编译期常量的作用。这可以使得我们不需要初始化一个类就能够直接访问其成员，对节约资源效率上有不少的提升。
所以我觉得老师可以顺带提一下static,或者放些补充学习的资料哈。
而以上东西其实可以进一步深挖，这就会关系到老师在第一讲提到过的类加载，验证，链接，初始化。这个过程，介于篇幅原因未能进一步展开，有兴趣的同学可以翻看TIJ和深入理解JVM进行学习哈。
以上是个人理解，若有错误，还望指正。
</div>2018-05-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/10/ff/dcd5b47e.jpg" width="30px"><span>李润林</span> 👍（0） 💬（1）<div>finalize应该是从c++的析构函数那里继承来的一个东西，随着垃圾收集算法的不断改进，变得完全不可控了。</div>2018-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/1a/7a/5ffb9d63.jpg" width="30px"><span>张勇</span> 👍（0） 💬（1）<div>老师咨询下，我小面这段代码String类型的参数用final修饰为啥我每次可以穿不同的参数进去，并且也可以运行成功final不是不可变么，public class MainActivity extends AppCompatActivity {
private static final String TAG=&quot;MainActivity&quot;;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        test(&quot;AAAAAAA&quot;);
        test(&quot;BBBBBBB&quot;);
        test(&quot;CCCCCCC&quot;);
        test(&quot;DDDDDDD&quot;);
    }

 public void test(final String  str){
     Log.d(TAG,str);
 }   

}</div>2018-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/8f/7ecd4eed.jpg" width="30px"><span>FF</span> 👍（0） 💬（1）<div>IDEA 的版本是2018.1.2，throw 一个方法没有声明的受检查 ex 也是合规的写法吗？即使 try 里面没有显示 throw</div>2018-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f9/8d/f56b4cb9.jpg" width="30px"><span>独嘉记忆</span> 👍（0） 💬（1）<div>老师，能否之后多开几讲，两三千字的限制怕知识点后面不够或者没法深入。</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/ba/d28174a9.jpg" width="30px"><span>Geek_zbvt62</span> 👍（0） 💬（1）<div>之前甚至不知道有cleaner这回事...希望杨老师后面有机会详细说说</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0a/b7/4d7b6a79.jpg" width="30px"><span>sharp</span> 👍（909） 💬（18）<div>这三个就是卡巴斯基和巴基斯坦的关系，有个基巴关系。。。</div>2018-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/a1/43d83698.jpg" width="30px"><span>云学</span> 👍（223） 💬（9）<div>请问这篇文章中涉及的知识点是java中最重要的吗？我感觉有点剑走偏锋，这种知识了解就好了，应该有很多知识比这更重要的吧，虽说面试中可能会问，但不能以面试为中心，而要把实际应用中最有用的真正核心的东西分享出来，把它讲透彻，不追求面面俱到，也不想成为语言专家，我期望通过这个专栏可以获得java中最核心最实用特性的本质认识，希望有一种醍醐灌顶的感觉，在阅读java开源框架代码时不再困惑。我有多年的c++开发背景，希望通过这个专栏对java也有提纲契领的本质认识。</div>2018-06-12</li><br/><li><img src="" width="30px"><span>zjh</span> 👍（218） 💬（5）<div>一直不懂为什么这三个经常拿来一起比较，本身就一点关系都没有啊，难道仅仅是长的像。我觉得final倒是可以和volatile一起比较下</div>2018-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/0f/4f/c75c4889.jpg" width="30px"><span>石头狮子</span> 👍（192） 💬（0）<div>列几个 fianlly 不会被执行的情况:
1. try-cach 异常退出。
try{
system.exit(1)
}finally{
print(abc)
}

2. 无限循环
try{
  while(ture){
    print(abc)
  }
}finally{
print(abc)
}

3. 线程被杀死
当执行 try，finally 的线程被杀死时。finally 也无法执行。


总结
1，不要在 finally 中使用 return 语句。
2，finally 总是执行，除非程序或者线程被中断。</div>2018-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2f/0f/3144a61f.jpg" width="30px"><span>★神峰★</span> 👍（146） 💬（0）<div>你们都看懂了吗？我怎么什么都不知道😂 </div>2018-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/16/5b/83a35681.jpg" width="30px"><span>Monday</span> 👍（93） 💬（6）<div>前提本节听了4遍，看了不下3遍，所花的时间大于4小时，写点心得与疑问。
一道如此“简单”的面试题，能够引申出性能、安全、GC的问题，再扩展出一些我以前没接触过或知之甚少的知识点，如Cleaner、try-catch-resources、编写immutable对象、幻象引用等等。
还有一些读起来很简单的语句，消化起来却很吃力，如：你无法保证finalize什么时候执行，执行是否符合预期。使用不当会影响性能，导致程序死锁，挂起等。又如：final class可以有效的避免API使用者更改基础功能，某种程度上，这是保证平台安全的必要手段。
疑问如下：
1、本文中自己不熟悉的知识点，需要每一种都花时间去死扣吗？
2、finalize使用不当会影响性能，导致程序死锁，挂起等，可否举几个通俗易懂的案例？
3、final class可以有效的避免API使用者更改基础功能，某种程度上，这是保证平台安全的必要手段。可否举知名案例证实若某类不设计为final class会导致更改其原有功能，进而影响平台安全？</div>2018-09-26</li><br/><li><img src="" width="30px"><span>Loong</span> 👍（66） 💬（0）<div>final、finally、finalize

1. final
	修饰类：不可被继承
	修饰方法：不可重写
	修饰变量：不可修改，只能约束引用不可以被再次赋值。匿名内部类访问局部变量时需要使用 final，因为 Innerclass 实际会 copy 一份局部变量，final 可以防止出现数据一致性问题

2. finally：Java 保证重点代码一定要被执行的机制，try - finally，除非在 finally 前执行了 System.exit（1）、try 中死循环、线程被杀死
	
3. finalize：基础类 Object 的一个方法，保证对象在被垃圾收集前完成特定的资源回收。由于 finalize 执行时间不确定且可能造成程序死锁、拖慢垃圾收集等问题，Java 9 中将改方法废弃
		优化：使用 Cleaner 配合幻想引用</div>2018-12-03</li><br/><li><img src="" width="30px"><span>有渔@蔡</span> 👍（34） 💬（0）<div>1.你说那异常被生吞，是指没写e.print...语句吧？另外我有个疑惑：super.clear()为什么写在exception里，理论上super方法写第一行，或finally里。2.在一个对象的生命周期里，其finalize方法应该只会被调用1次。3.强软弱虚引用大家都知道，这虚幻引用相比较有什么特别的吗？请再深入点。4.final是不是都在编译后确定位置？比如final List这样的，内存布局是怎样的？谢谢</div>2018-05-10</li><br/>
</ul>