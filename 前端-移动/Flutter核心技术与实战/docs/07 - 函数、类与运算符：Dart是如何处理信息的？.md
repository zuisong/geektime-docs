你好，我是陈航。

在上一篇文章中，我通过一个基本hello word的示例，带你体验了Dart的基础语法与类型变量，并与其他编程语言的特性进行对比，希望可以帮助你快速建立起对Dart的初步印象。

其实，编程语言虽然千差万别，但归根结底，它们的设计思想无非就是回答两个问题：

- 如何表示信息；
- 如何处理信息。

在上一篇文章中，我们已经解决了Dart如何表示信息的问题，今天这篇文章我就着重和你分享它是如何处理信息的。

作为一门真正面向对象的编程语言，Dart将处理信息的过程抽象为了对象，以结构化的方式将功能分解，而函数、类与运算符就是抽象中最重要的手段。

接下来，我就从函数、类与运算符的角度，来进一步和你讲述Dart面向对象设计的基本思路。

## 函数

函数是一段用来独立地完成某个功能的代码。我在上一篇文章中和你提到，在Dart中，所有类型都是对象类型，函数也是对象，它的类型叫作Function。这意味着函数也可以被定义为变量，甚至可以被定义为参数传递给另一个函数。

在下面这段代码示例中，我定义了一个判断整数是否为0的isZero函数，并把它传递了给另一个printInfo函数，完成格式化打印出判断结果的功能。

