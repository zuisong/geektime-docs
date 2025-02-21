在[上篇文章](https://time.geekbang.org/column/article/127495)中，我们讲了词法作用域、作用域链以及闭包，并在最后思考题中留了下面这样一段代码：

```
var bar = {
    myName:"time.geekbang.com",
    printName: function () {
        console.log(myName)
    }    
}
function foo() {
    let myName = "极客时间"
    return bar.printName
}
let myName = "极客邦"
let _printName = foo()
_printName()
bar.printName()
```

相信你已经知道了，在printName函数里面使用的变量myName是属于全局作用域下面的，所以最终打印出来的值都是“极客邦”。这是因为JavaScript语言的作用域链是由词法作用域决定的，而词法作用域是由代码结构来确定的。

不过按照常理来说，调用`bar.printName`方法时，该方法内部的变量myName应该使用bar对象中的，因为它们是一个整体，大多数面向对象语言都是这样设计的，比如我用C++改写了上面那段代码，如下所示：

```
#include <iostream>
using namespace std;
class Bar{
    public:
    char* myName;
    Bar(){
      myName = "time.geekbang.com";
    }
    void printName(){
       cout<< myName <<endl;
    }  
} bar;

char* myName = "极客邦";
int main() {
	bar.printName();
	return 0;
}
```

在这段C++代码中，我同样调用了bar对象中的printName方法，最后打印出来的值就是bar对象的内部变量myName值——“time.geekbang.com”，而并不是最外面定义变量myName的值——“极客邦”，所以**在对象内部的方法中使用对象内部的属性是一个非常普遍的需求**。但是JavaScript的作用域机制并不支持这一点，基于这个需求，JavaScript又搞出来另外一套**this机制**。

所以，在JavaScript中可以使用this实现在printName函数中访问到bar对象的myName属性了。具体该怎么操作呢？你可以调整printName的代码，如下所示：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/d9/c6/8be8664d.jpg" width="30px"><span>ytd</span> 👍（210） 💬（9）<div>&#47;&#47; 修改方法一：箭头函数最方便
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(() =&gt; {
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = &#39;female&#39;
    },100)
  }
}

userInfo.updateInfo()
setTimeout(() =&gt; {
  console.log(userInfo)
},200)

&#47;&#47; 修改方法二：缓存外部的this
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    let me = this;
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(function() {
      me.name = &quot;pony.ma&quot;
      me.age = 39
      me.sex = &#39;female&#39;
    },100)
  }
}

userInfo.updateInfo()
setTimeout(() =&gt; {
  console.log(userInfo);
},200)

&#47;&#47; 修改方法三，其实和方法二的思路是相同的
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    void function(me) {
      setTimeout(function() {
        me.name = &quot;pony.ma&quot;
        me.age = 39
        me.sex = &#39;female&#39;
      },100)
    }(this);
  }
}

userInfo.updateInfo()
setTimeout(() =&gt; {
  console.log(userInfo)
},200)

let update = function() {
  this.name = &quot;pony.ma&quot;
  this.age = 39
  this.sex = &#39;female&#39;
}

方法四: 利用call或apply修改函数被调用时的this值(不知掉这么描述正不正确)
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(function() {
      update.call(userInfo);
      &#47;&#47; update.apply(userInfo)
    }, 100)
  }
}

userInfo.updateInfo()
setTimeout(() =&gt; {
  console.log(userInfo)
},200)

&#47;&#47; 方法五: 利用bind返回一个新函数，新函数被调用时的this指定为userInfo
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  update: function() {
    this.name = &quot;pony.ma&quot;
    this.age = 39
    this.sex = &#39;female&#39;
  },
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(this.update.bind(this), 100)
  }
}</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f1/15/8fcf8038.jpg" width="30px"><span>William</span> 👍（28） 💬（7）<div>setTimeOut() 函数内部的回调函数，this指向全局函数。修复：在外部绑this或者使用箭头函数。
```
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex: &quot;male&quot;,
  updateInfo:function(){
    let that = this;
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(()=&gt;{
      that.name = &quot;pony.ma&quot;
      that.age = 39
      that.sex = &quot;female&quot;
    },100)
  }
}

userInfo.updateInfo()
```

```
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex: &quot;male&quot;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(()=&gt;{
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = &quot;female&quot;
    },100)
  }
}

userInfo.updateInfo()
```

