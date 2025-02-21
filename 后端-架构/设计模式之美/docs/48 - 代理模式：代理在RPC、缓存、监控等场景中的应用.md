前面几节，我们学习了设计模式中的创建型模式。创建型模式主要解决对象的创建问题，封装复杂的创建过程，解耦对象的创建代码和使用代码。

其中，单例模式用来创建全局唯一的对象。工厂模式用来创建不同但是相关类型的对象（继承同一父类或者接口的一组子类），由给定的参数来决定创建哪种类型的对象。建造者模式是用来创建复杂对象，可以通过设置不同的可选参数，“定制化”地创建不同的对象。原型模式针对创建成本比较大的对象，利用对已有对象进行复制的方式进行创建，以达到节省创建时间的目的。

从今天起，我们开始学习另外一种类型的设计模式：结构型模式。结构型模式主要总结了一些类或对象组合在一起的经典结构，这些经典的结构可以解决特定应用场景的问题。结构型模式包括：代理模式、桥接模式、装饰器模式、适配器模式、门面模式、组合模式、享元模式。今天我们要讲其中的代理模式。它也是在实际开发中经常被用到的一种设计模式。

话不多说，让我们正式开始今天的学习吧！

## 代理模式的原理解析

**代理模式**（Proxy Design Pattern）的原理和代码实现都不难掌握。它在不改变原始类（或叫被代理类）代码的情况下，通过引入代理类来给原始类附加功能。我们通过一个简单的例子来解释一下这段话。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJN64OCUT0Jp0h2Wiau9Os0o1WbwUeoq2QL0U2vZpib8ozPxo0XDiaPM9xcKfbkoBL24ztEHelxPIMVg/132" width="30px"><span>Kevin</span> 👍（2） 💬（1）<div>基于继承的静态代理实现的demo中稍微有些瑕疵。 
login() 和register() 方法应该直接调用super.login() 和 super.register() ,然后再super前后插入额外的代码 。这样更像在代理，而不是在继承修改父类。给争哥提个不成熟的小建议。

</div>2020-06-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e8/c1/e2cc1d04.jpg" width="30px"><span>海贼王</span> 👍（0） 💬（1）<div>文章很有实用性，对于拓展思路很有帮助</div>2020-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/d5/de/f9a465ab.jpg" width="30px"><span>成长型思维</span> 👍（0） 💬（1）<div>代理模式也叫中介模式吗</div>2020-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/40/6a/ab1cf396.jpg" width="30px"><span>小兵</span> 👍（176） 💬（8）<div>组合模式的优点在于更加灵活，对于接口的所有子类都可以代理，缺点在于不需要扩展的方法也需要进行代理。
继承模式的优点在于只需要针对需要扩展的方法进行代理，缺点在于只能针对单一父类进行代理。
</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f7/eb/e7127bb8.jpg" width="30px"><span>，</span> 👍（129） 💬（2）<div>      java中,动态代理的实现基于字节码生成技术(代码里就是newProxyInstance片段),可以在jvm运行时动态生成和加载字节码,类似的技术还有asm,cglib,javassist,平时编译java用的javac命令就是字节码生成技术的&quot;老祖宗&quot;
     java中用到字节码生成技术的还有JSP编译器.AOP框架,反射等等
     深入理解java虚拟机第三版里对动态代理的描述:
     动态代理中所说的&quot;动态&quot;,是针对使用Java代码实际编写了代理类的&quot;静态&quot;代理而言的,它的优势不在于省去了编写代理类那一点编码工作量,而是实现了可以在原始类和接口还未知的时候,就确定了代理类的行为,当代理类与原始类脱离直接联系后,就可以很灵活的重用于不同的应用场景之中
     </div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9e/1b/9cb138f0.jpg" width="30px"><span>free2one</span> 👍（32） 💬（7）<div>粗略“翻译”至PHP，中间省略了很多关键的判断，主要是想知道有多少PHPer在看。

interface IUserController 
{
    public function login(String $telephone, String $password);
    public function register(String $telephone, String $password);
}
  
class UserController implements IUserController 
{
    public function login(String $telephone, String $password) 
    {
        echo &#39;is Login&#39; . PHP_EOL;
    }
  
    public function register(String $telephone, String $password) 
    {

    }
}

class MetricsCollector
{
    public function recordRequest($requestInfo)
    {
    }
}

