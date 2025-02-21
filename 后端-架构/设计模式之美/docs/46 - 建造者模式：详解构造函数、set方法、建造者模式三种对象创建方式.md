上两节课中，我们学习了工厂模式，讲了工厂模式的应用场景，并带你实现了一个简单的DI容器。今天，我们再来学习另外一个比较常用的创建型设计模式，**Builder模式**，中文翻译为**建造者模式**或者**构建者模式**，也有人叫它**生成器模式**。

实际上，建造者模式的原理和代码实现非常简单，掌握起来并不难，难点在于应用场景。比如，你有没有考虑过这样几个问题：直接使用构造函数或者配合set方法就能创建对象，为什么还需要建造者模式来创建呢？建造者模式和工厂模式都可以创建对象，那它们两个的区别在哪里呢？

话不多说，带着上面两个问题，让我们开始今天的学习吧！

## 为什么需要建造者模式？

在平时的开发中，创建一个对象最常用的方式是，使用new关键字调用类的构造函数来完成。我的问题是，什么情况下这种方式就不适用了，就需要采用建造者模式来创建对象呢？你可以先思考一下，下面我通过一个例子来带你看一下。

假设有这样一道设计面试题：我们需要定义一个资源池配置类ResourcePoolConfig。这里的资源池，你可以简单理解为线程池、连接池、对象池等。在这个资源池配置类中，有以下几个成员变量，也就是可配置项。现在，请你编写代码实现这个ResourcePoolConfig类。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/86/25/25ded6c3.jpg" width="30px"><span>zhengyu.nie</span> 👍（47） 💬（2）<div>依赖关系（Dependencies）、合法校验（Preconditions）、不可变（Immutable）。
争哥这几个描述很精准！
借着思路延伸一下的话，很多库和设计都是以上这些理念的。
比如com.google.guava的校验、不可变集合，多线程设计模式中的Immutable模式、保护性拷贝（其中又可以分深浅api），java.lang.String的不可变设计。还有关于类状态的控制，还有Effective Java中类创建这一章中对于构造方法、set方法、Builder构建、枚举、静态工厂方法构建等对比，像Guava Lists、Sets、Maps、ImmutableList这种创建方式现在也很主流了</div>2020-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/12/6c/61a598e9.jpg" width="30px"><span>苏暮沉觞</span> 👍（4） 💬（1）<div>       小争哥，我在学习建造者模式的时候，发现传统的构建者模式写法跟文中的不太一样，传统的构建者模式存在监工，抽象Builder，具体Builder，产品类。可以通过不同的具体Builder，创建对应的产品类。而你在文章中的设计模式的写法，在某些文章中，被称为变种的构造者模式。
       我比较了一下两种方式，感觉传统的构建者模式需要提前定义好你要生产的产品对应的属性，而文中这种方法则是在构建产品时，自己动态的设置产品属性，虽然说这种方法更加灵活，但是侵入性更高。
      那么考虑到以后需求变更，是不是应该是用传统的构建者模式呢？不然要是资源池对应的参数变了，就要修改业务代码中的参数了。</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/96/31/d3a58c6f.jpg" width="30px"><span>是非～成败～</span> 👍（1） 💬（2）<div>&#47;**
 * 需求：
 * 当 isRef 为 true 的时候，arg 表示 String 类型的 refBeanId，type 不需要设置；
 * 当 isRef 为 false 的时候，arg、type 都需要设置。
 * 请根据这个需求，完善 ConstructorArg 类。
 *&#47;
public class ConstructorArg_02 {
    private boolean isRef;
    private Class type;
    private Object arg;

    private ConstructorArg_02(Builder builder) {
        this.isRef = builder.isRef;
        this.type = builder.type;
        this.arg = builder.arg;
    }

    public static class Builder {
        private boolean isRef;
        private Class type;
        private Object arg;

        &#47;&#47; 后面两个参数依赖isRef，所以isRef设置成必选参数
        public Builder(boolean isRef) {
            this.isRef = isRef;
        }

        public ConstructorArg_02 build() {
            return new ConstructorArg_02(this);
        }

        public Builder setType(Class type) {
            this.type = type;
            return this;
        }

