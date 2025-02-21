你好，我是winter。

我们在上一节课中已经讲过了JavaScript语法的顶层设计，接下来我们进入到更具体的内容。

JavaScript遵循了一般编程语言的“语句-表达式”结构，多数编程语言都是这样设计的。我们在上节课讲的脚本，或者模块都是由语句列表构成的，这一节课，我们就来一起了解一下语句。

在JavaScript标准中，把语句分成了两种：声明和语句，不过，这里的区分逻辑比较奇怪，所以，这里我还是按照自己的思路给你整理一下。

普通语句：

![](https://static001.geekbang.org/resource/image/81/55/8186219674547691cf59e5c095304d55.png?wh=564%2A786)

声明型语句：

![](https://static001.geekbang.org/resource/image/0e/38/0e5327528df12d1eaad52c4005efff38.jpg?wh=1043%2A625)

我们根据上面的分类，来遍历学习一下这些语句。

## 语句块

我们可以这样去简单理解，语句块就是一对大括号。

```JavaScript
{
    var x, y;
    x = 10;
    y = 20;
}
```

语句块的意义和好处在于：让我们可以把多行语句视为同一行语句，这样，if、for等语句定义起来就比较简单了。不过，我们需要注意的是，语句块会产生作用域，我们看一个例子：

```JavaScript
{
    let x = 1;
}
console.log(x); // 报错
```

这里我们的let声明，仅仅对语句块作用域生效，于是我们在语句块外试图访问语句块内的变量x就会报错。

## 空语句

空语句就是一个独立的分号，实际上没什么大用。我们来看一下：

```JavaScript
;
```

空语句的存在仅仅是从语言设计完备性的角度考虑，允许插入多个分号而不抛出错误。
<div><strong>精选留言（24）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/1a/c3/02bb2ebe.jpg" width="30px"><span>尤璐洁</span> 👍（1） 💬（1）<div>老师可以讲讲arguments吗，它是挂在哪里的呢，是个可迭代对象，但是不知道它是哪个的属性</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/9b/5d/629fa226.jpg" width="30px"><span>洛克不菲勒</span> 👍（1） 💬（2）<div>for(let e of [1, 2, 3, 4, 5])
    console.log(e);
老师你好，注意到文中有这样的写法，for()后面没有大括号这种写法好吗？
一直都有这样的疑问，if语句也有这样的问题</div>2019-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/21/d5/95304b5b.jpg" width="30px"><span>润群</span> 👍（1） 💬（2）<div>关于switch和ifelse的效率我有个疑问呢，假设ifelse的判断很多，然后判断到末尾才找到匹配的项，这样的话是不是比switch多了好多判断呢，因为我理解的switch不是只判断一次么？</div>2019-06-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/01/568ac2d6.jpg" width="30px"><span>K4SHIFZ</span> 👍（1） 💬（1）<div>请问老师，规范中的Statement和Declaration到底有什么区别？不都是声明的意思吗？</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/55/cb/1efe460a.jpg" width="30px"><span>渴望做梦</span> 👍（0） 💬（2）<div>winter老师，这个异步生成器函数是个什么东东啊，从网上搜了一下，也没找到相关介绍。</div>2019-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f5/b8/9f165f4b.jpg" width="30px"><span>mfist</span> 👍（74） 💬（2）<div>遍历了下window上面的全局对象，上面有Symbol.iterator的原生属性有15个，主要Array Set Map String相关的。当然还有很多宿主环境提供的全局对象有Symbol.iterator属性，他们有个共同的特征：都是些集合性质的数据结构。
0: &quot;Array&quot;
1: &quot;String&quot;
2: &quot;Uint8Array&quot;
3: &quot;Int8Array&quot;
4: &quot;Uint16Array&quot;
5: &quot;Int16Array&quot;
6: &quot;Uint32Array&quot;
7: &quot;Int32Array&quot;
8: &quot;Float32Array&quot;
9: &quot;Float64Array&quot;
10: &quot;Uint8ClampedArray&quot;
11: &quot;BigUint64Array&quot;
12: &quot;BigInt64Array&quot;
13: &quot;Map&quot;
14: &quot;Set&quot;</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fc/64/dafdb4c3.jpg" width="30px"><span>Chuck</span> 👍（49） 💬（1）<div>Object.getOwnPropertyNames(window).filter(prop =&gt; {
	return window[prop] &amp;&amp; window[prop].prototype &amp;&amp; window[prop].prototype[Symbol.iterator]
}) 