class RequestInfo
{
    public function __construct($apiName, $responseTime, $startTimestamp)
    {
    }
}


class MetricsCollectorProxy 
{
    private $proxiedObject;

    private $metricsCollector;

    public function __construct(MetricsCollector $metricsCollector)
    {
        $this-&gt;metricsCollector = $metricsCollector;
    }
    
    public function createProxy(object $object)
    {
        $this-&gt;proxiedObject = $object;
        return $this;
    }

    public function __call($method, $arguments)
    {
        $ref = new ReflectionClass($this-&gt;proxiedObject);
        if (!$ref-&gt;hasMethod($method))
            throw new Exception(&quot;method not existed&quot;);

        $method = $ref-&gt;getMethod($method);
        $startTimestamp = time();
        $userVo = $this-&gt;callMethod($method, $arguments);
        $endTimeStamp = time();
        $responseTime = $endTimeStamp - $startTimestamp;
        $requestInfo = new RequestInfo(&quot;login&quot;, $responseTime, $startTimestamp);
        $this-&gt;metricsCollector-&gt;recordRequest($requestInfo);

        return $userVo;    
    }


    private function callMethod(\ReflectionMethod $method, $arguments)
    {
        &#47;&#47;前置判断省略
        $method-&gt;invokeArgs($this-&gt;proxiedObject, $arguments);  
    }

}


