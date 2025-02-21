你好！我是郑晔。

上一讲，我们讲了开放封闭原则，想要让系统符合开放封闭原则，最重要的就是我们要构建起相应的扩展模型，所以，我们要面向接口编程。

而大部分的面向接口编程要依赖于继承实现，虽然我们在前面的课程中说过，继承的重要性不如封装和多态，但在大部分面向对象程序设计语言中，继承却是构建一个对象体系的重要组成部分。

理论上，在定义了接口之后，我们就可以把继承这个接口的类完美地嵌入到我们设计好的体系之中。然而，用了继承，子类就一定设计对了吗？事情可能并没有这么简单。

新的类虽然在语法上声明了一个接口，形成了一个继承关系，但我们要想让这个子类真正地扮演起这个接口的角色，还需要有一个好的继承指导原则。

所以，这一讲，我们就来看看可以把继承体系设计好的设计原则：Liskov替换法则。

## Liskov替换原则

2008年，图灵奖授予Barbara Liskov，表彰她在程序设计语言和系统设计方法方面的卓越工作。她在设计领域影响最深远的就是以她名字命名的Liskov替换原则（Liskov substitution principle，简称LSP）。

1988 年，Barbara Liskov在描述如何定义子类型时写下这样一段话：
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/f8/88/96b870fd.jpg" width="30px"><span>zcc</span> 👍（22） 💬（1）<div>那从父类的角度来考虑的话，应该是定义一个几何图形的接口，接口有计算面积的方法。然后长方形、正方形、圆形、三角形……都实现这个接口，然后各自实现计算面积的方法。各自有自己特别的关键属性，根据属性计算各自面积:长*宽、边长²、πr²、(底长*高)&#47;2、……</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/9c/a4bc748d.jpg" width="30px"><span>Janenesome</span> 👍（18） 💬（1）<div>千万要遏制自己写 if 的念头，一旦开了这个头，后续的代码也将变得难以维护。刚好前段时间看到过一种说法：以多态应用为荣，以分支判断为耻。哈哈</div>2020-10-23</li><br/><li><img src="" width="30px"><span>Geek_3b1096</span> 👍（11） 💬（1）<div>时刻提醒自己: 千万要遏制写if的念头</div>2020-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/24/c6b763b4.jpg" width="30px"><span>桃子-夏勇杰</span> 👍（6） 💬（1）<div>这个设计原则看着非常简单，提出者居然能获得图灵奖，可见这个设计原则的价值非常大。郑老师，这个设计原则的价值到底有多大呢？</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/7a/9c/a4bc748d.jpg" width="30px"><span>Janenesome</span> 👍（4） 💬（2）<div>郑老师给出的业务开发的案例真的挺接地气。

运行时类型识别我以前写过，后面回去维护的时候想打死自己，怎么写出这样的烂代码。

还有业务分析里的素材分类，太真实了，平时做需求时很多概念有点相似，放在一起好像也可以而且看起来还能省点力气，没有太深入思考的话就会放在一起了，一些差异化的部分就单独存或者用条件判断。</div>2020-10-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJbh5FQajwKhNlMrkoSklPpOXBtEYXCLvuWibhfWIS9QxHWDqzhEHJzEdmtUiaiaqFjfpsr2LwgNGpbQ/132" width="30px"><span>Geek_q29f6t</span> 👍（4） 💬（5）<div>RequestParser 中还是免不了用多个 if 来判断 identifier，从而返回特定的子类吧</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/94/e3/ed118550.jpg" width="30px"><span>Being</span> 👍（4） 💬（2）<div>全篇一直在强调行为，我想这也是思考题的突破口。长宽是数据，而Rectangle并没有将行为抽象出来，导致Rectangle和Square不能成为IS-A的关系，我们只要把求面积的行为放在Rectangle下，子类分别去实现面积的方法就好了。</div>2020-07-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/b2/3c/22028324.jpg" width="30px"><span>呆呆狗的兽</span> 👍（2） 💬（1）<div>lsp这一分享，很精髓也很精彩，is-a这个太重要了，遵循is-a会让系统越来越稳定且易拓展</div>2021-07-19</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/17/27/ec30d30a.jpg" width="30px"><span>Jxin</span> 👍（2） 💬（1）<div>如果业务场景合适，约束功能也不失为一个解决办法。让宽高不可变，初始化时就必须赋值。这样就能符合现实中的特性。自然也没有长宽赋不同值的麻烦。</div>2020-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/47/e4/17cb3df1.jpg" width="30px"><span>BBQ</span> 👍（1） 💬（1）<div>关于不同客户的不同格式问题，我们单独开发了一套系统，在这个系统里面做接口格式映射，然后再调用标准接口。
由于这个系统的受众是实施人员，所以界面做到可以通过拖拽来实现映射。
当然实际功能更多，包括聚合，转换，以及enrich 功能
总之，把这个映射的关注点单独独立成了一个系统。</div>2021-07-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/63/f5/9c7ef5ce.jpg" width="30px"><span>CPP</span> 👍（1） 💬（2）<div>两个set函数改成一个，setparam(int height,int width);</div>2020-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f9/88/cdda9e6f.jpg" width="30px"><span>阳仔</span> 👍（1） 💬（1）<div>Liskov替换的意思是子类型能够替换父类型，且在继承体系中保持接口的一致
长方形与正方形计算面积的行为接口是一样的，但是定义长方形和正方形的接口是不一样的，所以这两个行为可以分别抽离出来</div>2020-07-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJRCtuJkpyy2NTTABPFibg2k9tZscOOKx9wu80a85d5HspCorO9Nibj7Z7q9v1icPTVm5ia52r0RCzEaA/132" width="30px"><span>Stay_Gold</span> 👍（0） 💬（1）<div>之前一直对于LSP的理解不够深入，看老师前面的例子也觉得大部分历史符合子类可以替换父类的情况。
深入了解其实LSP是指导我们子类应该是对父类的扩展或者说增强，而不是去修改父类的行为预期。
如果实际情况子类需要有不符合父类的行为创建，代表我们需要进一步重构优化我们的继承关系，提出新的满足情况的继承关系。</div>2025-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/17/dd/7d88bc91.jpg" width="30px"><span>张chuang</span> 👍（0） 💬（1）<div>在正方形类中重写长方形的计算面积接口</div>2020-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（9） 💬（0）<div>刚知道 Liskov 是位女士，我原来记的是“里氏科夫”，所以就想当然的以为是男的了。

