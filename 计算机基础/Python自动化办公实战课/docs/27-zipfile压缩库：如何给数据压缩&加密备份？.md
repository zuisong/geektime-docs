你好，我是尹会生。

你在日常工作中，肯定和压缩文件打过交道，它们能把文件夹制作成一个体积更小的压缩文件，不仅方便数据备份，还方便作为邮件附件来传输，或者与他人共享。

但是如果你需要每天都进行数据备份，或者把压缩包作为每天工作的日报发送给领导，你肯定希望它能自动化的压缩。面对这个需求，我们同样可以通过python来解决。我们可以用Python来自动压缩文件夹，并为压缩包设置密码，保证备份数据的安全。

在Python中，要想实现数据的压缩，一般可以采用基于标准库zipfile的方式来实现，也可以采用命令行方式来实现。

当我们希望能够用Python自动压缩一个无需密码保护的文件夹时，可以通过zipfile来实现，它的好处是使用简单，而且不用安装任何的软件包，就能制作出“zip”格式的压缩包。不过zipfile没法对压缩文件进行加密，因此当你需要对压缩文件加密时，还需要调用可执行命令。

这两种实现方式就是我们今天要学习的重点了，接下来我们分别看一下这两种方式的具体操作方法。

## 使用zipfile实现无密码压缩

如果我想要把“C:\\data\\”文件夹压缩为“当前日期.zip”文件，就可以使用**目录遍历、按日期自动生成压缩包的文件名、把文件夹写入压缩文件这三个步骤来实现。**
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（2）<div>请问多个目录改怎么压缩?</div>2023-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b7/ab/75507dbf.jpg" width="30px"><span>碧海蓝天</span> 👍（0） 💬（1）<div>老师，请问一下我使用7z.exe a -tzip -ppwd666 C:\files 并没有压缩成功，这是为什么呢？</div>2021-07-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（0） 💬（1）<div>老师，请问为什么我用zipWithPassword()函数对文件夹进行压缩后，生成的压缩包还是没有密码的状态呢？</div>2021-04-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（0） 💬（1）<div>使用 yield 返回的对象被称作生成器对象，该对象没法像列表一样，一次性获得对象中的所有数据，你必须使用 for 循环迭代访问，才能依次获取数据。这句话怎么理解呢？调用一次getAllFiles是返回一个数据还是返回所有数据？</div>2021-04-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-24</li><br/>
</ul>