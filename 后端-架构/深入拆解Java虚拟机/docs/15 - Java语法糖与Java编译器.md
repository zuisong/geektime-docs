在前面的篇章中，我们多次提到了Java语法和Java字节码的差异之处。这些差异之处都是通过Java编译器来协调的。今天我们便来列举一下Java编译器的协调工作。

## 自动装箱与自动拆箱

首先要提到的便是Java的自动装箱（auto-boxing）和自动拆箱（auto-unboxing）。

我们知道，Java语言拥有8个基本类型，每个基本类型都有对应的包装（wrapper）类型。

之所以需要包装类型，是因为许多Java核心类库的API都是面向对象的。举个例子，Java核心类库中的容器类，就只支持引用类型。

当需要一个能够存储数值的容器类时，我们往往定义一个存储包装类对象的容器。

对于基本类型的数值来说，我们需要先将其转换为对应的包装类，再存入容器之中。在Java程序中，这个转换可以是显式，也可以是隐式的，后者正是Java中的自动装箱。

```
public int foo() {
  ArrayList<Integer> list = new ArrayList<>();
  list.add(0);
  int result = list.get(0);
  return result;
}
```

以上图中的Java代码为例。我构造了一个Integer类型的ArrayList，并且向其中添加一个int值0。然后，我会获取该ArrayList的第0个元素，并作为int值返回给调用者。这段代码对应的Java字节码如下所示：

```
public int foo();
  Code:
     0: new java/util/ArrayList
     3: dup
     4: invokespecial java/util/ArrayList."<init>":()V
     7: astore_1
     8: aload_1
     9: iconst_0
    10: invokestatic java/lang/Integer.valueOf:(I)Ljava/lang/Integer;
    13: invokevirtual java/util/ArrayList.add:(Ljava/lang/Object;)Z
    16: pop
    17: aload_1
    18: iconst_0
    19: invokevirtual java/util/ArrayList.get:(I)Ljava/lang/Object;
    22: checkcast java/lang/Integer
    25: invokevirtual java/lang/Integer.intValue:()I
    28: istore_2
    29: iload_2
    30: ireturn
```

当向泛型参数为Integer的ArrayList添加int值时，便需要用到自动装箱了。在上面字节码偏移量为10的指令中，我们调用了Integer.valueOf方法，将int类型的值转换为Integer类型，再存储至容器类中。
<div><strong>精选留言（20）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（61） 💬（1）<div>本节还是比较容易理解的，也搞清楚了泛型相关的疑惑点，非常感谢。
小结如下：
1:Java语法糖-是一种帮助开发人员提高开发效率的小甜点，原理是将一些繁琐的事情交给编译器来处理，开发人员少做一些事情，当然，本纸上这些事情还必须要做，只是有编译器来做了

2:Java语法糖有那几种呢？如下所示：
2-1:包装类型和基本类型间的转换，自动装箱和拆箱的设计
2-2:泛型的设计
2-3:变长参数的设计
2-4:try-with-resources，关闭资源的设计
2-5:在同一个catch代码块中捕获多种异常
2-6:finally代码块总是被执行的设计
2-7:foreach循环数组的设计
2-8:foreach循环Iterable对象的设计

3:编译器的具体实现细节不是很清楚，猜测是识别出对应的语法然后填充上对应的代码，将语法糖还原成其本质-一些重复繁琐的代码块

4:之前有同事问我泛型是怎么实现的？
我讲不出来，只晓得使用泛型后，不需要写类型强转的代码了，如果类型不对也会有提示且编译失败，现在知道的多一点了，本质上类型强转的工作还是必须要做的，只是不是有开发人员来做了，由编译器来做，并且编译器会擦除掉对应的泛型信息，使用合适的父类型来代替，可能是Object类也可能是声明泛型时指定的继承的类</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9a/01/1489f98d.jpg" width="30px"><span>^_^</span> 👍（9） 💬（3）<div>C++ 是真泛型，java 较之算是伪泛型</div>2018-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/9a/68/92caeed6.jpg" width="30px"><span>Shine</span> 👍（6） 💬（1）<div>每次看到示例代码的java字节码就犯懵，觉得很复杂，是不是有必要去了解下字节码</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d8/d6/47da34bf.jpg" width="30px"><span>任鹏斌</span> 👍（2） 💬（1）<div>有点落后刚升级到jdk8对10还一无所知</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/d4/f3/129d6dfe.jpg" width="30px"><span>李二木</span> 👍（2） 💬（2）<div>从实现上说可以设计一个int类型的list，而jdk中arrayList是object类型，这样做是不是为了通用型考虑呢？</div>2018-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/49/8b/3596a3e2.jpg" width="30px"><span>403</span> 👍（0） 💬（1）<div>相比来看，c#的泛型是真泛型</div>2018-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/bf/b6/ee3b4ef7.jpg" width="30px"><span>herome</span> 👍（0） 💬（1）<div>求老师画图啊 </div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/67/f4/9a1feb59.jpg" width="30px"><span>钱</span> 👍（0） 💬（1）<div>奇怪的是，Java 并不支持对 IntegerCache.low 的更改，也就是说，对于小于 -128 的整数，我们无法直接使用由 Java 核心类库所缓存的 Integer 对象。
这个奇怪的现象到底是为啥呢？</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/15/81/2c31cf79.jpg" width="30px"><span>永烁星光</span> 👍（18） 💬（0）<div>直到这节课逐渐感知到了学习jvm的妙处，我想将这专栏反复看和实践终能消化为自己的知识</div>2018-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/f8/db/c4edf697.jpg" width="30px"><span>曲东方</span> 👍（5） 💬（1）<div>var保存了泛型信息