        public Builder setArg(Object arg) {
            &#47;&#47; isRef为true, arg不是String类型就报错
            if (isRef &amp;&amp; arg.getClass() != String.class) {
                throw new RuntimeException(&quot;参数错误&quot;);
            }
            this.arg = arg;
            return this;
        }
    }
}
咱也不知道写的好不好，希望争哥看到了检视指导一二</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/36/ef/83c2a743.jpg" width="30px"><span>悠南</span> 👍（1） 💬（3）<div>你这建造者模式代码，看不懂，构造方法私有了，怎么来的Builder 方法</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c8/5d/1e3685e6.jpg" width="30px"><span>Morse</span> 👍（0） 💬（5）<div>为什么定义了一个长方形类，如果不使用建造者模式，采用先创建后 set 的方式，那就会导致在第一个 set 之后，对象处于无效状态？求大佬解答</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/26/38/ef063dc2.jpg" width="30px"><span>Darren</span> 👍（128） 💬（4）<div>简单理解就是：工厂模式是根据不同的条件生成不同Class的对象，构建者模式是根据不同参数生成一个class的不同对象。</div>2020-04-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（114） 💬（13）<div>public class ConstructorArg {
    private boolean isRef;
    private Class type;
    private Object arg;

    public boolean isRef() {
        return isRef;
    }

    public Class getType() {
        return type;
    }

    public Object getArg() {
        return arg;
    }

    private ConstructorArg(Builder builder) {
        this.isRef = builder.isRef;
        this.type = builder.type;
        this.arg = builder.arg;
    }

    public static class Builder {
        private boolean isRef;
        private Class type;
        private Object arg;

        public ConstructorArg build() {
            if(isRef &amp;&amp; type != null) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }

            if (!isRef &amp;&amp; type == null) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }

            if (this.isRef &amp;&amp; (arg != null &amp;&amp; arg.getClass() != String.class)) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }

            if (!this.isRef &amp;&amp; arg == null) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }

            return new ConstructorArg(this);
        }

        public Builder setRef(boolean ref) {
            if(ref &amp;&amp; this.type != null) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }
            this.isRef = ref;
            return this;
        }

        public Builder setType(Class type) {
            if (this.isRef || type == null) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }
            this.type = type;
            return this;
        }

        public Builder setArg(Object arg) {
            if (this.isRef &amp;&amp; (arg != null &amp;&amp; arg.getClass() != String.class)) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }

            if (!this.isRef &amp;&amp; arg == null) {
                throw new IllegalArgumentException(&quot;...&quot;);
            }
            this.arg = arg;
            return this;
        }
    }
}</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/2f/7a/ab6c811c.jpg" width="30px"><span>相逢是缘</span> 👍（55） 💬（4）<div>打卡
一、使用场景：
1）类的构造函数必填属性很多，通过set设置，没有办法校验必填属性
2）如果类的属性之间有一定的依赖关系，构造函数配合set方式，无法进行依赖关系和约束条件校验
3）需要创建不可变对象，不能暴露set方法。
（前提是需要传递很多的属性，如果属性很少，可以不需要建造者模式）
二、实现方式：
把构造函数定义为private，定义public static class Builder 内部类，通过Builder 类的set方法设置属性，调用build方法创建对象。

三、和工厂模式的区别：
1）工厂模式：创建不同的同一类型对象（集成同一个父类或是接口的一组子类），由给定的参数来创建哪种类型的对象；
2）建造者模式：创建一种类型的复杂对象，通过很多可设置参数，“定制化”的创建对象</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/44/47/3ddb94d0.jpg" width="30px"><span>javaadu</span> 👍（52） 💬（0）<div>课堂讨论题：

&#47;**
 * 在下面的 ConstructorArg 类中，
 * 当 isRef 为 true 的时候，arg 表示 String 类型的 refBeanId，type 不需要设置；
 * 当 isRef 为 false 的时候，arg、type 都需要设置
 *
 * @author javaadu
 *&#47;
public class ConstructorArg {
    private boolean isRef;
    private Class type;
    private Object arg;

    private ConstructorArg(Builder builder) {
        this.isRef = builder.isRef;
        this.type = builder.type;
        this.arg = builder.arg;
    }

    public static class Builder {
        private boolean isRef;
        private Class type;
        private Object arg;

        public ConstructorArg build() {
            if (arg == null) {
                throw new IllegalArgumentException(&quot;arg必须设置&quot;);
            }
            if (isRef) {
                if (!(arg instanceof String)) {
                    throw new IllegalArgumentException(&quot;arg必须为String类型的对象&quot;);
                }
            } else {
                if (type == null) {
                    throw new IllegalArgumentException(&quot;arg必须设置&quot;);
                }
            }

            return new ConstructorArg(this)
        }

