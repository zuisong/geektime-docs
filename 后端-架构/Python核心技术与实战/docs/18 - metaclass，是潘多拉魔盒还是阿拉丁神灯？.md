你好，我是蔡元楠，极客时间《大规模数据处理实战》专栏的作者。今天我想和你分享的主题是：metaclass，是潘多拉魔盒还是阿拉丁神灯？

Python中有很多黑魔法，比如今天我将分享的metaclass。我认识许多人，对于这些语言特性有两种极端的观点。

- 一种人觉得这些语言特性太牛逼了，简直是无所不能的阿拉丁神灯，必须找机会用上才能显示自己的Python实力。
- 另一种观点则是认为这些语言特性太危险了，会蛊惑人心去滥用，一旦打开就会释放“恶魔”，让整个代码库变得难以维护。

其实这两种看法都有道理，却又都浅尝辄止。今天，我就带你来看看，metaclass到底是潘多拉魔盒还是阿拉丁神灯？

市面上的很多中文书，都把metaclass译为“元类”。我一直认为这个翻译很糟糕，所以也不想在这里称metaclass为元类。因为如果仅从字面理解，“元”是“本源”“基本”的意思，“元类”会让人以为是“基本类”。难道Python的metaclass，指的是Python 2的Object吗？这就让人一头雾水了。

事实上，meta-class的meta这个词根，起源于希腊语词汇meta，包含下面两种意思：

