你好，我是石川。

今天，我们来讲讲JavaScript中的this。其实讲this的资料有很多，其中不少已经把这个概念讲的很清楚了。但是为了课程的系统性，我今天也从这个单元咱们讲到的**对象和面向对象的角度**来说一说。

因为现在正好赶上国庆假期，咱们这节课的内容不是很长，所以你学起来也不会很辛苦。但是字少事大，this的概念还是很重要的。所以如果你之前没有具体了解过，还是希望这节课能帮助你更好地理解this。

从直观的印象来看，你可能觉得 this 指的是函数本身或它所在的范围，其实这样的理解都是不对。在JavaScript中，this 是在运行时而不是编写时绑定的。所以要正确地使用它，需要考虑到函数调用时的执行上下文。

## 默认绑定

我们来看一个简单的例子，在下面的例子中，a 是在全局定义的，aLogger的函数是在全局被调用的，所以返回的this就是全局上下文，所以a的值自然就是2。

```javascript
function aLogger() {
    console.log( this.a );
}
var a = 2;
aLogger(); // 2
```

这种默认的绑定只在非strict mode的情况下是可以的。所以如果在strict mode下，这种默认的的绑定是不可以的，则会返回 TypeError: `this` is `undefined`。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/6d/d6/f071d69d.jpg" width="30px"><span>缄默</span> 👍（4） 💬（3）<div>关于“new 是强于 hard binding 的”结论这一块的例子，bind方法本身就是返回一个新函数，对logger这个函数并无影响。而new出来的obj2的this肯定只与new传参时的值相关 。所以这个例子并不能推论出这一结论</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（3） 💬（1）<div>其他语言中也有this，python也有类似的self。JS的特殊之处在于支持多种编程范式，比如面向对象和函数式编程。本来this是在面向对象中使用就好，但是JS中没有类，有时候要靠函数创建对象，自然地，this从面向对象中被“移植”到了函数式编程中。像new，bind，apply，箭头函数这些，都像是一些补丁，以便更好地同时支持两种编程方式。正是这种适配，导致了JSer理解上的困惑。

java没有这个问题，其函数不能独立于对象使用。python虽然支持函数独立于对象使用，但是在对象外的函数，不再支持self，因此也没有这个困惑。</div>2022-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a8/cc/7a507bf9.jpg" width="30px"><span>了ei磊</span> 👍（1） 💬（1）<div>隐式绑定那一节, aLogger跟代码里不一致</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（0）<div>简答总结下，js 确实麻烦，作为一个 Android 工程师，我觉得还是 java 和 kotlin 好～～～～

1、全局作用域下，this 始终指向全局对象 window，无论是否是严格模式！

2、普通函数内的 this 分为两种情况，严格模式下和非严格模式下。

严格模式下：直接调用函数，this 指向 undefined，window.test() 调用函数 this 指向 window
非严格模式下：直接调用函数和 window.test() 调用函数对象，this 都指向 window。

3、对象内部方法的 this 指向调用这些方法的对象，也就是谁调用就指向谁。多层嵌套的对象，内部方法的 this 指向离被调用函数最近的对象。

4、箭头函数：this 指向于函数作用域所用的对象。
箭头函数的重要特征：箭头函数中没有 this 和 arguments，都是从外层继承的；
箭头函数会捕获自己定义所处的外层执行环境，并且继承这个 this 值，指向当前定义时所在的对象。
箭头函数的 this 指向在被定义的时候就确定了，之后永远都不会改变。即使使用 call()、apply()、bind() 等方法改变 this 指向也不可以。

5、构造函数中的 this 是指向构造函数创建的实例。

6、原型链中的 this：在一个继承机制中，仍然是指向它原本属于的对象，而不是从原型链上找到它时，它所属于的对象。

</div>2023-03-14</li><br/>
</ul>