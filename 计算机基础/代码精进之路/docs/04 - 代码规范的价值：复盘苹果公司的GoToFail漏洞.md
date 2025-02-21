我们在上一讲中讨论了一个优秀的程序员都需要具备哪些良好的品质，第一点就是要熟练掌握一门编程语言。

作为每天都要和代码打交道的人，光是熟练掌握还不够。我们需要像文字写作者一样，对代码有一种“洁癖”，那就是强调代码的规范化。

## 什么是编码规范？

要回答为什么需要编码规范，我们首先要了解编码规范指的是什么。

编码规范指的是针对特定编程语言约定的一系列规则，通常包括文件组织、缩进、注释、声明、语句、空格、命名约定、编程实践、编程原则和最佳实践等。

一般而言，一份高质量的编码规范，是严格的、清晰的、简单的，也是权威的。但是我们有时候并不想从内心信服，更别提自觉遵守了。你可能想问，遵循这样的约定到底有什么用呢？

编码规范可以帮我们选择编码风格、确定编码方法，以便更好地进行编码实践。 简单地说，**一旦学会了编码规范，并且严格地遵守它们，可以让我们的工作更简单，更轻松，少犯错误**。

这个问题弄明白了，我们就能愉快地遵守这些约定，改进我们的编程方式了。

## 规范的代码，可以降低代码出错的几率

**复杂是代码质量的敌人**。 越复杂的代码，越容易出现问题，并且由于复杂性，我们很难发现这些隐藏的问题。

我们在前面已经讨论过苹果公司的安全漏洞（GoToFail漏洞），接下来再来看看这个bug的伪代码。这个代码很简单，就是两个if条件语句，如果判断没问题，就执行相关的操作。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/74/68/3725546b.jpg" width="30px"><span>Carlos</span> 👍（5） 💬（2）<div>我感觉我就是一个有代码洁癖的人，写代码时有自己的原则和规范方法，其中做到易读和结构简洁是首要原则，这里面像命名，缩进，空行这种静态规则，有IDE的帮助还算比较容易做到。对于不少人来说比较难做到的可能是代码逻辑的组织。前几天刚看了个同事写的代码，关于视频课程管理的，表结构设计也是他做的。业务上要求课程需要属于某个等级，等级属于类别，类别属于厂商，为了做到同一个课程向不同客户展示不同的价格，又设计了个课程价格关系模型。这几个子项都有对应的业务模型和业务接口类。问题来了，添加课程时，在课程的某一个controller方法里，分别通过getparameter获取参数，构造数据对象，然后调用业务逻辑接口执行插入，最终完成多个业务模型的操作，有的是一对多再来个循环。一个方法里干这么多事情，我都接受了，居然把获取参数和给对象赋值无规律的穿插进行，偶尔还穿插来个参数校验，并且还在方法内部把获取过来的参数加个中文注释。删除课程数据时，需要把关联子模型数据也删除掉，他把各个子模型的删除方法都写到课程的service里。另外还存在A引用B，B又引用A，同时A又被其他好几个地方引用，不同引用之间通过不同参数走不同分支，并且有些参数在哪个场景下传过来的，他自己也弄不清了。带来这样问题就是写代码前，没把逻辑脉络梳理清楚，完全跟着感觉走，就一个简单的增删改查能写成这样，真怀疑要是把一个后端数据服务的代码给他写不知道能给写成啥样。</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（13） 💬（2）<div>读烂代码就想抽人。
类似于new一堆对象。然后在几十行以后才使用   如果命名规范还好，如若不规范就要点回去看。
还有这样奇怪的代码，写了个循环便利集合，但是循环中只有
if（list.get（0）！=null）｛
return list.get（0）；
｝
每次读这样的代码。全都要研究一下这个循环是干啥的。
还有这样的，解决异常。try包了一大串代码，找哪一行抛的异常很费劲。
还有实体类型字段，String state=“1”；
然后后面备注。1代表啥，2代表啥，3代表啥。
不老老实实写个枚举或者常量嘛？
还有代码里的无端空行。写一行，空一行......一个半屏幕滚动能看完的代码，硬是看了两个半屏幕。
关键是还没法去说，毕竟同事之间。只是默默祈祷，不要让自己维护他的代码就好。</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/88/c8/6af6d27e.jpg" width="30px"><span>Y024</span> 👍（10） 💬（2）<div>阿里巴巴 java 开发规范，官方已提供了 idea、eclipse 插件，详情可以访问官方链接：https:&#47;&#47;github.com&#47;alibaba&#47;p3c&#47;blob&#47;master&#47;README.md

