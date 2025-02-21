你好，我是尹会生。今天是咱们的第一节课，我先带你学习下，如何用Python操作Excel。

Excel是我们在工作中用到的最频繁的软件之一，它有着强大的计算能力和便捷的图表功能。如果我们要在同一个Excel文件中进行操作，手工进行也很方便，但问题是，如果我们需要同时操作多个Excel文件，就是一件非常耗时的事情了。

在工作场景中，需要同时操作多个Excel的情况主要有2种：批量合并和批量拆分。我来带你看2个场景。

- 批量合并。假设你需要对某些工作内容进行问卷调查，这时你用Excel做了调查问卷模版。我想你会这样做：先把Excel通过工作群分发给所有员工，再把群里收集到的反馈附件汇总成一个文件。
- 批量拆分。假设你是公司的财务人员，你需要使用Excel对员工工资进行核算，之后再打印出来。但是公司要求员工薪水保密，所以每个员工的工资需要拆分成一个独立的文件，最后还需要打印出来。

无论是合并，还是拆分，我们都面临着一个困境：没有现成的软件可以实现多个Excel文件的合并和拆分操作，所以你只好对每一个Excel文件都进行“打开-复制粘贴-保存”的工作。

很多人在面对这样的工作需求时，都**忍不住立马去做，却很少停下来分析问题**。其实，这三步是很简单的工作，不过也是无意义的重复工作，既浪费了时间，又没有真正产生价值。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（0） 💬（0）<div>编辑小提示：专栏的完整代码位置是https:&#47;&#47;github.com&#47;wilsonyin123&#47;python_productivity，可点击链接下载查看。

或者通过网盘链接提取后下载，链接是: https:&#47;&#47;pan.baidu.com&#47;s&#47;1UvEKDCGnU6yb0a7gHLSE4Q?pwd=5wf1，提取码: 5wf1。</div>2022-03-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/58/28/c86340ca.jpg" width="30px"><span>达文西</span> 👍（14） 💬（1）<div>上周刚碰到类似的需求,客户发过来的excle跟系统要求的模板跟数据格式都不对应,上万条数据,手动改肯定是搞不来了.就自己摸索着一天用python处理了一下做适配.不得不说python确实简单好学,很适合处理这些简单重复的业务场景.</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/2c/c8/7f32200e.jpg" width="30px"><span>李京斌</span> 👍（10） 💬（3）<div>能否共享讲课中提到的文件（EXCEL文件等）。</div>2021-02-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/82/e4/c456fa79.jpg" width="30px"><span>旧草</span> 👍（10） 💬（2）<div>例子保存的excel是xlsx，而官方文档写着：
xlwt is a library for writing data and formatting information to older Excel files (ie: .xls) by https:&#47;&#47;xlwt.readthedocs.io&#47;en&#47;latest&#47;</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/51/07/b5a945b6.jpg" width="30px"><span>Nick</span> 👍（9） 💬（2）<div>老师，我现在正好也碰到类似这样合并Excel文件的业务场景。大概有几十个拆分的Excel文件，要合并导入到数据库中，按照今天课程的思路，将所有的数据合并到一个Excel文件中来处理，但现在的问题是数据量比较大，超过了千万条记录。已经超出了Excel的最大范围，请问这种情况该怎么处理？我自己目前想到的是通过循环读所有的Excel文件，将数据一条条的插入到数据库中，请问老师还有什么高见？</div>2021-02-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/87/0f/9876789d.jpg" width="30px"><span>唐超伟</span> 👍（8） 💬（6）<div>2.01版本的xlrd不支持xlsx文件，只支持xls文件
亲测装旧版本的可用
 pip install xlrd==1.2.0</div>2021-03-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/04/60/64d166b6.jpg" width="30px"><span>Fan</span> 👍（8） 💬（3）<div>哈哈哈，这个主题讲得好，比爬虫，Django 那些内容实用多了。</div>2021-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/5b/bc/2cc1cc02.jpg" width="30px"><span>陈芳</span> 👍（6） 💬（1）<div>像我这样情况的，是不是应该学习【零基础学Python】，而不是这个课程。感觉十分吃力，连怎么开门都不知道</div>2021-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c8/16/619765bf.jpg" width="30px"><span>比国王</span> 👍（3） 💬（1）<div>老师，只论报表的拆分和合并，Python比VBA强在哪些方面？因为打开Excel就可以写VBA，非常方便，但如果知道Python比VBA更好的话，就可以说服自己学习Python而放弃使用VBA了。</div>2021-12-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eoQG9QxO3VicX7YnLGxd33v0dAOxBlQmankC6hdSmTLdIw0HNnAjqNl75mnMyTibQj63o4F10wnSH7A/132" width="30px"><span>巩春雨</span> 👍（3） 💬（2）<div>老师，您讲的都是对于一些简单格式的excel数据有效。实际工作中财务的一些表格都是包含大量的格式，如合并单元格，涂色，隐藏，筛选及单元格内存在大量的公式。如果我把10个文件合并到一个文件中的不同sheet，如何能把相应的格式及公式快速的复制过去</div>2021-02-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/47/e4/17cb3df1.jpg" width="30px"><span>BBQ</span> 👍（3） 💬（1）<div>老婆总是让我批量处理文件，上次学用 PowerShell 写了一个小程序，非常难写。用Python 简单多了。 </div>2021-02-05</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLShOEsneaMR6ysiaDaxdsvUPB24iaVOSyEblwmsqia2N0u5XCnC8YeLAtrBkxX8wbocTxFe1gfILuqg/132" width="30px"><span>老李书店</span> 👍（2） 💬（2）<div>请问下有案例文件吗</div>2021-04-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/81/df/066ffab3.jpg" width="30px"><span>落曦</span> 👍（2） 💬（2）<div>老师您好，我试了一下您的代码，第一个有问题，运行出错：