```
bool isZero(int number) { //判断整数是否为0
  return number == 0; 
}

void printInfo(int number,Function check) { //用check函数来判断整数是否为0
  print("$number is Zero: ${check(number)}");
}

Function f = isZero;
int x = 10;
int y = 0;
printInfo(x,f);  // 输出 10 is Zero: false
printInfo(y,f);  // 输出 0 is Zero: true
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/5d/c5/2f359dc3.jpg" width="30px"><span>Young</span> 👍（89） 💬（5）<div>1.一般来讲，单继承，多实现，混入是多继承
A.继承是子类需要复用父类的方法实现
B.实现接口是复用接口的参数，返回值，和方法名，但不复用方法的实现，在Dart中实现抽象类 更像在java中实现用interface修饰的接口
C.混入是多继承，当被混入的类有多个同名方法时，调用子类的该方法时，会调用with声明的最后一个拥有该方法的类中的该方法，同时混入中的父类不能继承
</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/54/3f/fdbdffe0.jpg" width="30px"><span>宋锡珺</span> 👍（21） 💬（1）<div>1.
父类继承：和java类似，继承了父类的实例变量和各种方法。但是不能用一个普通方法重写getter。
抽象类：抽象类不能实例化，会报出AbstractClassInstantiationError错误。
接口：成员变量，成员函数需要重新声明实现。和java不一样的是，没有接口声明，可以通过抽象类来描述接口。
mixin:使一个类有多个父类。例如：在Flutter中常见的我们需要继承state。如果需要页面保持状态，我们还需要AutomaticKeepAliveClientMixin来保持页面状态。这时就需要通过with来使用mixin.
2.
子类构造函数调用父类非命名，无参构造函数。先父后子。
1.初始化列表
2.父类的无参构造函数
3当前类的无参构造函数
通过named constructors可以使父类有多个构造函数，但是子类是不能继承父类的构造函数的。如果使用父类的构造函数，子类需要实现父类的构造函数。</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/bb/a3/af469d27.jpg" width="30px"><span>Qilin Lou</span> 👍（13） 💬（1）<div>一个小问题，在覆写相等运算符时为何需要传入dynamic变量，而不能传入Vector呢？
bool operator==(dynamic v) =&gt; x == v.x &amp;&amp; y == v.y;
bool operator==(Vector v) =&gt; x == v.x &amp;&amp; y == v.y; &#47;&#47; 报错</div>2019-07-14</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/h0KAdRFKjCOSLRjzictvlaHOxsEiaWMSqcO68oiaUqffzyYlEKrDRvicHociabv72HNuR2VdECr8mVFIRiayM0Dd7bNDnaiceicHysF7/132" width="30px"><span>Geek_869250</span> 👍（8） 💬（2）<div>mixin和react有什么不同，react已经不使用了</div>2019-07-29</li><br/><li><img src="" width="30px"><span>昨夜星辰</span> 👍（5） 💬（2）<div>可选命名参数和可忽略参数有什么区别？</div>2019-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/5a/7f/c50d520e.jpg" width="30px"><span>颜为晨</span> 👍（4） 💬（1）<div>可选命名参数是不是可以理解成 map？</div>2019-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/9c/5e/a23c8962.jpg" width="30px"><span>路灯客栈</span> 👍（4） 💬（3）<div>小白问下
Point(this.x, this.y) : z = 0;
这里的‘ : ’的用法解释？ 和‘=&gt;’有什么区别？</div>2019-07-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/83/e8/f726c635.jpg" width="30px"><span>加温后的啤酒</span> 👍（0） 💬（2）<div>老师，你文中说“子类可以根据需要覆写构造函数及父类方法”，这句话用在大多数编程语言比如java中是对的，但是用在Dart中是不对的吧。Dart构造函数的特点是子类不会继承父类的构造函数，Dart官方文档里也有提到“Subclasses don’t inherit constructors from their superclass”，所以也就谈不上覆写构造函数。老师，我的理解对吗？</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/ea/25/9fda39a1.jpg" width="30px"><span>sherry慈</span> 👍（0） 💬（2）<div>问老师一个问题，可选命名参数可以和必传参数共存吗</div>2019-12-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/59/ed/15465917.jpg" width="30px"><span>Captain</span> 👍（0） 💬（1）<div>就像，具体什么是命名构造函数，好处是什么？什么是初始化列表？是指什么列表呢？好处是什么？</div>2019-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3b/44/dd534c9b.jpg" width="30px"><span>菜头</span> 👍（0） 💬（1）<div>命名构造函数？有例子吗</div>2019-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/6c/56/07920099.jpg" width="30px"><span>微笑美男😄</span> 👍（0） 💬（1）<div>有课件没 我是新手,按照课程上的示例代码写了以后,总是报错,运行不起来</div>2019-09-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqJV94SB9GY6ErM23QZ3jbYY7eIqbhoWHIMR2uusibj2Jib0CvAj64MLibkjwcCN6tOdgfW6dfNPpuhw/132" width="30px"><span>Zxt</span> 👍（0） 💬（1）<div>为什么作为mixin的类 只能继承自object呢？也是为了防止多继承出现的菱形问题么？</div>2019-08-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqJV94SB9GY6ErM23QZ3jbYY7eIqbhoWHIMR2uusibj2Jib0CvAj64MLibkjwcCN6tOdgfW6dfNPpuhw/132" width="30px"><span>Zxt</span> 👍（0） 💬（1）<div>一个声明了构造函数的类  无法被别的类混入了  这个是为什么呢？</div>2019-08-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqJV94SB9GY6ErM23QZ3jbYY7eIqbhoWHIMR2uusibj2Jib0CvAj64MLibkjwcCN6tOdgfW6dfNPpuhw/132" width="30px"><span>Zxt</span> 👍（0） 💬（1）<div>请教个问题，一个类可以同时混入多个类嘛？</div>2019-08-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/49/58/15625db4.jpg" width="30px"><span>mj</span> 👍（0） 💬（2）<div>如果不加“_”，则默认为 public。不过，“_”的限制范围并不是类访问级别的，而是库访问级别

请问库访问级别是什么意思</div>2019-07-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/08/d9/8d1759d1.jpg" width="30px"><span>云中大鹏</span> 👍（0） 💬（1）<div>dart中有没有的 == 与===的区别</div>2019-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/93/ed/9cc44242.jpg" width="30px"><span>JakePrim</span> 👍（0） 💬（1）<div>继承和接口实现，与java类似，但是混入就不太理解了，什么场景下会用到呢？flutter好像也用不到这么复杂的逻辑吧</div>2019-07-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/55/61/ac1729d3.jpg" width="30px"><span>Mkl</span> 👍（0） 💬（1）<div>老师您好，请问“我们只要在声明变量与方法时，在前面加上“”即可作为 private 方法使用。如果不加“”，则默认为 public。”这里边的双引号中的内容是什么，看不到呀😳</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/0f/7a/385e4816.jpg" width="30px"><span>tao.ai.dev</span> 👍（39） 💬（0）<div>讲真，可选参数部分我一开始没参透，其实应该这么讲。参数分为“必选”和“可选”，当两者同时存在时，
必选在前，可选在后。可选参数又分为两种：第一种是“可选命名参数”，使用{}；第二种是“可选位置参数”，使用[]。两者区别在于调用函数传参时：前者须署名参数名，但是调用顺序可变（但是必须在必选参数后面）。后者不必署名参数名，但是位置不可变。
</div>2020-04-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/e0/d7/744bd8c3.jpg" width="30px"><span>空白昵称</span> 👍（3） 💬（0）<div>Function作为函数类型使用，但是丢失了函数的具体类型内容。
所以一般采用 typedef 定义一个Function类型？
相较而言，Swfit的闭包更具表达。</div>2020-07-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/37/33/7425bd10.jpg" width="30px"><span>Jason</span> 👍（2） 💬（1）<div>没有发现有回答这个课后题的，按照自己的理解写了一下，不知道对不对

Vector(): this.make(0, 0, 0);
Vector.left(x): this.make(x, 0, 0); 
Vector.middle(z): this.make(0, 0, z);
Vector.right(y): this.make(0, y, 0);
Vector.make(x, y, this.z): super.make(x, y);</div>2021-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/54/7b/1b85c629.jpg" width="30px"><span>路口台灯</span> 👍（1） 💬（0）<div>1. 完全不允许重载，一个类中不允许存在方法名相同的多个函数，不论是通过继承、实现、还是混入。
2. 混入可以理解为多继承，可以复用成员变量和方法实现。
3. 被混入类的父类必须是Object类型，这解决了普通多继承的菱形问题，即被混入的类不能继承其他类，但可以实现其他接口。
4. 成员变量和方法复用冲突时，以复用机制的最后一个实现为准。</div>2021-07-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIBC94guaFqiaSlFhyibfo6kySHPqJCfQKzzz8JwumEMGiaVDfXJTbFAMK4vS6t9UJib4S8icmtsd7NAsg/132" width="30px"><span>Geek_d7ea11</span> 👍（1） 💬（0）<div>感觉叫可选命名参数  和可选位置参数  更加贴切</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/7a/df/5cd2b06d.jpg" width="30px"><span>Harris</span> 👍（1） 💬（0）<div>class A with B implements C {
  &#47;&#47;&#47; ...
}

class A extends C with B {
  &#47;&#47;&#47; ...
}
注意with语句必须写在implements的前面，extends的后面</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/96/81/4b5cd55b.jpg" width="30px"><span>joyce</span> 👍（0） 💬（0）<div>enable3Flags会报错：Error: The parameter &#39;hidden&#39; can&#39;t have a value of &#39;null&#39; because of its type &#39;bool&#39;, but the implicit default value is &#39;null&#39;.
Try adding either an explicit non-&#39;null&#39; default value or the &#39;required&#39; modifier.
void enable3Flags(bool bold, [bool hidden]) =&gt; print(&quot;$bold,$hidden&quot;);</div>2024-10-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/18/b8/06241e2a.jpg" width="30px"><span>Kevin</span> 👍（0） 💬（0）<div>简直是缝合怪啊</div>2024-05-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/dd/22/1dc0fd86.jpg" width="30px"><span>小小的存在</span> 👍（0） 💬（0）<div>继承：子类有父类的所有属性和方法。使用场景：有一个通用的类，而另一个类需要大部分或全部相同的功能时，可以使用继承。

接口：类似OC里面的协议， 使用场景，比如我要封装一个推拉流的类，我就把推拉流的类继承某个协议，协议有开始推流等方法，但里面内部实现我可能使用a厂家的sdk，也可以用b厂家的sdk，面向协议编程的时候使用

混入：想要在多个类之间共享代码时，可以使用混入</div>2024-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/c9/833d5060.jpg" width="30px"><span>玉皇大亮</span> 👍（0） 💬（0）<div>class Point {
  num x, y;
  Point() : this.make(0,0);
  Point.left(x) : this.make(x,0);
  Point.right(y) : this.make(0,y);
  Point.make(this.x, this.y);
  void printInfo() =&gt; print(&#39;($x,$y)&#39;);
}

class Vector extends Point{
  num z = 0;
  Vector(): super.make(0,0) {
    z = 0;
  }
  Vector.left(num x): super.left(x) {
    z = 0;
  }
  Vector.right(num y): super.right(y) {
    z = 0;
  }
  
  Vector.middle(num z): super.make(0, 0) {
    this.z = z;
  }
  
  Vector.make(num x, num y, num z): super.make(x, y) {
    this.z = z;
  }
    
  @override
  void printInfo() =&gt; print(&#39;($x,$y,$z)&#39;); &#47;&#47;覆写了printInfo实现
}

void main() {
  var vector = Vector.make(3, 4, 5);
  vector.printInfo();
}</div>2024-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/71/6f/07e1452a.jpg" width="30px"><span>微尘</span> 👍（0） 💬（0）<div>mixin我感觉最好不要用，看着都😨</div>2022-11-03</li><br/>
</ul>