此外还有FindBugs、PMDPlugin、CheckStyle
、JavaNCSS、sonarlint，可以多管齐下，为你保驾护航。</div>2019-01-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/50/4d/abb7bfe3.jpg" width="30px"><span>richey</span> 👍（6） 💬（1）<div>范老师，阿里的代码规约检查插件已经有了，还挺好用的</div>2019-01-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKjoHHMVibKZicReibTxbZtNQRgqneI5lOaiaTvtxaiau6YXjMSvA2rM2chV10WliayrkAJcGT6p3ZWkT0Q/132" width="30px"><span>cocoa</span> 👍（6） 💬（1）<div>1.属性明确加上private
2.泛型赋值的时候自动判断类型，不用显示加
3.if的第一个或条件不需要
4.if使用大括号
5.map一般用来转换，这块用迭代foreach就行了
6.不用使用顺序迭代，本来集合list就有顺序
7.toSring显示标明override</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/71/05/db554eba.jpg" width="30px"><span>👽</span> 👍（2） 💬（1）<div>“我替你想两个办法，一个是琢磨琢磨怎么说他会愉快滴接受，并且感谢你。或者，琢磨琢磨怎么搞个规范，让流程帮助他。 他变好了，你也工作轻松，心情愉快，对吧？ 多赢！ 这种事情，也能给你带来成就感，不信你就试一试😄。”
为了看到规范代码。我做了以下的事：
1. 自己先更加严格要求自己的代码。
2. 参加了阿里巴巴代码规范的认证考试，并拿到了证书。
3. 把证书给领导看一眼（证明我自己是规范的），然后说规范很有用。
4.领导表示，嗯，他也觉得是这样。
5.领导在群里通知，建议大家考一下，费用公司报销。
5几个月过去了，我还是唯一一个我们单位执证上岗的。
6. 报了范老师的课程。无法要求别人，但是更不能停止精进自己！最起码不能让别人骂我的代码！
希望这段留言不会被我同事或者领导看到，紧张。
不过，被看到了，貌似也有好处，没准我们公司的代码明天就规范化了呢。</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/82/ab3f0985.jpg" width="30px"><span>槛外人</span> 👍（2） 💬（1）<div>希望能多点最佳实践，最近几期好像有点重复了</div>2019-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/9b/ba/333b59e5.jpg" width="30px"><span>Linuxer</span> 👍（2） 💬（2）<div>看自己的代码不顺眼，看别人的也是，开源代码很多就看着赏心悦目。总感觉那方面还需要加强，总是不得其法</div>2019-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/50/fb/872e2cf1.jpg" width="30px"><span>秦凯</span> 👍（2） 💬（1）<div>分享两条简单、有价值的实践：
在编辑器中设置使用指定的空格数（一般四个）替换tab键；
范老师之前提到的，用if else 替换三目运算符，以及用 i += 1; 替换 ++i;等，可以让代码逻辑更易于理解，降低阅读成本。</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（1）<div>这里想问老师一个问题：那金融业务编码规范又是什么呢？包含什么内容？</div>2024-01-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/68/86/348be7f8.jpg" width="30px"><span>Lingo</span> 👍（0） 💬（1）<div>我们需要像文字写作者一样？？
文字写作者？
作者写文章？</div>2023-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/da/ec/779c1a78.jpg" width="30px"><span>往事随风，顺其自然</span> 👍（0） 💬（1）<div>为什么后面追加要改成流逝的数据？</div>2019-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/c0/d38daa2d.jpg" width="30px"><span>yaya</span> 👍（0） 💬（1）<div>这个课程是以java作为基础的吗？虽然还是可以读懂，但是有些细节比较模糊</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/c0/d38daa2d.jpg" width="30px"><span>yaya</span> 👍（0） 💬（1）<div>现在有什么统一的规范吗，我对于变量命名，方法命名，对于英语不是很好词汇量不是很多的人感觉有点困难，有什么ide可以用吗</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d3/c0/d38daa2d.jpg" width="30px"><span>yaya</span> 👍（0） 💬（1）<div>现在有什么统一的规范吗，我对于变量命名，方法命名，对于英语不是很好词汇量不是很多的人感觉有点困难，有什么ide可以用吗</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/73/a0/7dcc9212.jpg" width="30px"><span>adang</span> 👍（0） 💬（1）<div>编码规范没有绝对的好与坏，最重要的是大家要遵守，目的就是为了高效率的协作，就像范老师所说的流水线要顺畅</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/79/69/5960a2af.jpg" width="30px"><span>王智</span> 👍（0） 💬（1）<div>刚开始工作,感觉自己写的代码好low,时间复杂度很高,自己写的都不想看,(╥╯^╰╥),还得磨练,这个需要加强,加油.</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/a0/58/abb7bfe3.jpg" width="30px"><span>Kai</span> 👍（0） 💬（1）<div>我觉得每个公司都可以有一套自己的或者fork当前流行的代码规范，这样做code review也会更容易。另外设置一个lint自动帮助格式化代码，提出警告也是十分必要的</div>2019-01-11</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ibZVAmmdAibBeVpUjzwId8ibgRzNk7fkuR5pgVicB5mFSjjmt2eNadlykVLKCyGA0GxGffbhqLsHnhDRgyzxcKUhjg/132" width="30px"><span>pyhhou</span> 👍（0） 💬（1）<div>1. 第十一行那加泛型的方式容易出错
2. 第十五行，十六行没有大括号和缩进
3. 第二十二行的_item，感觉没有使用到，是不是可以省略</div>2019-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/e2/9a/9ff4869c.jpg" width="30px"><span>阔别</span> 👍（2） 💬（1）<div>我不明白换行这个事情有什么必要来回说的, 现在工具不都可以格式化吗, 我无意diss作者,但是我已经看到第四节了,依然没有看到真正有任何价值的东西</div>2021-05-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7e/83/27fd9c50.jpg" width="30px"><span>ownraul</span> 👍（1） 💬（0）<div>代码首先是给自己看的，然后是给别人看的，最终还要给以后的自己看的
只有让人一眼望去，其中想要表达的逻辑能清晰明了，一览无遗，这才是好代码</div>2019-01-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/02/94/abb7bfe3.jpg" width="30px"><span>Geek_wip5z8</span> 👍（0） 💬（0）<div>import javax.net.ssl.SNIServerName;
import java.util.Collections;
import java.util.List;

