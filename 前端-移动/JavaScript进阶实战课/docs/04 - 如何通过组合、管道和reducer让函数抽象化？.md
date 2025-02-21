你好，我是石川。

上节课我们讲到，通过部分应用和柯里化，我们做到了从抽象到具象化。那么，今天我们要讲的组合和管道，就是反过来帮助我们把函数**从具象化变到抽象化**的过程。它相当于是系统化地把不同的组件函数，封装在了只有一个入口和出口的函数当中。

其实，我们在上节课讲处理函数输入问题的时候，在介绍unary的相关例子中，已经看到了组合的雏形。在函数式编程里，组合（Composition）的概念就是把组件函数组合起来，形成一个新的函数。

![图片](https://static001.geekbang.org/resource/image/50/a0/5087972778481dd701518185a2866fa0.jpg?wh=1920x944)

我们可以先来看个简单的组合函数例子，比如要创建一个“判断一个数是否为奇数”的isOdd函数，可以先写一个“计算目标数值除以2的余数”的函数，然后再写一个“看结果是不是等于1”的函数。这样，isOdd函数就是建立在两个组件函数的基础上。

```javascript
var isOdd = compose(equalsToOne, remainderOfTwo);
```

不过，你会看到这个组合的顺序是反直觉的，因为如果按照正常的顺序，应该是先把remainderByTwo放在前面来计算余数，然后再执行后面的equalsToOne， 看结果是不是等于1。

那么，这里为什么会有一个反直觉的设计呢？今天这节课，我们就通过回答这个问题，来看看组合和管道要如何做到抽象化，而reducer又是如何在一系列的操作中，提高针对值的处理性能的。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/17/2b/c7/9c8647c8.jpg" width="30px"><span>鐘</span> 👍（10） 💬（3）<div>靜下心來重看一次, 好像看懂了, 以下是我對於 composeReducer 的實作：

```
const { filterTR, mapTR, composeReducer } = (() =&gt; {
	function applyTypeForFunction(fn, type) {
		fn.type = type;
		return fn;
	}

	function filterTR(fn) {
		return applyTypeForFunction(fn, &quot;filter&quot;);
	}

	function mapTR(fn) {
		return applyTypeForFunction(fn, &quot;map&quot;);
	}

	function composeReducer(inputArray, fnArray) {
		return inputArray.reduce((sum, element) =&gt; {
			let tmpVal = element;
			let tmpFn;

			for (let i = 0; i &lt; fnArray.length; i++) {
				tmpFn = fnArray[i];
				if (tmpFn.type === &quot;filter&quot; &amp;&amp; tmpFn(tmpVal) === false) {
					console.log(`failed to pass filter: ${element} `);
					return sum;
				}
				if (tmpFn.type === &quot;map&quot;) {
					tmpVal = tmpFn(tmpVal);
				}
			}

			console.log(`${element} pass, result = ${tmpVal}`);
			sum.push(tmpVal);

			return sum;
		}, []);
	}

	return {
		filterTR,
		mapTR,
		composeReducer
	};
})();

const isEven = (v) =&gt; v % 2 === 0;
const passSixty = (v) =&gt; v &gt; 60;
const double = (v) =&gt; 2 * v;
const addFive = (v) =&gt; v + 5;

var oldArray = [36, 29, 18, 7, 46, 53];
var newArray = composeReducer(oldArray, [
	filterTR(isEven),
	mapTR(double),
	filterTR(passSixty),
	mapTR(addFive)
]);

console.log(newArray);
```</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0c/56/9b2bca2f.jpg" width="30px"><span>卡卡</span> 👍（5） 💬（1）<div>我的理解是：reduce可以对原集合的每个元素使用map回调函数进行映射或者使用filter回调函数进行过滤，然后将新值放入新的集合

mapReduce的实现：
Array.prototype.mapReduce = function (cb, initValue) {
  return this.reduce(function (mappedArray, curValue, curIndex, array) {
    mappedArray[curIndex] = cb.call(initValue, curValue, curIndex, array);
    return mappedArray;
  }, []);
};

filterReduce的实现：
Array.prototype.filterReduce = function (cb, initValue) {
  return this.reduce(function (mappedArray, curValue, curIndex, array) {
    if (cb.call(initValue, curValue, curIndex, array)) {
      mappedArray.push(curValue);
    }
    return mappedArray;
  }, []);
};</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/3e/d7/399d2ba5.jpg" width="30px"><span>雨中送陈萍萍</span> 👍（2） 💬（2）<div>看了下阮老师对PointFree风格的描述(https:&#47;&#47;www.ruanyifeng.com&#47;blog&#47;2017&#47;03&#47;pointfree.html)，可以直接简单理解成对多个运算过程的合成，不涉及到具体值的处理，所以compose和pipeline就是这种风格.</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/a2/95/8f34237c.jpg" width="30px"><span>I keep my ideals💤</span> 👍（2） 💬（1）<div>想请教一下老师compose组合的新函数里面如果有某一个是异步函数，或者没有返回值的情况下该怎么处理呢。还有多条件分支的情况下又该如何处理呢</div>2022-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/dd/a6/4d0c9ee6.jpg" width="30px"><span>程序员一土</span> 👍（1） 💬（1）<div>业务上函数拆这么细会被打吧</div>2022-12-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c9/55/3b2526ce.jpg" width="30px"><span>深山何处钟</span> 👍（1） 💬（1）<div>请问老师，compose那个函数，直接fns后不接reverse，是不是就是pipe的效果呢？</div>2022-09-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（1） 💬（1）<div>最近两篇文章的知识常在框架和库的代码里面见到，也会给我们阅读源码提供帮助。
具体和抽象都是为使用目标服务的，不管是柯里化还是函数组件，都是给使用者提供某种场景下的便利性，只不过有的需要具体的手段，有的需要抽象的手段。</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/10/5e/42f4faf7.jpg" width="30px"><span>天择</span> 👍（1） 💬（1）<div>point free的理解：把参数去掉，是指参数的含义已经体现在函数声明（名字）里面了，比如equalsToOne，那就是说传入的值是否等于1，如果是equalsToA，那么这个A就得传为参数，加上要比较的x就是两个参数了。这就是所谓“暴露给使用者的就是功能本身”。</div>2022-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/56/08/bd75f114.jpg" width="30px"><span>WGH丶</span> 👍（0） 💬（1）<div>function compose(...fns) {
    return fns.reverse().reduce( function reducer(fn1,fn2){
        return function composed(...args){
            return fn2( fn1( ...args ) );
        };
    } );
}


老师好，请教下：这里如果不用reverse，且交换下fn1，fn2的执行顺序能达到同样的效果。之所以使用reverse，是为了保证fn1先于fn2执行吗，还是别的原因？</div>2022-12-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/f7/3b/b94f06bb.jpg" width="30px"><span>23568</span> 👍（0） 💬（1）<div>
var oldArray = [36, 29, 18, 7, 46, 53];

var newArray = composeReducer(oldArray, [
  filterTR(isEven),
  mapTR(double),
  filterTR(passSixty),
  mapTR(addfive),
]); 

console.log (newArray); &#47;&#47; 返回：[77,97]

“在这个例子里，我们对一组数组进行了一系列的操作，先是筛选出奇数，再乘以二，之后筛出大于六十的值，最后加上五。在这个过程中，会不断生成中间数组。”
看返回结果是 [77, 97] ，这里好像筛选出来的是奇数吧老师
</div>2022-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（0） 💬（1）<div>经常写函数式代码的时候函数套函数，不知道如何高效调试，不知道老师后面有没有经验分享。</div>2022-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/aa/1d/b8fdd622.jpg" width="30px"><span>laoergege</span> 👍（0） 💬（1）<div>```js

function compose(...fns) {
    return fns.reverse().reduce( function reducer(fn1,fn2){
        return function composed(...args){
            return fn2( fn1( ...args ) );
        };
    } );
}
```
这里 reverse 是不是多余了。。</div>2022-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（0） 💬（1）<div>Point-Free 这个例子是不是不对，毕竟 x 参数被显示定义了。
&#47;&#47; Not point-free - `x` is an explicit argument
var isOdd = (x) =&gt; equalsToOne(remainderOfTwo(x));

Pointe-Free Style

定义函数时，不显式地指出函数所带参数。这种风格通常需要柯里化或者高阶函数。也叫 Tacit programming。

&#47;&#47; 已知：
const map = (fn) =&gt; (list) =&gt; list.map(fn)
const add = (a) =&gt; (b) =&gt; a + b

&#47;&#47; 所以：

&#47;&#47; 非Points-Free —— number 是显式参数
const incrementAll = (numbers) =&gt; map(add(1))(numbers)

&#47;&#47; Points-Free —— list 是隐式参数
const incrementAll2 = map(add(1))

incrementAll 识别并且使用了 numbers 参数，因此它不是 Point-Free 风格的。 incrementAll2 仅连接函数与值，并不提及它所使用的参数，因为它是 Point-Free 风格的。

Point-Free 风格的函数就像平常的赋值，不使用 function 或者 =&gt;。</div>2022-10-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/af/07/a32e3f4e.jpg" width="30px"><span>灯火阑珊</span> 👍（0） 💬（1）<div>我是从制造业转行的，对pipe和流水线有天然的接受度，上个工序的半成品就是下个工序的入参。</div>2022-09-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/08/8b/1b7d0463.jpg" width="30px"><span>晴空万里</span> 👍（0） 💬（0）<div>从第二节开始作为一个初学者感觉很费劲是不是得补充点基础课？</div>2023-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/6f/10/bfbf81dc.jpg" width="30px"><span>海绵薇薇</span> 👍（0） 💬（0）<div>我理解使用composeReducer或者管道计算步骤没有变（因为每个函数还是单一功能），区别是composeReducer将计算过程在内部组装好了，并且计算的中间值也是由composeReducer内部进行传递，所以从封装角度来看文章中的案例，composeReducer的封装程度要高于管道。

附上我的composeReducer版本：

const filterTR = (condition) =&gt; (value) =&gt; value.filter(condition);

const mapTR = (mapValue) =&gt; (value) =&gt; value.map(mapValue);

function composeReducer(val, reducerlist) {
  return reducerlist.reduce((total, cur) =&gt; cur(total), val);
}

function isEven(val) {
  return val % 2 === 0;
}

function double(val) {
  return val * 2;
}

function passSixty(val) {
  return val &gt; 60;
}

function addFive(val) {
  return val + 5;
}

var oldArray = [36, 29, 18, 7, 46, 53];
var newArray = composeReducer(oldArray, [filterTR(isEven), mapTR(double), filterTR(passSixty), mapTR(addFive)]);
console.log(newArray); &#47;&#47; 返回：[77,97]</div>2023-01-12</li><br/>
</ul>