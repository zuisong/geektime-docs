你好，我是尹会生。

在工作中，会遇到和Windows操作系统紧密结合又需要批量操作的工作需求，比如文件的批量重命名，还有按照扩展名搜索文件。那么今天这节课，我将给你介绍一个主要应用于Windows操作系统自动化的脚本--PowerShell。

你肯定会有疑问，为什么我们不用Python，而是要另外学习PowerShell脚本呢？原因就在于，遇到这类工作需求，PowerShell脚本会比Python功能更强大，使用更方便，学习起来也更容易。

首先，Windows的所有操作，都有对应的PowerShell操作，可以达到办公自动化的目标。而使用Python，会因为Windows没有提供接口，有些功能就不能完全实现，或者有些操作还需要手动执行。

其次，PowerShell的语法简洁，比Python更加友好，降低了你阅读代码的难度。这一点你在这节课我讲解的例子中会有更深刻的体会。

最后，PowerShell在Windows上能做到开箱即用，安装完成后就可以正常运行了。而Python还需要安装解释器和配置环境。比如在金融和证券领域中，基于公司的规定，你可能无法安装操作系统之外的软件，这时候PowerShell的优势就体现出来了。
<div><strong>精选留言（4）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/19/10/00/a9932fb1.jpg" width="30px"><span>小小明</span> 👍（1） 💬（1）<div>查到文档地址是：https:&#47;&#47;docs.microsoft.com&#47;zh-cn&#47;previous-versions&#47;powershell&#47;module&#47;microsoft.powershell.management&#47;remove-item?view=powershell-6

直接Remove-Item  *.txt就可以删除当前目录下的文本文件</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（1） 💬（1）<div>思考题：Remove-Item * -Include *.txt -Recurse，亲测有效。</div>2021-03-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/06/32/3de6a189.jpg" width="30px"><span>范</span> 👍（1） 💬（0）<div>powershell以前主要执行服务器端命令。内置很多命令，也可以调用各种命令。</div>2021-04-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-12</li><br/>
</ul>