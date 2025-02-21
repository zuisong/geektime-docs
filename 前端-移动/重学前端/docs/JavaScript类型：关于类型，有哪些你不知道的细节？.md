你好，我是winter。今天我们来讲讲JavaScript的内容，在这个部分，我首先想跟你聊一聊类型。

JavaScript类型对每个前端程序员来说，几乎都是最为熟悉的概念了。但是你真的很了解它们吗？我们不妨来看看下面的几个问题。

- 为什么有的编程规范要求用void 0代替undefined？
- 字符串有最大长度吗？
- 0.1 + 0.2不是等于0.3么？为什么JavaScript里不是这样的？
- ES6新加入的Symbol是个什么东西？
- 为什么给对象添加的方法能用在基本类型上？

如果你答起来还有些犹豫的地方，这就说明你对这部分知识点，还是有些遗漏之处的。没关系，今天我来帮你一一补上。

我在前面提到过，我们的JavaScript模块会从运行时、文法和执行过程三个角度去剖析JS的知识体系，本篇我们就从运行时的角度去看JavaScript的类型系统。

> 运行时类型是代码实际执行过程中我们用到的类型。所有的类型数据都会属于7个类型之一。从变量、参数、返回值到表达式中间结果，任何JavaScript代码运行过程中产生的数据，都具有运行时类型。

## 类型

JavaScript语言的每一个值都属于某一种数据类型。JavaScript语言规定了7种语言类型。语言类型广泛用于变量、函数参数、表达式、函数返回值等场合。根据最新的语言标准，这7种语言类型是：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/9d/65/ef4fc8e1.jpg" width="30px"><span>咕叽咕叽</span> 👍（247） 💬（14）<div>感谢winter老师的分享，受益匪浅。

但是本文有两点是值得商榷的。
其一：
原文：Undefined 跟 null 有一定的表意差别，null表示的是：“定义了但是为空”。
私以为，undefined表示的是：“定义了但是为空”。而非null。

二：
原文：
    var o = {
        valueOf : () =&gt; {console.log(&quot;valueOf&quot;); return {}},
        toString : () =&gt; {console.log(&quot;toString&quot;); return {}}
    }

    o + &quot;&quot;
    &#47;&#47; toString
    &#47;&#47; valueOf
    &#47;&#47; TypeError

很多朋友已经提出来了，应该是先执行valueof，再执行toString。

这个问题，可以从ecmascript规范中寻找答案：

规范指出，类型转换的内部实现是通过ToPrimitive ( input [ , PreferredType ] )方法进行转换的，这个方法的作用就是将input转换成一个非对象类型。

参数preferredType是可选的，它的作用是，指出了input被期待转成的类型。

如果不传preferredType进来，默认的是&#39;number&#39;。

如果preferredType的值是&quot;string&quot;，那就先执行&quot;toString&quot;, 后执行&quot;valueOf&quot;。否则，先执行&quot;valueOf&quot;, 后执行&quot;toString&quot;。

由此可见，&quot;toString&quot;, &quot;valueOf&quot;的执行顺序，取决于preferred的值。

规范原文请移步：http:&#47;&#47;www.ecma-international.org&#47;ecma-262&#47;#sec-toprimitive

再回到我们的例子
var o = {
        valueOf : () =&gt; {console.log(&quot;valueOf&quot;); return {}},
        toString : () =&gt; {console.log(&quot;toString&quot;); return {}}
}

o + &quot;&quot;

类型转换时，把对象o进行转换，调用toPrimitive方法，即toPrimitive(o[ , PreferredType ] )。关键的点是，preferredType是否被传值，传的是什么值？

我们再去看下规范，看看加法运算符的规则。

加法运算符运算过程中有两行代码很重要，如下
    Let lprim be ? ToPrimitive(lval).
    Let rprim be ? ToPrimitive(rval).

可以看出，调用ToPrimitive方法时，第二个参数是没有传参的。

所以preferredType取默认的值&quot;number&quot;。最终先执行&quot;valueOf&quot;, 后执行&quot;toString&quot;。