public class ServerNameSpec {
    final List&lt;SNIServerName&gt; serverNames;

    ServerNameSpec(List&lt;SNIServerName&gt; serverNames) {
        this.serverNames = Collections.unmodifiableList(serverNames);
    }

    @Override
    public String toString() {
        if (serverNames == null || serverNames.isEmpty()) {
            return &quot;&quot;;
        }
        StringBuilder builder = new StringBuilder(512);
        serverNames.forEach((_item) -&gt; {
            builder.append(_item.toString());
            builder.append(&quot;\n&quot;);
        });
        return builder.toString();
    }
}
</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>优秀的代码不光是给自己看的，也是给别人看的，而且首先是给别人看的。--记下来</div>2022-07-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/34/cf/0a316b48.jpg" width="30px"><span>蝴蝶</span> 👍（0） 💬（0）<div>Stream的缩进烧脑 override加上 成员变量私有 我想改的</div>2022-05-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7b/bd/ccb37425.jpg" width="30px"><span>进化菌</span> 👍（0） 💬（0）<div>规范规范，有规矩有范例，遵守规矩效仿案例。
练习里，有看到没有使用合理的缩进和大括号……其实，最近看自己一个月前的代码，一个方法了放过重的逻辑，看的也是很头大。
代码如写诗，总得努力改变，让Ta如同自己一般清晰稳健的劳动~</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/d3/77/fb38ccf1.jpg" width="30px"><span>玄兴梦影</span> 👍（0） 💬（0）<div>代码如诗！</div>2020-03-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/5b/08/b0b0db05.jpg" width="30px"><span>丁丁历险记</span> 👍（0） 💬（0）<div>对o  为啥不加大括号？？？  脑子进水了？？？</div>2020-01-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/6a/2d/09700017.jpg" width="30px"><span>華</span> 👍（0） 💬（0）<div>编码规范除了个人要有良好的编码习惯外，最好还是能有一些工具来辅助，比如阿里的编码规范插件，还有团队协作编码，基础的规则，可以使用EditorConfig制定。</div>2019-08-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ooZCPFY1xgC81h0Eu3vuqbWG5MaBp8RNmvXXGQwupo2LpSOLq0rBlTDRAF1yM6wF09WdeG49rA9dJSVKIUBxnQ/132" width="30px"><span>Sisyphus235</span> 👍（0） 💬（0）<div>代码不是写给自己看的，也没有代码不需要迭代开发，规范的代码能提高协作的效率</div>2019-05-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/60/be/68ce2fd0.jpg" width="30px"><span>小田</span> 👍（0） 💬（0）<div>代码规范是协作的基础，质量的保证，因此促成了开发的高质量、高效率</div>2019-01-12</li><br/>
</ul>