</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/26/cc28a05a.jpg" width="30px"><span>悬炫</span> 👍（25） 💬（8）<div>关于箭头函数，文章中说其没有自己的执行上下文，难道箭头函数就像let定义的变量一样是哥块级作用域吗？其内部定义的变量都是存储在词法环境中是吗？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/be/53/71057a8b.jpg" width="30px"><span>风一样的浪漫</span> 👍（15） 💬（2）<div>老师请问下outer的位置是在变量对象内还是外，第10节描述是在内部的，可是11节的图outer放在变量对象外面了</div>2019-09-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4d/04/5e0d3713.jpg" width="30px"><span>李懂</span> 👍（6） 💬（5）<div>文章只是简单讲了下this的几种场景，不像前面变量申明，可以很清晰的知道在执行上下文的位置，也没有画图，看完还是不知道不能深入理解，更多的是一种记忆，这种是指向window，那种是指向对象。能不能深入到是如何实现this，才能知道缺陷的原因，这里一直是没理解的难点！</div>2019-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（6） 💬（1）<div>思考题，有两种方法
1. 将 setTimeout 里面的函数变成箭头函数
2. 在 setTimeout 外将 this 赋值给其他的变量，setTimeout 里面的函数通过作用域链去改变 userInfo 的属性

很不错的文章，受益匪浅，感谢老师。这里有一个疑问就是，关于箭头函数，文章中说其没有自己的执行上下文，这里指的是箭头函数并不会创建自己的执行上下文变量并压栈，其只是被看作是一个块区域吗？那么在实际的开发中如何在普通函数和箭头函数之间做选择？关于这一点，老师有没有相关推荐的文章呢？谢谢老师</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/cf/3e/5c684022.jpg" width="30px"><span>朱维娜🍍</span> 👍（4） 💬（3）<div>之前看到一种说法：this指向的永远是调用它的对象。按照这种说法，嵌套函数的调用者是window，与文中所述的“showThis调用内部函数不能继承this”有所出入，想请老师解答一下这种说法是否正确？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/c9/ba/f50e9ea4.jpg" width="30px"><span>潘启宝</span> 👍（3） 💬（6）<div>let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(function(){
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = &#39;female&#39;
    }.bind(this),100)
  }
}

userInfo.updateInfo()</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/28/8c83d109.jpg" width="30px"><span>子曰</span> 👍（1） 💬（1）<div>let userInfo = {
    name:&quot;jack.ma&quot;,
    age:13,
    sex:&quot;male&quot;,
    updateInfo:function(){
      &#47;&#47; 模拟 xmlhttprequest 请求延时
      setTimeout(()=&gt;{
        this.name = &quot;pony.ma&quot;
        this.age = 39
        this.sex = &quot;female&quot;
      },100)
    }
  }
  userInfo.updateInfo()</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（1） 💬（1）<div>延时函数更新此时的this对象指向了window全局对象。
解决方法就是文章老师提到的两种方法。
1 this保存给self变量，通过变量作用域机制传递给嵌套函数。
2箭头函数去锁定函数定义时候的this对象，箭头函数没有上下文，它会继承函数初始化对应上下文。

思考:
1 能否通过bind和apply改变箭头函数this指向？
回头试一下，然后好好理理这几节内容

</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/80/7a/02fdf1a2.jpg" width="30px"><span>FreezeSoul</span> 👍（0） 💬（2）<div>感觉还缺一个property，原型链</div>2020-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEKpW6pOyXOVXF31iaLJsxAqEoPs5pa4om9icGU8fEECAaA1ZPLB21TgyNRiaibypChBiaBrSs3iaMau4qzg/132" width="30px"><span>Geek_b42f75</span> 👍（0） 💬（3）<div>发现一个事，虽然setTimeout改成箭头函数了，里面的this指向userInfo这个对象了。
但是在console.log(userInfo.age)打印age的时候，为什么还是13，没有改成39呢？
我看不用setTimeout，直接在updateInfo方法里调用this.age = 39是能改变的。
let userInfo = {
     name:&quot;jack.ma&quot;,
     age:13,
     sex:&#39;male&#39;,
     updateInfo:function(){
        &#47;&#47; this.age = 39
        &#47;&#47; 模拟 xmlhttprequest 请求延时
        setTimeout( () =&gt; {
            this.name = &quot;pony.ma&quot;
            this.age = 39
            this.sex = &#39;female&#39;
         },100)
      }
}
userInfo.updateInfo()
console.log(userInfo.age)</div>2019-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/84/b91ee3a9.jpg" width="30px"><span>stone</span> 👍（0） 💬（1）<div>
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:male,
  &#47;&#47; 1, 
  const that = this
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(function(){
      that.name = &quot;pony.ma&quot;
      that.age = 39
      that.sex = female
    },100)
  }

  &#47;&#47; 2 
  updateInfo :function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(() =&gt; {
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = female
    },100)
  }
}