个人愚见，如有纰漏，还请各位同仁指正。</div>2019-02-15</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKLLTwMonrzBnx3tuRqY0NJtV3R68xibgZyFwewBPE1MTbLulicYWBFSqMw68qZqjKW6ibjr0IVucXJg/132" width="30px"><span>blueshell</span> 👍（17） 💬（3）<div>#### 重写十进制的parseInt&#47;parseFloat
`
var myParse = function (val) {
    if (val) {
        var num = val.match(&#47;^\d*\.?\d+&#47;);
        if (num !== null) {
            return num[0] - 0;
        }else{
            return NaN;
        }
    }else{
        return NaN;
    }
}
`</div>2019-02-19</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqjpcoomiaZF83ibmKHuzJkq0w2IsvNIPH71HBaB6bjVlmho4sm5Hf6HCOtOnLxFDibdtUyAhms9tLLA/132" width="30px"><span>酷儿</span> 👍（7） 💬（1）<div>不用原生的 Number 和 parseInt 进行类型Stirng to Number转换用~~就好了， ~~&quot;7&quot; = 7</div>2019-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cc/10/f83353d8.jpg" width="30px"><span>Leung</span> 👍（3） 💬（3）<div>+&#39;3&#39;转number,3+&#39;&#39;转string</div>2019-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/b5/92/ac0d4705.jpg" width="30px"><span>geek_syk</span> 👍（1） 💬（1）<div>ES10 又推出了 BigInt 这种类型，javascript 的数据类型已增加至 8 种了是吧</div>2019-10-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/70/148a208c.jpg" width="30px"><span>逍竹</span> 👍（1） 💬（2）<div>作者您好，可以用 null 关键字来获取 null 值，这句话是什么意思呢？</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/f3/63/63d30619.jpg" width="30px"><span>mingingคิดถึง</span> 👍（0） 💬（1）<div>String 有最大长度是 2^53 - 1

我理解是String最多有53个二进制位，每个二级制位都有0&#47;1两种选择，一共有2^53中情况，那为什么要减一呢</div>2019-10-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/K7iaUFMAQqvNzvLr8PMgrUHdGg8E8HoNNEYgpzIWlu3HCvFP810UYgC1iaHjgSsrU0mZhvUrEvoGm7vzvMLjNEibQ/132" width="30px"><span>Geek_c90ff4</span> 👍（0） 💬（2）<div>老师，您好！我好像还不太理解Symbol.iterator在时间工作中的使用场景</div>2019-10-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/1b/d3/5cf53a64.jpg" width="30px"><span>脱尼</span> 👍（0） 💬（1）<div>请问下2^53-1 是怎么得到的？</div>2019-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/a8/31/b765627e.jpg" width="30px"><span>ionlyleaf</span> 👍（0） 💬（1）<div>上面类型转换的图，Object(null) 为TypeError？应该是{}才对吧：The Object constructor creates an object wrapper for the given value. If the value is null or undefined, it will create and return an empty object。</div>2019-08-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/2b/cded5870.jpg" width="30px"><span>沙岵杨</span> 👍（0） 💬（1）<div>true + null = 1;   false + null = 0，并不是像作者说的那样</div>2019-08-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/00/23/e1f36fb9.jpg" width="30px"><span>后知后觉</span> 👍（0） 💬（1）<div>字符串转化为数字可以用隐式转换： eg:   &#39;2&#39; - 1 + 1</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/00/23/e1f36fb9.jpg" width="30px"><span>后知后觉</span> 👍（0） 💬（1）<div>实例不是new 一个类吗，为什么是javascript的类型系统中的内置对象呢？</div>2019-08-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/25/2c/8f61089f.jpg" width="30px"><span>宗麒麟</span> 👍（0） 💬（2）<div>1. 0.8+0.4 -1.2  &lt; Number.EPSILON  false
2. 0.8*7 -5.6 &lt; Number.EPSILON  false
3. 0.1+0.2 - 0.3 &lt; Number.EPSILON true
老师，用这种方式判断 是否相等，怎么不大行</div>2019-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/3f/a9045589.jpg" width="30px"><span>敏儿</span> 👍（0） 💬（2）<div>0.1+0.2不等于0.3的原因应该是进制转换造成的</div>2019-07-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJEPMj69Hy9qq8SuEsiccKKaJQt20vvjl9Z9DMJxNmvrq6X3LrDMONTT6Jkg70kEVg13Lkdc6eMWlA/132" width="30px"><span>Geek_e21f0d</span> 👍（0） 💬（1）<div>function stringToNumber(str) {
    let isNumberReg = &#47;^(\d*)(\.\d*)?&#47;;
    let matchResult = isNumberReg.exec(str);
    if (isNumberReg.exec(str) === null) {
        return NaN;
    } else {
        let integers = matchResult[1];
        let index = integers.length - 1;
        let multiple = 1;
        let result = 0;
        while(index &gt;= 0) {
            let char = integers.charAt(index);
            let num;
            switch(char) {
                case &#39;1&#39;:
                    num = 1;
                    break;
                case &#39;2&#39;:
                    num = 2;
                    break;
                case &#39;3&#39;:
                    num = 3;
                    break;
                case &#39;4&#39;:
                    num = 4;
                    break;
                case &#39;5&#39;:
                    num = 5;
                    break;
                case &#39;6&#39;:
                    num = 6;
                    break;
                case &#39;7&#39;:
                    num = 7;
                    break;
                case &#39;8&#39;:
                    num = 8;
                    break;
                case &#39;9&#39;:
                    num = 9;
                    break;
                case &#39;0&#39;:
                    num = 0;
                    break;
            }
            result = result + num * multiple;
            multiple = multiple * 10;
            index--;
        }
        return result;
    }
}</div>2019-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/fc/d1/3aeba287.jpg" width="30px"><span>不想说什么</span> 👍（0） 💬（2）<div>老师，对于NaN，占用了 9007199254740990这个值，那为什么NaN 不等于NaN了</div>2019-05-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/d6/76fe5259.jpg" width="30px"><span>Dream.</span> 👍（0） 💬（1）<div>JavaScript 字符串把每个 UTF16 单元当作一个字符来处理，所以处理非 BMP（超出 U+0000 - U+FFFF 范围）的字符时，你应该格外小心。

