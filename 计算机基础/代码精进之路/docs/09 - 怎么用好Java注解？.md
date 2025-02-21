如果你使用面向对象的概念和技术有一段时间了，不知道你会不会有这样的困惑： 面向对象技术带来的麻烦，一点都不比它带来的好处少！

比如说，我们辛辛苦苦继承了一个类，重写了它的方法。过几天，这个类居然修改了它的接口，而且没人通知我们。然后，我们写的子类还可以美滋滋地编译，运行，就是总出错误，怎么调试都没发现这个子类的实现有什么不妥。直到有人说，父类变了！这时候，我们就想找杯咖啡暖暖手，一个人静静。

面向对象技术确实有它值得傲娇的地方。但是，只有把类似上面的小麻烦解决掉，它的使用才更合理。 比如说，父类做了修改，能不能立即就通知我？ 别等到问题出现了，我们还被蒙在鼓里。

Java注解就可以帮助我们。

## 什么是Java注解

Java注解是Java 1.5引入的一个工具，类似于给代码贴个标签，通过注解可以为代码添加标签信息。这些标签信息可以添加在字段、方法和类上。开发工具、部署工具或者运行类库，可以对这些标签信息进行特殊的处理，从而获得更丰富的功能。

经过十多年的发展，注解已经成了Java生态系统一个非常重要的技术。使用注解可以大幅度降低我们的开发强度，提高工作效率，减少潜在的错误。像Java类库一样，注解也有了越来越丰富的定义和规范，成了我们需要掌握的重要技术之一。
<div><strong>精选留言（23）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（52） 💬（2）<div>老师，问3个很重要的题外问题：
1. 大专学历，想直接自学考本科或研究生，自考学历中大型公司承认的吗？
2. 大公司对年龄有限制的吗？
3. 30多岁，运维（编程自学java一年，没项目经验），只有小公司工作经验，技术一般，发展方向是什么？很多IT公司好像都不要年龄大点的~~人生80，那不是40岁就没得工作了？
</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/34/3d/51762e76.jpg" width="30px"><span>大白给小白讲故事</span> 👍（16） 💬（1）<div>lombok插件的很多实用的注解
@Data 使用在类上，该注解会提供getter、setter、equals、canEqual、hashCode、toString方法。
@NonNull 该注解使用在属性上，该注解用于属的非空检查，当放在setter方法的字段上，将生成一个空检查，如果为空，则抛出NullPointerException。
@AllArgsConstructor 该注解使用在类上，该注解提供一个全参数的构造方法，默认不提供无参构造。
@NoArgsConstructor 该注解使用在类上，该注解提供一个无参构造。
等等</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/3f/87/8860f508.jpg" width="30px"><span>卞雪达</span> 👍（3） 💬（1）<div>哈哈哈，最常用的注解，现在都成Spring的@Autowired啦，还有Spring的各种注解，给我的感觉，Spring使用多了，都是注解编程啦，我参数检验都用注解完成。我也会写自己的注解，我刚刚还完成了一个@Excel，我这是个Web的项目，有的接口产生的数据，可能会被导出成Excel，我捣鼓了几波，终于弄了一个注解，放在controller层的方法上，让那种简单的回List的接口，可以直接导出成Excel（配合下http参数），我遇到比较大的麻烦，是我之前设计了一个@Page的注解，注在Service层方法上，帮助开启数据库分页（也要配合http参数，且是一个方法查一次数据的那种），而@Excel跟它有个比较大的冲突：@Page是要分页，@Excel是不要分页。用户肯定是查询的时候看到分页接口，导出的时候拿到全部结果，我得想办法通知一下@Page，我最开始尝试给@Page里面的default方法弄个参数，然后改这个值，后来发现这个值竟然不是每个线程独有的，而是唯一的，也就是改了大家全都改，后来想了想，大概是因为注解本质上是个接口或类似接口？最终选择了ThreadLocal来通知@Page，我已经使用了很多ThreadLoacal了，我之前用它不是很多，现在有些上瘾，又隐隐担心别有坑，比如我知道有个不remove可能有内存溢出的坑。回到注解的话题，注解编程我觉得挺帅的，@Override我也爱加，能给方法加多少注解我就加多少，感觉是一种加持，哈哈哈，不过创造、使用注解就像是创造、使用规则，得对这个规则熟悉，好多注解编译器也不能判断你是不是符合了规则，用的时候还是有些学习成本。</div>2019-05-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（3） 💬（1）<div>阿里巴巴的扫描插件或许会有帮助的,在使用idea的过程中,安装了Alibaba Java Coding Guidelines之后,代码的规范等等插件就会检测出来报红,虽然可以运行,但是对于有强迫症和代码洁癖的人来说就很难受.
包括了if不写括号,继承的方法没有使用@Override注解.

对于刚刚工作的我,java中的注解用的最多的就是@Override了. 废弃方法在idea中会有横线作为标记,有这种标记的方法一律不使用.