userInfo.updateInfo()
</div>2019-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbh5FQajwKhNlMrkoSklPpOXBtEYXCLvuWibhfWIS9QxHWDqzhEHJzEdmtUiaiaqFjfpsr2LwgNGpbQ/132" width="30px"><span>Geek_q29f6t</span> 👍（0） 💬（1）<div>思考题：
这份代码在开发中是很常见的一种操作，调用了api后，希望在callback中执行一些操作。但此时，callback中的this已经不是原先那个caller了（即题目中的updateInfo）, 而是callback

常见的方式是在后台的api中返回一个对象，如：{result: true, data:{name:&#39;pony.ma&#39;,age:39, sex:&#39;female&#39;}};

let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(function(resp){
	  if(resp.result){
	     var data = {name:&#39;pony.ma&#39;, age:39, sex:&#39;female&#39;}
         userInfo.name = data.name;
          userInfo.age = data.age;
          userInfo.sex = data.sex
	  }
      
    },100)
  }
}

userInfo.updateInfo()
</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/90/bb/c29f0f99.jpg" width="30px"><span>谢海涛</span> 👍（0） 💬（1）<div>let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&quot;male&quot;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(()=&gt;{
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = &quot;female&quot;
    },100)
  }
}</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/65/88/2aba7bb0.jpg" width="30px"><span>依然爱你</span> 👍（0） 💬（1）<div>和某位仁兄同样的问题，箭头函数没有自己的执行上下文，那么里面的变量环境和词法环境在哪？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/80/dae518d2.jpg" width="30px"><span>羽蝶曲</span> 👍（0） 💬（1）<div>var myObj = {
  name : &quot; 极客时间 &quot;,
  showThis: function(){
    this.name = &quot; 极客邦 &quot;
    console.log(this)
  }
}
var foo = myObj.showThis
foo();
(myObj.showThis)();
老师，您好，我想问个问题，为何(myObj.showThis)()的this指向的是myObj而不是window呢，和foo = myObj.showThis的区别是什么呢？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/94/82/d0a417ba.jpg" width="30px"><span>蓝配鸡</span> 👍（0） 💬（1）<div>思考题个人看法

settimeout中的回掉函数中的this是window

所以最终结果window里多了几个变量
调用的对象本身并没有update</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f0/de/ef564e67.jpg" width="30px"><span>歌在云端</span> 👍（0） 💬（2）<div>    let userInfo = {
        name: &quot;jack.ma&quot;,
        age: 13,
        sex: &quot;male&quot;,
        updateInfo: function () {
            &#47;&#47; 模拟 xmlhttprequest 请求延时

            &#47;&#47; setTimeout(function () {
            &#47;&#47;     this.name = &quot;pony.ma&quot;
            &#47;&#47;     this.age = 39
            &#47;&#47;     this.sex = &quot;female&quot;
            &#47;&#47; }.call(this), 100)
            setTimeout( () =&gt;{
                this.name = &quot;pony.ma&quot;
                this.age = 39
                this.sex = &quot;female&quot;
            }, 100)
        }
    }
试了一下用箭头函数和将this绑定到一个self变量上面都不可以，只有用call里面传入this才行。老师能讲一下为什么吗</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/67/80/dae518d2.jpg" width="30px"><span>羽蝶曲</span> 👍（0） 💬（1）<div>let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(()=&gt;{
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = &#39;female&#39;
    },100)
  }
}

userInfo.updateInfo()</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（1）<div>思考题：读了老师的文章，很容易解决这个问题。三种方式：
1.定义局部self：var self = this
2.使用箭头函数
3.内部function使用bind：setTimeout(function(){...}.bind(userInfo),100)</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/bb/5e5c37c1.jpg" width="30px"><span>Angus</span> 👍（0） 💬（1）<div>setTimeout的第一个参数是一个函数，这个函数将会延迟执行，执行时，这个函数的this将会指向全局window。解决办法就像文中提到的两种方式：使用self变量保存this或者使用箭头函数。