        public Builder setRef(boolean ref) {
            isRef = ref;
            return this;
        }

        public Builder setArg(Object arg) {
            this.arg = arg;
            return this;
        }

        public Builder setType(Class type) {
            this.type = type;
            return this;
        }
    }
}</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（18） 💬（0）<div>说说自己读了 Builder 模式的最大感悟：
1、Builder 模式可以保证对象的状态。
2、Builder 模式可以把对象的构造鉴定逻辑写在Builder类中，保证了类的简洁。

平时普普通通地使用 lombok 生成 Builder，应该更加深入地了解一下。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（12） 💬（2）<div>打卡~
最近半年用的最多的就是Builder模式了</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/c1/66/e8dfeef4.jpg" width="30px"><span>王涛</span> 👍（9） 💬（0）<div>最近，在学习本专栏的过程中。
逐渐体会到“知其然，更知其所以然”的感觉
</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a0/a3/8da99bb0.jpg" width="30px"><span>业余爱好者</span> 👍（7） 💬（0）<div>创建型模式的作用在于，将对象“获取”（没有用创建）的过程独立出来，形成单独的类。这在获取复杂或者有特殊需求的对象时可以更好的体现单一职责原则---我负责拿到（ready to use）对象,你只管使用就可以了。你不需要关系我是不是懒加载之类的问题。

一个可以使用的对象，它的意义绝不单单是new一下就完事了，还有一系列其他的考量。
如果要求一个类只有一个全局唯一的对象，如基本不变化的配置信息类，这就是单例模式。如何控制只有一个对象，当然是拦截掉所有其他创建对象的路径，只留下一条路---使用类唯一的静态方法获取对象。这就是为什么，单例一般都要求将构造方法私有化。（spring的单例bean其实只是一种单例的约定，你完全可以自己new一个。）单例模式还设计到懒加载的问题，不过由于只有一个访问入口，处理起来比较简单。

工厂模式就比较纯粹了，工厂的意义就是在于获取一个对象。简单工工厂类如果是无状态的话，完全可以使用静态方法的形式，没有必要每创建一个对象都先弄个完全一样的工厂出来。
当需要有根据不同情况创建不同子类的时候，如果分支不多的话，完全可以使用if else,不过也可以考虑使用多态。不同的情况创建不同的工厂，将相应子类各异的创建逻辑分开。这就是工厂方法。
而如果是创建一个产品系列的话，就使用抽象工厂模式。

建造者用于处理创建参数过多的情形，同时可以校验参数，避免对象创建过程中的不一致状态。

原型用于快速拷贝一个对象。</div>2020-08-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/93/c7/86352ccc.jpg" width="30px"><span>1024</span> 👍（7） 💬（2）<div>做了一下课后题，和其他同学的答案比较了下，还是有些疑惑，疑惑在属性的判断逻辑是放在Builder的setAttr()内还是放在build()内
个人认为：
setAttr()放属性自己的逻辑判断，比如不要为null，不能大于或小于某个常量
build()方法放多个属性间的校验逻辑，因为调用builde()时，属性都set完成，这时候才有机会通过builde()来全局考虑所有属性的逻辑。
基于此，我的答案如下
public class ConstructorArg {
    private boolean isRef;
    private Class type;
    private Object arg;

    private ConstructorArg(Builder builder) {
        this.isRef = builder.isRef;
        this.type = builder.type;
        this.arg = builder.arg;
    }
    &#47;&#47; 省略getter方法

    public static class Builder {
        private Object arg;
        private Class type;
        private boolean isRef;

        private ConstructorArg build() {
            if (isRef) {
                if (!(arg instanceof String)) {
                    &#47;&#47;这里refBeanId是ConstructorArg吗？只是判断了下arg类型是否为String
                    throw new IllegalArgumentException(&quot;当 isRef 为 true 的时候，arg 表示 String 类型refBeanId&quot;);
                }
                if (type != null) {
                    throw new IllegalArgumentException(&quot;当 isRef 为 true 的时候，type 不需要设置&quot;);
                }
            }
            if (!isRef) {
                if (arg == null || type == null) {
                    throw new IllegalArgumentException(&quot;当 isRef 为 false 的时候，arg、type 都需要设置&quot;);
                }
            }
            return new ConstructorArg(this);
        }