var定义变量必须直接初始化，基于初始化的值做类型推导，javac编译期间的语法糖

所以不能声明函数的参数为var类型


foreach语法糖，对于实现了迭代器Iterable&lt;T&gt;接口的类型，使用迭代器方法；
foreach对于数组和变长参数的处理方式与上述略有不同，先求数组长度，再做类似while循环遍历
</div>2018-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e9/0b/1171ac71.jpg" width="30px"><span>WL</span> 👍（3） 💬（3）<div>invokestatic Double.valueOf:(D)Ljava&#47;lang&#47;Double;
想请教一下老师这个字节码中的(D)和java前的L的作用是标记什么, 查了半天都没查到, 希望老师回答一下.</div>2018-12-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/cc/de/e28c01e1.jpg" width="30px"><span>剑八</span> 👍（2） 💬（0）<div>java设计也是分内核与外延的设计
内核是整个加载器，执行器，编绎器，堆栈这些是相对稳定的
而语法糖是为了提升开发效率，相当于是多变的外延。
本质上这个语法糖是由编绎器帮开发人员做了转换的工作。
泛型在编绎器转换后会变成字节码层页的object，或者如果泛型有继承某个特定父类则在字节码层面就是这个限定类，最终在存取的时候会做强制转换。</div>2020-06-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（1） 💬（0）<div>看老师的课，最好就在电脑边，边看边实践。</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c0/6c/29be1864.jpg" width="30px"><span>随心而至</span> 👍（1） 💬（0）<div>赞，这节课的内容即便全忘了，也完全可以自己跑自己命令，看下字节码文件，知道到底是怎么回事。这就是授人以渔，谢谢老师。</div>2019-10-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/4c/86/3be94807.jpg" width="30px"><span>angel😇txy🤓</span> 👍（0） 💬（0）<div>ava 程序中的泛型信息会被擦除。具体来说，Java 编译器将选取该泛型所能指代的所有类中层次最高的那个，作为替换泛型的具体类，具体来说：
若泛型类型没有指定具体类型，用Object作为原始类型；
若有限定类型&lt; T exnteds XClass &gt;，使用XClass作为原始类型；
若有多个限定&lt; T exnteds XClass1 &amp; XClass2 &gt;，使用第一个边界类型XClass1作为原始类型；</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/26/54f2c164.jpg" width="30px"><span>靠人品去赢</span> 👍（0） 💬（1）<div>var应该是保留了泛型，支不支持自动不太确定，但是那个后面的代码add添加的操作是不行的。</div>2020-07-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/55/f2/ba68d931.jpg" width="30px"><span>有米</span> 👍（0） 💬（1）<div>感觉java越来越不严谨了。。。还是喜欢 int i=0; 不要来var i=0;。。。。。</div>2020-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/43/79/18073134.jpg" width="30px"><span>test</span> 👍（0） 💬（0）<div>课后题可以编译成功，看了下字节码，var声明的list，add的入参是Object。</div>2020-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/6e/8e/5d309a85.jpg" width="30px"><span>拯救地球好累</span> 👍（0） 💬（0）<div>大部分语法糖其实都是编译器为我们提供了一些便利，这些代码在编译后会变成一些基础代码
自动拆装箱：编译器会插入诸如Integer.valueof方法
泛型：编译器会根据继承关系做类型擦除</div>2019-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/4f/b8/35cdada6.jpg" width="30px"><span>Zhgdbut</span> 👍（0） 💬（7）<div>老师你好，我遇到了一个这种问题
Long a = null;
Long rs = 1=1 ? a: 0L;
报了空指针异常的错误，1=1只是一个条件，表明rs一定等于a!
请问是咋回事呀？我该怎么修改？</div>2019-05-22</li><br/>
</ul>