继续加油去了.</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/99/ff/046495bb.jpg" width="30px"><span>小成</span> 👍（2） 💬（1）<div>C++11引入了override关键字，对应Java的override.
C++14引入了deprecated关键字，对应Java的deprecated.</div>2019-01-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/f5/3bf66adb.jpg" width="30px"><span>web</span> 👍（2） 💬（1）<div>题目有点大, 以为是讲怎么写注解; 内容有点水, 半个版面怎么写override</div>2019-01-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（2） 💬（1）<div>现在基本上是用静态代码检查工具扫描业务代码，jdk中的废弃方法基本替换掉</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/8e/83bac3bb.jpg" width="30px"><span>程龙</span> 👍（1） 💬（1）<div>老师 我想问下，接口和实现类，注解应该写在接口 上面还是实现类?</div>2019-04-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKcg9I9LFukCRm0r06JZFnUrERQVlh7EZqTWibXcMHHAJdLJGIjy4ZvWlXfqCFvRjBW9RoqkwLXibMg/132" width="30px"><span>醉侠</span> 👍（1） 💬（1）<div>老师，想知道文章里String的构造函数为什么被移除，是因为字符编码的问题吗？</div>2019-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/e3/ed118550.jpg" width="30px"><span>Being</span> 👍（1） 💬（1）<div>Override对应C++就是virtual了，经常用，以前还真不太清楚为什么重写的方法要加，就觉得好区别，就保留这个习惯了，今天才意识到要避免父类删除继承方法后，能快速通过编译器定位问题。
貌似C++没有JAVA的Depraceted和SuppressWarnings类似的，我再查查确认下，Deprecated的用处挺大的，及时止损呀</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/44/a7/171c1e86.jpg" width="30px"><span>啦啦啦</span> 👍（1） 💬（1）<div>课程都是以java讲解的吗，没有其他编程语言吗</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/52/3b/f1501d79.jpg" width="30px"><span>不工</span> 👍（0） 💬（1）<div>老师，什么时候用 {@link } {@code } ？</div>2021-04-10</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ooZCPFY1xgC81h0Eu3vuqbWG5MaBp8RNmvXXGQwupo2LpSOLq0rBlTDRAF1yM6wF09WdeG49rA9dJSVKIUBxnQ/132" width="30px"><span>Sisyphus235</span> 👍（0） 💬（1）<div>注解如果没有校检功能就是注释，如果需要校检功能，各个语言都有自己的特色，比如 python 的装饰器，能够极大的提高代码可读性，模块封装的更好。
是否使用注解应该是个开放话题，注释倒是必须写清楚的。</div>2019-05-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/X9fK7y43n7oAo19GlYHQZRQQ2Y0Dj8wHUEDXHWXUauxXOiaMtAc0TPtv1dyXHWDr4P7icDITmOLbaKVWXnY5oReQ/132" width="30px"><span>悲劇の輪廻</span> 👍（0） 💬（1）<div>虽然只是为了举例而写的代码段，但一般情况下需要被equals的对象为字符串时我们会声明一个字符串常量，而当一个从方法获得的值需要与字符串常量作比较的时候，通常把方法返回值放在被equals的位置，这样也能避免方法返回null时抛出空指针异常，而且不会引起逻辑上的错误。:-)</div>2019-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>看你介绍，您是DBA大神，有哥们小公司搞DBA几年，会mysql、MSSQL、mongoDB，群集、分库，分表、分区简单优化等，不懂开发，我想问一下：
1.DBA一般发展方向是怎样的呀？运维和开发我了解，DBA没接触过，无法给建议，一般的升级过程是怎样的？
2.DBA开发语言选择是C++还是java，还是其它？
3.以后发展方向是怎样？现在都是开源、大数据时代时代，阿里又搞“去IOE”，一般oracle DBA发展前景不好吧？

DBA工资普遍比开发、运维高，但感觉很难~~能帮菜鸟指一个大概的方向吗？谢谢~~</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/41/27/3ff1a1d6.jpg" width="30px"><span>hua168</span> 👍（0） 💬（1）<div>非常感谢您的认真回答！谢谢……</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/6e/6a/38a3fa8d.jpg" width="30px"><span>多拉格·five</span> 👍（0） 💬（1）<div>在项目中使用Lombok可以减少很多重复代码的书写。使用注解在class文件中生成getter&#47;setter&#47;toString等方法。</div>2019-01-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0b/4e/fd946cb2.jpg" width="30px"><span>allean</span> 👍（0） 💬（1）<div>Findbugs？</div>2019-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/14/ee/d72a8222.jpg" width="30px"><span>攻城拔寨</span> 👍（1） 💬（0）<div>用的最多的应该是Lombox的@Data了</div>2019-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>不要等到压力山大的时候才救火。--记下来</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（0） 💬（0）<div>重写的方法，总是使用；
过时的接口，尽早废弃；
废弃的接口，不要使用。
虽然我们的开发语言没有注解一说，但是可以这都是借鉴的地方，赞~</div>2021-11-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/4e/1c654d86.jpg" width="30px"><span>Omooo</span> 👍（0） 💬（0）<div>用得最多的肯定就是 Android 里面的 NonNull 和 Nullable 了。</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/1a/66/2d9db9ed.jpg" width="30px"><span>苦行僧</span> 👍（0） 💬（0）<div>spring注解才是坑超级多</div>2019-03-11</li><br/>
</ul>