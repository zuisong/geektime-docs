你好，我是尹会生。

打印，是办公中必不可少的一步，比如在会议上，我们需要通过Excel表格向客户/领导展示工作成果。

但在使用Python对Excel进行打印的时候，我们还得给Python安装上Excel、Windows和硬件设备管理的库，过程极其复杂，远远达不到我们自动化办公的需要。尤其是面对类似的临时性需求，就更没必要使用Python了。

庆幸的是，Excel自带了打印功能，而我们可以利用Excel的扩展——“宏”来实现打印，并且通过VBA脚本增强“宏”的功能，从而实现批量打印，满足我们自动化办公的要求。

那么在今天这节课，我就带着你学习Excel的另一个自动化功能：“宏”和VBA脚本。

### 宏和VBA脚本的用途

宏是Excel自带的扩展功能，可以记录的内容包括对Excel格式和文字的修改，它会像录像机一样记录下你在Excel中的操作。当你有一系列的动作需要多次执行，并且每次执行动作的顺序又完全相同，就可以重新播放，把这些操作自动再执行一遍。所以对于办公中临时性的需求，使用宏要比掌握每个Excel操作对应的Python函数要更简单。

你可以使用宏的录制功能，把格式调整、复制粘贴、打印等重复操作记录下来，并保存成一个**快捷键。**当你需要重复执行这条流水线作业时，就可以通过执行快捷键实现自动化操作。
<div><strong>精选留言（5）</strong></div><ul>
<li><img src="" width="30px"><span>zhb</span> 👍（0） 💬（1）<div>用老师介绍的sublime text2编写vba需要安装什么插件吗？</div>2021-03-29</li><br/><li><img src="" width="30px"><span>zhb</span> 👍（0） 💬（2）<div>老师，vba的编辑器能美化不？不能美化的话，有替代的好看点的编辑器吗？</div>2021-03-20</li><br/><li><img src="" width="30px"><span>zhb</span> 👍（0） 💬（1）<div>老师，今天有用了python的xlwings模块，它有一个api属性，我用的vscode怎么没办法智能提示，自动补全呢?</div>2021-03-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/ac/6383e8d3.jpg" width="30px"><span>Dr.Strangelove</span> 👍（2） 💬（0）<div>现在office和wps都支持js宏、js API了，这要比vba好用</div>2022-05-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-11</li><br/>
</ul>