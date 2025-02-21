早期的JavaScript程序员一般都有过使用JavaScript“模拟面向对象”的经历。

在上一篇文章我们已经讲到，JavaScript本身就是面向对象的，它并不需要模拟，只是它实现面向对象的方式和主流的流派不太一样，所以才让很多人产生了误会。

那么，随着我们理解的思路继续深入，这些“模拟面向对象”，实际上做的事情就是“模拟基于类的面向对象”。

尽管我认为，“类”并非面向对象的全部，但我们不应该责备社区出现这样的方案，事实上，因为一些公司的政治原因，JavaScript推出之时，管理层就要求它去模仿Java。

所以，JavaScript创始人Brendan Eich在“原型运行时”的基础上引入了new、this等语言特性，使之“看起来语法更像Java”，而Java正是基于类的面向对象的代表语言之一。

但是JavaScript这样的半吊子模拟，缺少了继承等关键特性，导致大家试图对它进行修补，进而产生了种种互不相容的解决方案。

庆幸的是，从ES6开始，JavaScript提供了class关键字来定义类，尽管，这样的方案仍然是基于原型运行时系统的模拟，但是它修正了之前的一些常见的“坑”，统一了社区的方案，这对语言的发展有着非常大的好处。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/04/8e/e75ecc5e.jpg" width="30px"><span>浩明啦</span> 👍（152） 💬（6）<div> 这些知识真的不止这个价格了， 感谢老师  </div>2019-01-31</li><br/><li><img src="" width="30px"><span>羲</span> 👍（7） 💬（1）<div>winter老师，有一些浏览器对es6语法部分不兼容，一般开发中依旧用新的es6语法，然后找插件转换成浏览器支持的语法，想问下，你对这种做法怎么看？这样做是不是有点兜圈子了，直接用旧语法也可以写，但又有些想尝试用新的语法</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/15/89/84e6495d.jpg" width="30px"><span>雪中抱猪行</span> 👍（5） 💬（1）<div>JQ的‘$’兼具，对象，类(构造函数)，函数三种角色。老师多这种用法持什么观点。</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/13/1a/b725629b.jpg" width="30px"><span>lt-零度</span> 👍（5） 💬（1）<div>老师，我的留言都没回复过我，伤心</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1c/4b/7ccd2499.jpg" width="30px"><span>F.</span> 👍（2） 💬（2）<div>老师，为什么直接输出 v.toString() 的结果和  Object.prototype.toString.call(v) 不一样</div>2019-02-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqtaHMciakwNRfMqLRIDvOBhjYZllqXDYjXnGJibF7vCtiauUwvDA6F90RQ7TojgyWrgVvT0DfqhRScw/132" width="30px"><span>看啥看看不懂</span> 👍（1） 💬（1）<div>我感觉不是我们需要模拟类，而是我们需要真正类的形式。我认为单纯的原型形式去做项目，在复用，扩展方面不是很适合，比如 每次生成的对象没有办法判断是否从属一类；使用Object.create方法，会将对象的属性放在原型链上，这样该对象的私有属性就成了公共的，违背了属性最好私有化的开发概念。在开发中也容易出现bug。我感觉，类的想法很适合扩展，复用。原型链变为了它的内在实现方式。如果手动用原型链写，也可以实现，但就是麻烦些。</div>2019-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/61/882eb821.jpg" width="30px"><span>奋奋</span> 👍（1） 💬（2）<div>老师好，关于原型系统两条概括的第一条，“如果所有对象都有私有字段[[prototype]]，就是对象的原型”，这句话我反复阅读，也不能理解，所有对象是什么？怎么就成对象的原型了？望能再细说一下</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/ca/71/b5ac045e.jpg" width="30px"><span>Gavin 峰</span> 👍（1） 💬（2）<div>“类”并非面向对象的全部，如何理解？</div>2019-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/d3/42566a75.jpg" width="30px"><span>LaMer</span> 👍（0） 💬（2）<div>“所有对象都有私有字段[[prototype]]” 这句不是很理解 我发现 现在chrome普通对象都是有_proto_字段 ，没发现[[prototype]]字段 望老师解答！！！！</div>2019-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/02/e0/3baadd39.jpg" width="30px"><span>八脚</span> 👍（0） 💬（1）<div>老师：听您课程受益匪浅，想问个问题我设计继承类的时候会经常在super前面对父类参数做加工，这样的做法是否合理，或者有更合适的做法？
class 猫{
    constroct({skin: 黑色, ...other}){
         this.skin = skin;
    }
    ......
}; 

class 花斑虎 extends 猫 {
    constroct(config){
        config.skin = 花斑;
        super(config);
    }
     ......
}
</div>2019-02-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK7IdBDXwAHfj7fV3oddk4DKibUBEiaictJtGm0AgQbAlh6ublw0aoUrJ7icsve4Azib31R1UBJb3YyU6A/132" width="30px"><span>Ewet</span> 👍（0） 💬（1）<div>想问下操作原型有什么作用，感觉看得不是很明白，来自小白的提问，哈哈哈</div>2019-02-13</li><br/><li><img src="" width="30px"><span>Youngwell</span> 👍（169） 💬（13）<div>感觉是像在听天书，前端工作快三年了，悲催了</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0b/e7/1b79a53c.jpg" width="30px"><span>ashen1129</span> 👍（120） 💬（1）<div>本篇厘清了一些我对面向对象的理解误区，说明了“基于类”和“基于原型”作为两种编程范式的区别，感谢。

不过感觉本篇在写的时候有一些地方讲的不够严谨：

1. [[class]]和Symbol.toStringTag实质上是控制的“ the creation of the default string description of an object”，但举例中使用了一个o.toString()来讲述，感觉容易造成误解。

