你好，我是周爱民。欢迎回到我的专栏。今天，是传说中的加餐时间，我将与你解说前11讲内容的整体体系和结论。

我们从一个问题讲起，那就是：JavaScript到底是怎么运行起来的呢？

看起来这个问题最简单的答案是“解析→运行”。然而对于一门语言来说，“引擎解释与运行”都是最终结果的表象，真正处于原点的问题其实是：“JavaScript运行的是什么？”

在前11讲中，我是试图将JavaScript整个的运行机制摊开在你的面前，因此我们有两条线索可以抓：

1. 表面上，它是讲引用和执行过程；
2. 在底下，讲的是引擎对“JavaScript是什么”的理解。

## 从文本到脚本

我们先从第二条线索，也就是更基础层面的线索讲起。

JavaScript的所谓“脚本代码”，在引擎层面看来，首先就是一段文本。在性质上，装载`a.js`执行与`eval('...')`执行并没有区别，它们的执行对象都被理解为一个“字符串”，也就是字符串这一概念本身所表示的、所谓的“字符序列”。

在字符序列这个层面上，最简单和最经济的处理逻辑是**正向遍历**，这也是为什么“语句解析器”的开发者总是希望“语言的设计者”能让他们“一次性地、不需要回归地”解析代码的原因。

回归（也就是查看之前“被parser过的代码”）就意味着解析器需要暂存旧数据，无法将解析器做得足够简洁，进而无法将解析器放在小存储的环境中。根本上来说，JavaScript解析引擎是“逐字符”地处理代码文本的。
<div><strong>精选留言（16）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/b2/e0/bf56878a.jpg" width="30px"><span>kkxue</span> 👍（3） 💬（2）<div>个人觉得老师说明下您理解编程语言背后的哲学逻辑或者体系，我们上道才更快。</div>2020-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/05/9976b871.jpg" width="30px"><span>westfall</span> 👍（2） 💬（1）<div>“所以本质上，引用还是指向值、代表值的一个概念，它只是“获得值的访问能力”的一个途径。最终的结果仍然指向原点：计算值、求值。”
不明白引用与指针的区别。</div>2020-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/30/3a/e970285b.jpg" width="30px"><span>刘长锋</span> 👍（2） 💬（1）<div>D2 大会上听老师说，要有新书发布，很是期待！</div>2020-03-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/bb/01/568ac2d6.jpg" width="30px"><span>K4SHIFZ</span> 👍（1） 💬（2）<div>老师，下个课程什么时候出啊，迫不及待想学了</div>2020-03-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/08/c77d8a5a.jpg" width="30px"><span>Kids See Ghost</span> 👍（0） 💬（1）<div>关于GetValue最后再请教一下
规范里的是
```
6.2.4.5 GetValue ( V )
The abstract operation GetValue takes argument V. It performs the following steps when called:

1. ReturnIfAbrupt(V).
2. If V is not a Reference Record, return V.
3. If IsUnresolvableReference(V) is true, throw a ReferenceError exception.
4. If IsPropertyReference(V) is true, then
a. Let baseObj be ? ToObject(V.[[Base]]).
b. If IsPrivateReference(V) is true, then
i. Return ? PrivateGet(baseObj, V.[[ReferencedName]]).
c. Return ? baseObj.[[Get]](V.[[ReferencedName]], GetThisValue(V)).
5. Else,
a. Let base be V.[[Base]].
b. Assert: base is an Environment Record.
c. Return ? base.GetBindingValue(V.[[ReferencedName]], V.[[Strict]]) (see 9.1).
```
我以为这个被get的value就是跟base有关。我看了您说的prepack-core里的代码，这部分貌似是叫_dereference。代码大概是
```
  _dereference(realm: Realm, V: Reference | Value, deferenceConditionals?: boolean = true): Value {
    &#47;&#47; This step is not necessary as we propagate completions with exceptions.
    &#47;&#47; 1. ReturnIfAbrupt(V).

    &#47;&#47; 2. If Type(V) is not Reference, return V.
    if (!(V instanceof Reference)) return V;

    &#47;&#47; 3. Let base be GetBase(V).
    let base = this.GetBase(realm, V);
    &#47;&#47;....
    if (this.HasPrimitiveBase(realm, V)) {
        &#47;&#47; i. Assert: In this case, base will never be null or undefined.
        invariant(base instanceof Value &amp;&amp; !HasSomeCompatibleType(base, UndefinedValue, NullValue));

        &#47;&#47; ii. Let base be To.ToObject(base).
        base = To.ToObject(realm, base);
      }
      invariant(base instanceof ObjectValue || base instanceof AbstractObjectValue);

      &#47;&#47; b. Return ? base.[[Get]](GetReferencedName(V), GetThisValue(V)).
      return base.$GetPartial(this.GetReferencedNamePartial(realm, V), GetThisValue(realm, V));
```
这里怎么看都是跟base有关系。实在是看不懂到底怎么样把一个value用getValue取出来。您的课也我也没有看到有直接讲到这个。所以能不能麻烦最后再指点一下，到底规范里面的哪一步是把像obj = {x: &#39;abcdef&#39;}，当【obj.x】作为一个引用时，我们把字符串给用getValue取出来的？
</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/08/c77d8a5a.jpg" width="30px"><span>Kids See Ghost</span> 👍（0） 💬（1）<div>再请教一下：在JS里做equality check的时候, 比如用 === - 这个时候我们是在比value还是比reference？也就是说 x === y - 等于是 getValue(x) === getValue(y) 吗？
相应地，是不是说在JS里面，能拿来比较的东西只能是 value，两个reference是肯定不一样的？
请问规范里面有相应的章节吗？
</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/08/c77d8a5a.jpg" width="30px"><span>Kids See Ghost</span> 👍（0） 💬（1）<div>1. 请教一下，您说“例如obj = {x: &#39;abcdef&#39;}，当【obj.x】作为一个引用时，base是obj，而不是那个字符串&#39;abcdef&#39;。又例如全局的变量let x = &#39;abcdef&#39;，base将是全局词法环境，指向Global.lexEnv。”

假如我现在把obj.x赋值给一个变量，那getValue(obj.x)拿出来的值不应该是字符串&#39;abcdef&#39;吗？https:&#47;&#47;tc39.es&#47;ecma262&#47;#sec-getvalue 我理解的规范里的getValue 最终拿出来的value就是base，请问这个理解是错的吗？如果是错的，那getValue里拿出来的value到底是什么？

换一个问法，如果当【obj.x】作为一个引用时，错误地把base是当成了那个字符串&#39;abcdef&#39;，会造成什么样的理解错误呢，请问您能举个例子吗？

2. 另外想请教一下在https:&#47;&#47;tc39.es&#47;ecma262&#47;#sec-reference-record-specification-type 里定义的 Reference Record Specification Type里，[[ReferencedName]]	提到 &quot;The name of the binding. Always a String if [[Base]] value is an Environment Record.&quot;这句话的意思是什么？意思是如果base不是一个Environment Record，那ReferencedName可以不是string？请问Environment Record又是啥。。</div>2022-01-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/36/08/c77d8a5a.jpg" width="30px"><span>Kids See Ghost</span> 👍（0） 💬（1）<div>几个问题想向老师请教一下：
1. Reference Record Specification Type （https:&#47;&#47;tc39.es&#47;ecma262&#47;#sec-reference-record-specification-type）就是您一直提到的“规范层面的引用（References）”吗？
2. 引用reference里的Base，我们是可以理解为真正的那个数字&#47;字符串&#47;object etc. 吗？而不是指针&#47;引用（内存层面上的）或者了另一个reference?
3. 最想问的一个问题是，想知道在call function的时候，规范里有规定是pass by value还是pass by reference吗？假如说我们有 
```
function fn(x) {}
const a = {}
const b = 1

fn(a)
fn(b)
```
这里第一次给fn传入`a`的时候，整个过程我们有`x = getValue(a)` 吗还是说我们直接把`a`的reference给了`x`? fn(b) 也一样吗？ 
我在规范里找了很久都找不到相应的章节，请问您能给一个链接到专门讲**函数传参**的章节吗？
4.最后，您说“这个框架的核心在于——ECMAScript 的目的是描述“引擎如何实现”，而不是“描述语言是什么”。”这句话确定没有说反了吗？难道不是 ECMAScript的目的是设计一个语言，具体语言怎么实现是javascript engine的事情。比如ECMAScript里面不会讲memory layout应该会怎么样，什么东西放到stack上，什么放到heap上，因为这个是implementation details，由引擎自己决定。
感谢！</div>2022-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/1b/a6/6373416f.jpg" width="30px"><span>青史成灰</span> 👍（0） 💬（2）<div>老师，关于上面“为什么要有‘引用’这么个东西呢”的解释，读下来感觉和C++的指针很像，指针是内存的地址，指向堆内存中的对象，需要访问指针指向的成员时，直接解引用这个指针，v = *p，就和此处的x=GetValue(r)一样。 不知道这样理解是否正确？</div>2019-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/dc/90/c980113a.jpg" width="30px"><span>行问</span> 👍（0） 💬（2）<div>eval(str) 是执行语句，而{$str}是执行表达式

这里是 {$str} 正确，还是 ${str} 正确？
</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/18/65/35361f02.jpg" width="30px"><span>潇潇雨歇</span> 👍（2） 💬（3）<div>结合《程序原本》重新回顾前几讲，有趣</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/89/5b/d8f78c1e.jpg" width="30px"><span>孜孜</span> 👍（1） 💬（0）<div>这两章的东西，虽说是js的，但是我感觉这是不限制在某个语言层面的。</div>2020-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/c4/c311b591.jpg" width="30px"><span>Amundsen</span> 👍（0） 💬（0）<div>每次反复阅读都能收获，感觉看到了不一样的自己 :)</div>2020-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/a4/24/0f4a9157.jpg" width="30px"><span>伪装</span> 👍（0） 💬（0）<div>按照ecma规范写一套解析器就是js了</div>2019-12-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/04/8d/005c2ff3.jpg" width="30px"><span>weineel</span> 👍（0） 💬（0）<div>知识密度太大。</div>2019-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（0） 💬（0）<div>老师还是很良心的，时不时就来给我们一个加餐。</div>2019-12-09</li><br/>
</ul>