前不久，“虚拟机”赛马俱乐部来了个年轻人，标榜自己是动态语言，是先进分子。

这一天，先进分子牵着一头鹿进来，说要参加赛马。咱部里的老学究Java就不同意了呀，鹿又不是马，哪能参加赛马。

当然了，这种墨守成规的调用方式，自然是先进分子所不齿的。现在年轻人里流行的是鸭子类型（duck typing）\[1]，只要是跑起来像只马的，它就是一只马，也就能够参加赛马比赛。

```
class Horse {
  public void race() {
    System.out.println("Horse.race()"); 
  }
}

class Deer {
  public void race() {
    System.out.println("Deer.race()");
  }
}

class Cobra {
  public void race() {
    System.out.println("How do you turn this on?");
  }
}
```

(如何用同一种方式调用他们的赛跑方法？)

说到了这里，如果我们将赛跑定义为对赛跑方法（对应上述代码中的race()）的调用的话，那么这个故事的关键，就在于能不能在马场中调用非马类型的赛跑方法。

为了解答这个问题，我们先来回顾一下Java里的方法调用。在Java中，方法调用会被编译为invokestatic，invokespecial，invokevirtual以及invokeinterface四种指令。这些指令与包含目标方法类名、方法名以及方法描述符的符号引用捆绑。在实际运行之前，Java虚拟机将根据这个符号引用链接到具体的目标方法。

可以看到，在这四种调用指令中，Java虚拟机明确要求方法调用需要提供目标方法的类名。在这种体系下，我们有两个解决方案。一是调用其中一种类型的赛跑方法，比如说马类的赛跑方法。对于非马的类型，则给它套一层马甲，当成马来赛跑。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erozFScHpVRM5OCwMW7giaM13NE7gN5iatw9Ozwu93ibRZZjmSmcfzBLSXs8tYtwW7Q2E8eUdy9lGl5A/132" width="30px"><span>Geek_488a8e</span> 👍（43） 💬（2）<div>这篇读的好吃力，我的一个建议，先抛出一个使用方法句柄的代码例子，然后再剖析代码在虚拟机的实际过程。自顶向下的讲，由浅入深，这篇直接自底向上了，咬咬牙读到最后，才发现这是类似反射的模拟方法调用的方法</div>2018-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/04/9a/f2c0a206.jpg" width="30px"><span>ext4</span> 👍（5） 💬（1）<div>雨迪，我看了一下MethodHandle的增操作，即你所提到的bindTo这个API，它貌似只能用于为virtual method绑定第一个参数（即caller的this*指针），并不能普适地为方法绑定一个任意参数（例如把参数列表(int, int)里的第一个参数绑定为常数4）。那么你例子中所提到的更为一般性的柯里化又是怎么实现的呢？</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/20/1299e137.jpg" width="30px"><span>秋天</span> 👍（96） 💬（4）<div>这个东西的应用场景是什么？讲的挺深，联系不起来知识</div>2018-08-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/4e/87e40222.jpg" width="30px"><span>Yoph</span> 👍（40） 💬（1）<div>方法句柄VS反射VS代理：
从访问控制层面来讲，反射需要调用setAccesible()，可能会受到安全管理器的禁止警告；代理有些情况下通过内部类实现，但是内部类只能访问受限的函数或字段；而方法句柄则在上下文中对所有方法都有完整的访问权限，并且不会受到安全管理器的限制，这是方法句柄的优势之一。
从执行速度层面来讲，在上一篇中老师也讲到了反射的性能会受到参数方法、类型的自动装箱和拆箱、方法内联的影响，相对来讲反射算是执行较慢的了（当然并没有和方法句柄通过执行具体操作示例作对比，可能在不同的JVM配置情况下执行情况不一样，比如解释器模式或编译模式下等）；通过代理的方式因调用JAVA函数实现，速度与其它调用函数的速度是一样的，相对较快；而方法句柄可能不会有代理方式那样的执行速度快，但同样会受到JVM等不同的配置导致速度不同，但从JVM设计者的角度来说，应该是力求达到像调用函数一样快的速度，目前可能是达不到的。
从类的开销层面来讲，代理通常声明多个类，需要占用方法区，而方法句柄并不需要像代理一样有多个类的开销，不需要方法区的开销。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fa/18/710018cb.jpg" width="30px"><span>飞翔明天</span> 👍（10） 💬（2）<div>老师说后面会简单一点，但是我到这篇，感觉好难，看不懂了</div>2019-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（9） 💬（0）<div>那么方法句柄是否可以取代反射了呢？</div>2018-08-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0b/59/08065309.jpg" width="30px"><span>雨亦奇</span> 👍（7） 💬（0）<div>个人觉得还是按老师的课程安排来走吧。跳来跳去的讲可能会零散不系统。上面两位的说法我不赞同。</div>2018-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d7/e0/bc774bfb.jpg" width="30px"><span>lornsoul</span> 👍（5） 💬（0）<div>1.将句柄设为常量；
2.将new Foo() 和 new Object() 提到循环体外；
3.参数设置 ‘-Djava.lang.invoke.MethodHandle.CUSTOMIZE_THRESHOLD=1’  （好像作用不大）