在新推出的es2019中，超出范围后，用json转义序列表示了。</div>2019-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1c/55/72729c45.jpg" width="30px"><span>可茜</span> 👍（0） 💬（1）<div>特想知道0.1+0.2==0.3为false，而0.1+0.3==0.4为true，根据百度的0.1在计算机编程时是舍入误差，那么0.1+0.3==0.4应该为false的，怎么解释</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/79/cc/3597f652.jpg" width="30px"><span>Bottle</span> 👍（0） 💬（1）<div>老师你好，您说的&quot;.&quot;运算符提供了临时的装箱操作，生成了临时对象，才使得基础类型上能访问到对象上的方法，可我根据以下的输出咋觉得是因为原型链才导致能使用呢？
```
var a = 1;
console.log(a.__proto__.__proto__.constructor === Object); &#47;&#47; true
```</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/42/2c/ba09dc1e.jpg" width="30px"><span>卫斯理</span> 👍（0） 💬（1）<div>  console.log( Math.abs(0.1 + 0.2 - 0.3) &lt;= Number.EPSILON);&#47;&#47;比较浮点数的方法
为什么给对象添加的方法能用在基本类型上？
答：运算符提供了装箱操作，它会根据基础类型构造一个临时对象，使得我们能在基础类型上调用对应对象的方法。


