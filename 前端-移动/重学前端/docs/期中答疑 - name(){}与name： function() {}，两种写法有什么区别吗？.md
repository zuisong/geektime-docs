你好，我是winter。

随着专栏进度过半，我们专栏的评论区留言量也日渐上涨。除了大家的小作业和学习心得，我还看见很多同学们在学习过程中提出了不少问题。

这其实是一种很好的学习方式，通过问题，我们可以对这部分知识记得更为牢固。

所以，我鼓励你在阅读文章之外，多思考，多提问，把自己不懂的地方暴露出来，及时查缺补漏，这样可以更好地吸收知识。同时，你也可以通过回答别人的问题来检验自己对知识的掌握情况。

我们一起来看看，大家都提出什么问题。

* * *

**1.老师你好！我语义化标签用得很少，多数用到的是header、footer、 nav等语义化标签，想问老师section和div混合使用，会不会效果不好呢？**

答：不会效果不好的，因为本来就是这么用的。遇到不确定的情况，请千万不要乱用标签，用div和span就好。

**2.我一直看见闭包这个词，但是一直也没有弄清楚它是什么东西，老师可以简单概括一下什么是闭包吗？**

答：你可以这样理解，闭包其实就是函数，还是能访问外面变量的函数。

**3.“事实上，JavaScript 中的“类”仅仅是运行时对象的一个私有属性，而 JavaScript 中是无法自定义类型的。”**