Array,String,Uint8Array,Int8Array,Uint16Array,Int16Array,Uint32Array,Int32Array,Float32Array,Float64Array,Uint8ClampedArray,BigUint64Array,BigInt64Array,Map,Set,SourceBufferList,RTCStatsReport,Plugin,PluginArray,MimeTypeArray,MIDIOutputMap,MIDIInputMap,AudioParamMap,URLSearchParams,TouchList,TextTrackList,TextTrackCueList,StyleSheetList,StylePropertyMapReadOnly,StylePropertyMap,SVGTransformList,SVGStringList,SVGPointList,SVGNumberList,SVGLengthList,RadioNodeList,NodeList,NamedNodeMap,MediaList,Headers,HTMLSelectElement,HTMLOptionsCollection,HTMLFormElement,HTMLFormControlsCollection,HTMLCollection,HTMLAllCollection,FormData,FileList,DataTransferItemList,DOMTokenList,DOMStringList,DOMRectList,CSSUnparsedValue,CSSTransformValue,CSSStyleDeclaration,CSSRuleList,CSSNumericArray,webkitSpeechGrammarList,KeyboardLayoutMap,MediaKeyStatusMap</div>2019-06-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/0a/0b/4e3e70c3.jpg" width="30px"><span>timik</span> 👍（14） 💬（4）<div>老师，我记得有的书上或者是资料上说超过五次的if else 就最好用 switch case来替换。这样效率更好。您这里为什么说不用这个呢？</div>2019-05-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（9） 💬（0）<div>大概就这些？
Array, Map, Set, String, Float32Array, Float64Array, Int8Array, Int16Array, Int32Array, Uint8Array, Uint16Array, Uint32Array, Uint8ClampedArray</div>2019-04-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3a/78/85d264c3.jpg" width="30px"><span>break</span> 👍（7） 💬（0）<div>感觉这文章应该从后往前看😆</div>2019-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（4） 💬（0）<div>Some built-in types have a default iteration behavior, while other types (such as Object) do not. The built-in types with a @@iterator method are:
Array.prototype[@@iterator]()
TypedArray.prototype[@@iterator]()
String.prototype[@@iterator]()
Map.prototype[@@iterator]()
Set.prototype[@@iterator]()</div>2019-04-02</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/EJZoM46wR6QqTeibhPZsO5wJTeUia4RndGicWfDZLw153WibjsnJXqEtGZICxAa8icb36pDkficTic3FViaySd1z9HmQBw/132" width="30px"><span>翰弟</span> 👍（3） 💬（0）<div>Array、Map、Set、String、TypedArray、函数的arguments、NodeList对象</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6d/a9/4f461d80.jpg" width="30px"><span>固执的鱼wu</span> 👍（2） 💬（6）<div>let 和 const 声明虽然看上去是执行到了才会生效，但是实际上，它们还是会被预处理，为什么在const a=1之前console.log(a)是报错，而不是吧报undefinded呢</div>2020-01-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/84/9e/05ed50dd.jpg" width="30px"><span>2020</span> 👍（1） 💬（0）<div>据我能查到的资料，String, Array, TypedArray, Map and Set 是所有内置可迭代对象。</div>2020-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b3/19/0083394e.jpg" width="30px"><span>培根熏肉</span> 👍（1） 💬（2）<div>Switch那么好看难道我要写一堆if else？？不明白原文说没有用switch的意义在哪里</div>2019-11-21</li><br/><li><img src="" width="30px"><span>常德华</span> 👍（0） 💬（0）<div>特别喜欢听老师的声音，感觉特别酥，😄😄😄</div>2023-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fa/d0/17c6ef3b.jpg" width="30px"><span>静</span> 👍（0） 💬（0）<div>老师的声音好催眠，听信听着不知不觉睡着了而不自知😂</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5e/28/c0a8f859.jpg" width="30px"><span>Thinker</span> 👍（0） 💬（0）<div>
function sleep(duration) {
    return new Promise(function(resolve, reject) {
        setTimeout(resolve,duration);
    })
}
async function* foo(){
    i = 0;
    while(true) {
        await sleep(1000);
        yield i++;
    }
        
}
for await(let e of foo())
    console.log(e);</div>2020-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/a3/ea/53333dd5.jpg" width="30px"><span>HoSalt</span> 👍（0） 💬（1）<div>赋值语句这种属于表达式语句?</div>2020-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/74/1c/2a78a51a.jpg" width="30px"><span>千虑必有一得</span> 👍（0） 💬（0）<div>普通语句和声明型语句，简单清晰明了。</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/44/0e/ce14b7d3.jpg" width="30px"><span>-_-|||</span> 👍（0） 💬（0）<div>文中“此外，JavaScript 还为异步生成器函数配备了异步的 for of，我们来看一个例子：.........for await(let e of foo()) console.log(e);” for of 循环为什么要加 await 呢，不加按理说也可以。</div>2020-02-27</li><br/><li><img src="" width="30px"><span>lsy</span> 👍（0） 💬（0）<div>      console.log(&#39;有 iterator：&#39;);
      for (let key in window)
        window[key] &amp;&amp; window[key][Symbol.iterator] &amp;&amp; console.log(key);

      console.log(&#39;实例有 iterator：&#39;);
      Object.getOwnPropertyNames(window).forEach(
        key =&gt;
          window[key] &amp;&amp;
          window[key][&#39;prototype&#39;] &amp;&amp;
          window[key][&#39;prototype&#39;][Symbol.iterator] &amp;&amp;
          console.log(key)
      );</div>2019-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2c/88/2a7fe1a9.jpg" width="30px"><span>让时间说真话</span> 👍（0） 💬（0）<div>Map，set，arguments</div>2019-04-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/c2/8ffd2ad0.jpg" width="30px"><span>qqq</span> 👍（0） 💬（0）<div>catch 中可以使用 var 重新声明</div>2019-04-03</li><br/>
</ul>