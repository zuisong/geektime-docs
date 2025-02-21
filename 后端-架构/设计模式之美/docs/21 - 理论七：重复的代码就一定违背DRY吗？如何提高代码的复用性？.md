在上一节课中，我们讲了KISS原则和YAGNI原则，KISS原则可以说是人尽皆知。今天，我们再学习一个你肯定听过的原则，那就是DRY原则。它的英文描述为：Don’t Repeat Yourself。中文直译为：不要重复自己。将它应用在编程中，可以理解为：不要写重复的代码。

你可能会觉得，这条原则非常简单、非常容易应用。只要两段代码长得一样，那就是违反DRY原则了。真的是这样吗？答案是否定的。这是很多人对这条原则存在的误解。实际上，重复的代码不一定违反DRY原则，而且有些看似不重复的代码也有可能违反DRY原则。

听到这里，你可能会有很多疑问。没关系，今天我会结合具体的代码实例，来把这个问题讲清楚，纠正你对这个原则的错误认知。除此之外，DRY原则与代码的复用性也有一些联系，所以，今天，我还会讲一讲，如何写出可复用性好的代码。

话不多说，让我们正式开始今天的学习吧！

## DRY原则（Don’t Repeat Yourself）

DRY原则的定义非常简单，我就不再过度解读。今天，我们主要讲三种典型的代码重复情况，它们分别是：实现逻辑重复、功能语义重复和代码执行重复。这三种代码重复，有的看似违反DRY，实际上并不违反；有的看似不违反，实际上却违反了。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/bc/a7/d36843c9.jpg" width="30px"><span>花颜</span> 👍（11） 💬（2）<div>老师，我有个问题，在大型多人协作项目当中，类、功能都是分散给不同的人开发的，不同的开发者质量良莠不齐，而实现逻辑重复有代码重复率校验工具可以做检测，而功能语义重复和代码执行重复其实不是那么容易能够发现，即使通过有效的codeReview，有没有什么工具可以辅助我们查找功能语义重复和代码执行重复这两类重复，以及在大型团队项目下，如何应用这些原则呢？毕竟靠自觉总是很难的</div>2019-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ca/c7/00e544c2.jpg" width="30px"><span>黄林晴</span> 👍（4） 💬（8）<div>“Rule of Three”中的“Three”并不是真的就指确切的“三”，这里就是指“二”。😂
这句话看了好几遍</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c2/2e/c4a527d9.jpg" width="30px"><span>blacknhole</span> 👍（3） 💬（3）<div>1，提个小问题：

“实现逻辑重复”一节的代码是不是有点问题啊？