- **文中说“类”是私有属性，可以具体表现是什么，不是很能理解具体含义？**
<div><strong>精选留言（17）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/d3/897fc6df.jpg" width="30px"><span>Geeker1992</span> 👍（41） 💬（1）<div>我知道答案了。在 promise 出现之前，javascript 并没有异步，有异步的是宿主环境。</div>2019-04-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4f/d3/897fc6df.jpg" width="30px"><span>Geeker1992</span> 👍（10） 💬（1）<div>老师，为什么说没有了微任务就没有了异步？不是还有 setTimeout 的吗？</div>2019-04-03</li><br/><li><img src="" width="30px"><span>哈哈</span> 👍（0） 💬（2）<div>function foo(a) {
    var a;
    return a;
}
function bar(a) {
    var a = &#39;bye&#39;;
    return a;
}
[foo(&#39;hello&#39;), bar(&#39;hello&#39;)]&#47;&#47;输出结果为：hello，bye
两个函数内部的 return a; 根据作用域链寻找都是返回函数作用域的 a 吧。
第二个输出我可以理解，可是第一个的输出结果是 hello ，
第一个函数的a 不是undefined 吗？</div>2019-05-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（8） 💬（0）<div>&#47;**
 * @param {string} str
 *&#47;
function str2num (str) {
  const [m, e = &#39;&#39;] = str.split(&#39;e&#39;)
  const [i, f = &#39;&#39;] = m.split(&#39;.&#39;)
  let result = 0
  &#47;&#47; handle int
  let sign = 1
  for (let x of i) {
    if (x === &#39;+&#39;) {
      continue
    } else if (x === &#39;-&#39;) {
      sign *= -1
      continue
    } else {
      result *= 10
      result += c2n(x)
    }
  }

  &#47;&#47; handle fraction
  if (f) {
    result += str2num(f) &#47; (10 ** f.length)
  }

  &#47;&#47; handle exponent
  if (e) {
    let exponent
    let sign = 1
    if (e[0] === &#39;-&#39;) {
      sign = -1
      exponent = str2num(e.slice(1))
    } else if (e[0] === &#39;+&#39;) {
      exponent = str2num(e.slice(1))
    } else {
      exponent = str2num(e)
    }
    if (sign === -1) {
      result &#47;= 10 ** exponent
    } else {
      result *= 10 ** exponent
    }
  }

  &#47;&#47; handle sign
  result *= sign
  return result
}

function c2n (char) {
  const n = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9][char]
  if (n == null) throw new Error(`unknown char: &quot;${char}&quot;`)
  return n
}

function assert (input) {
  let output = str2num(input)
  let expect = Number(input)
  if (output !== expect) {
    throw new Error(`input ${input}, got ${output}, while expect ${expect}`)
  }
}

void function test () {
  assert(&#39;13.4e-7&#39;)
  assert(&#39;.4e+7&#39;)
  assert(&#39;-.2e+1&#39;)
  assert(&#39;+.6e+0&#39;)
  assert(&#39;0&#39;)
  assert(&#39;-0e-0&#39;)
  assert(&#39;0e0&#39;)
  assert(&#39;123&#39;)
  assert(&#39;2e1&#39;)
  assert(&#39;2e-0&#39;)
  assert(&#39;.1&#39;)
  console.log(&#39;All right.&#39;)
}()
</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/3a/26708d86.jpg" width="30px"><span>自由之翼</span> 👍（3） 💬（1）<div>一般都是缓存 数据 吧 ,个人感觉 缓存 js css 纯属没事儿找事儿.</div>2019-04-03</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKzwpgrdbZlSb30EaOZ37lDlBDjEjHMOpjbK1pPlY4hyFctE8GsicibUuyAB8pzx8F3Ne7Ymzkn2cSQ/132" width="30px"><span>Geek_c43534</span> 👍（2） 💬（2）<div>老师，jquery ajax 同步请求的原理是?目前用axios库，不支持同步请求，如果希望执行同步请求有什么解决办法？</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（2） 💬（2）<div>老师您好，把JS代码缓存在 localStorage 中，从 localStorage 取出后怎么执行？ 如果缓存的是 css 呢？</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/18/77/d665f258.jpg" width="30px"><span>EmilyLucky</span> 👍（1） 💬（0）<div>好像对异步任务的分类又多了一点理解。异步中任务分为宏任务和微任务，微任务是后来出现的，它其实是JS引擎内部的机制，而宏任务是宿主环境下的异步。老师，这么理解对吗？那么设计微任务的初衷仅仅就是为了让JS引擎内部有异步么？</div>2020-05-12</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/pic1ibj7XibmJrGmiaiceVVAUEVQ1g9bmxsicy2FaCOIffpYicflUs8iaULPmw5yopN7ltbjbI1TCF0OovC1alssX6cAaA/132" width="30px"><span>xiaolu289</span> 👍（1） 💬（0）<div>js如果取出来是字符串，目前我想到一个方案是用eval去执行，不过感觉直接用localstrage存储js代码这种操作可能会有安全问题，毕竟locastrage在浏览器是随便我怎么改都行的....
css的话，直接插一个style不就好了嘛....js其实也可以插一个script....所以具体什么场景采用什么方案，还得根据业务场景来决定

不知道我理解得是否正确..</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（1） 💬（0）<div>写的过程中遇到了个精度问题：
比如13.4e-7，一开始我的结果是0.0000013399999999999999，然后我把乘法改成了对应的除法，就可以了。这说明JS引擎对除法的处理不是简单的乘以相应的倒数，具体的机制不知道 winter 老师能不能给个解释。</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ac/f0/5d52d73e.jpg" width="30px"><span>Jy</span> 👍（1） 💬（0）<div>name()和name: function，本质上前面的是Method，后面是函数属性。
具体的差异不大，有个小栗子: 在name: function中使用super会报错，而name()不会。</div>2019-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/1e/c5/4e640126.jpg" width="30px"><span>momo</span> 👍（0） 💬（0）<div>那个函数使用，o.func()和a=o.func这俩，如果函数内部使用了this，还是会有差别的，不过，一般不会有人用a=o.func这种方式的吧…</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/b8/79/a4dbe9ee.jpg" width="30px"><span>blueBean</span> 👍（0） 💬（1）<div>请问类和类型有什么区别呢</div>2020-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4b/b6/ec4301b5.jpg" width="30px"><span>洛小贼</span> 👍（0） 💬（0）<div>请问第4个问题产生这种差异是否是因为o1用了闭包所以可以访问自己，o2没有用闭包所以不能访问它自身？</div>2019-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/1a/1c/2898f78f.jpg" width="30px"><span>veath</span> 👍（0） 💬（0）<div>请问下，link preload 解析执行时机和构建 CSSOM一样吗---html从上往下解析到link preload才会解析执行？还是说并行解析html 和preload</div>2019-04-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b6/5e/a7660b26.jpg" width="30px"><span>Daniel</span> 👍（0） 💬（0）<div>老师您好，请教你个问题。 link与script都可以引用js代码，这两者的区别是什么呢？</div>2019-04-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/b3/3f0b69f9.jpg" width="30px"><span>杨学茂</span> 👍（0） 💬（0）<div>请问：var,let 和 const 在 babel 中都会被编译为 var, 那怎么区分 const 是常量呢？</div>2019-03-30</li><br/>
</ul>