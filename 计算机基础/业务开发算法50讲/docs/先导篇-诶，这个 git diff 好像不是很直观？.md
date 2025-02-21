你好，我是微扰君。

相信你每天都会使用Git，作为一款免费、开源的分布式版本控制系统，Git最初是 Linus Torvalds 为了帮助管理 Linux 内核开源协作而开发的，随着GitHub的流行和Git本身的系统优势，它也渐渐成为我们广大研发人员日常工作中必不可少的版本管理利器。

在使用Git的过程中，你一定会常常用到 git diff 的命令，去查看这次待提交的本地代码和修改前的代码有什么区别，确定没有问题才会进行 commit 操作。像 git diff 这样求解两段文本差异的问题，我们一般称为“文本差分”问题。

但是不知道你有没有思考过文本差分的算法是怎么实现的呢？

如果你现在静下心来思考一下，就会发现**写出一个简明的文本差分算法并不是一件非常容易的事情**。因为代码的文本差分展现形式可能有很多，但并不一定都有非常好的可读性。

而 git diff 给我们展示的，恰恰是比较符合人们阅读习惯且简明的方式，简明到让我们即使天天都在使用这个功能也不会有意识地去思考：“诶，这个difference生成的好像不是很清晰？是怎么做的呢？”。

就让我们从这样一个“简单”、有趣、常用的文本差分算法开始，探索那些其实就在我们身边却常常被熟视无睹的算法们吧。希望能给你一些启发，而且探索算法思想的过程也会非常有趣（如果你在学习这一讲的过程中觉得有点难，最后我们会揭秘原因）。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/a4/d7/5d2bfaa7.jpg" width="30px"><span>Aliliin</span> 👍（12） 💬（4）<div>逐渐听不懂系列...😂</div>2021-12-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/a8/b2/5acb4806.jpg" width="30px"><span>Daneil</span> 👍（7） 💬（1）<div>状态方程应该是dp[d][k] = max(dp[d-1][k-1]+1， dp[d-1][k+1])</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/97/25/8c35cc85.jpg" width="30px"><span>天上星多月不亮</span> 👍（4） 💬（4）<div>请问下 m+n-2*LC 是如何推的呢</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/90/b1/fcc9e6df.jpg" width="30px"><span>萧戏</span> 👍（2） 💬（1）<div>第一课没有听明白，还是适合吗？</div>2022-06-17</li><br/><li><img src="" width="30px"><span>时间小偷</span> 👍（2） 💬（1）<div>最长公共子序列我只会O(mn)时间复杂度的动态规划解法，O(n*logn)时间复杂度是怎么解的？</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/40/72/2d97df54.jpg" width="30px"><span>随风</span> 👍（2） 💬（1）<div>没有明白，对应的k-lines的行号指的是什么意思</div>2021-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erAhtlpeFFwRk5g5LvzLcZgybImECIdKmhG1aPxdbnqWP6LmeNz5ibYibOedUwF7NjTy1asZqUur5uQ/132" width="30px"><span>kenan</span> 👍（2） 💬（2）<div>老师，看目录没有维特比算法，可否加餐一下呢？</div>2021-12-09</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/rvQxUmekECjyZu1RwbUguBWpBcQuKywQPtiaxNVFJSib07QMZnNUr8MnRF3RYEsn6MhgGFJibwlrVomibEicYMiaia7ZQ/132" width="30px"><span>Geek_a8ce05</span> 👍（1） 💬（1）<div>第二节直接劝退</div>2022-04-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/49/0a6be1bc.jpg" width="30px"><span>大飞</span> 👍（1） 💬（1）<div>略难，学完之后能搞懂不</div>2022-03-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKotsBr2icbYNYlRSlicGUD1H7lulSTQUAiclsEz9gnG5kCW9qeDwdYtlRMXic3V6sj9UrfKLPJnQojag/132" width="30px"><span>ppd0705</span> 👍（1） 💬（1）<div>伪代码翻译成Python的版本如下，请大家斧正 ：
```python
def git_diff(a: str, b: str) -&gt; int:
    a = &quot; &quot; + a
    b = &quot; &quot; + b
    v = {0: 0}
    d = 0
    break_out = False
    while True:
        d += 1
        for k in range(-d, d + 1, 2):
            if k == -d:
                x = v[k + 1]
            elif k == d:
                x = v[k - 1] + 1
            else:
                if k + 1 not in v:
                    x = v[k - 1] + 1
                else:
                    x = max(v[k + 1], v[k - 1] + 1)
            y = x - k
            while x &lt; len(a) - 1 and y &lt; len(b) - 1 and a[x + 1] == b[y + 1]:
                x += 1
                y += 1
            v[k] = x
            if x &gt;= len(a) - 1 and y &gt;= len(b) - 1:
                break_out = True
                break
        v = {k: x for k, x in v.items() if (k + d) % 2 == 0}
        if break_out:
            break
    return d
```
</div>2022-03-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/6LaITPQ4Lk5fZn8ib1tfsPW8vI9icTuSwAddiajVfibPDiaDvMU2br6ZT7K0LWCKibSQuicT7sIEVmY4K7ibXY0T7UQEiag/132" width="30px"><span>尔东橙</span> 👍（1） 💬（1）<div>仿佛回到读研时文章算法推导的时候。。</div>2022-03-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（1） 💬（1）<div>这篇导读真的很有深度，老师太棒了！</div>2022-01-04</li><br/><li><img src="" width="30px"><span>Geek_62b378</span> 👍（1） 💬（1）<div>把之前的递推例子过程画到二维表格中大概如下图所示，横轴的数字代表着 D-Path 的 D 也就是操作数，纵轴的数字代表 k-Lines 的行号
这里的纵轴的数字代表k-Lines的行号
这里的行号是不是说的是k-Lines中的k</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/f4/c7/037235c9.jpg" width="30px"><span>kimoti</span> 👍（1） 💬（1）<div>看起来还是很困难</div>2021-12-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/e7/8e/ef2e91f3.jpg" width="30px"><span>疯帽子</span> 👍（0） 💬（1）<div>老师,这一篇看不懂,可以跳过不看吗😳</div>2022-09-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8f/9f/e49b68ea.jpg" width="30px"><span>幽弥狂</span> 👍（0） 💬（1）<div>第一章就这么硬？？？</div>2022-08-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/98/ad/f9d755f2.jpg" width="30px"><span>邓嘉文</span> 👍（0） 💬（1）<div>直接听不懂了</div>2022-07-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/06/1f/9537d8cb.jpg" width="30px"><span>打不过就跑</span> 👍（0） 💬（1）<div>讲的很不错，不过这章的算法相对较难，如果能有完整的能跑起来的代码会更好，个人觉得一般人都学过一些编程语言，使用任意一种完善的编程语言比使用伪代码要更好理解。</div>2022-02-03</li><br/><li><img src="" width="30px"><span>jntv</span> 👍（0） 💬（2）<div>（4,0）点为什么在D=2这条线上？通过2步增或删到不了这个点呀</div>2021-12-24</li><br/><li><img src="" width="30px"><span>jntv</span> 👍（0） 💬（2）<div>D=2这条线怎么理解？</div>2021-12-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/e0/26/4942a09e.jpg" width="30px"><span>猫头鹰爱拿铁</span> 👍（0） 💬（1）<div>老师，你的代码是什么语言写的？前面还能看明白，到了代码实现部分，就觉得难度马上上升了。主要是要递推的那个图比较难理解。实现部分横轴和纵轴正好和递推图的轴是反的，估计不理解的都是卡在k这。</div>2021-12-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/50/2b/2344cdaa.jpg" width="30px"><span>第一装甲集群司令克莱斯特</span> 👍（0） 💬（2）<div>我不藏拙，这篇，我没看明白，我很菜，当头一棒，差点被劝退！</div>2021-12-16</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIL1K9WKIkvsdicFYrgiaUYLucECQMpZyEhl6L6LE5324BlDCEhJmyticcHwN8c37icQOC7q78VoKFdNQ/132" width="30px"><span>Geek_7bed70</span> 👍（0） 💬（1）<div>老师，有一个问题，状态压缩成单维数组，内循环的时候会更新vk的值，这时候后面用到的就不是d-1时候的值了，而是d的值，这样会不会有问题</div>2021-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/75/dd/9ead6e69.jpg" width="30px"><span>黄海峰</span> 👍（1） 💬（0）<div>确实需要死磕，不懂的地方琢磨到懂为止。。。不能寄希望于读完后面这里就懂了</div>2023-02-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/2d/e4/728b3f4a.jpg" width="30px"><span>聪聪</span> 👍（1） 💬（0）<div>看大家都说没看懂我就放心了
</div>2022-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/97/23446114.jpg" width="30px"><span>火云邪神霸绝天下</span> 👍（0） 💬（0）<div>能做一个动图就好了</div>2024-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/31/21/41/d8f2fe6d.jpg" width="30px"><span>阴晦</span> 👍（0） 💬（0）<div>抱着巩固一下 树之类的数据结构的想法打开第一节课，然后被DP来了狠狠一击</div>2024-08-08</li><br/><li><img src="" width="30px"><span>Geek_12e8fd</span> 👍（0） 💬（0）<div>四大算法统一于dga
</div>2024-06-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/95/af/b7f8dc43.jpg" width="30px"><span>拓山</span> 👍（0） 💬（0）<div>整体上我看明白了，但是该文的上下文里有三个地方讲的不严谨：
1、【Myers 采取的是一种贪心的策略】这里说的是贪心策略，但代码思路里用的却是动态规划，这俩算法思路压根不是一回事，应该是笔误。
2、【我们很容易发现最短的编辑脚本的长度就等于 m + n - 2 * LC】这里没有给出推导步骤，写的不严谨。 不过在评论中给出了。
3、 动态规划推导公式是有问题的，按照你的理论dp[d][k]描述的是最大横向坐标，那么如果从横向移动，那么应该是dp[d-1][k] +1 ，而非dp[d-1][k-1]+1。如果从竖行移动，那么应该是dp[d-1][k-1] 而非什么dp[d-1][k+1]。所以这个公式应该是 p[d][k] = max(dp[d-1][k]+1，dp[d-1][k-1])</div>2023-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/45/b9/3db96ade.jpg" width="30px"><span>锅菌鱼</span> 👍（0） 💬（0）<div>关于d+2，“整个树的结构是二叉的，奇数步时，必然处于奇数行号，偶数步时必然处于偶数行号”，有点难理解</div>2022-10-19</li><br/>
</ul>