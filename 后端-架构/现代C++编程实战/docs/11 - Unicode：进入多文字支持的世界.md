你好，我是吴咏炜。

这一讲我们来讲一个新话题，Unicode。我们会从编码的历史谈起，讨论编程中对中文和多语言的支持，然后重点看一下 C++ 中应该如何处理这些问题。

## 一些历史

ASCII \[1] 是一种创立于 1963 年的 7 位编码，用 0 到 127 之间的数值来代表最常用的字符，包含了控制字符（很多在今天已不再使用）、数字、大小写拉丁字母、空格和基本标点。它在编码上具有简单性，字母和数字的编码位置非常容易记忆（相比之下，设计 EBCDIC \[2] 的人感觉是脑子进了水，哦不，进了穿孔卡片了；难怪它和 IBM 的那些过时老古董一起已经几乎被人遗忘）。时至今日，ASCII 可以看作是字符编码的基础，主要的编码方式都保持着与 ASCII 的兼容性。

![](https://static001.geekbang.org/resource/image/cc/35/cc7fb695569c7ea460c1b89fc7859735.gif?wh=715%2A488)

ASCII 里只有基本的拉丁字母，它既没有带变音符的拉丁字母（如 é 和 ä ），也不支持像希腊字母（如 α、β、γ）、西里尔字母（如 Пушкин）这样的其他欧洲文字（也难怪，毕竟它是 American Standard Code for Information Interchange）。很多其他编码方式纷纷应运而生，包括 ISO 646 系列、ISO/IEC 8859 系列等等；大部分编码方式都是头 128 个字符与 ASCII 兼容，后 128 个字符是自己的扩展，总共最多是 256 个字符。每次只有一套方式可以生效，称之为一个代码页（code page）。这种做法，只能适用于文字相近、且字符数不多的国家。比如，下图表示了 ISO-8859-1（也称作 Latin-1）和后面的 Windows 扩展代码页 1252（下图中绿框部分为 Windows 的扩展），就只能适用于西欧国家。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/97/75/7f76341b.jpg" width="30px"><span>c1rew</span> 👍（39） 💬（4）<div>http:&#47;&#47;c1rew.github.io&#47;2017&#47;03&#47;02&#47;字符集和字符编码&#47;
很早之前写的一篇文章，供大家参考</div>2020-02-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/33/a2/6c0ffc15.jpg" width="30px"><span>皮皮侠</span> 👍（4） 💬（5）<div>问个题外问题，Qt里中文的处理总是有问题，老师怎么看，有什么终极解决办法呢？</div>2020-02-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f3/cf/851dab01.jpg" width="30px"><span>Milittle</span> 👍（2） 💬（1）<div>1.  有一个问题想问下老师，传统编码是不是相对于UTF编码之外的那些编码方式。
2. 再就是对于我们编程中使用的不同编码方式的字面量来说，最后生成的字节数对应是不同的么？是这个意思么？
3. 还有就是u8string u16string u32string 默认是一个元素所占的字节数分辨是 1 2 4么？
4. 老师文章中提出一个UTF-16在0XD800-0XDFFF之间没有用作unicode code point。这是历史原因决定么 然后就是怎么可以找到unicode code point所对应的文字关系表？ 从UTF-32转UTF-8和UTF-16老师给出例子，这个可以当作一个算法来记忆。
5. 就是操作系统的编码方式是最终决定你的字符串显示在终端的样子么？我举一个例子，加入你程序中一个字符串是UTF-8，但是你的操作系统使用的是GBK，那么显示出来的样子应该会乱码吧？ 我的理解也就是程序什么编码方式，操作系统也应该是什么编码方式，才能输出正确的文字？
以上问题有些可能是我没有理解对 王老师给予指导 谢谢～</div>2020-02-26</li><br/><li><img src="" width="30px"><span>勿更改任何信息</span> 👍（1） 💬（2）<div>由于 Unicode 不使用 U+FFFE --&gt; 应该是不使用 U+FEFF 吧</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/42/de/9db45d7d.jpg" width="30px"><span>天天</span> 👍（1） 💬（1）<div>1. utf32字节数固定支持随机访问字符，其他2个则需要遍历前面的字节，经过计算才能解出第N个字符
3. 要看具体存储的是啥字符， 英文utf8省空间， 中文utf16</div>2020-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/c9/e3/28c16afa.jpg" width="30px"><span>三味</span> 👍（1） 💬（1）<div>这两天写玩具代码,  环境就是win10, vs2017, 写控制台. 我源代码是utf8无bom格式. 什么都好, 就是用fgets获取输入, 无法获取中文字符串... 折腾好久... 最后还是都改成了ansi... ansi这个诡异的名字确实值得吐槽啊...明明就是GBK... 字符编码真是太麻烦了...</div>2019-12-20</li><br/><li><img src="" width="30px"><span>Geek_0705cc</span> 👍（0） 💬（1）<div>大头在前、小头在前是什么意思呢？不如这样说的清楚。大端模式指的是：高位字节存储在内存的低地址处；</div>2023-01-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/2ibrq71Y5Ww3KDRibDxF1gt9YDEPuZkv4ITHEP1u4vvjpPDukkLoK4ngQy1hKKzccnsicLkUAda7sPpibR6Kyb0cfQ/132" width="30px"><span>chang</span> 👍（0） 💬（2）<div>文中“由于 Unicode 不使用 U+FFFE，在文件开头加一个 BOM 即可区分各种不同编码：”，应该是U+FEFF吧</div>2021-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/7a/38a27e47.jpg" width="30px"><span>蓦然回首</span> 👍（0） 💬（1）<div>上面这几种之间相互有影响吗？到底之间关系是如何？平时我们开发过程中，应该怎么理解这几者之间的关系？感觉这方面一直没弄清楚</div>2021-01-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/e2/7a/38a27e47.jpg" width="30px"><span>蓦然回首</span> 👍（0） 💬（4）<div>老师，请教个问题，我们平时开发，好像编码有几种方面的编码问题:
1.源码文件本身的编码，IDE或者编辑器设置的编码等
2.程序运行时刻当中程序本身的编码，
3.程序运行过程中所打开文件的编码
4.接收或者发送网络数据的不同编码
在编码方面一直这方面有些困惑，希望能解答一下！</div>2021-01-27</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/aFAYPyw7ywC1xE9h1qibnTBwtWn2ClJqlicy5cMomhZVaruMyqSq76wMkS279mUaGhrLGwWo9ZnW0WCWfmMovlXw/132" width="30px"><span>木瓜777</span> 👍（0） 💬（2）<div>你好，如果c++通过socket专递带 中文的字符串 到 web前端，请问是不是需要 转码啊？ 转码的话，是不是 从 utf8 到 gb2312？ 目前后端是linux系统</div>2020-09-23</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eqf54z1ZmqQY1kmJ6t1HAnrqMM3j6WKf0oDeVLhtnA2ZUKY6AX9MK6RjvcO8SiczXy3uU0IzBQ3tpw/132" width="30px"><span>Geek_68d3d2</span> 👍（0） 💬（1）<div>1 UTF-32是定长编码，而且能表示的字符比较多，所以处理起来比较容易且少了这种字符表示不了的尴尬局面。

2 UTF-32在需要转换成其他编码的时候可能比较麻烦，比如转成UTF-8还需要计算本字符实际占几个字节，还要更改前几个比特位

3 肯定是UTF-8空间利用率高啊</div>2020-04-19</li><br/><li><img src="https://wx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI9zRdkKuXMKh30ibeludlAsztmR4rD9iaiclPicOfIhbC4fWxGPz7iceb3o4hKx7qgX2dKwogYvT6VQ0g/132" width="30px"><span>Initiative Thinker</span> 👍（0） 💬（1）<div>老师问个问题，WIndows下命令行输出的是由ANSI编码还是UTF-16编码？
ANSI提出就是为了兼容非英文字符吗？
对老师的例子做了一些修改
#include &lt;fcntl.h&gt;
#include &lt;io.h&gt;
#include &lt;iostream&gt;

int main()
{
    &#47;*_setmode(_fileno(stdout),
        _O_WTEXT);*&#47;
    std::cout
        &lt;&lt; &quot;中文Español Français\n&quot;;
    std::cout
        &lt;&lt; &quot;Narrow characters are &quot;
        &quot;also OK on wcout\n&quot;;
    &#47;&#47; but not on cout...
}
输出法语部分直接是？，这个？的产生原因是由于窄字符输出无法识别造成的吗？</div>2020-04-18</li><br/><li><img src="" width="30px"><span>zKerry</span> 👍（0） 💬（1）<div>干货满满</div>2020-02-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/fc/b0/df0468c9.jpg" width="30px"><span>清风静婷</span> 👍（0） 💬（1）<div>问题2-不知是不是因为. UTF-32 如果有字节全部为0，转换成其他会认为是结束符</div>2020-02-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/29/c0/86fa3e92.jpg" width="30px"><span>贾陆华</span> 👍（0） 💬（2）<div>2. UTF-32不兼容ASCII编码，会导致处理之前的文件和系统接口都会转换一次，有些麻烦，这就是为什么采用兼容的UTF-8编码的原因之一</div>2020-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/6c/ea/e03fec22.jpg" width="30px"><span>泰伦卢</span> 👍（0） 💬（1）<div>唉，一直对这个字符编码不太感冒</div>2019-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/89/da/e86b9932.jpg" width="30px"><span>_呱太_</span> 👍（0） 💬（1）<div>老师好！能不能提前透露一下单元测试库是用的哪个库啊，最近在看 TDD，想上手一下，感觉现在最缺的也是测试方面的能力。</div>2019-12-21</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJnw8P84Wg1a8wcQL33folC4sI003oCUviau3OicHlnEEpvbNLFQVhaic2yeN7hPmrV06DjVPXmHU4vg/132" width="30px"><span>Geek_6baqph</span> 👍（0） 💬（3）<div>1.每个字符的字节数固定，可能需要判断的就是一个大小端的问题
2.有些表情符号(如emoji)，会使用两个字符来产生，增加了可见字符的判断
3.utf-8是最省空间的编码方式，每个编码只用到需要最少的字节数</div>2019-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/9c/b2/1a9beeb1.jpg" width="30px"><span>转遍世界</span> 👍（1） 💬（0）<div>把我头看大了</div>2023-12-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d0/e7/c4c6096f.jpg" width="30px"><span>晴朗</span> 👍（0） 💬（0）<div>找到一个对字符编码讲解很详细的系列文章
https:&#47;&#47;www.cnblogs.com&#47;benbenalin&#47;tag&#47;Unicode&#47;</div>2019-12-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/dc/4a/0f56e0ad.jpg" width="30px"><span>LiKui</span> 👍（0） 💬（0）<div>通过BOM判断文件编码方式：
如果文件开头是0x0000 FEFF,则是UTF-32 BE方式编码
如果文件开头是0xFFFE 0000,则是UTF-32 LE方式编码
如果文件开头是0xFFFE,则是UTF-16 LE的方式编码
如果文件开头是0xFEFF,则是UTF-16 BE的方式编码
如果文件开头是0xEF BB BF，则是UTF-8方式编码
否则编码方式使用其它算法确定
</div>2019-12-20</li><br/>
</ul>