        public Builder setRef(boolean ref) {
            isRef = ref;
            return this;
        }

        public Builder setArg(Object arg) {
            this.arg = arg;
            return this;
        }

        public Builder setType(Class type) {
            this.type = type;
            return this;
        }
    }
public static void main(String[] args) {
        ConstructorArg.Builder builder = new ConstructorArg.Builder();
&#47;&#47;        java.lang.IllegalArgumentException: 当 isRef 为 true 的时候，arg 表示 String 类型refBeanId
        builder.setRef(true).setArg(1).build();
    }</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（7） 💬（0）<div>用php实现了一个
&lt;?php
class ResourcePoolConfig{
    private $maxTotal;
    private $maxIdle;
    private $minIdle;
    public function __construct(build $build)
    {
        $this-&gt;maxTotal = $build-&gt;maxTotal;
        $this-&gt;maxIdle = $build-&gt;maxIdle;
        $this-&gt;minIdle = $build-&gt;minIdle;
        echo &#39;maxTotal&#39;.$this-&gt;maxTotal;
        echo &#39;&lt;br &#47;&gt;&#39;;
        echo &#39;maxIdle&#39;.$this-&gt;maxIdle;
        echo &#39;&lt;br &#47;&gt;&#39;;
        echo &#39;minIdle&#39;.$this-&gt;minIdle;
        echo &#39;&lt;br &#47;&gt;&#39;;
    }
}

class Builder{
    public $maxTotal;
    public $maxIdle;
    public $minIdle;
    public function noodleValidate(){
        if($this-&gt;maxIdle&gt;$this-&gt;maxTotal){
            throw new Exception(&quot;maxIdle抛出异常&quot;);
        }
        if($this-&gt;minIdle&gt;$this-&gt;maxTotal){
            throw new Exception(&quot;minIdle抛出异常&quot;);
        }
    }

    public function setMaxTotal($value=20){
        $this-&gt;maxTotal = $value;
        return $this;
    }

    public function setMaxIdle($value=10){
        $this-&gt;maxIdle = $value;
        return $this;
    }

    public function setMinIdle($value=10){
        $this-&gt;minIdle = $value;
        return $this;
    }
}

$b = new Builder();
$b-&gt;setMaxTotal(5)-&gt;setMaxIdle()-&gt;setMinIdle()-&gt;noodleValidate();
new ResourcePoolConfig($b);</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4e/d0/d8a5f720.jpg" width="30px"><span>Ken张云忠</span> 👍（7） 💬（2）<div>public class ConstructorArg {
    private boolean isRef;
    private Class type;
    private Object arg;
    public ConstructorArg(ConstructorArgBuilder builder) {
        this.isRef = builder.isRef;
        this.type = builder.type;
        this.arg = builder.arg;
    }
    public static class ConstructorArgBuilder {
        private boolean isRef;
        private Class type;
        private Object arg;
        public ConstructorArg builder() {
            if (arg == null) {
                throw new IllegalArgumentException(&quot;arg should not be null&quot;);
            }
            if (isRef == true) {
                if (arg instanceof String) {
                    type = String.class;
                } else {
                    throw  new IllegalArgumentException(&quot;when isRef is true,arg should be String type&quot;);
                }
            } else {
                type = arg.getClass();
            }
            return new ConstructorArg(this);
        }
        public ConstructorArgBuilder(boolean isRef) {
            this.isRef = isRef;
        }
        public ConstructorArgBuilder setArg(Object arg) {
            this.arg = arg;
            return this;
        }
    }
}
 &#47;&#47; use case
ConstructorArg constructorArg = new ConstructorArgBuilder(true).setArg(0).builder();
ConstructorArg constructorArg1 = new ConstructorArgBuilder(false).setArg(1).builder();</div>2020-02-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/bvj76PmeUvW8kokyu91IZWuRATKmabibDWbzAj2TajeEic7WvKCJOLaOh6jibEmdQ36EO3sBUZ0HibAiapsrZo64U8w/132" width="30px"><span>梦倚栏杆</span> 👍（6） 💬（2）<div>“如果我们并不是很关心对象是否有短暂的无效状态”

中间短暂的无效状态会怎么样呢？没理解。是在多线程下会有问题吗？如果是，如果是类对象，这本身一组操作就应该加锁，如果是方法内部不存在线程安全问题，所以没理解短暂的无效状态会怎么样