if (!(c &gt;= &#39;a&#39; &amp;&amp; c &lt;= &#39;z&#39;) || (c &gt;= &#39;0&#39; &amp;&amp; c &lt;= &#39;9&#39;) || c == &#39;.&#39;) {}似乎应该改为if (!((c &gt;= &#39;a&#39; &amp;&amp; c &lt;= &#39;z&#39;) || (c &gt;= &#39;0&#39; &amp;&amp; c &lt;= &#39;9&#39;) || c == &#39;.&#39;)) {}。

2，说个小体会：

“可复用性、可扩展性、可维护性……”与“复用性、扩展性、维护性……”，加不加“可”，其实没有本质差别。我以为，在通常的语境中（或者几乎任何情况下），两者都是可以通用的。

比如，可复用性高，说明能够复用，与当前是否已经复用无关。复用性高，是指当前已经大量复用，说明在这之前可复用性高。已经大量复用时，依然可以更多地复用，也即：复用性高，意味着可复用性依然高。

通常的语境中，也即通常提到“复用性”时，人们几乎只关注能不能复用，而不是已经复用了多少。所以，可以认为，可复用性高等同于复用性高。</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c1/24/0ea08c9e.jpg" width="30px"><span>柴柴777</span> 👍（1） 💬（1）<div>我 之前就有个问题就说 我们如果用了组件化 每个模块算是单独的  尽管可能会写一个单独的util模块但是 还是存在着 重复代码,但是这些重复代码不在一个module里,那这样的到底算不算重复呢,,这些简单的部分的少量的重复不值得去单独加一个module</div>2020-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0d/eb/c3ff1e85.jpg" width="30px"><span>🐝</span> 👍（0） 💬（1）<div>为了不重复，在合并代码里写if else 是否合适</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/50/d7/f82ed283.jpg" width="30px"><span>辣么大</span> 👍（204） 💬（20）<div>1、注释或者文档违反DRY
2、数据对象违反DRY

对于1，例如一个方法。写了好多的注释解释代码的执行逻辑，后续修改的这个方法的时候可能，忘记修改注释，造成对代码理解的困难。实际应用应该使用KISS原则，将方法写的见名知意，尽量容易阅读。注释不必过多。

对于2、例如类
class User
  String id
  Date registerDate
  int age
  int registedDays
其中 age可以由身份证号码算出来，而且每年都会递增。注册会员多少天了，也可以算出来。所以是不是可以考虑，数据只存储id和注册时间。其余两个字段可以算出来。

补充：
DRY不是只代码重复，而是“知识”的重复，意思是指业务逻辑。例如由于沟通不足，两个程序员用两种不同的方法实现同样功能的校验。
DRY is about the duplication of knowledge, of intent. It’s about expressing the same thing in two different places, possibly in two totally different ways.

当代码的某些地方必须更改时，你是否发现自己在多个位置以多种不同格式进行了更改？ 你是否需要更改代码和文档，或更改包含其的数据库架构和结构，或者…？ 如果是这样，则您的代码不是DRY。

when some single facet of the code has to change, do you find yourself making that change in multiple places, and in multiple different formats? Do you have to change code and documentation, or a database schema and a structure that holds it, or…? If so, your code isn’t DRY.

参考：
The Pragmatic Programmer: your journey to mastery, 20th Anniversary Edition (2nd Edition)</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（30） 💬（18）<div>加油啊感觉更新太慢了一个下午就看完了..,一个星期至少更新10课吧.</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（27） 💬（5）<div>产品经理有时候设计产品功能的时候也会重复</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ed/4d/1d1a1a00.jpg" width="30px"><span>magict4</span> 👍（20） 💬（5）<div>&gt; 重复执行最明显的一个地方，就是在 login() 函数中，email 的校验逻辑被执行了两次。一次是在调用 checkIfUserExisted() 函数的时候，另一次是调用 getUserByEmail() 函数的时候。这个问题解决起来比较简单，我们只需要将校验逻辑从 UserRepo 中移除，统一放到 UserService 中就可以了。

这样处理会有一个问题：如果别的 xxxService 也需要用到 UserRepo，而且没有对 email 跟 password 进行校验，直接调用了 UserRepo.checkIfUserExisted() ，会产生异常。

一种方法是约定，所有关于 User 的操作都只能通过 UserService 进行，不能直接调用 UserRepo。

另一种方法是“强制” xxxService 进行校验。我们可以把 UserRepo.checkIfUserExisted 的方法签名改成 

UserRepo.checkIfUserExisted(Email email, Password password)

并且把 validation 的逻辑封装在 Email 跟  Password 类的构造函数中。这样 xxxService 必须先把 email 跟 password 从 String 类型转成对应的 Email&#47;Password 类，才能调用 UserRepo，validation 的逻辑会在转换中被强制执行。</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/ad/18/41831eae.jpg" width="30px"><span>AaronChun</span> 👍（17） 💬（1）<div>数据库转换对象beanDb和数据展现beanVo，从属性定义上来看可能存在大量重复，但从业务或系统分层来看，却是职责明确，功能单一的对象，所以这并不违反DRY原则。相反如果将两者共性部分抽离提取，后期倘若业务变更，修改就会牵扯到前台和后台，不符合单一职责和接口隔离原则。</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/fa/ab/0d39e745.jpg" width="30px"><span>李小四</span> 👍（8） 💬（0）<div>设计模式_20

# 作业：
想到的只有文档和注释的重复了，比如两个不同功能的文档，同时描写一个细节时，可能“负责”的产品经理会各自清清楚楚地写一遍。然后：
- 看的人就会懵，(描述相同时)写了两个地方，看一下是不是还有别的地方有描述；(描述不同时)，应该以哪个为准。
- 改的人也会懵，很容易忘记修改更新，更何况文档不更新程序又不会报错。。。


#感想：
回到“少干活 和 少犯错”的宗旨，重复的代码不仅写的时候会多些一遍，改的时候也要多看很多地方，多想很多差异性，多改很多地方，这样就违背了“少干活”；改的时候，容易忘记一些地方，维护多种逻辑实现的同一个逻辑，也容易疏忽而出错，这样就违背了“少出错”。

说句题外话，文中提到“Rule of Three”时，原来外国人也用“三”表示多个，而且表示的还是2个。。。</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/bb/11/28d86278.jpg" width="30px"><span>人月聊IT</span> 👍（6） 💬（0）<div>总结：功能语义重复才是真的重复，实现逻辑重复不一定就是重复，代码执行重复就一定是重复</div>2021-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/65/a8/6431f8b0.jpg" width="30px"><span>Kang</span> 👍（5） 💬（0）<div>是不是所有包含or and的方法名的函数其实都不满足单一职责？</div>2020-09-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/9b/65f98192.jpg" width="30px"><span>Wh1</span> 👍（4） 💬（0）<div>二刷时存在一个小问题，&quot;只能允许用户名、密码字符串为小写字符&quot; 与 &quot;字符范围只能是a-z、0-9、.&quot; 这个条件是不是也存在重复？按理说，只需要判断&quot;字符范围只能是 a-z、0-9、.&quot; 这个条件就满足字符全是小写了。</div>2020-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4e/8d/34e0f6f3.jpg" width="30px"><span>江小田</span> 👍（3） 💬（0）<div>收货最大的就是复用的范围定义：
业务语意层面的重复违反DRY原则；
代码写法角度的重复不违反DRY原则。</div>2021-03-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/86/20/e71b5585.jpg" width="30px"><span>蓝二哥哥我才是无羡啊👻</span> 👍（3） 💬（0）<div>模块常量重复定义也算违反DRY原则吧</div>2020-08-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/b0/29/7ab573f4.jpg" width="30px"><span>哈喽沃德</span> 👍（3） 💬（2）<div>啥时能出设计模式的教程，我的大刀早已饥渴难耐了</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/22/41/74c666f3.jpg" width="30px"><span>plain</span> 👍（3） 💬（0）<div>设计每个模块、类、函数，都要像设计外部api一样去思考，隐藏可变的细节、暴露不变的接口。</div>2019-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qOdqzmC507sibL6sichNSDaVmyoMKibEIqHWpic4CftgOQnoA3QKeRPwic9j1Ha8MLtzzqzfSRavR9GWMju09SMADUg/132" width="30px"><span>Ilearning99</span> 👍（2） 💬（0）<div>逻辑重复，功能重复，执行重复。其实执行上的重复，有时候我觉得并不能算违反DRY原则，可能是为了代码的可复用性，为了方便其他调用方的调用。</div>2020-10-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/44/58/a901cfce.jpg" width="30px"><span>LiYou</span> 👍（2） 💬（0）<div>把简单的知识点做细节对比和区分，把一些编码方法总结成点，从而形成体系。虽然都是偏理论的知识点，但读完后受益匪浅。</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/b5/e4/e6faf686.jpg" width="30px"><span>握了个大蚂蚱</span> 👍（2） 💬（0）<div>DRP：dont repeat yourself。
逻辑重复，解决方法是想办法复用并优化方法名或是方法结构；
语义重复（比如取request里的ip有两种方法），解决方法是统一成一种，不然维护困难；
代码执行重复(比如上层StringUtils.isNotBlank已经校验了，下层又去校验)，主要是性能问题而且代码也很冗余，加重理解负担。解决方法是写代码时脑子放清楚</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/68/fe/1353168d.jpg" width="30px"><span>岁月</span> 👍（2） 💬（0）<div>看完最后这个Rlue of three , 我感觉把可扩展填进去也是有道理的, 一开始不一定写得出扩展性很好的代码, 所以可以先简单来, 后面需求明确了再慢慢重构把代码变得更加可以扩展?</div>2019-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8c/80/8746de4f.jpg" width="30px"><span>刘星星</span> 👍（1） 💬（1）<div>DRY这一章让我视野开阔了，对“重复”的定义有了新的认识。
以前的代码我对代码有点走火入魔般得追求消除重复。
虽然提交时申请气爽，但是一旦需求改变或追加，就非常痛苦。
疑问就在于，为什么按照原则精简并有“复用性”的代码，在这种场景中变得寸步难行。</div>2024-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/18/bb/9299fab1.jpg" width="30px"><span>Null</span> 👍（1） 💬（0）<div>老师咱们别弄那么多正正反反的了话术了。
管代码的实现逻辑是相同的，但语义不同，我们判定它并不违反 DRY 原则，其实违反啊，可以通过更细粒度的抽来重复的地方（这个您说到了），函数只保留不同的地方，就不违反了。但是如果代码基本一样，即使语义不一样还是违反，这个没有必要”洗白“。</div>2022-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/81/c457def1.jpg" width="30px"><span>鹤涵</span> 👍（1） 💬（0）<div>DRY就是修改只修改一处。</div>2020-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/02/9b/b1a3c60d.jpg" width="30px"><span>CDz</span> 👍（1） 💬（0）<div>* DRY——don’t repeat yourself(不要重复自己）
* 重复有几种
    * 逻辑重复（代码逻辑）
    * 语义重复（不同的方法名，意思相同，实现上有所不同，但目的相同）
    * 执行重复（同一个业务中，重复执行一段代码，一般是校验上的代码）
* 以上三种重复，第一种有时候不算违反DRY，但是看起来最像是违反DRY。后面两种需要在代码中尽量避免
* DRY与代码的可复用性是两回事
* 提高代码复用性（概念，没有深入理解）
    * 减少代码耦合
    * 满足单一职责原则
    * 模块化
    * 业务与非业务逻辑分离
    * 通用代码下沉（如何下沉，什么东西下沉？）
    * 继承、多态、抽象、封装
    * 应用模板等设计模式
* Rule of three——如果一个需求没有明确需要复用性，并且未来复用性可能性并不高，写出复用性代码成本比较高，就不需要管复用性。等到下次写重复逻辑时，再进行重构。
* DRY不是只代码重复，而是“知识”的重复，意思是指业务逻辑。例如由于沟通不足，两个程序员用两种不同的方法实现同样功能的校验。
DRY is about the duplication of knowledge, of intent. It’s about expressing the same thing in two different places, possibly in two totally different ways.</div>2019-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f1/de/3ebcbb3f.jpg" width="30px"><span>DullBird</span> 👍（1） 💬（0）<div>课堂讨论没有想到其他的了。
理解一下DRY，总结就是抽取统一“逻辑”，还有相似逻辑的简化统一，
为的就是同一“逻辑”，维护一块地方就行了。</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/23/a1/b08f3ee7.jpg" width="30px"><span>何妨</span> 👍（1） 💬（2）<div>整体来说我们要做的是不写&quot;重复&quot;代码，同时考虑代码的复用性，但要避免过度设计。
这几点说起来简单其实做起来还是有些难度的，在平常写代码的时候需要多思考，写完之后要反复审视自己的代码看看有没有可以优化的地方。说起来我感觉我还算是对代码有些追求的……但是真的需求来了为了赶需求基本就一遍过了……😂，对于一些脚本代码更是过程编程，惭愧啊</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/47/31/f35367c8.jpg" width="30px"><span>小晏子</span> 👍（1） 💬（0）<div>老师概括的很全面了，提一个看看，
数据定义重复，比如数据库里定义了两个schema几乎相同的数据表，然后数据表映射到代码里的结构体或xml也几乎相同，没有把公共部分剥离。</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2c/c6/416bd86e.jpg" width="30px"><span>阿杰</span> 👍（0） 💬（0）<div>课程小结：
1、DRY原则：dont repeat yourself！直译过来就是不要重复你自己，不要写重复代码。
1.1、什么代码算是重复代码呢？代码重复包括实现逻辑重复、功能语义重复、执行重复。其中实现逻辑重复，但功能语义不重复并不违反dry原则，实现逻辑不重复，但功能语义重复违反dry原则。执行重复违反dry原则。
1.2、dry原则和代码可复用有什么区别和关联？满足dry原则，不一定代码就可复用。项目中没有重复代码，不一定就说明代码是可复用的。
2、代码可复用性：字面含义，描述的是一种代码可重复使用的特性。
2.1、如何提高代码的可复用性？
* 降低代码耦合；单一职责原则；模块化思想；业务代码与非业务代码分离；通用代码下层；抽象、封装、继承、多态；应用模板方法等设计模式；有复用意识。
* rule of three：第一次写代码时，如果没有明确的复用场景和需求，或者实现复用成本较高，那么就直接针对特定场景写代码即可；如果后面写代码时，发现可以复用这段代码，再考虑抽象出可复用的模块、类或方法。</div>2024-05-04</li><br/>
</ul>