以前在考虑继承或者子类的时候，其实没有想到要“行为相同”，更多的是把相同的方法提取到父类，自以为 DRY，洋洋自得。

“创作者素材”和“可销售素材”这个例子有点晦涩了，经过文中的分析，能看明白是两个领域，但是还是有一点疑惑，这两种素材之间不可以转换么？比如从创作者素材转为可销售素材？

可能比较简单直接的做法是在素材类里面设置一个状态——是否可销售，不过这样一来的确会给编码带来很多麻烦。

用解析器代替 if 语句，代码顿时就“高大上”起来了。

LSP 的重点在于接口继承。

在专栏后续的依赖倒置原则里面，有一条编码规则：任何类都不应继承自具体类。</div>2020-09-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/32/e1/c9aacb37.jpg" width="30px"><span>段启超</span> 👍（8） 💬（0）<div>发表一下我的想法：长方形正方形问题反应出的是大多人认为的正方形是一种特殊的长方形，在面向对象的世界中不成立的。面向对象的出发点是对象的行为，只要行为一致，他们就可以是一类东西，这个和《head first 设计模式》一文中开篇的那个各种不同类型的鸭子是一个道理，虽然有的是玩具鸭，有的是实实在在的鸭子， 只要有叫的行为，飞的行为，游泳的行为，那么他们就可以成为“鸭子”。 
最近在写代码的过程中发现一个有趣的问题，我们总在对象中依赖各种对象，但是实际上只是依赖了那个对象中的某个行为（方法，或者是能力），依赖的具体类多了，免不了就会把那些不需要的能力引进来；而且具体的类依赖的多了，循环依赖不可避免的就会出现。 所以我想，以后引入某个依赖的时候不妨先考虑一下，我这里需要的真的是这个对象么？ 如果不是，能否把自己需要的那个能力单独放到一个接口或者是一个单独的对象中呢?</div>2020-09-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/84/0d/4e289b94.jpg" width="30px"><span>三生</span> 👍（4） 💬（0）<div>所有的形状都有求面积的方式，但是计算方式都不同，这行为应该是“正常的”，但是设置长和宽的行为不正确，因为长方体有宽和高，正方形只有宽或高，这里只能抽象出计算面积这个方法。

比如企鹅和麻雀，我们认为所有的鸟都会飞，但企鹅不会飞，而他却具有了飞的行为，这是“不正常”的</div>2020-07-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ea/1d/efddaad6.jpg" width="30px"><span>小麦</span> 👍（1） 💬（0）<div>千万要遏制自己写 if 的念头，一旦开了这个头，后续的代码也将变得难以维护
public class Animal {
    public void makeSound(String animalType) {
        if (&quot;cat&quot;.equals(animalType)) {
            System.out.println(&quot;meow&quot;);
        } else if (&quot;dog&quot;.equals(animalType)) {
            System.out.println(&quot;woof&quot;);
        } else if (&quot;cow&quot;.equals(animalType)) {
            System.out.println(&quot;moo&quot;);
        } else {
            throw new IllegalArgumentException(&quot;Unknown animal type: &quot; + animalType);
        }
    }
}



public interface Animal {
    void makeSound();
}

public class Cat implements Animal {
    @Override
    public void makeSound() {
        System.out.println(&quot;meow&quot;);
    }
}