‘将方法句柄变成常量’获得的性能提升是怎么来的呢？JVM做了什么优化了吗？

public class Foo {

    public void bar(Object o) {
    }

    static final MethodHandle mh;
    static {
        MethodHandles.Lookup l = MethodHandles.lookup();
        MethodType t = MethodType.methodType(void.class, Object.class);
        MethodHandle mh0 = null;
        try {
            mh0 = l.findVirtual(Foo.class, &quot;bar&quot;, t);
        } catch (NoSuchMethodException | IllegalAccessException e) {
            e.printStackTrace();
        } finally {
            mh = mh0;
        }
    }

    public static void main(String[] args) throws Throwable {
        Foo foo = new Foo();
        Object o = new Object();
        long current = System.currentTimeMillis();
        for (int i = 1; i &lt;= 2_000_000_000; i++) {
            if (i % 100_000_000 == 0) {
                long temp = System.currentTimeMillis();
                System.out.println(temp - current);
                current = temp;
            }
            mh.invokeExact(foo, o);
        }
    }
}</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/4e/87e40222.jpg" width="30px"><span>Yoph</span> 👍（5） 💬（0）<div>方法句柄VS反射VS代理：
从访问控制层面来讲，反射需要调用setAccesible()，可能会受到安全管理器的禁止警告；代理有些情况下通过内部类实现，但是内部类只能访问受限的函数或字段；而方法句柄则在上下文中对所有方法都有完整的访问权限，并且不会受到安全管理器的限制，这是方法句柄的优势之一。
从执行速度层面来讲，在上一篇中老师也讲到了反射的性能会受到参数方法、类型的自动装箱和拆箱、方法内联的影响，相对来讲反射算是执行较慢的了（当然并没有和方法句柄通过执行具体操作示例作对比，可能在不同的JVM配置情况下执行情况不一样，比如解释器模式或编译模式下等）；通过代理的方式因调用JAVA函数实现，速度与其它调用函数的速度是一样的，相对较快；而方法句柄可能不会有代理方式那样的执行速度快，但同样会受到JVM等不同的配置导致速度不同，但从JVM设计者的角度来说，应该是力求达到像调用函数一样快的速度，目前可能是达不到的。
从类的开销层面来讲，代理通常声明多个类，需要占用方法区，而方法句柄并不需要像代理一样有多个类的开销，不需要方法区的开销。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/08/4e/87e40222.jpg" width="30px"><span>Yoph</span> 👍（4） 💬（1）<div>方法句柄其实就是可以取得与反射相同的效果，不过方法句柄使用的代码更简洁。使用方法句柄，可以去掉反射中很多套路化的代码，提高代码的可读性。</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c7/07/5798c17e.jpg" width="30px"><span>小阳</span> 👍（2） 💬（0）<div>思考题： 
   1. 启动时配置参数 -Djava.lang.invoke.MethodHandle.CUSTOMIZE_THRESHOLD=1
   2. 将new Foo（）和 new Object（） 提到到循环外， 具体代码如下 

MethodHandles.Lookup l = MethodHandles.lookup();
MethodType t = MethodType.methodType(void.class, Object.class);
MethodHandle mh = l.findVirtual(Foo.class, &quot;bar&quot;, t);

        long current = System.currentTimeMillis();
        Foo foo = new Foo();
        Object param = new Object();
        for (int i = 1; i &lt;= 2_000_000_000; i++) {
            if (i % 100_000_000 == 0) {
                long temp = System.currentTimeMillis();
                System.out.println(temp - current);
                current = temp;
            }
            mh.invokeExact(foo, param);
        }</div>2020-05-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4d/5e/c5c62933.jpg" width="30px"><span>lmtoo</span> 👍（2） 💬（0）<div>invokedynamic和MethodHandle有啥关系？</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/25/80/fdd5a88f.jpg" width="30px"><span>ゞ﹏雨天____゛</span> 👍（2） 💬（0）<div>有些内容，第一遍读总是看不懂，听不明白，当你多次读了之后，并查阅相关内容后，你会发现雨迪老师讲的内容，真的很到位，值得学习。</div>2019-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/80/bf/3041138b.jpg" width="30px"><span>　素丶　　</span> 👍（2） 💬（1）<div>暂时只能想到把他绑定到一个固定的 “Foo” 实例上。。。。