Traceback (most recent call last):
  File &quot;D:&#47;pycharmproject&#47;Exceldemo.py&quot;, line 10, in &lt;module&gt;
    value = table.cell_value(rowx=4, colx=4)
  File &quot;D:\pycharmproject\venv\lib\site-packages\xlrd\sheet.py&quot;, line 420, in cell_value
    return self._cell_values[rowx][colx]
IndexError: list index out of range

后来当我调试您github上的代码时，没有错误，然后根据留言区@旧草的提示，打开了您工资单.xlsx的文件，发现命名错误，于是我重命名为工资单.xls后来就能直接在excel上读取内容了。

所以我意识到xlrd 只适用于xls文件，老师您的电脑是mac，我用的windows可能是系统的不同吗？
python 3.7.0
xlrd 1.2.0
xlwt 1.3.0
pip  21.0.1
</div>2021-02-07</li><br/><li><img src="" width="30px"><span>刘春富</span> 👍（1） 💬（1）<div># 调用自定义函数write_to_file()写入新的文件 
write_to_file(filename = content[1], cnt = new_content)

这个write_to_file()函数的代码是怎样的？谢谢</div>2022-01-11</li><br/><li><img src="" width="30px"><span>Geek_39bcb2</span> 👍（1） 💬（1）<div>初学者，老师帮忙解答一下找个是怎么回事
H:\PycharmProjects\pythonProject1\venv\Scripts\python.exe H:&#47;PycharmProjects&#47;pythonProject1&#47;main.py
  File &quot;H:\PycharmProjects\pythonProject1\main.py&quot;, line 2
    pip3 install xlrd
         ^
SyntaxError: invalid syntax

Process finished with exit code 1

</div>2021-12-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7c/01/f1b8ba78.jpg" width="30px"><span>巩会杰</span> 👍（1） 💬（1）<div>卸载旧版本包出现错误：

C:\Users\Administrator&gt;pip uninstall xlrd
Traceback (most recent call last):
  File &quot;D:\Program Files\Python310\lib\runpy.py&quot;, line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File &quot;D:\Program Files\Python310\lib\runpy.py&quot;, line 86, in _run_code
    exec(code, run_globals)
  File &quot;D:\Program Files\Python310\Scripts\pip.exe\__main__.py&quot;, line 4, in &lt;module&gt;
ModuleNotFoundError: No module named &#39;pip&#39;

开始就错误不知道怎么学习了，求老师解答下，这个有学习群吗？</div>2021-11-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7c/01/f1b8ba78.jpg" width="30px"><span>巩会杰</span> 👍（1） 💬（1）<div>报错--xlrd.biffh.XLRDError: Excel xlsx file; not supported
老师最后一行代码 table.cell_value。为什么输入table.后没有自动提示其他的属性？？

代码如下：
import xlrd

