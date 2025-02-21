你好，我是于航。

在上节课的最后，我举了一个简单的例子，来帮助你理解了 Wasm 二进制模块内部字节码的基本结构。在这短短的几十个十六进制数字中，我们看到了组成 Wasm 模块所不可或缺的“魔数”与“版本号”编码，以及组成了各个 Section 结构的专有编码。

在这些字节码中，Wasm 会使用不同的编码方案来处理不同的字段数据。比如对于 Section 的通用头部结构来说，Wasm 会用名为 “varuint7” 的编码方式，来编码各个 Section 的专有 ID。

除此之外，对于字符串以及浮点数，Wasm 也会分别通过 UTF-8 以及 IEEE-754 编码来将这些字面量值转换为对应的二进制编码，并存储到最终的 Wasm 二进制模块文件中。

那么本节课，我们就来一起看看 Wasm 所使用的这些数据编码方式，它们决定了 Wasm 在二进制层面的具体数据存储规则。

## 字节序

首先，作为字节码组成方式最为重要的一个特征，我们来聊一聊与具体编码方案无关的另外一个话题 —— 字节序。

那么什么是“字节序”呢？相信仅从字面上理解，你就能够略知一二。字节序也就是指“字节的排列顺序”。在计算机中，数据是以最原始的二进制 0 和 1 的方式被存储的。在大多数现代计算机体系架构中，计算机的最小可寻址数据为 8 位（bit)，即 1 个字节（byte）。
<div><strong>精选留言（8）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（8） 💬（1）<div>替换出 UTF-8 编码对应的三个字节。在替换时，你需要将从上一步获得的二进制序列中的各个二进制位，按照从左到右的顺序依次替换掉 UTF-8 编码中用于占位的 “x”
=======================
这一步是怎么替换的？ 没有看明白的

01100111 10000001 ---&gt; 11100110 10011110 10000001</div>2020-09-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/4f/6fb51ff1.jpg" width="30px"><span>奕</span> 👍（3） 💬（2）<div>为什么要有那么多编码方式呢？ 虽说每种编码方式都是针对的场景，但是还是没有个整体的概念。 要不老师来个加餐讲讲各种编码方式出现的历史背景和要解决的问提？ 期待</div>2020-09-16</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/PiajxSqBRaEJ4tXsamhbfSibStexd5mC7DBWFkwCFhRl55PmdY659j4ibgQmAdHjkfXYEmFRvKfALiacby7rQjuxsw/132" width="30px"><span>Geek_58a18e</span> 👍（2） 💬（1）<div>大学没学懂的知识 工作好几年后配上老师的教程 醍醐灌顶 感谢</div>2020-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d0/15/886f5c66.jpg" width="30px"><span>Twittytop</span> 👍（0） 💬（1）<div>”其左侧填充指定的二进制位来增加整个有符号数的总位数，并同时保证该二进制数本身的值不会被改变。“这句话中并同时保证该二进制数本身的值不会被改变是什么意思？是说左侧填充了符号位之后本身的值没改变？好像不对，还是左侧位填充1，其他的不变？
另外为什么要是7的倍数，是这个编码方式就是这么规定的吗？</div>2022-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/f7/e5/b290e605.jpg" width="30px"><span>AIGC Weekly 周报</span> 👍（0） 💬（2）<div>有符号数 “-654321” 在 varint32 类型下的可能编码值之一是：0x58、0x88、0x8f。
想请问一下老师，如果出现了占位的 0x80 或 0xff 应该怎么计算呢？有知道的小伙伴也可以说下，谢谢！
</div>2021-12-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/69/27/b6358f79.jpg" width="30px"><span>champ</span> 👍（5） 💬（1）<div>-654321

原码:
1 1001 1111 1011 1111 0001

反码:
1 0110 0000 0100 0000 1110

补码:
1 0110 0000 0100 0000 1111

符号扩展:(无需扩展)
1 0110 0000 0100 0000 1111

分组:
1011000 0001000 0001111

填充:
01011000 10001000 10001111

16进制表示:
0x58 0x88 0x8f</div>2021-01-17</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLIpicRcvnmGNAfxuiaFdzIjR2FecqU5IS6KAZ5MS57sGybHxcraxCoUqaERl3kF2JvfHPrAgTqs1cQ/132" width="30px"><span>vividlipi</span> 👍（2） 💬（0）<div>第一步:
-654321:第一个1表示符号位,补码表示是:101100000010000001111
第二步:
有符号拓展扩展到7的倍数: 1011000 0001000 0001111
第三步:
分组填充: 01011000 10001000 10001111
第四步:
0x58 0x88 0x8f</div>2020-10-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/d3/a3/52702576.jpg" width="30px"><span>becky</span> 👍（1） 💬（0）<div>除了0x58 0x88 0x8f，“-654321”是也可以将数字值扩展为32位后再编码吧，编码后是0x7f 0xff 0xd8 0x88 0x8f</div>2023-08-11</li><br/>
</ul>