</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/a1/b08f3ee7.jpg" width="30px"><span>何妨</span> 👍（6） 💬（0）<div>建造者模式:用于已知类创建，创建构造复杂需校验参数的类
工厂模式:用于未知类创建，根据传入参数创建相似的类处理不同逻辑</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（5） 💬（1）<div>课后讨论题：

 public class ConstructorArg {
    private boolean isRef;
    private Class type;
    private Object arg;
    &#47;&#47; TODO: 待完善...

    private ConstructorArg(Builder builder) {
        this.isRef = builder.isRef;
        this.type  = builder.type;
        this.arg   = builder.arg;
    }

    public static class Builder {
        private boolean isRef;
        private Class type;
        private Object arg;

        public ConstructorArg build() {
            if (!isRef) {
                if (type == null || arg == null){
                    throw new IllegalArgumentException(&quot;type and arg must be set when isRef is false&quot;)
                }
            } else {
                if (!(arg instanceof String)) {
                    throw new IllegalArgumentException(&quot;arg must be a String instance when isRef is true&quot;)
                }
            }
            return new ConstructorArg(this);
        }
    }

    public Builder setIsRef(boolean isRef){
        this.isRef = isRef;
        return this;
    }

    public Builder setType(Class type) {
        this.type = type;
        return this;
    }

    public Builder setObject(Object arg) {
        this.arg = arg;
        return this;
    }
  }

  &#47;&#47;use case
  ConstructorArg ca = ConstructorArg.Builder()
        .setIfRef(false)
        .setType(Integer)
        .setObject(2)
        .build();</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/02/828938c9.jpg" width="30px"><span>Frank</span> 👍（4） 💬（0）<div>当在开发中需要创建一个具体的对象，如果必填属性很多，属性存在复杂的校验和属性之间存在依赖关系，可以使用建造者模式来避免类的构造函数参数列表过长，导致可读性差，不易使用的问题。建造者模式可以将类的构造方法私有，不提供类的setter方法，因此可以创建一个不变的对象。同时在某些场景下将属性构造好可以解决类的无效状态。
使用思路：把校验逻辑放置到 Builder 类中，先创建建造者，并且通过 set() 方法设置建造者的变量值，然后在使用 build() 方法真正创建对象之前，做集中的校验，校验通过之后才会创建对象。除此之外，我们把主类的构造函数为了private 私有权限，只能通过建造者来创建 类对象，并且主类没有提供任何 set() 方法，这样创建出来的对象就是不可变对象了。</div>2020-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（4） 💬（1）<div>建造者模式核心代码:
ResourcePoolConfig config = new ResourcePoolConfig.Builder()
        .setName(&quot;dbconnectionpool&quot;)
        .setMaxTotal(16)
        .setMaxIdle(10)
        .setMinIdle(12)
        .build();</div>2020-02-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/QYKSUV20DMgBHAPLfgngdw4N8FHRCSBLCJueVRu9Ya1Ba2x4icx70zoVVFOZtG1K6TkHj5CFbuztQhRFyCjWXHQ/132" width="30px"><span>zaab</span> 👍（3） 💬（0）<div>写得真好，之前看了几次不知道建造者模式的作用，不知道为啥看了一下这篇我就理解了。。</div>2020-12-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIma3PJUyqDEQKt40nEh3Jt840af6hKnuK8k8dIscm43EUzJwLvynbxRnvO9Ivibv7KssUSqoBdY1w/132" width="30px"><span>PHP是世界上最好的需要</span> 👍（3） 💬（6）<div>总感觉只是把校验逻辑挪到了bulder 里。没直观的感觉到builder 的有点呢。老师~</div>2020-02-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKhABWsNOGReVBNqwYCn52ibbaog3AWU6lPRARibCkibhlNf885vaQPQ8n37ic4wFr7HMBw2wRLcpYkcw/132" width="30px"><span>小学生</span> 👍（2） 💬（3）<div>参数搞成一个类，传入构造函数是否也可以解决参数过长+校验的问题？</div>2020-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/68/ba/c0cf8bf3.jpg" width="30px"><span>天天向上卡索</span> 👍（2） 💬（0）<div>在 .net core 大量使用了 builder 模式代码</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e4/2e/899a8fa2.jpg" width="30px"><span>Riley</span> 👍（2） 💬（1）<div>1、请问lombox中@builder思想是不是来自建造者模式的思想？