file = &#39;D:&#47;py-test&#47;AAA.xlsx&#39;
data = xlrd.open_workbook(file)
table = data.sheets()[0]
value = table.cell_value(rowx=4,colx=4)</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/b6/17/4212a3ca.jpg" width="30px"><span>Nichkhun</span> 👍（1） 💬（2）<div>老师，有课程里用到的文件吗？</div>2021-05-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/30/712491d6.jpg" width="30px"><span>湘</span> 👍（1） 💬（1）<div>老师，我从github上下载您的代码是乱码，请问我这边需要做什么操作才能看到代码呢？谢谢。</div>2021-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/38/fe/be/5cb1ddca.jpg" width="30px"><span>小行迹</span> 👍（0） 💬（1）<div>在读取xlsx文件的时候报错：BadZipFile: File is not a zip file. 请问是excel文件格式损坏了吗
</div>2024-09-05</li><br/><li><img src="" width="30px"><span>Geek_2f3cf7</span> 👍（0） 💬（1）<div>老师，我很喜欢您用案例讲课的思路，但我作为一个小白，对于代码处于半看明白半不明白的状态。灵活运用现在肯定不太可能，照着思路写我都觉得有点困难。是否有一些扩展资料需要我们再看看呢？另外，我下载了课件，发现result中的文件也显示不出来是为什么呢？</div>2023-05-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/d6/83/bd4a8410.jpg" width="30px"><span>白开水</span> 👍（0） 💬（1）<div>windows的电脑下载链接中的课件遇到乱码问题，文件名乱码，execl打不开，只有程序可以打开。</div>2023-04-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/d3/99/e488fbac.jpg" width="30px"><span>薇薇的肉肉</span> 👍（0） 💬（1）<div>只有汉字，没有视频讲解吗
</div>2022-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/51/6e/5309b6e2.jpg" width="30px"><span>魏建鸿</span> 👍（0） 💬（1）<div>老师好，百度网盘下载的实战课资料名称是乱码，另外，每课的excel表格下载链接不能用，怎么办？</div>2022-06-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/03/e2/5768d26e.jpg" width="30px"><span>inrtyx</span> 👍（0） 💬（1）<div>为了学习必须买个mac啊</div>2022-02-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/84/2a7ff72d.jpg" width="30px"><span>Alizee</span> 👍（0） 💬（1）<div>
您好老师，之前买的课程现在开始学习，但是GitHub里链接的文章代码无法下载，请老师指导原因，谢谢老师。Safari 不能连接到服务器
Safari 打不开页面
&quot;https:&#47;&#47;raw.githubusercontent.com&#47;wilsonyin123&#47;python_productivity&#47;main&#47;文章1代
码.zip”，因为无法连接到服务器
“raw.githubusercontent.com”</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5c/84/2a7ff72d.jpg" width="30px"><span>Alizee</span> 👍（0） 💬（1）<div>老师，您好，之前买的课程现在开始学习，但是GitHud网站的文章代码无法下载，请老师知道原因，谢谢老师。以下是网站显示的内容：
无法访问此网站
网tN hetps:raw.githubusercontent.com&#47;vilsonyin123&#47;pythonproductivity&#47;main&#47;文章
1代码,z1p 的网 可能暂时无法连接，或者已已永久性地移动到了新网址</div>2021-12-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/7c/01/f1b8ba78.jpg" width="30px"><span>巩会杰</span> 👍（0） 💬（1）<div>读取表格时候报错提示：xlrd.biffh.XLRDError: Excel xlsx file; not supported

代码如下：

import xlrd
file=&#39;D:&#47;py-test&#47;AAA.xlsx&#39;
data=xlrd.open_workbook(file)
table=xlrd.sheet()[0]
value=table.cell_value(rowx=4,colx=4)</div>2021-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/27/1c/1e/b5d76759.jpg" width="30px"><span>，，，</span> 👍（0） 💬（1）<div>xlrd不支持打开.xlsx文件?</div>2021-07-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/kQx90MH3kCpNVFiaZWRHicQGBEE4ntt75evcwibTPH9z89ic1zqgBmMUj9HSh5C7PsqskU87cPOsgBmJ0ZucO3VNdA/132" width="30px"><span>小卢</span> 👍（0） 💬（3）<div>老师好，请教下如果一个大文件夹里面有许多子文件夹，子文件夹里分别还有许多文件，如果想提取里面的文件名，这个是属于爬虫范畴还是办公自动化呢</div>2021-07-22</li><br/>
</ul>