public class Dog implements Animal {
    @Override
    public void makeSound() {
        System.out.println(&quot;woof&quot;);
    }
}

public class Cow implements Animal {
    @Override
    public void makeSound() {
        System.out.println(&quot;moo&quot;);
    }
}</div>2023-06-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（1） 💬（1）<div>用父类的角度去思考，设计行为一致的子类--记下来
课后问题: 是否设计一个矩形父类，长方形和正方形都继承矩形呢？</div>2022-05-18</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEIbHkxDx8BWGChVr3WmJrLfRUmdNZYQVVGENW25JfrgycYFuibBmDiaSktTD2skqEaQEVKNeSulhtJw/132" width="30px"><span>pangou</span> 👍（0） 💬（0）<div>为了避免违反里氏替换原则（LSP）并解决Square和Rectangle的问题，我们可以重新设计这些类的结构。一种方法是使用一个共同的基类或接口，例如Shape，然后让Rectangle和Square各自独立地实现这个接口或继承自这个基类。这样，我们就不会期望Square能够替换Rectangle，从而避免了违反LSP的问题。

以下是使用接口的一个示例解决方案：
```java
&#47;&#47; 定义一个形状接口，包含计算面积的方法
interface Shape {
    int area();
}

&#47;&#47; 长方形类实现形状接口
class Rectangle implements Shape {
    private int height;
    private int width;

    public Rectangle(int height, int width) {
        this.height = height;
        this.width = width;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public void setWidth(int width) {
        this.width = width;
    }

    @Override
    public int area() {
        return this.height * this.width;
    }
}

&#47;&#47; 正方形类实现形状接口
class Square implements Shape {
    private int side;

    public Square(int side) {
        this.side = side;
    }

    public void setSide(int side) {
        this.side = side;
    }

    @Override
    public int area() {
        return this.side * this.side;
    }
}
```

在这个解决方案中，Rectangle和Square都实现了Shape接口，这意味着它们都必须提供area()方法的实现。这样，我们就可以在需要形状对象时使用这个接口，而不用担心LSP问题，因为现在没有隐含的假设说一个Square应该能够替换一个Rectangle。</div>2024-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/fd/58/1af629c7.jpg" width="30px"><span>6点无痛早起学习的和尚</span> 👍（0） 💬（0）<div>看完还是有点迷糊，这里对于最后一个案例（优化 if）有个思考，这个优化也结合了开闭原则去优化的吧。</div>2023-09-22</li><br/><li><img src="" width="30px"><span>Geek_99dc8a</span> 👍（0） 💬（0）<div>我觉得技术是ok的，但是码字码的不是很明白，并非通俗易懂</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/15/f9/0b14785a.jpg" width="30px"><span>三三</span> 👍（0） 💬（0）<div>关注父类的行为</div>2022-09-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/25/54/ef2ca14f.jpg" width="30px"><span>KK</span> 👍（0） 💬（0）<div>关于长方形正方形问题的解决思路: 
- 接口不应该共享; 
- 如果square要复用rectangle的功能, 通过组合来实现即可;</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/57/2a/cb7e3c20.jpg" width="30px"><span>Nio</span> 👍（0） 💬（0）<div>关注公共的行为
这个应该是本文的重点</div>2022-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/c3/d0/10fe80f1.jpg" width="30px"><span>RainJeyin</span> 👍（0） 💬（0）<div>今天这一讲没有看明白，自己还要多学习。</div>2022-02-10</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kBKTRyV4wnhV4YN9iaFgKYIJ4451n0zIiazFumcSpCXdEDhdexgc8PQdrDEmy4BCOUgsUlibicEwQlGo6K5Nibv7SEg/132" width="30px"><span>托马斯赵四</span> 👍（0） 💬（0）<div>听到这，使用javascript语言的我还是有些似懂非懂，看来还是得多学多思考</div>2021-12-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJUCiacuh59wMbq1icuB8U1T7Vpic8FjKFdanvdt9bzClBmYqFUXmtKmh2Zibn9Dic6A8pjdoBiaia1LCrnA/132" width="30px"><span>tdd学徒</span> 👍（0） 💬（0）<div> public void setSide(int side) {    this.setHeight(side);    this.setWidth(side); }
这里setSide是super.setHeight(side)吧 </div>2021-05-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/21/c0/38816c31.jpg" width="30px"><span>春之绿野</span> 👍（0） 💬（1）<div>我想问下老师，我写的都是pipeline 和里面嵌套的shell 脚本，不能用接口多态这些技术，里面for if else嵌套好多层，太头大了，这种怎么改进啊？</div>2021-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/0c/89/d5077e61.jpg" width="30px"><span>可笑的霸王</span> 👍（0） 💬（0）<div>看起来组合才适合正长方形</div>2021-03-05</li><br/>
</ul>