之前我是这么记忆this指向的：对于函数中的this，谁调用了这个函数，函数的this就指向谁；对于箭头函数，定义的时候就决定了this指向，在哪里定义的this就指向谁。

另外关于改变this的第二种方式：通过对象调用方式设置。利用这种方式，可以用来模拟实现call&#47;apply&#47;bind方法。

执行上下文包括：变量环境、词法环境、外部环境、this。

除了这种标准概念式的东西，其实更像知道为何这样设计，浏览器是如何处理的。</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/60/40/e6d4c1b4.jpg" width="30px"><span>ChaoZzz</span> 👍（0） 💬（5）<div>思考题：
1. 变量 self 保存外层 this
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
	const self = this;
    setTimeout(function(){
      self.name = &quot;pony.ma&quot;
      self.age = 39
      self.sex = &#39;female&#39;
    },100)
  }
}

2. 自执行函数把外层 this 传进去
let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout((function(context){
      context.name = &quot;pony.ma&quot;
      context.age = 39
      context.sex = &#39;female&#39;
    })(this),100)
  }
}

3. 改为箭头函数不创建执行上下文直接引用外层函数 this

let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&#39;male&#39;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    setTimeout(() =&gt; {
      this.name = &quot;pony.ma&quot;
      this.age = 39
      this.sex = &#39;female&#39;
    },100)
  }
}</div>2019-08-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/3XbCueYYVWTiclv8T5tFpwiblOxLphvSZxL4ujMdqVMibZnOiaFK2C5nKRGv407iaAsrI0CDICYVQJtiaITzkjfjbvrQ/132" width="30px"><span>有铭</span> 👍（0） 💬（2）<div>老师，你不觉得箭头函数这种“与众不同的没有自己上下文”的设计，也是一种问题吗？</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/d7/a2/5f6b90a9.jpg" width="30px"><span>wuqilv</span> 👍（0） 💬（2）<div>let userInfo = {
  name:&quot;jack.ma&quot;,
  age:13,
  sex:&quot;male&quot;,
  updateInfo:function(){
    &#47;&#47; 模拟 xmlhttprequest 请求延时
    that = this
    setTimeout(function(){
      that.name = &quot;pony.ma&quot;
      that.age = 39
      that.sex = &quot;female&quot;
    },100)
  }
}

userInfo.updateInfo()</div>2019-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b3/26/cc28a05a.jpg" width="30px"><span>悬炫</span> 👍（94） 💬（1）<div>老师的文章是我目前见过的，将浏览器原理讲的最生动易懂的文章了，没有之一，大赞</div>2020-05-01</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVBIIzaXQs2Y6rcwwOK510sowo5dH4zTQ2lUuQwsEW4OeDpKgBcEDHN8RcHZ1w2WmFhozAsNFlbA/132" width="30px"><span>刘晓东</span> 👍（8） 💬（3）<div>老师您好，我想问您一下，这些知识您是怎么获得的？是看的书，还是自己研究了什么源代码？方便告知吗？</div>2020-03-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/9b/e0ef47df.jpg" width="30px"><span>凭实力写bug</span> 👍（8） 💬（1）<div>我记得执行上下文包括变量环境,词法环境,outer,this,如果箭头函数没有执行上下文,他的这些内容又是怎样的,还有他的作用域呢</div>2019-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/7e/89/0a9c4a35.jpg" width="30px"><span>大威先生🐯🐯</span> 👍（6） 💬（0）<div>最后一个案例中，myObj对象的 showThis函数内部定义了bar函数，bar函数的执行环境具有全局性，因此this对象通常指向window；----摘要《JavaScript高级程序设计》</div>2019-10-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/ce/52/67781a8a.jpg" width="30px"><span>White</span> 👍（4） 💬（0）<div>老师，关于箭头函数，文章中说”箭头函数并不会创建其自身的执行上下文“，那么在调用箭头函数时，是将什么推入调用栈了呢？其内部变量又放在哪里了呢？我看评论并没有说的很清楚呢？这块是否可以讲具体些呢？执行箭头函数时，是怎样一个过程呢？</div>2020-07-30</li><br/>
</ul>