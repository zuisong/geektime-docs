你好，我是周爱民。

今天这一讲的标题呢，比较长。它是我这个专栏中最长的标题了。不过说起来，这个标题的意义还是很简单的，就是返回一个用`Object.create()`来创建的对象。

因为用到了`return`这个子句，所以它显然应该是一个函数中的退出代码，是不能在函数外单独使用的。

这个函数呢，必须是一个构造器。更准确地说，标题中的代码必须工作在构造过程之中。因为除了`return`，它还用到了一个称为元属性（*meta property*）的东西，也就是`new.target`。

迄今为止，`new.target`是JavaScript中唯一的一个元属性。

## 为什么需要定义自己的构建过程

通过之前的课程，你应该知道：JavaScript使用原型继承来搭建自己的面向对象的继承体系，在这个过程中诞生了两种方法：

1. 使用一般函数的构造器；
2. 使用ECMAScript 6之后的类。

从根底上来说，这两种方法的构建过程都是在JavaScript引擎中事先定义好了的，例如在旧式风格的构造器中（以代码`new X`为例），对象`this`实际上是由new运算依据`X.prototype`来创建的。循此前例，ECMAScript 6中的类，在创建`this`对象时也需要这个`X.prototype`来作为原型。
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/a6/6373416f.jpg" width="30px"><span>青史成灰</span> 👍（3） 💬（2）<div>老师，最后的这个例子：
```

class MyClass {
  constructor() { return new Date };
}

class MyClassEx extends MyClass {
  constructor() { super() }; &#47;&#47; or default
  foo() {
    console.log(&#39;check only&#39;);
  }
}

var x = new MyClassEx;
console.log(&#39;foo&#39; in x); &#47;&#47; false
```
因为`foo`并不在`x`实例上，那假如我要访问`foo`，那得通过什么方式？或者说，那我这个类中定义的`foo`定义到哪里去了？</div>2020-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/13/7b/74e90531.jpg" width="30px"><span>Astrogladiator-埃蒂纳度斯</span> 👍（3） 💬（1）<div>new.target为什么称为元属性，它与a.b（例如 super.xxx，或者’a’.toString）有什么不同？
个人理解是new.target是用来描述构造器本身的属性，指代是当前这个构造器函数this， 它不属于实例对象的一部分，它可以由super函数传递至根类，并最终由根类创建带有子类实例的对象。</div>2019-12-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（3） 💬（2）<div>这里的代码在 Chrome 或 Node 是报错的


class MyClass extends Object {
  constructor() {
    return 1;
  }
}

function MyConstructor() {
  return 1;
}


console.log(new MyClass)
console.log(new MyConstructor)</div>2019-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e8/43/f9c0faed.jpg" width="30px"><span>小童</span> 👍（2） 💬（2）<div>老师，我在看规范的时候，有那么一句话不理解，状态和方法都会被对象承载，结构，行为和状态都能被继承。
这句怎么理解呢？
比如:
function Car(){


}
Car.prototype.name=&quot;car1&quot;;
Car.prototype.run=function(){
     console.log(&quot;run&quot;)
}
var car1=new Car();
&#47;&#47;对象 承载状态和方法 指name 状态 run方法

function Dog(){

}
Dog.prototype=Car.prototype;
&#47;&#47;继承 Dog 继承了Car对象的结构 行为指继承了run方法吗？ 状态是name属性吗？</div>2020-04-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/18/11/f1f37801.jpg" width="30px"><span>James</span> 👍（2） 💬（1）<div>老师，在看react源码的context时候，遇到一个问题，简化如下，如果var a = {}, a.a =a,最终a.a.a...好像会无限下去，这样，会不会执行这个代码的时候，就内存泄漏了啊，如果造成内存泄漏的化，怎么会在react源码里面呢？

export function createContext&lt;T&gt;(
  defaultValue: T,
  calculateChangedBits: ?(a: T, b: T) =&gt; number,
): ReactContext&lt;T&gt; {

  const context: ReactContext&lt;T&gt; = {
    $$typeof: REACT_CONTEXT_TYPE,
    _calculateChangedBits: calculateChangedBits,
    _currentValue: defaultValue,
    _currentValue2: defaultValue,
    Provider: (null: any),
    Consumer: (null: any),
  };

  context.Provider = {
    $$typeof: REACT_PROVIDER_TYPE,
    _context: context,
  };

  let hasWarnedAboutUsingNestedContextConsumers = false;
  let hasWarnedAboutUsingConsumerProvider = false;
context.Consumer = context;

  return context;
}
</div>2020-03-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d4/37/528a43e7.jpg" width="30px"><span>Elmer</span> 👍（1） 💬（1）<div>定制的构造方法中，如果返回通过return传出的对象（也就是一个用户定制的创建过程），这个时候返回的对象原型并不是子类的原型，那不是不需要再设置this的原型了吗。。
function test (){
  return {a: 1};
}
const b = new test();
b instanceof test  &#47;&#47; false;此时如果test有父类也不需要设置this的原型？</div>2020-01-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ee/28/c04a0c83.jpg" width="30px"><span>小炭</span> 👍（0） 💬（1）<div>“迄今为止，new.target是 JavaScript 中唯一的一个元属性。” 对这句话有疑惑，就是下面这些不是元属性吗？
{
  value: 123,
  writable: false,
  enumerable: true,
  configurable: false,
  get: undefined,
  set: undefined
}</div>2020-11-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>
&#47;&#47; 在JavaScript内置类Date()中可能的处理逻辑
function _Date() {
  this = Object.Create(Date.prototype, { _internal_slots });
  Object.setPrototypeOf(this, new.target.prototype);
  ...
}
1. Create应该是小写
2. 这段代码前面设置的__proto__会被后面的覆盖吧，下面这样实现没问题吧，和继承null那个例子类似
function _Date() {
  this = Object.create(new.target.prototype);
  ...
}</div>2020-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c2/8ffd2ad0.jpg" width="30px"><span>qqq</span> 👍（0） 💬（0）<div>因为可以改变默认的原型继承行为</div>2019-12-18</li><br/>
</ul>