1. “Beyond”，例如技术词汇metadata，意思是描述数据的超越数据；
2. “Change”，例如技术词汇metamorphosis，意思是改变的形态。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/b0/7be55531.jpg" width="30px"><span>尘墨</span> 👍（96） 💬（9）<div>我尝试着自己写了一个例子，发现好像清晰多了，没有看懂的大家可以看一下
class Mymeta(type):
    def __init__(self, name, bases, dic):
        super().__init__(name, bases, dic)
        print(&#39;===&gt;Mymeta.__init__&#39;)
        print(self.__name__)
        print(dic)
        print(self.yaml_tag)

    def __new__(cls, *args, **kwargs):
        print(&#39;===&gt;Mymeta.__new__&#39;)
        print(cls.__name__)
        return type.__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print(&#39;===&gt;Mymeta.__call__&#39;)
        obj = cls.__new__(cls)
        cls.__init__(cls, *args, **kwargs)
        return obj
    
class Foo(metaclass=Mymeta):
    yaml_tag = &#39;!Foo&#39;

    def __init__(self, name):
        print(&#39;Foo.__init__&#39;)
        self.name = name

    def __new__(cls, *args, **kwargs):
        print(&#39;Foo.__new__&#39;)
        return object.__new__(cls)

foo = Foo(&#39;foo&#39;)
把上面的例子运行完之后就会明白很多了，正常情况下我们在父类中是不能对子类的属性进行操作，但是元类可以。换种方式理解：元类、装饰器、类装饰器都可以归为元编程(引用自 python-cook-book 中的一句话)。</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d8/4f/65abc6f0.jpg" width="30px"><span>KaitoShy</span> 👍（6） 💬（3）<div>yaml.load(&quot;&quot;&quot;
--- !Monster
name: Cave spider
hp: [2,6]    # 2d6
ac: 16
attacks: [BITE, HURT]
&quot;&quot;&quot;)
运行时报错，pyyaml版本PyYAML-5.1，将语句改成
yaml.load(&quot;&quot;&quot;
--- !Monster
name: Cave spider
hp: [2,6]    # 2d6
ac: 16
attacks: [BITE, HURT]
&quot;&quot;&quot;，Loader=yaml.Loader)即可，参见&quot;https:&#47;&#47;github.com&#47;yaml&#47;pyyaml&#47;issues&#47;266&quot;</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/62/a5/43aa0c27.jpg" width="30px"><span>TKbook</span> 👍（4） 💬（2）<div>一开始还以为我打开错专栏了。   目前看了好多解释metaclass的文章，感觉这一篇看起来最明了。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/49/71/fc2b5cf2.jpg" width="30px"><span>隔壁家老鲍</span> 👍（1） 💬（1）<div>感觉入门了，不过还是有一些问题
@修饰符是在python里是怎么实现的呢
老师如果看到了可以给点意见么</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/5a/37/8775d714.jpg" width="30px"><span>jackstraw</span> 👍（0） 💬（1）<div>这代码跑都跑不通</div>2020-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/45/63/d3319b80.jpg" width="30px"><span>奔跑的蜗牛</span> 👍（123） 💬（5）<div>看不懂了 😄</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3e/6d/248335d2.jpg" width="30px"><span>=_=</span> 👍（41） 💬（0）<div>基础不够，之前没接触过metaclass，这一讲读起来太费劲了</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fe/44/3e3040ac.jpg" width="30px"><span>程序员人生</span> 👍（36） 💬（1）<div>装饰器像AOP，metaclass像反射机制</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/f1/21/52e8267b.jpg" width="30px"><span>Hoo-Ah</span> 👍（28） 💬（0）<div>之前讲装饰器的时候讲到函数装饰器和类装饰器，而类装饰器就是在雷里面定义了__call__方法，之后在函数执行的时候会调用类的__call__方法。
在metaclass中重载了__call__方法，在使用metaclass实例化生成类的时候也是调用了__call__方法，从这方面来讲是很像。
要说不一样的话，一个是在执行层面，一个是在生成层面。
可以讲讲type和object的区别吗以及可以用一篇专栏讲讲python的魔术方法。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/51/86/b5fd8dd8.jpg" width="30px"><span>建强</span> 👍（24） 💬（0）<div>1.metaclass拦截了类的构造，类似于黑客，改变了类的行为，在某些场合可简化程序设计。
2.python装饰器：不会去改变类的行为，但通过装饰类，可以加强类的功能，通过不同的装饰器使类的功能更加丰富。</div>2019-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/f6/1ef70cab.jpg" width="30px"><span>你看起来很好吃</span> 👍（9） 💬（7）<div>‘用户自定义类，只不过是 type 类的__call__运算符’
景老师，这里这段是不是有点问题，我做了以下实验：

class MyMeta(type):
    def __init__(cls, name, bases, dict):
        print(&#39;MyMeta __init__&#39;)

    def __new__(cls, name, bases, dict):
        print(&#39;MyMeta __new__&#39;)
        return type.__new__(cls, name, bases, dict)

    def __call__(cls):
        print(&#39;MyMeta __call__&#39;)
        return type.__call__(cls)

class Test(metaclass=MyMeta):
    a = 10

    def __init__(self):
        pass

    def __new__(cls):
        return super(Test, cls).__new__(cls)

test = Test()
我发现在使用class Test()定义类时，会依次调用MyMeta的__new__和__init__方法构建Test类，然后在使用test = Test()创建类对象时，才会调用MyMeta的__call__方法来调用Test类的__new__和__init__方法。好像和您说的不一样？
我看您说的意思是，在使用class定义类的时候，先调用metaclass的__call__,然后再调用metaclass的__new__和__init__？</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/77/da/54c663f3.jpg" width="30px"><span>Wing·三金</span> 👍（8） 💬（1）<div>个人粗浅的理解是：metaclass 与 类装饰器相似，大多数情况下本质上都是重载了 __call__ 函数，但有一个明显的区别是前者对【继承了 metaclass 的子类本身】的属性造成了影响，而类装饰器是对【作为装饰器本身的类】造成影响而已，对【被装饰的类】的属性没有直接影响（间接影响就看被装饰的函数怎么操作了）。</div>2019-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/69/f6/40c497a3.jpg" width="30px"><span>Jon徐</span> 👍（8） 💬（3）<div>之前没有接触过 metaclass，感觉用metaclass的作用就是超动态生成类。这节课感觉确实比较魔术，跟上一节装饰器还要再细想一下。

pyyaml 5.1以上，这段代码会报错，要把 yaml.load() 改成 yaml.load_all()
yaml.load(&quot;&quot;&quot;
--- !Monster
name: Cave spider
hp: [2,6]    # 2d6
ac: 16
attacks: [BITE, HURT]
&quot;&quot;&quot;)


</div>2019-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/84/70340e87.jpg" width="30px"><span>向南</span> 👍（5） 💬（0）<div>metaclass的应用：单例模式、ORM模式</div>2020-03-08</li><br/><li><img src="" width="30px"><span>Ray</span> 👍（5） 💬（0）<div>我的感觉装饰器是通过正常的函数的调用、闭包等方法实现附加的功能。metaclass直接就是一种hack的方法。另外，在前面type类的说明代码中：
type(instance)# 输出 &lt;class &#39;__main__.C&#39;&gt;  --&gt; 应该是&lt;class &#39;__main__.MyClass&#39;&gt;？</div>2020-02-22</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/DYAIOgq83eppQqDE6TNibvr3DNdxG323AruicIgWo5DpVr6U7yZVNkbF2rKluyDfhdpgAEcYEOZTAnbrMdTzFkUw/0" width="30px"><span>图·美克尔</span> 👍（5） 💬（0）<div>装饰器和metaclass都是给对象增加一些额外的公共配件，但装饰器不影响对象本身，而metaclass是将对象本身进行改造。是设计模式层面的东西。</div>2019-06-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bc/29/022905e6.jpg" width="30px"><span>SCAR</span> 👍（5） 💬（0）<div>哎，对metaclass的机制真是一知半解啊，是90%那坨的！
metaclass和类装饰器都可以动态定制或修改类，类装饰器比metaclass以更简单的方式做到创建类时定制类，但它只能定制被装饰的这个类，而对继承这个类的类失效。metaclass的功能则是要强大的多，它可以定制类的继承关系。</div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d5/c7/5a78596a.jpg" width="30px"><span>起个啥名字呢</span> 👍（4） 💬（0）<div>一点没懂</div>2019-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/d5/82/fc50e63a.jpg" width="30px"><span>仲薛蒲</span> 👍（3） 💬（3）<div>推荐知乎上一篇文章辅助理解 https:&#47;&#47;zhuanlan.zhihu.com&#47;p&#47;65214982 </div>2021-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/70/4e/2808a1af.jpg" width="30px"><span>Sean</span> 👍（3） 💬（0）<div>再补充一段，忘记说“装饰器”和“metaclass”的区别了，装饰器就没有基因编辑那么神奇了，它是用来装饰用的，相当于一个外在的辅助功能，而且只对被装饰的函数有效果，好比美颜相机的功能，每一张要被装饰的面孔都需要用美颜相机进行一次装饰（@装饰函数），而且，你被装饰之后，你的子女不会被装饰，就不存在代代继承的效果了，使用起来也更加灵活，你可以选择美颜后再发圈，也可以选择不美颜直接发圈。</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/03/b8/961a5342.jpg" width="30px"><span>吴月月鸟</span> 👍（2） 💬（0）<div>这篇蛮好玩的，天堂和地狱只有一步之遥。</div>2019-07-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a5/98/a65ff31a.jpg" width="30px"><span>djfhchdh</span> 👍（1） 💬（0）<div># Python 3 和 Python 2 类似
class MyClass:
  pass

instance = MyClass()

type(instance)
# 输出
&lt;class &#39;__main__.C&#39;&gt;  ##这里写错了，应该是&lt;class &#39;__main__.MyClass&#39;&gt;

type(MyClass)
# 输出
&lt;class &#39;type&#39;&gt;
</div>2019-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f4/87/644c0c5d.jpg" width="30px"><span>俊伟</span> 👍（1） 💬（1）<div>我还有一个问题，好多框架的源码比如django的metaclass都重写了new方法而不是重写init方法，这有什么区别吗？重新这两个方法任意一个都可以吧，为什么总重写new方法呢？</div>2019-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/13/00/a4a2065f.jpg" width="30px"><span>Michael</span> 👍（1） 💬（0）<div>class TestMetaClass(type):

    def __new__(mcs, *args, **kwargs):
        print(&#39;TestMetaClass.__new__&#39;, mcs)
        return type.__new__(mcs, *args, **kwargs)

    def __init__(cls, name, bases, kwds):
        print(&#39;TestMetaClass.__init__&#39;, cls)
        super(TestMetaClass, cls).__init__(name, bases, kwds)

    def __call__(cls, *args, **kwargs):
        print(&#39;TestMetaClass.__call__&#39;)
        return super(TestMetaClass, cls).__call__(*args, **kwargs)


class A(metaclass=TestMetaClass):

    def __new__(cls, *args, **kwargs):
        print(&#39;A.__new__&#39;)
        return super(A, cls).__new__(cls)

    def __init__(self, name=None):
        self.name = name
        print(&#39;A.__init__&#39;)


A(&#39;hello&#39;)</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a9/3b/f4ca20d8.jpg" width="30px"><span>吴林辉</span> 👍（1） 💬（0）<div>有个疑问请教下老师，例子里YAMLObject 把 metaclass 声明成了 YAMLObjectMetaclass，换成YAMLObject 继承 YAMLObjectMetaclass ，单纯的做YAMLObjectMetaclass的子类，然后super父类的__init__ 方法，不是也能实现一样的功能么
</div>2019-07-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83er4HlmmWfWicNmo3x3HKaOwz3ibcicDFlV5xILbILKGFCXbnaLf2fZRARfBdVBC5NhIPmXxaxA0T9Jhg/132" width="30px"><span>Geek_Wison</span> 👍（1） 💬（3）<div>老师你好，为什么我执行示例代码会一个constructor错误，查了好久资料都解决不了。
import yaml
class Monster(yaml.YAMLObject):
  yaml_tag = u&#39;!Monster&#39;
  def __init__(self, name, hp, ac, attacks):
    self.name = name
    self.hp = hp
    self.ac = ac
    self.attacks = attacks
  def __repr__(self):
    return &quot;%s(name=%r, hp=%r, ac=%r, attacks=%r)&quot; % (
       self.__class__.__name__, self.name, self.hp, self.ac,      
       self.attacks)

yaml.load(&quot;&quot;&quot;
--- !Monster
name: Cave spider
hp: [2,6]    # 2d6
ac: 16
attacks: [BITE, HURT]
&quot;&quot;&quot;)

错误信息：
ConstructorError: could not determine a constructor for the tag &#39;!Monster&#39;
  in &quot;&lt;unicode string&gt;&quot;, line 2, column 5:
    --- !Monster
        ^</div>2019-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/4b/53/67c08006.jpg" width="30px"><span>John Si</span> 👍（1） 💬（0）<div>装饰器跟metaclass这两节课内容都很复杂，不知老师能否再详细说明一下，谢谢老师</div>2019-06-19</li><br/><li><img src="" width="30px"><span>hlz-123</span> 👍（1） 💬（0）<div>关于类装饰器和metaclass，我的理解如下：
1、类装饰器实现功能
     class A:
            def __init__:
            ......
            def __call__:
      @class A
       def my_func():
       每次执行函数my_fund()时，首先执行A类中__call__函数，再执行my_func()。
2、metaclass实现功能
     class A:
     class B(metaclass=A) 
     B类的基类就改变到了A类，不是原来以前缺省的基类，比如object,
     在python中，生成类时，最终的基类应该是type，但metaclass可以改变基类，所以翻译成元类也有 
     几分道理。
3、相同点和区别
     相同点：类装饰器和metaclass都指定了一个类
     区别：类装饰器是去执行其指定类中的__call__函数，而meataclass是指定基类，基类的构成函数和 
     属性 能够被子类继承。 </div>2019-06-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/97/23446114.jpg" width="30px"><span>火云邪神霸绝天下</span> 👍（1） 💬（0）<div>“元类就是深度的魔法，99%的用户应该根本不必为此操心。如果你想搞清楚究竟是否需要用到元类，那么你就不需要它。那些实际用到元类的人都非常清楚地知道他们需要做什么，而且根本不需要解释为什么要用元类。” —— Python界的领袖 Tim Peters</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（0） 💬（0）<div>第18讲打卡~</div>2024-06-19</li><br/>
</ul>