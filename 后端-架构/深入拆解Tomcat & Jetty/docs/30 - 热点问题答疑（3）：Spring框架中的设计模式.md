在构思这个专栏的时候，回想当时我是如何研究Tomcat和Jetty源码的，除了理解它们的实现之外，也从中学到了很多架构和设计的理念，其中很重要的就是对设计模式的运用，让我收获到不少经验。而且这些经验通过自己消化和吸收，是可以把它应用到实际工作中去的。

在专栏的热点问题答疑第三篇，我想跟你分享一些我对设计模式的理解。有关Tomcat和Jetty所运用的设计模式我在专栏里已经有所介绍，今天想跟你分享一下Spring框架里的设计模式。Spring的核心功能是IOC容器以及AOP面向切面编程，同样也是很多Web后端工程师每天都要打交道的框架，相信你一定可以从中吸收到一些设计方面的精髓，帮助你提升设计能力。

## 简单工厂模式

我们来考虑这样一个场景：当A对象需要调用B对象的方法时，我们需要在A中new一个B的实例，我们把这种方式叫作硬编码耦合，它的缺点是一旦需求发生变化，比如需要使用C类来代替B时，就要改写A类的方法。假如应用中有1000个类以硬编码的方式耦合了B，那改起来就费劲了。于是简单工厂模式就登场了，简单工厂模式又叫静态工厂方法，其实质是由一个工厂类根据传入的参数，动态决定应该创建哪一个产品类。

Spring中的BeanFactory就是简单工厂模式的体现，BeanFactory是Spring IOC容器中的一个核心接口，它的定义如下：
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/ec/13/49e98289.jpg" width="30px"><span>neohope</span> 👍（14） 💬（1）<div>&#47;&#47;在Proxy类里中：
&#47;&#47;constructorParams的定义如下：
private static final Class&lt;?&gt;[] constructorParams = { InvocationHandler.class };

&#47;&#47;newProxyInstance无限精简之后就是：
public static Object newProxyInstance(ClassLoader loader, Class&lt;?&gt;[] interfaces, InvocationHandler h)
        throws IllegalArgumentException {
    &#47;&#47;通过ProxyClassFactory调用ProxyGenerator生成了代理类
    Class&lt;?&gt; cl = getProxyClass0(loader, interfaces);
    &#47;&#47;找到参数为InvocationHandler.class的构造函数
    final Constructor&lt;?&gt; cons = cl.getConstructor(constructorParams);
    &#47;&#47;创建代理类实例
    return cons.newInstance(new Object[]{h});
}


&#47;&#47;在ProxyGenerator类中：
public static byte[] generateProxyClass(final String name,Class&lt;?&gt;[] interfaces, int accessFlags)){}
private byte[] generateClassFile() {}
&#47;&#47;上面两个方法，做的就是
&#47;&#47;将接口全部进行代理
&#47;&#47;并生成其他需要的方法，比如上面用到的构造函数、toString、equals、hashCode等
&#47;&#47;生成对应的字节码
&#47;&#47;其实这也就说明了，为何JDK的动态代理，必须需要至少一个接口</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（11） 💬（1）<div>老师能讲一下spring这么解决循环依耐的吗</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/05/7f/a7df049a.jpg" width="30px"><span>Standly</span> 👍（10） 💬（1）<div>老师 ，工厂方法模式没看懂。另外DefaultSingletonBeanRegistry的getBean方法的实现存在线程安全问题吧？虽然用了ConcurrentHashMap,但是if (singletonObject == null) 存在竞态条件， 可能有2个线程同时判断为true，最后产生了2个对象实例。应该用putIfAbsent方法。</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/6d/8f/81e282e2.jpg" width="30px"><span>802.11</span> 👍（0） 💬（1）<div>文中的工厂模式，有一个疑惑，它确实解决了对象的创建问题，但是对象每一个字段的赋值，工厂模式可以解决吗？或者怎么解决呢，谢谢</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/79/4b/740f91ca.jpg" width="30px"><span>-W.LI-</span> 👍（12） 💬（0）<div>之前硬着头皮看过这个源码，中间有一步weakcache印象深刻。弱引用缓存，先从缓存中取，没取到获取字节码，校验魔术版本号之类的，最后反射实现。反射效率不高也是这个原因导致的，要获取源文件校验准备初始化(轻量级累加载一次)。</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（6） 💬（0）<div>动态代理的思路便是动态生成一个新类，先通过传入的classLoader生成对应Class对象，后通过反射获取构造函数对象并生成代理类实例，jdk动态代理是通过接口实现的，但很多类是没有针对接口设计的，但是我们知道可以通过拼接字节码生成新的类的自由度是十分大的，所以cglib框架就是通过拼接字节码来实现非接口类的代理。</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7b/57/a9b04544.jpg" width="30px"><span>QQ怪</span> 👍（4） 💬（0）<div>老师这次加餐面试必问题</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ee/ea/c8136dfd.jpg" width="30px"><span>草戊</span> 👍（3） 💬（1）<div>BeanFactory和FactoryBean的代码示例是一样的？</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（1） 💬（0）<div>这个工厂模式，这各其实实例化的出来我觉得还是工厂bean，但是可以通过getObject来获取bean。这里可以看一下Spring的ObjectFactoryCreatingFactoryBean（通过继承AbstractFactoryBean ，然后由AbstractFactoryBean实现BeanFactory的）
public Object getObject() throws BeansException {
			return this.beanFactory.getBean(this.targetBeanName);
		}
