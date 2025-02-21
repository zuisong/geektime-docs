你好，我是周爱民。

今天我只跟你聊一件事，就是JavaScript构造器。标题中的这行代码中规中矩，是我这个专栏题目列表中难得的正经代码。

> NOTE：需要稍加说明的是：这行代码在JavaScript 1.x的某些版本或具体实现中是不能使用的。即使ECMAScript ed1开始就将它作为标准语法之一，当时也还是有许多语言并不支持它。

**构造器**这个东西，是JavaScript中面向对象系统的核心概念之一。跟“属性”相比，如果属性是静态的结构，那么“构造器”就是动态的逻辑。

没有构造器的JavaScript，就是一个充填了无数数据的、静态的对象空间。这些对象之间既没有关联，也不能衍生，更不可能发生交互。然而，这却真的就是JavaScript 1.0那个时代的所谓“面向对象系统”的基本面貌。

## 基于对象的JavaScript

为什么呢？因为JavaScript1.0的时代，也就是最早最早的JavaScript其实是没有继承的。

你可能会说，既然是没有继承的，那么JavaScript为什么一开始就能声称自己是“面向对象”的、“类似Java”的一门语言呢？其实这个讲法是前半句对，后半句不对。JavaScript和Java名字相似，但语言特性却大是不同，这就跟北京的“海淀五路居”和“五路居”一样，差了得有20公里。
<div><strong>精选留言（18）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（11） 💬（1）<div>谈谈今天的理解：

在 instanceof 运算中，x instanceof AClass 表达式的右侧是一个类名（对于 instanceof 的理解之前是有误解，今天才领悟到）

ECMAScript 6 的类是由父类或祖先类创建 this 实例的（也就是 this 是继承而来的，也能够契合前面说的”在调用结束之前，是不能使用 this 引用。不知道这个理解能否正确）</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/a6/6373416f.jpg" width="30px"><span>青史成灰</span> 👍（7） 💬（1）<div>首先谢谢老师每次都认真的回答每个问题，但是下面的这个问题，我一下子没想明白。。。