2、 还有网上很多人不建议用lombox插件，请问你对此有何建议？</div>2020-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（2） 💬（3）<div>感觉课后思考题的arguments逻辑判断相对复杂，再加上想尝试一下建造者模式，所以抛砖引玉，给一个Python的尝试，有一个困惑是对于Python这种语言，如何避免对用户暴露在调用builder之前build方法之前初始化的ConstructorArg对象？

class ConstructorArg(object):
    def __init__(self, isRef):  #如何避免暴露这个实例对象？
        self.isRef = isRef
        self.type = None
        self.arg = None
    
    def __repr__(self):
        string = f&quot;isRef:  {self.isRef}\n&quot; + \
                 f&quot;type:   {self.type}\n&quot; + \
                 f&quot;arg:    {self.arg}\n&quot;
        return string

    class ConstructorArgBuilder(object):
        def __init__(self, isRef):
            self.constructorArg = ConstructorArg(isRef)

        def addType(self, typeObj):
            self.constructorArg.type = typeObj
            return self

        def addArg(self, argObj):
            self.constructorArg.arg = argObj
            return self

        def build(self):
            if self.constructorArg.isRef:
                if self.constructorArg.type is None:
                    raise Exception(&quot;type cannot be None when isRef&quot;)
                elif not isinstance(self.constructorArg.type, str):
                    raise Exception(&quot;type must be string when isRef&quot;)
            elif not self.constructorArg.isRef:
                if self.constructorArg.type is None:
                    raise Exception(&quot;type cannot be None when not isRef&quot;)
                if self.constructorArg.arg is None:
                    raise Exception(&quot;arg cannot be None when not isRef&quot;)
            return self.constructorArg</div>2020-02-17</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLe9iavda8ia7vNkbMVEHsCKs43l6U6HGWibiaxxKd9PuiaYu5wRedicC96PLicZ9VIh0ic5Jg8YHPrta3IAQ/132" width="30px"><span>Geek_00e01b</span> 👍（1） 💬（0）<div>对于没有内部类机制的编程语言，就没那么友好了。需要单独为需要创建对象的类创建一个builder类。而且，也是因为单独创建了一个类，所以需要创建对象的类的构造函数没办法变为private</div>2021-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/8d/5b/383a49e4.jpg" width="30px"><span>charmsongo</span> 👍（1） 💬（0）<div>总结
1、为什么需要建造者模式？
	成员变量过多，变量赋值逻辑判断复杂，就需要考虑使用建造者模式，先设置建造者的变量，然后再一次性地创建对象
	避免对象存在无效状态
	缺点是，会有重复代码，成员变量，要在 Builder 类中重新再定义一遍。
2、与工厂模式有何区别？
	工厂模式是用来创建不同但是相关类型的对象（继承同一父类或者接口的一组子类），由给定的参数来决定创建哪种类型的对象。
	建造者模式是用来创建一种类型的复杂对象，通过设置不同的可选参数，“定制化”地创建不同的对象。
	简单理解就是：工厂模式是根据不同的条件生成不同Class的对象，构建者模式是根据不同参数生成一个class的不同对象。</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/1b/f9/018197f1.jpg" width="30px"><span>小江爱学术</span> 👍（1） 💬（0）<div>&#47;**
 * 构造者模式demo: ConstructorArg
 *&#47;
public class ConstructorArg {
    private boolean isRef;
    private Class type;
    private Object arg;

    private ConstructorArg(boolean isRef, Class type, Object arg) {
        this.isRef = isRef;
        this.type = type;
        this.arg = arg;
    }

    public static class Builder {
        private boolean isRef;
        private Class type;
        private Object arg;

        public ConstructorArg build() throws Exception {
            if (isValidParams()) {
                return new ConstructorArg(isRef, type, arg);
            }
            throw new Exception(&quot;params invalid&quot;);
        }

        public Builder setIsRef(boolean isRef) {
            this.isRef = isRef;
            return this;
        }

        public Builder setType(Class type) {
            this.type = type;
            return this;
        }

        public Builder setObject(Object arg) {
            this.arg = arg;
            return this;
        }

        private boolean isValidParams() {
            if (isRef &amp;&amp; arg instanceof String) {
                return true;
            }
            if (!isRef &amp;&amp; arg != null &amp;&amp; type != null) {
                return true;
            }
            return false;
        }
    }
}</div>2021-06-09</li><br/>
</ul>