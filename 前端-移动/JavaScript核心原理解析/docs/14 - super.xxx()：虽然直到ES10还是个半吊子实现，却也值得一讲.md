你好，我是周爱民，接下来我们继续讲述JavaScript中的那些奇幻代码。

今天要说的内容，打根儿里起还是得从JavaScript的1.0谈起。在此前我已经讲过了，JavaScript 1.0连继承都没有，但是它实现了以“类抄写”为基础的、基本的面向对象模型。而在此之后，才在JavaScript 1.1开始提出，并在后来逐渐完善了原型继承。

这样一来，在JavaScript中，从概念上来讲，所谓对象就是一个从原型对象衍生过来的实例，因此这个子级的对象也就具有原型对象的全部特征。

然而，既然是子级的对象，必然与它原型的对象有所不同。这一点很好理解，如果没有不同，那就没有必要派生出一级关系，直接使用原型的那一个抽象层级就可以了。

所以，有了原型继承带来的子级对象（这样的抽象层级），在这个子级对象上，就还需要有让它们跟原型表现得有所不同的方法。这时，JavaScript 1.0里面的那个“类抄写”的特性就跳出来了，它正好可以通过“抄写”往对象（也就是构造出来的那个this）上面添加些东西，来制造这种不同。

也就是说，JavaScript 1.1的面向对象系统的设计原则就是：**用原型来实现继承，并在类（也就是构造器）中处理子一级的抽象差异**。所以，从JavaScript 1.1开始，JavaScript有了自己的面向对象系统的完整方案，这个示例代码大概如下：
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（5） 💬（1）<div>读后感
1. super的出现是为了解决子类同名属性覆盖父类的属性，通过super可以直接访问到父类。
2. 伪代码：key[[HomeObject]].__proto__ === super，不知道对不对</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/9a/af/ac09799f.jpg" width="30px"><span>小毛</span> 👍（3） 💬（1）<div>老师，请教个问题，为什么ECMAScript 6中的class定义里方式是prototype原型方法，而属性又是实例属性呢，这样有点诡异
class A {
    x=1
}
class B extends A {
    constructor() {
        super();
        this.y = super.x + 1;
    }
}
let b = new B;
console.log(b.x);&#47;&#47;1
console.log(b.y);&#47;&#47;NAN</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（3） 💬（1）<div>实话实说，对 Class 和 super 的知识概念还不熟悉，有几个问题请教下老师

1、在“继承”上，xxx.apply() 和 xxx.call() 算是继承吗？与 super.xxx() 又有什么区别？

2、super.xxx() 的 this 引用是在当前环境的上下文中查找的。那么，x = super.xxx.bind(...) 绑定的 this 是从父类 or 祖先类“继承”而来，这与 constructor() 中直接调用 super() 是否一致？

另，大师可以适当添加一些代码 or 图片 or 思维导图，在阅读理解上可以帮助我们更好理清，感谢！
</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/06/54/16bb64d0.jpg" width="30px"><span>蛋黄酱</span> 👍（2） 💬（2）<div>二刷了，来回又看了三遍左右才理解老师表达的是什么。特来评论一下。
老师的内容真的很好，但是我强烈觉得老师的语言表达需要提高，很多地方其实本身并不复杂，但是因为老师的表述具有强烈的迷惑性，绕了一个大弯，把人给绕晕了，最后并不知道你在讲什么。
实际上你看楼上@穿秋裤的男孩 的总结就及其简洁好懂。</div>2020-03-28</li><br/><li><img src="" width="30px"><span>油菜</span> 👍（1） 💬（2）<div>“在 JavaScript 中，super 只能在方法中使用”
----
老师，我的测试问题在哪呢？