2.在讲解ES6中的类时，文中指出“类中定义的方法和属性则会被写在原型对象之上”，事实上一般数据属性写在对象上，而访问器属性和方法才是写在原型对象之上的。

3.class和extends实质上是作为语法糖，统一了JS程序员对基于类的面向对象的模拟，但感觉文中讲的不是很清楚。

以上是一些个人看法，如有不对的地方欢迎winter老师指正。</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/ac/6a/b6f6810c.jpg" width="30px"><span>简单</span> 👍（49） 💬（5）<div>老师，我听了几遍为什么觉得什么都不懂，越听越复杂，不理解也记不住😂</div>2019-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f4/55/0025dfcb.jpg" width="30px"><span>乐亦栗</span> 👍（42） 💬（10）<div>有像我一样平常根本不用面向对象写代码的吗……</div>2019-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/19/f0/4f73dba3.jpg" width="30px"><span>Nina.</span> 👍（33） 💬（6）<div>winter的文章很适合反复去听，每次都有新的领悟。
今年毕业啦，选择了前端，去实习时有接触到winter所说的知识，但是我只能略懂，单词我懂，哈哈。
虽然现在还是前端渣渣，但是我相信，通过自己的努力，一定可以成为大神级的程序媛，相信我嘛~哈哈哈</div>2019-05-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/53/e3/39dcfb11.jpg" width="30px"><span>来碗绿豆汤</span> 👍（31） 💬（4）<div>如果说运行时还是基于prototype的，那是不是可以理解为class其实是个语法糖，它最终还是被翻译成功prototype形式来执行？或者说prototype形式写的代码执行起来更高效。</div>2019-02-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/45/3cb5cdc6.jpg" width="30px"><span>拾迹</span> 👍（15） 💬（0）<div>老师对贺老反对&#39;class fileds&#39;持什么看法？虽然听了两次贺老的演讲，仍然还是有点没搞明白。链接：https:&#47;&#47;github.com&#47;hax&#47;js-class-fields-chinese-discussion</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/56/09/4a9d4a35.jpg" width="30px"><span>zj坚果</span> 👍（10） 💬（4）<div>看完这一章的内容，忍不住想推荐Michael S.Mikowski和Josh C. Powell 的《单页Web应用-JavaScript从前端到后端》，这里面的第二章就是专门介绍 JavaScript 基础的，其中就有对基于原型和基于类的两种方式进行比较，个人觉得讲得听清楚的。</div>2019-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（9） 💬（0）<div>讲得很好，今天是不是因为放假了，人好像有点少...平时写代码，基本上没写过class，都是function，体积大了就拆成小的...可能还是没遇到复杂的场景吧...而且vue等框架本身就解决了一定的复杂度</div>2019-01-31</li><br/><li><img src="" width="30px"><span>Jasmin</span> 👍（7） 💬（2）<div>java工程师转过来的前端 很容易理解class extends 相反 基于原型的继承 function神马的 一直不能很好的理解....</div>2019-04-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJxhkqxtWKQeYrYlVYphlicHXW5KmHAvibx6hmice4NTvmn60ZEfTpLp3480umVEquqPdMfwOnecj6Aw/132" width="30px"><span>焦糖大瓜子</span> 👍（6） 💬（0）<div>私有属性prototype与私有字段 [[prototype]] 的如何区分?
</div>2019-05-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/51/9f/1840385e.jpg" width="30px"><span>胡永</span> 👍（6） 💬（1）<div>这篇文章读一遍有一遍新的体会，厉害了</div>2019-02-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/21/51/12568118.jpg" width="30px"><span>Rickyshin</span> 👍（6） 💬（5）<div>平时用react的话，class还是比较多的，那么想问一下，现在的react不推荐写constructer，而是推荐使用箭头函数直接写方法，是不是constructer会在未来变的不是那么重要呢</div>2019-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/be/10/ef6fe900.jpg" width="30px"><span>辉子</span> 👍（5） 💬（0）<div>所以为什么typescript火起来了，是ES6的超集，也对Java后端开发者更友好了。</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/07/97/68388d28.jpg" width="30px"><span>王小宏music</span> 👍（4） 💬（1）<div>有些东西，真的是，工作好几年可能都摸不透的，高手跟大牛之间，差距就是在于理解的通透性！ </div>2019-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/68/92/a8d58030.jpg" width="30px"><span>dearfat</span> 👍（4） 💬（0）<div>感谢winter，总之就是通透，这个境界太难了</div>2019-02-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f9/bc/cbc0207b.jpg" width="30px"><span>Scorpio</span> 👍（4） 💬（0）<div>很早就开始使用class了，主要是我以前是写java的，用的习惯</div>2019-01-31</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIEODRricvc32UpO3PxoPrFBDgmoGXdiagcibNh0outmZicXFg1icV4c5ibSknc4be3PWUPsIa3OjdMmlwA/132" width="30px"><span>study</span> 👍（3） 💬（0）<div>组合使用构造函数模式和原型模式应该可以模拟class。具体来说就是，构造函数模式用于定义实例属性，而原型模式用于定义方法和共享的属性。
function Person(name){
  this.name = name;
  this.friends = [&quot;Shelby&quot;, &quot;Court&quot;];
}
Person.prototype = {
  constructor : Person,
  sayName : function(){}
}</div>2019-02-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/39/30/f7df6ba7.jpg" width="30px"><span>米斯特菠萝</span> 👍（3） 💬（0）<div>写class多，抽象化以后，用class 看着更规整得多，易读性也更好

给微信小程序写的第一个拖拽排序的插件就是class写的，new Sortable就完事了</div>2019-02-01</li><br/>
</ul>