</div>2019-02-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fe/0c/f9cb1af4.jpg" width="30px"><span>李艺轩</span> 👍（0） 💬（2）<div>var symbolObject = (function(){ return this; }).call(Symbol(&quot;a&quot;));的结果为啥是个对象呢？是因为后面说的，call方法会显式装箱吗？</div>2019-02-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/39/ab/42622d70.jpg" width="30px"><span>James Bond</span> 👍（0） 💬（1）<div>this指的是什么呢？为什么有的时候会没定义呢</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/06/bb/f7b06ee6.jpg" width="30px"><span>人生如茶</span> 👍（0） 💬（1）<div>最后一张图没有问题，它表达的是同一个值在typeof运算符运算后以及在运行时两种情况下得出的&quot;类型&quot;的对比。由于早上我没有理解这张图，发表了过激的留言（现已删除），在此向编辑和作者致歉。</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/70/4b/9b7c7258.jpg" width="30px"><span>bertZuo</span> 👍（243） 💬（23）<div>老师，对于Number 类型有一个疑惑，您举列的console.log( 0.1 + 0.2 == 0.3)为false，我就另测试了了一下console.log( 0.3 + 0.2 == 0.5)就为true了呢，试试其他都是true，为啥只有是否等于0.3才为false呀？</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/cb/3a/b030da22.jpg" width="30px"><span>奔跑的兔子</span> 👍（97） 💬（5）<div>我发现有很多同学都在纠结undefined问题，为什么不去读一下mdn呢。
https:&#47;&#47;developer.mozilla.org&#47;en-US&#47;docs&#47;Web&#47;JavaScript&#47;Reference&#47;Global_Objects&#47;undefined
前两段写的很明确了。
undefined is a property of the global object; i.e., it is a variable in global scope. The initial value of undefined is the primitive value undefined.
In modern browsers (JavaScript 1.8.5 &#47; Firefox 4+), undefined is a non-configurable, non-writable property per the ECMAScript 5 specification. Even when this is not the case, avoid overriding it.
在ES5之前的时候，undefined是可以被赋值的。在现代浏览器当中已经把undefined设置为一个non-configurable, non-writable属性的值了。
</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/d0/ba4d7a90.jpg" width="30px"><span>yuuk</span> 👍（91） 💬（5）<div>undefined在全局环境没法被赋值，在局部环境是可以被赋值的！</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/48/b7/c41ee146.jpg" width="30px"><span>🍃Spring🍃</span> 👍（80） 💬（3）<div>String转number
Math.floor(&quot;1000&quot;)
Math.round(&quot;1000&quot;)
Math.ceil(&quot;1000&quot;)
var num = +&quot;1000&quot;
&quot;1000&quot;&gt;&gt;&gt;0
~~&quot;1000&quot;
&quot;1000&quot;*1
</div>2019-01-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/fd/84/0017fe79.jpg" width="30px"><span>饭小笛 🐱</span> 👍（76） 💬（3）<div>关于Number类型，如果想要进一步理解可以去参考IEEE 754中关于浮点数的表达规范，了解这64位中各个位数段表达的含义

文中有几个叙述不清的地方：

1. NaN和+Infinity的规定实际是IEEE 754标准规定的特殊值：

（e为指数的位数，双精度中e=11）

- 指数为2^e – 1且尾数的小数部分全0，这个数字是±∞。（符号位决定正负）
- 指数为2^e – 1且尾数的小数部分非全0，这个数字是NaN，比如单精度浮点数中按位表示：S111 1111 1AXX XXXX XXXX XXXX XXXX XXXX，S为符号位值无所谓，A是小数位的最高位（整数位1省略），其取值表示了NaN的类型：X不能全为0，并被称为NaN的payload

2. NaN，占用了 9007199254740990，这个叙述不对

留言里很多童鞋都提出了 9007199254740990 被占用是什么意思的疑问，实际是第一点描述的关于NaN规定和参考双精度浮点数的表达方式，尾数共有53位，指数固定为2^e – 1并去掉±∞两个值，那么NaN其实是 2^53-2 个特殊数字的合集（2^53-2 = 9007199254740990 ）；

并不是 9007199254740990 被占用，而是 9007199254740990 个特殊值被占用来表示 NaN

扩展一下，我们就可以理解为什么NaN !== NaN了，它确实不是一个值，而是一群值呢0 0！</div>2019-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e5/d9/8fd0aef1.jpg" width="30px"><span>于江水</span> 👍（61） 💬（2）<div>
1. 实现字符串转数字的同学，不要单纯考虑这个字符串一定全是数字而用运算符来实现。放在实际场景会出现大量 NaN。

2. “需要注意的是，parseInt 和 parseFloat 并不使用这个转换，所以支持的语法跟这里不尽相同。” 使用是不是打错了？应该是 适用？

3. 代码 Object((Symbol(‘a’)) 要么左边多了括号要么右边少了括号。

4. 希望类似装箱转换、拆箱转换这样的专属名词如果有英文单词可以补充下方便检索更多信息。
</div>2019-01-29</li><br/>
</ul>