对应类名字传过来即可，若果是动态那工厂模式就大显神威了。
</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ff/98/6e17646a.jpg" width="30px"><span>桔子</span> 👍（1） 💬（0）<div>谢谢，我学会了动态代理~</div>2019-09-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/54/cf/fddcf843.jpg" width="30px"><span>芋头</span> 👍（0） 💬（0）<div>老师，其实我蛮好奇怎么样才能看到动态代理后的类代码</div>2023-03-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/07/d2/0d7ee298.jpg" width="30px"><span>惘 闻</span> 👍（0） 💬（0）<div>老师你说的代理模式是为了增强被代理类的方法。可是这不是装饰器模式的定义吗？代理模式主要是提供一种间接访问被代理类的方式和控制。</div>2021-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/36/65/08140028.jpg" width="30px"><span>liyanzhaog</span> 👍（0） 💬（0）<div>动态反射的理解：
       &#47;&#47;创建目标对象StudentDao
        IStudentDao stuDAO = new StudentDao();
        &#47;&#47; 创建目标对象的代理对象类
Class proxyClass=
Proxy.getProxyClass(stuDAO.getClass().getClassLoader(),stuDAO.getClass().getInterfaces());
        &#47;&#47; 获取代理对象类的构造器
 Constructor constructors=proxyClass.getConstructor(InvocationHandler.class);
        &#47;&#47; 获取代理对象实例
IStudentDao studentDao=
(IStudentDao)constructors.newInstance(new InvocationHandler() {
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                System.out.println(&quot;开启事务...&quot;);
                Object rst=method.invoke(stuDAO,args);
                System.out.println(&quot;提交事务...&quot;);
                return rst;
            }
        });
        &#47;&#47; 调用代理对象的方法
        studentDao.save();

和静态代理的区别就在第一步创建对象的代理类，proxyClass的代码：
public final class $Proxy0 extends Proxy implements IStudentDao {
private static Method m3=
 Class.forName(&quot;com.sustcoder.design.proxy.IStudentDao&quot;).getMethod(&quot;save&quot;);
    public $Proxy0(InvocationHandler var1) throws {
        super(var1);
    }
    public final void save() throws {
        try {
            super.h.invoke(this, m3, (Object[])null);
        } catch (RuntimeException | Error var2) {
            throw var2;
        } catch (Throwable var3) {
            throw new UndeclaredThrowableException(var3);
        }
    }</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1e/3a/5b21c01c.jpg" width="30px"><span>nightmare</span> 👍（0） 💬（0）<div>如果是基于反射实现的，那增强的业务这么植入的</div>2019-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（2）<div>工厂方法模式说的就是抽象工厂模式吧</div>2019-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/98/eb/bf53184b.jpg" width="30px"><span>阿青，你学到了吗</span> 👍（0） 💬（0）<div>基于反射实现的</div>2019-07-18</li><br/>
</ul>