import java.lang.invoke.*;

public class Foo {
  public void bar(Object o) {
  }

  public static void main(String[] args) throws Throwable {
    MethodHandles.Lookup l = MethodHandles.lookup();
    MethodType t = MethodType.methodType(void.class, Object.class);
	Foo foo = new Foo();
    MethodHandle mh = l.findVirtual(Foo.class, &quot;bar&quot;, t).bindTo(foo);

    long current = System.currentTimeMillis();
    for (int i = 1; i &lt;= 2_000_000_000; i++) {
      if (i % 100_000_000 == 0) {
        long temp = System.currentTimeMillis();
        System.out.println(temp - current);
        current = temp;
       }
       mh.invokeExact(new Object());
    }
  }
}
</div>2018-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4e/85/3096d893.jpg" width="30px"><span>hresh</span> 👍（1） 💬（0）<div>关于方法句柄的权限，自己做了一点小总结，欢迎阅读：https:&#47;&#47;juejin.cn&#47;post&#47;7072735300761419783</div>2022-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/ec/235b74c0.jpg" width="30px"><span>ppyh</span> 👍（1） 💬（1）<div>雨迪老师，在获取方法句柄时，也传参传入了方法的名字了啊，为什么说不关心方法的类名和方法名呢？希望老师解答一下。</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（1） 💬（0）<div>方法句柄就是一个方法的抽象，可用于调用不同类的方法
这个实际用处感觉很少</div>2020-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（1） 💬（0）<div>性能测试下来，反射》final MethodHandle》MethodHandle</div>2019-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/2b/fa/1cde88d4.jpg" width="30px"><span>大俊stan</span> 👍（1） 💬（0）<div>how do you turn this on 笑死了</div>2019-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c6/6a/b3fab71d.jpg" width="30px"><span>鑫</span> 👍（1） 💬（0）<div>invokedynamic与方法句柄的关系是怎么样的?f方法句柄替invokedynamic抽象出调用点?</div>2019-02-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/14/98/0251b8fd.jpg" width="30px"><span>Cy190622</span> 👍（1） 💬（0）<div>当使用方法句柄时，我们不关心方法句柄指向方法的类名或者方法名。
那怎么区分不同类同名方法</div>2019-01-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/BB8CE2wSeZz93JgJviaZ6vXNM0krEaleN7FAURPt8lib1W5uR910p5JyfAGXvZxDSQ7ZRRonxIPuEk8YUnE7H0lQ/132" width="30px"><span>Geek_9dc53b</span> 👍（0） 💬（0）<div>https:&#47;&#47;blog.csdn.net&#47;Herishwater&#47;article&#47;details&#47;123389961</div>2023-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（0） 💬（0）<div>一个具体的使用场景就是：需要使用反射调用方法的地方，优先使用方法句柄；mybitis-spring中有使用</div>2023-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f8/c3/1d557354.jpg" width="30px"><span>o my love</span> 👍（0） 💬（0）<div>神智不清了看的</div>2023-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/fe/a3/414c47cc.jpg" width="30px"><span>旺仔小馒头</span> 👍（0） 💬（0）<div>这篇看不懂，感觉没头没尾呢</div>2022-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e1/82/1c5d285d.jpg" width="30px"><span>(￣o￣) . z Z</span> 👍（0） 💬（0）<div>感觉好懵逼啊。。。</div>2022-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/47/b0/a9b77a1e.jpg" width="30px"><span>冬风向左吹</span> 👍（0） 💬（0）<div>mybatis里面有实际的使用</div>2022-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9d/ec/235b74c0.jpg" width="30px"><span>ppyh</span> 👍（0） 💬（0）<div>还有LambdaForm是怎么来的啊，我看那生成的字节码和java.lang.invoke包下的LambdaForm不一样</div>2021-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/72/89/1a83120a.jpg" width="30px"><span>yihang</span> 👍（0） 💬（0）<div>比喻太精彩！</div>2020-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/85/2d/94b76324.jpg" width="30px"><span>梦想是星空</span> 👍（0） 💬（0）<div>DUMP_CLASS_FILES是怎么用的？生成的文件在哪里？</div>2020-06-22</li><br/>
</ul>