```
function Device() {
  this.id = 0; &#47;&#47; or increment
}

function Car() {
  this.name = &quot;Car&quot;;
  this.color = &quot;Red&quot;;
}

Car.prototype = new Device();

var x = new Car();
console.log(x.id); &#47;&#47;
```
这个例子中， 为什么`x.constructor === Device`，按我的理解应该是`x.constructor === Car`才对。但是如果我把`Car.prototype = new Device()`这行代码注释掉，那么就符合我的理解了。。。</div>2020-01-12</li><br/><li><img src="" width="30px"><span>油菜</span> 👍（4） 💬（1）<div>“函数的“.prototype”的属性描述符中的设置比较特殊，它不能删除，但可以修改（‘writable’ is true）。当这个值被修改成 null 值时，它的子类对象是以 null 值为原型的；当它被修改成非对象值时，它的子类对象是以 Object.prototype 为原型的；否则，当它是一个对象类型的值时，它的子类才会使用该对象作为原型来创建实例。”
---------------------
老师，我的测试结果和这个结论不大一样。
function F(){ this.name1 = &#39;father&#39;}
function S1(){ this.name1 = &#39;son1&#39;}
F.prototype = null;
S1.prototype =F;
var s1 = new S1();
s1.constructor.prototype; &#47;&#47;原型对象是[Function] 而不是null
s1 instanceof S1;  &#47;&#47;true;
s1 instanceof F;  &#47;&#47;TypeError: Function has non-object prototype &#39;null&#39; in instanceof check
-------------
class S2 extends F {}
var s2 = new S2();
s2.constructor.prototype; &#47;&#47;  &#47;原型对象是S2 {}，不是null
s2 instanceof S2; &#47;&#47; true;
s2 instanceof F; &#47;&#47;Function has non-object prototype &#39;null&#39; in instanceof check</div>2020-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（1） 💬（1）<div>请问老师，constructor 这个属性是不是可有可无的？</div>2021-02-04</li><br/><li><img src="" width="30px"><span>二二</span> 👍（1） 💬（1）<div>老师您好，关于：有一些“类 &#47; 构造器”在 ECMAScript 6 之前是不能派生子类的，例如 Function，又例如 Date。
但是我看babel将es6转成es5是可以实现对于Function的继承，并调用的，请问babel是怎么达到这个效果的呢？
</div>2020-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/b3/15/01ef8470.jpg" width="30px"><span>人间动物园</span> 👍（1） 💬（3）<div>思考题 1 ，
直接执行一个函数也可以创建新的对象：
function Person(name){
    this.name = name;
    return this;
}
person1 = Person(&#39;xiaoming&#39;);</div>2020-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/97/abb7bfe3.jpg" width="30px"><span>CoolSummer</span> 👍（1） 💬（1）<div>1.创建新的对象
字面量方法创建、Object.create()、工厂模式、构造函数模式
2.操作原型 &#47; 原型链
Object.defineProperty( )&#47;Object.getProperty( )
ES6 的 proxy 和 Reflect</div>2020-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/78/51/4790e13e.jpg" width="30px"><span>Smallfly</span> 👍（1） 💬（1）<div>老师文中多次提到类继承，您这里指的是从类抄写属性到对象么？我的理解是这个过程属于对象的实例化。JS 只有原型继承一种方式。

还是说因为实例化的过程，包含向 this 对象写入原型，所以称它为类继承，并且包含原型继承？</div>2020-02-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/58/ba171e09.jpg" width="30px"><span>小胖</span> 👍（1） 💬（1）<div>{Foo () {}}创建的Foo方法不能使用new关键字调用；
但{Foo: function Foo() {}}是可以的。
所以说，ES6提供的方法简写形式添加的方法和不使用简写形式添加的方法是有区别的。
</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/08/c77d8a5a.jpg" width="30px"><span>Kids See Ghost</span> 👍（0） 💬（1）<div>请问老师，在规范里有没有具体哪里讲了如何比较两个object的？比如为什么两个empty object不想等 `{} !== {}` 在规范里找了很久没找到. 在规范里 https:&#47;&#47;tc39.es&#47;ecma262&#47;#sec-samevaluenonnumeric 只说了 &quot;7. If x and y are the same Object value, return true. Otherwise, return false. &quot;. 但是没有具体地说怎么样的object value算一样，怎么样算不一样。比如`{}` 和 `{}`就不一样。</div>2022-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/91/dc/eca877c4.jpg" width="30px"><span>Chor</span> 👍（0） 💬（1）<div>老师，下面这段话：
“函数的“.prototype”的属性描述符中的设置比较特殊，它不能删除，但可以修改（‘writable’ is true）。当这个值被修改成 null 值时，它的子类对象是以 null 值为原型的” 是否可以改成 “它的子类对象是以 Object.prototype 为原型的” 呢？
因为：
const Fn = function( ){ }
Fn.prototype = null
const obj = new Fn( )
Object.getPrototypeOf(obj) === Object.prototype      &#47;&#47; true
</div>2021-05-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（0） 💬（1）<div>我还是理解不了以下代码? `testF.call` 明明是function啊。
let testF = Object.create(Function.prototype);
testF.call({}) &#47;&#47;Uncaught TypeError: testF.call is not a function</div>2020-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>「后两种特征（没有[[Construct]]内部槽和prototype属性）完全排除了一个普通方法用作构造器的可能」
老师没有prototype能直接看到，「没有[[Construct]]内部槽」这个能看见吗，这是在方法对象上还是方法对象的原型链上？</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>在ES6之前 new X 先生成this,再将设置this.__proto__=X.prototype
那在class 继承中这一步是在何时执行的，最后一个supuer执行完后，还是最祖先类生成this的时候执行的？
class X extends Y{}
new X</div>2020-05-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（5） 💬（0）<div>Object.create( )
Object.defineProperty( )
ES6 的 proxy 和 Reflect</div>2019-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（3） 💬（0）<div>ES6操作原型&#47;原型链方法：Obejct.create()、Object.setPrototypeOf()、Object.getPrototypeOf()</div>2019-12-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（0） 💬（0）<div>1、Object.create()
</div>2019-12-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（0） 💬（1）<div>
function X() {
  this.x = 4
}

function Y() {
  this.y = 5
}

&#47;&#47; Y.prototype = new X()， new 运算可以用以下三行模拟。
var xxx = {}
X.apply(xxx)
xxx.__proto__ = X.prototype

Y.prototype = xxx

&#47;&#47; var y = new Y()
var y = {}
Y.apply(y)
y.__proto__ = Y.prototype
</div>2019-12-13</li><br/>
</ul>