function F1(){
	this.a1=&#39;aaa&#39;;
	this.b1=&#39;bbb&#39;; 
	this.f1=function(){
		console.log(&#39;f1f1&#39;)
		}
	}
	
class S1 extends F1{
	k1(){
		super.f1();  &#47;&#47;调用父类了f1()方法
		}
	}
	
new S1().f1(); &#47;&#47; f1f1
new S1().k1(); &#47;&#47; Uncaught TypeError: (intermediate value).f1 is not a function</div>2020-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（1） 💬（1）<div>老师好，我理解的基于类构造对象的过程如下：

类的构造过程是在继承的顶层通过new.target拿到最底层的构造函数，

然后拿到继承连最底层构造函数的原型属性，然后顶层的构造函数使用这个原型属性构造一个对象，

经过中间一层一层的构造函数的加工返回出来。

所以对象是从父类返回的，在constructor中如果有继承需要先调用super才能拿到this

这个过程几乎描述了整个基于类构造对象的经过，但关于类实例化对象的过程，我还有以下疑问：

类有一个相对较新的语法如下：

```
class A {
    c = function () {}
    b = this.c.bind(this)
}
```
这个 = 是一个表达式用于创建实例的属性，是需要执行来计算属性值的，那么这个 b = this.c.bind(this)的执行环境是什么？？？

合理的猜想是constructor 中super调用之后，因为这个环境中有this。

但是：

```
class A {
    constructor () {
        var e = 1
    }
    
    c = e
}
```

这样实例化的时候会报错，如果 c = e 的环境在constructor中应该不会报错

除了在constructor中执行 c = e 找不到肉眼可见的作用域可以执行这个表达式了

------------------------------------------------------------------------

探索过程如下：

class E {
    constructor () {
        console.log(222) &#47;&#47; 2
    }
}

class E1 extends E {
    constructor () {
           console.log(111)  &#47;&#47; 1
           super()
           console.log(this.c) &#47;&#47; 4
           var e = 1
           console.log(555) &#47;&#47; 5
    }
    
    c = (function() {
            console.log(333) &#47;&#47; 3
            return &#39;this.c&#39;
          })()
}

c = …. 这个表达式是在super()之后调用的，但却不是在constructor中调用的，

感觉这其中隐藏了什么，望老师指点。

------------------------------------------------------------------------
感谢老师的时间
------------------------------------------------------------------------

还有一个非本专栏的问题想问下，为什么 = 是表达式 &#47; 运算？？？

javascript语编3中描述 = 是运算，并不能理解 = 是运算（表达式）的说法（虽然确实如此，因为

它可以出现在表达式才能出现的地方，例如(a = 1)不会报错）。

一直以为 = 是语句，赋值语句，作用是将右边的值赋值给左边的引用，并不做运算，虽然有返回值，

但我理解这只是 = 的副作用。

当然符号是运算的说法也不能说服自己，例如 + - 是运算所以 = 符号也是运算这有点接受不了，

毕竟javascript语编3中还介绍了和return相对的yield还是表达式呢，所以没理由=不能是语句，

= 不是语句的原因应该是它本身就不是语句和它是符号的形式没关系。

另：java中也可以打印出 a = 1的结果。 Number a = 0; System.out.println(a = 1);

------------------------------------------------------------------------
再次感谢老师的时间
------------------------------------------------------------------------</div>2020-09-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/4d/ce/a248c9ad.jpg" width="30px"><span>zy</span> 👍（0） 💬（2）<div>最近看到一段代码：
{
    function foo(){}
    foo = 1
    foo = 2
    foo = 3
    foo = 4
    foo = 5
    function foo(){}
    foo = 6
    foo = 7
    foo = 8
    foo = 9
    foo = 10
}
console.log(foo)
打印出来是5，分析了半天没搞明白为什么，能不能请老师帮忙分析一下</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>「ECMAScript 约定了优先取 Super 引用中的 thisValue 值，然后再取函数上下文中的」
「super.xxx() 是对 super.xxx 这个引用（SuperReference）作函数调用操作，调用中传入的 this 引用是在当前环境的上下文中查找的」
老师，前面一段话说可能从两个地方取「Super 引用中的 thisValue 值」是指通过bind方法绑定的值？
</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>「在 MyClass 的构造方法中访问 super 时，通过 HomeObject 找到的将是原型的父级对象。而这并不是父类构造器」
老师，理论上可以通过HomeObject.constructor 拿到 MyClass，是因为HomeObject.constructor拿到的值不靠谱，所以不这么去拿？</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（0） 💬（1）<div>ECMAScript 为此约定：只能在调用了父类构造方法之后，才能使用 super.xxx 的方式来引用父类的属性，或者调用父类的方法，也就是访问 SuperReference 之前必须先调用父类构造方法
-----------------
eg:
class Parent { getName() { return this } };
class Son extends Parent { getName() { return super.getName() } };
const s = new Son();
s.getName(); &#47;&#47; 会正常打印Son类。
-----------------
疑问：现在的js引擎是不是会自动加一个默认的constructor函数，并且执行super(),不然按照老师的说法，这边在用super之前没有super(),是不能访问super.getName()的吧？</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（0） 💬（3）<div>1. 在类声明中，如果是类静态声明，也就是使用 static 声明的方法，那么主对象就是这个类，例如 AClass
-----------------
前提：我理解您这边的说的主对象就是指super
-----------------
例子：
class Parent { static obj = { name: &#39;parent static obj name&#39; } }
class Son extends Parent {
    static obj = { name: &#39;son static obj name&#39; }
    static getObj() { return super.obj === Parent.obj } &#47;&#47; static声明的方法
}
Son.getObj(); &#47;&#47; true
--------------------
问：按照您说的话，static声明的方法，super应该指像Son，那么Son.obj应该是指向自己的static obj,也就不应该出现super.obj === Parent.obj为true的结论。这边是不是应该是：super指向Son的__proto__,也就是Parent本身？</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（0） 💬（1）<div>其实很简单，在这种情况下 JavaScript 会从当前调用栈上找到当前函数——也就是 new MyClass() 中的当前构造器，并且返回该构造器的原型作为 super。
这句话没懂。。
 JavaScript 会从当前调用栈上找到当前函数——也就是 new MyClass() 中的当前构造器， 是MyClass.prototype.constructor? 指向的是MyClass ?
该构造器的原型？请问这里是怎么指向Object.prototype.constructor的。</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（0） 💬（1）<div>Hello 老师好：

感悟：

constructor() {
	super()
}
为什么不能写成

constructor() {
	super.constructor()
}
这种形式呢？之后过了好一会转念一想super.constructor是需要this的但是上面super调用之前是拿不到this的。

问题1：

a.b()方法中this是动态获取的，是作为this传入的a。
super.b 中的this是super.b这个引用的thisValue（执行环境的this），引用的thisValue优先级高于作为this传入的super。
通过测试发现bind绑定的this优先级高于super.a这个引用的thisValue。

但是bind，call，apply这些方法绑定的this是存在哪里的呢？bind的mixin底层也是调用的apply。</div>2019-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（0） 💬（1）<div>https:&#47;&#47;github.com&#47;aimingoo&#47;prepack-core 我克隆下来了  我不理解在如何引擎级别打断点？ 不知道怎么搞 看到一个scripts文件夹里面有 test262-runner.js文件  然后运行了脚本没运行成功。</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（0） 💬（1）<div>我在浏览器中输出的方法中没有看到 [[HomeObject]]插槽，老师这个能在哪里找到吗？</div>2019-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3a/93/d7be8a1a.jpg" width="30px"><span>晓小东</span> 👍（0） 💬（1）<div>问题1： 如果super.xxx.bind(obj)() xxx执行上下文的thisValue域 将会被改变为obj， 而调用super.yyy()则按正常处理逻辑进行。（我这里只是测试了下执行效果， 老师可否用引擎执行层面的术语帮我们解答一下）
问题2： super 是静态绑定的，也就是说super引用跟我们书写代码位置有关。super引用的thisValue是动态运行，是从执行环境抄写过来的，所以当我调用一个从别处声明的方法是，其super代表其他地方声明对象的父类。（不知道这样表述的正不正确）代码如下：
    let test = {
        a() {
            this.name = super.name;
        } 
    }
    Object.setPrototypeOf(test, {name: &#39;test proto&#39;})

    class B extends A {
        constructor() {
            super();
            this.a = test.a;
            this.a();
            console.log(this.name);  &#47;&#47; test proto
        }
    }

问题3： super.xxx 如果是属性，也就代表对属性的进行存取两个操作 当super.xxx 进行取值时 super 所代表的的是父类的对象，super.xxx(规范引用：父类的属性引用）所以可以正常取到父类的属性值（值类型数据或引用类型据）
但如果向super.xxx置值时，此时会发生在当前this身上（而不是父类对象身上）。 分析：应当是当super.xxxx当做左操作数时（规范引用）,会从其引用thisValue取值，属性存取发生在了thisValue所在引用类型的数据数据身上，而该引用正是当前被抄写过来的this
总结： super.xxx 取值时拿到的是父类的属性值
super.xxx 置值时会作用在当前this, 也就是实例身上
这样可以防止父类对象在子类实例化中被篡改

有个问题老师，对于规范引用是否都有一个thisValue域， 是只有SuperReference有吗， 其作用是什么？</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/33/07/8f351609.jpg" width="30px"><span>JustDoDT</span> 👍（0） 💬（1）<div>老师能不能详细贴一下每讲对应的 ecma 规范地址呢？对照着看会更好 </div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/96/da/862a9599.jpg" width="30px"><span>恐怖如斯</span> 👍（0） 💬（0）<div>之前看关于super的题感觉好乱好难背容易忘，看了老师的课后，理解了如何实现的原理反而清晰易懂，赞</div>2022-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/28/4c/afe2ab34.jpg" width="30px"><span>云</span> 👍（0） 💬（0）<div>好绕，难懂。 得静下心来多刷，然后看评论。

老师很厉害。</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/0e/ce/1e02a513.jpg" width="30px"><span>刘大夫</span> 👍（0） 💬（0）<div>不得不说，super 这节讲的真好，其实也不一定非得逐字逐句把周老说的抠懂，毕竟每个人的表达方式都不一样。再加上周老多少年的浸淫，有些含义不是几句话就能说清楚的，我的收获是，
1、super 当做函数使用，只能在子类的 constructor 中调用，ES6规范规定继承时必须先跑一次super();
2、super 当做对象使用，如果是在类的一般方法(原型方法)里，其“主对象” 就是这个类的原型，若 Child extends Parent，其主对象就是 Parent，那么 super 指向 Parent.prototype；
如果在类的静态方法里使用，主对象就是这个类 Child 本身，super 指向 主对象的原型即 Parent；
如果在对象字面量声明的方法里使用，道理和上面一样，可以自己写个方法试试
class Parent {
        constructor() {
          &#47;&#47; console.log(new.target);
        }
        a() {
          console.log(&#39;Parent a&#39;);
        }
        b () {
          console.log(&#39;Parent b&#39;)
        }
        static b() {
          console.log(&#39;Parent static b&#39;);
        }
      }

      class Child extends Parent {
        constructor() {
          super();
        }
        a() {
          console.log(super.prototype);
          &#47;&#47; super.b();
        }
        static a() {
          console.log(super.prototype.constructor);
          &#47;&#47; super.a();
        }
        static b() {
          super.b();
        }
      }

      const child = new Child();
      child.a();
      &#47;&#47; Child.b();
      Child.a();</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/ae/a0/707350ef.jpg" width="30px"><span>穿秋裤的男孩</span> 👍（0） 💬（0）<div>2. 就是一般声明，那么该方法的主对象就是该类所使用的原型，也就是 AClass.prototype。
-----------------
eg:
class Parent {
   getName() { return &#39;Parent prototype name&#39; }
};
class Son extends Parent {
   getName() {
      console.log(super.getName === Son.prototype.__proto__.getName);
      console.log(super.getName === Son.prototype.getName);
   }
}
const s = new Son();
s.getName(); &#47;&#47; true; false;
--------------------
问：从打印的结果看，如果是普通形式的声明，那么方法内部的super应该是指向Son.prototype.__proto__对象，而不是Son.prototype。
我感觉这个super就是当前对象的__proto__，即伪代码：obj.__proto__ === obj.super</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>老师讲得很好，我要再消化消化</div>2019-12-16</li><br/>
</ul>