$proxy = new MetricsCollectorProxy(new MetricsCollector);
$userController = $proxy-&gt;createProxy(new UserController);
$userController-&gt;login(13800138000, &#39;pwd&#39;);
</div>2020-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/4c/6d/c20f2d5a.jpg" width="30px"><span>LJK</span> 👍（28） 💬（5）<div>是时候展示我动态语言Python的彪悍了，通过__getattribute__和闭包的配合实现，其中有个注意点就是在获取target时不能使用self.target，不然会递归调用self.__getattribute__导致堆栈溢出：
class RealClass(object):
    def realFunc(self, s):
        print(f&quot;Real func is coming {s}&quot;)

class DynamicProxy(object):
    def __init__(self, target):
        self.target = target
    
    def __getattribute__(self, name):
        target = object.__getattribute__(self, &quot;target&quot;)
        attr = object.__getattribute__(target, name)
        
        def newAttr(*args, **kwargs):
            print(&quot;Before Calling Func&quot;)
            res = attr(*args, **kwargs)
            print(&quot;After Calling Func&quot;)
            return res
        return newAttr</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/a0/6b/0a21b2b8.jpg" width="30px"><span>迷羊</span> 👍（27） 💬（0）<div>Java中的动态代理原理就是运行的时候通过asm在内存中生成一份字节码，而这个字节码就是代理类的字节码，通过System.getProperties().put(&quot;sun.misc.ProxyGenerator.saveGeneratedFiles&quot;, &quot;true&quot;);设置可以保存这份字节码，反编译后看下其源码就知道Java中的动态代理是什么原理了。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（17） 💬（3）<div>感谢争哥，今天终于学会了“动态代理”
还是要动手试试，代码在这是 https:&#47;&#47;bit.ly&#47;37UqLNf

学有余力的小伙伴，附上一些资料吧：
https:&#47;&#47;docs.oracle.com&#47;javase&#47;8&#47;docs&#47;technotes&#47;guides&#47;reflection&#47;proxy.html
https:&#47;&#47;www.baeldung.com&#47;java-dynamic-proxies</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/37/98991aeb.jpg" width="30px"><span>不似旧日</span> 👍（12） 💬（2）<div>笔记：

- 什么是代理模式：它在不改变原始类（或叫被代理类）代码的情况下，通过引入代理类来给原始类附加功能。

- 代理模式得实现：
  - 静态代理
    1. 实现被代理对象口： 要求被代理类和代理类同时实现相应的一套接口，通过代理类调用重写接口的方法，实际上调用的是原始对象的同样的方法。
    2. 继承被代理对象：代理类继承原始类，然后扩展附加功能。
  - 动态代理 ： 在运行的时候，动态地创建原始类对应的代理类，然后在系统中用代理类替换掉原始类。 
    1.  jdk动态代理是利用反射机制生成一个实现代理接口的匿名类，在调用具体方法前调用InvokeHandler来处理。
    2. cglib动态代理是利用asm开源包，对被代理对象类的class文件加载进来，通过修改其字节码生成子类来处理。 </div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/e6/47742988.jpg" width="30px"><span>webmin</span> 👍（11） 💬（0）<div>1. .net支持反射和动态代理，所以实现方式和java类似；golang目前看到的都是习惯使用代码生成的方式来达成，根据已有代码生成一份加壳代码，调用方使用加壳代码的方法，例好：easyJson给类加上序列化和反序列化功能；gomock生成mock代理。
2. 组合与继承的优缺点：
没有绝对的优缺点，要看场景比如：
当被代理的类所有功能都需要被代理时，使用继承方式就可以编译器检查（被代理类修改时编译期就可以检查出问题）；
当被代理的类只是部分功能需要被代理时，使用组合方式就可按需代理，但是如果原来不需要的，后来也需要了就比较尴尬了。
继承可能会让代理类被迫实现一些对代理类来说无意义代码，继承方式对代理类的侵入比较大，而组合的侵入影响比继承可控。</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/b8/dd/37726c34.jpg" width="30px"><span>小马哥</span> 👍（10） 💬（1）<div>不少同学纠结代理模式与后面要学的装饰器模式在功能上不能区分, 小马哥给个最简单的解释
 *          在行为效果上, 两种设计模式都可以实现增强
 *          代理模式的增强: 添加非业务功能;
 *          装饰器模式的增强: 弥补或者扩展业务功能;
如果你非要使用装饰器进行非业务功能的增强, 以及使用代理模式扩展业务功能是否可以? 可以, 但是我们学习设计模式的目的是为了写出大牛一样专业的代码, 那么就借鉴设计模式的规则.
去高速公路上开车就遵守高速的限速规定</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3d/00/7daa7403.jpg" width="30px"><span>Eden Ma</span> 👍（9） 💬（5）<div>1、OC中通过runtime和分类来实现动态代理.
2、组合优势可以直接使用原始类实例,继承要通过代理类实例来操作,可能会导致有人用原始类有人用代理类.而继承可以不改变原始类代码来使用.</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/64/9b/d1ab239e.jpg" width="30px"><span>J.Smile</span> 👍（8） 💬（3）<div>动态代理有两种:jdk动态代理和cglib动态代理。</div>2020-02-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoiaP1gptuBzj3AXMpY8yLTIkpuarouOVzLde4636UJ7zAgnOEZibiaAIRVAicFaO64ftH45YOn1pD3VA/132" width="30px"><span>Geek_35cfdd</span> 👍（7） 💬（1）<div>动态代码虽然对使用场景讲了，先不说自己如何实现一个动态代码没有讲。就算拿java的现成接口，是不是最起码应该讲下里面的实现。做到知其然知其所以然呢？你这动态代理讲的就像一个hello world。</div>2020-09-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（7） 💬（3）<div>为啥我感觉静态代理像是装饰器模式</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/e1/0e/9ce05946.jpg" width="30px"><span>distdev</span> 👍（5） 💬（1）<div>请问 如果对于业务方法 有多个非业务功能 比如metrics, logging还有其他的 应该实现在一个代理class里？还是一个filter chain里?</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（5） 💬（0）<div>C#中可以通过emit技术实现动态代理。
基于继承的代理适合代理第三方类，jdk中的动态代理只能代理基于接口实现的类，无法代理不是基于接口实现的类。所以在spring中有提供基于jdk实现的动态代理和基于cglib实现的动态代理。</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/7a/f5/54a5084b.jpg" width="30px"><span>简单猫</span> 👍（3） 💬（0）<div>代理顾名思义 就是对要调用的方法再次封装到一个新类中，这个类会调用你需要目标方法。
一、
function a(){&#47;&#47;要做的事}
function 代理(){
&#47;&#47;你可以在你要代理的方法前加逻辑
a();
&#47;&#47;也可以在方法后面加
}
调用  代理() 
二、动态代理
所有要被代理的类都是用同一个规范。
比方说都用invoke(){具体逻辑}
a.invoke
b.invoke
c.invoke
.....这样写太麻烦。
可以在动态代理类中放一个list&lt;string&gt;变量
用来存存储要代理的类名

动态代理里面调用方法
public void invoke(){
    迭代list 
    {
     反射 创建被代理的具体类
    具体类.invoke 
    }
}

</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/75/6b/fd685164.jpg" width="30px"><span>lcf枫</span> 👍（3） 💬（5）<div>目前看到这里有点懵 分不清代理和装饰器了
</div>2020-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/d9/ff/b23018a6.jpg" width="30px"><span>Heaven</span> 👍（2） 💬（0）<div>
今天我回答下第二个问题,在原有的JDK中的代理,是一种基于接口的代理模式,要求代理类只能去代理某些接口,于是乎,为了能直接代理一个代理类,cglib加入了,可以传入一个对象实例,来进行包裹,从而达到代理这种需求,两者实际来说,JDK的代理类创建时间比cglib快的太多了,于是乎更加适合在框架中定义为非单例的类去代理,cglib适合于生成单例式类的代理类</div>2020-03-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/73/74/3bf4b74e.jpg" width="30px"><span>阿德</span> 👍（2） 💬（4）<div>动态代理那里的invoke方法的第一个参数proxy有什么用，一直搞不清楚</div>2020-03-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/a5/e4c1c2d4.jpg" width="30px"><span>小文同学</span> 👍（2） 💬（0）<div>继承的代理类是通过重写来实现代理，如果超类本身方法间会调用，则被新增的代码也会被重复调用。这其实已经是一种修改，不是一种扩展了。相比下，组合型代理就没有这个问题

组合型代理需要原来的类有接口(抽象类)，代理类可以实现接口，来通过组合构成代理。继承型代理则没这个问题。</div>2020-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/48/f3/65c7e3ef.jpg" width="30px"><span>cricket1981</span> 👍（2） 💬（0）<div>@Aspect
@Component
public class CacheAspect {

    @Pointcut(&quot;execution(* com.example.demo.controller..*(..))&quot;)
    public void controller() { }

    @Around(&quot;controller()&quot;)
    public Object around(ProceedingJoinPoint point) throws Throwable {
        HttpServletRequest request = ((ServletRequestAttributes) RequestContextHolder.getRequestAttributes()).getRequest();
        Map&lt;String, String[]&gt; parameterMap = request.getParameterMap();
        Object retVal = null;
        if (parameterMap.containsKey(&quot;cached&quot;) &amp;&amp; parameterMap.get(&quot;cached&quot;)[0].equals(&quot;true&quot;)) {
            &#47;&#47; parameterMap
            System.out.println(&quot;get data from cache&quot;);
            retVal = 1; &#47;&#47; 省略从cache获取值
        } else {
            Object[] args = point.getArgs();
            retVal = point.proceed(args);
        }
        return retVal;
    }

}</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/3a/0dd9ea02.jpg" width="30px"><span>Summer  空城</span> 👍（2） 💬（5）<div>老师好，有个地方不太明白，请指点下。
Spring框架实现AOP的时候是在BeanFactory中生成bean的时候触发动态代理替换成代理类的么？
如果我们自己想对某个Controller做代理的时候要怎么处理呢？一般是用@Controller注解某个Controller的，而且这个Controller不会实现接口。
谢谢老师！</div>2020-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/56/85/6da913fa.jpg" width="30px"><span>LIFE l=new LIFE()</span> 👍（1） 💬（0）<div>反射+动态代理是框架的基石</div>2022-01-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/10/275ae749.jpg" width="30px"><span>懒猫</span> 👍（1） 💬（0）<div>golang框架一般会用middleware实现这种所谓的代理（所有接口都需要的某个功能，如记录下接口参数），不过其实是基于职责链模式</div>2021-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/24/d2/a5e272ce.jpg" width="30px"><span>夜空咏叹调</span> 👍（1） 💬（0）<div>以前在使用java的动态代理时都有点知其然而不知其所以然的感觉，一直没想明白为什么要多构造一个代理类出来，今天看代理模式突然有种豁然开朗的感觉，这个专栏真的收获很多！！</div>2020-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（1） 💬（0）<div>AOP简直是代理模式的最佳实践。
</div>2020-05-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/yicibWmBIDaSpBYI5wCBDQcYu6mxjvz3XZzBibxSNXFfqCS6OJOjvy2Nc2lyDicZfmneW9ZY4KbicA1sNgLktVSicgkw/132" width="30px"><span>老余</span> 👍（1） 💬（0）<div>动态代理和 js 中的类装饰器如出一辙哈</div>2020-03-24</li><br/>
</ul>