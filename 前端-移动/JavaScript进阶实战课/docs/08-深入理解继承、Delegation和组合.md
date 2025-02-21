你好，我是石川。

关于面向对象编程，最著名的一本书就数[GoF](https://zh.wikipedia.org/zh-cn/%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F%EF%BC%9A%E5%8F%AF%E5%A4%8D%E7%94%A8%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E8%BD%AF%E4%BB%B6%E7%9A%84%E5%9F%BA%E7%A1%80)（Gang of Four）写的[《设计模式：可复用面向对象软件的基础》](https://book.douban.com/subject/34262305/)了。这本书里一共提供了23种不同的设计模式，不过今天我们不会去展开了解这些细节，而是会把重点放在其中一个面向对象的核心思想上，也就是**组合优于继承**。

在JS圈，有不少继承和组合的争论。其实无论是继承还是组合，我们都不能忘了要批判性地思考。批判性思考的核心不是批判，而是通过深度思考核心问题，让我们对事物能有自己的判断。

所以，无论是继承还是组合，都只是方式、方法，它们要解决的核心问题就是**如何让代码更加容易复用**。

![图片](https://static001.geekbang.org/resource/image/e3/ff/e32437db6ecda3149a4422a540ffc2ff.jpeg?wh=1920x1080)

那么接下来，我们就根据这个思路，看看JavaScript中是通过哪些方法来解决代码复用这个问题的，以及在使用不同的方法时它们各自解决了什么问题、又引起了什么问题。这样我们在实际的业务场景中，就知道如何判断和选择最适合的解决方式了。

## 继承

在传统的OOP里面，我们通常会提到继承（Inheritance）和多态（Polymorphism）。继承是用来在父类的基础上创建一个子类，来继承父类的属性和方法。多态则允许我们在子类里面调用父类的构建者，并且覆盖父类里的方法。

那么下面，我们就先来看下在JavaScript里，要如何通过构建函数来做继承。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/aa/1d/b8fdd622.jpg" width="30px"><span>laoergege</span> 👍（3） 💬（1）<div>组合优于继承，是不是更加适用于平时业务开发？做为基础设施给用户使用的场景，继承更加简洁方便？比如 react 框架下，提供的 Component 类。</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/2c/0f7baf3a.jpg" width="30px"><span>Change</span> 👍（1） 💬（0）<div> &#47;********* JS 中的类和继承中的 super **************** *&#47;
  function Widget() {
    this.appName = &quot;核心微件&quot;;
  }

  Widget.prototype.getAppName = function () {
    return this.appName;
  };

  function Calendar() {
    &#47;&#47; 调用super
    let widget = new Widget();
    this.__proto__.__proto__ = widget.__proto__; &#47;&#47; Calendar.prototype.__proto__ = Widget.prototype;
    for (let key in widget) {
      if (widget.hasOwnProperty(key)) {
        this[key] = widget[key];
      }
    }

    this.name = &quot;Calendar&quot;;
  }

  Calendar.prototype.getName = function () {
    return this.name;
  };

  &#47;**********Object.create************** *&#47;
  function Person() {
    this.name = &quot;Person&quot;;
  }

  &#47;&#47; Object.Create
  function ObjectCreate(o) {
    let obj = {};
    obj.__proto__ = o;
    return obj;
  }

  let o = ObjectCreate(new Person());</div>2022-10-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b5/32/43b46132.jpg" width="30px"><span>褚琛</span> 👍（1） 💬（0）<div>&#47;&#47;js中的类和继承
function Widget (appName) {
  this.appName = appName
}

Widget.prototype.getName = function() {
  return this.appName;
}

function Calendar (appName) {
  Widget.call(this, appName);
}

Calendar.prototype = { ...Widget.prototype };

var calendar = new Calendar(&#39;日历应用&#39;);
console.log(calendar.hasOwnProperty(&quot;appName&quot;)); &#47;&#47; 返回 true
console.log(calendar.getName()); &#47;&#47; 返回 &quot;日历应用&quot;
console.log(typeof calendar.getName); &#47;&#47; 返回 function
console.log(calendar.getName()); &#47;&#47; 返回 “日历应用”

&#47;&#47;Object.create()
function create(o) {
  let Cls = function() {};
  let obj = new Cls();
  obj.prototype = o;
  return obj;
}</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>ES6 当中的 assign 来做到组合混入，我看下和 java 的组合有很大的区别，java 是通过持有其他对象的引用来实现组合，js 是直接拷贝属性，差异很大</div>2023-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>作为一个 Android 工程师，我怎么感觉授权就是继承呢？？就是基于原型链的继承？？</div>2023-03-13</li><br/>
</ul>