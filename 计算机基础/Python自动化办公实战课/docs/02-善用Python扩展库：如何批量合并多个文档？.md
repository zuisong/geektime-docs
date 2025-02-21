你好，我是尹会生。

在日常工作中，我们打交道最多的文件就要数Word和Excel了。我们经常面临这么一种场景：需要将Excel的内容合并到Word中。你可以想一想，完成这个需求，需要手动进行几个步骤的操作呢？很显然，有4步。

- 首先，要手动打开Excel、Word文件；
- 接着，复制一个单元格的文字到Word指定位置；
- 然后，如果有多个单元格，就需要重复复制多次；
- 最后，保存Word文件，并关闭Excel和Word文件。

如果只有两个文件，这几步手动操作一定不成问题，不会耗费太多的时间。但是如果文件特别多，哪怕只有十几个，手动操作就相当耗费时间了，而且一不小心还容易出错。幸运的是，现在我们可以通过Python来实现批量文件合并功能，你只需要执行一个Python程序就能搞定所有文件的合并操作。

所以今天这节课，我们先从比较简单的内容讲起：用Python自动合并两个Word文件。然后再进阶，学习如何合并Word和其他类型的文件。一步一步来，相信你会掌握得既牢固又扎实。

## 手工操作和用Python操作的区别

首先我们要知道，为什么在合并文件的时候用Python更高效。我用一个例子来给你讲解手工操作和用Python操作的区别。比如下面这一段文字：
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（0） 💬（0）<div>编辑小提示：专栏的完整代码位置是https:&#47;&#47;github.com&#47;wilsonyin123&#47;python_productivity，可点击链接下载查看。

或者通过网盘链接提取后下载，链接是: https:&#47;&#47;pan.baidu.com&#47;s&#47;1UvEKDCGnU6yb0a7gHLSE4Q?pwd=5wf1，提取码: 5wf1。</div>2022-03-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83ep5btvTnP5B4oLRUpgVolf6A48G8xYle6WXlYqhEJZjLmS7PNZPSibbiaibkWXqAqia536COibRH9VAXNg/132" width="30px"><span>周文玲</span> 👍（4） 💬（1）<div>老师，零基础学些这门课程感觉有些困难，一开始以为只是在excel里面去写函数就可以实现，听了您的课发现讲的挺详细的，但感觉自己不太能理解和应用，还是有点懵，如何有成效的学习这门课呢？</div>2021-09-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/56/60/fb5ca9e5.jpg" width="30px"><span>黄矢</span> 👍（4） 💬（1）<div>沿用老师的代码，生成docx文件，然后使用python拓展库将docx文件批量转pdf，最后将pdf批量转图片</div>2021-02-07</li><br/><li><img src="" width="30px"><span>建明</span> 👍（3） 💬（1）<div>老师其实我真的是完全的0基础，我听了前几节课如果能学好必然会对我的工作效率有质的提升，我目前还有一个0基础学Python，现在学这门课很困难，但我想学这门课，能否给我推荐一个学习的思路呢，如何构建我Python学习体系呢。</div>2021-03-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/08/5e/191013be.jpg" width="30px"><span>吴杨</span> 👍（2） 💬（1）<div>老师的文稿能否发到其他云空间供我们下载，GitHub被墙的概率太高了。</div>2021-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/27/805786be.jpg" width="30px"><span>笨笨</span> 👍（0） 💬（1）<div>老师这个‘excel 提前处理为 python 的基础类型–字典（链接）’代码有吗？或者有把Excel处理好后的字典形式的最终结果吗？这里是把excel处理成了两个文件了吗？我想象如果要处理成一个字典的话是这样的：{姓名：韩梅梅，姓名：李雷，称呼：女士，称呼；女士}。但这样不太合理。</div>2023-06-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/80/f4/564209ea.jpg" width="30px"><span>纳兰容若</span> 👍（0） 💬（2）<div>老师您好 为什么提示我在docx.py中没有Document类 我是在windows下用的pycharm python3.10</div>2022-10-25</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epNx7CCsqNO0qiavCXp2AQEU7ZIpL8aNpRr7ypmKPrf5MOia5rV5ibTLKrlMQxiafPoRLicOvfSicwukIbw/132" width="30px"><span>刘慧慧</span> 👍（0） 💬（1）<div>def merge_without_format(docx_files: list): 这个list整个代码未见使用定义在这里是干什么的？去掉这个list运行报
File &quot;&#47;Users&#47;hhliu&#47;Documents&#47;test&#47;autoWork&#47;day01&#47;mergeDoc.py&quot;, line 9, in merge_without_format
    another_doc = Document(docx_file)
  File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.6&#47;lib&#47;python3.6&#47;site-packages&#47;docx&#47;api.py&quot;, line 25, in Document
    document_part = Package.open(docx).main_document_part
  File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.6&#47;lib&#47;python3.6&#47;site-packages&#47;docx&#47;opc&#47;package.py&quot;, line 128, in open
    pkg_reader = PackageReader.from_file(pkg_file)
  File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.6&#47;lib&#47;python3.6&#47;site-packages&#47;docx&#47;opc&#47;pkgreader.py&quot;, line 32, in from_file
    phys_reader = PhysPkgReader(pkg_file)
  File &quot;&#47;Library&#47;Frameworks&#47;Python.framework&#47;Versions&#47;3.6&#47;lib&#47;python3.6&#47;site-packages&#47;docx&#47;opc&#47;phys_pkg.py&quot;, line 31, in __new__
    &quot;Package not found at &#39;%s&#39;&quot; % pkg_file
docx.opc.exceptions.PackageNotFoundError: Package not found at &#39;c&#39;</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/c4/22/af245290.jpg" width="30px"><span>Armstrong</span> 👍（0） 💬（1）<div>merge_without_format函数里面newpar = doc.add_paragraph(&#39;&#39;) ......其中doc没有定义，是不是会报错？</div>2021-08-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/5b/dc/4e872447.jpg" width="30px"><span>紫薯酸牛奶</span> 👍（0） 💬（3）<div>问题1：
replace_content = {
    &#39;&lt;姓名&gt;&#39; : &#39;no_name&#39;,
    &#39;&lt;性别&gt;&#39; : &#39;m_f&#39;,
    &#39;&lt;今天日期&gt;&#39; : today,
}

老师我想问下，制作邀请函中的
这个代码里面的no_name, 和m_f的含义是什么，
我自己想做个扩展练习，把邀请函模板里的酒店也批量替换掉，一直成功不了

问题2：
关于保存路径
# 邀请函路径
invitation_path = &#39;测试文件&#47;邀请函样例文件&#47;111&#39;
下面保存生成的文件代码是这个
file_name = PurePath(invitation_path).with_name(replace_content[&#39;&lt;姓名&gt;&#39;]).with_suffix(&#39;.docx&#39;)
    doc.save(file_name)
为啥总是保存在上一级文件夹（邀请函示例文件）而不是111这个文件夹

烦请老师帮忙解答下</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/03/83a3d8e9.jpg" width="30px"><span>cathy2052</span> 👍（0） 💬（1）<div>在定义了合并函数后，想合并一个目录下所有文件
wordfilespath = &#39;C:&#47;Users&#47;82695&#47;办公自动化课程&#47;文章2代码&#47;word样例文件&#39;
p1=Path(wordfilespath)
merger_without_format(p1)

 执行后的错误：
 File &quot;&lt;ipython-input-12-b09143b771a9&gt;&quot;, line 13
    wordfilespath = &#39;C:&#47;Users&#47;82695&#47;办公自动化课程&#47;文章2代码&#47;word样例文件&#39;
                ^
SyntaxError: invalid syntax</div>2021-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/03/83a3d8e9.jpg" width="30px"><span>cathy2052</span> 👍（0） 💬（1）<div>merger_without_format(&#39;C:&#47;Users&#47;82695&#47;办公自动化课程&#47;文章2代码&#47;word样例文件&#47;绩效考核管理制度1.docx&#39;,&#39;C:&#47;Users&#47;82695&#47;办公自动化课程&#47;文章2代码&#47;word样例文件&#47;绩效考核管理制度2.docx&#39;)
SyntaxError: invalid syntax
调用函数时出错，看不出哪里错了</div>2021-02-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/34/4d/d6eaa473.jpg" width="30px"><span>鬼脸嘟嘟</span> 👍（0） 💬（1）<div>老师，使用你提供的图片导入word的那窜代码，无法实现</div>2021-02-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/33/7b/9e012181.jpg" width="30px"><span>Soul of the Dragon</span> 👍（0） 💬（1）<div>老师，我用上述方法进行Excel与Word文档合并的时候，发现无法显示出日期信息，将其强制转化为字符串后，最终显示出的是日期的文本格式，而不是标准的日期格式，请问这个问题该如何解决呢？</div>2021-02-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/da/eb/0a356fdb.jpg" width="30px"><span>开元₂³³³³³³³</span> 👍（3） 💬（0）<div>老师，我用vscode编写，python-docx很多都没有代码提示，这是正常的吗？</div>2022-05-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/7e/a6/4e331ef4.jpg" width="30px"><span>骑行的掌柜J</span> 👍（1） 💬（0）<div>还不错 感觉这课程对有Python基础的更友好😂</div>2022-04-16</li><br/><li><img src="" width="30px"><span>new</span> 👍（1） 💬（0）<div>说实话不是所有的小白都适合，如果对编程一点基础都没有的话不合适听，功能都找不全，还是要有点儿编程基础</div>2021-10-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/c8/99/db9a5878.jpg" width="30px"><span>CHEN诚</span> 👍（0） 💬（0）<div>你在课程中的编程软件是python自带的编程平台还是其他的第三编程平台
</div>2022-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2e/f0/de/fa161d6b.jpg" width="30px"><span>憨憨丶小完能</span> 👍（0） 💬（0）<div>老师这个其实是适合进阶的，零基础学起来是会有些困难的。联系先学一下简单的零基础课程再来学就更快一些</div>2022-10-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/85/ce/df1c7a91.jpg" width="30px"><span>陈小远</span> 👍（0） 💬（0）<div>老师，添加图片的写的比较简单了，我试了下添加图片，按照示例代码添加进图又太小了，设置长宽后又不太合适，始终达不到直接粘贴到word中的那种效果。所以想请教老师，实际编码过程中，如何设置添加图片的大小才能确保图片不过小或过大导致变形或显示不全等问题呢？</div>2022-07-09</li><br/><li><img src="" width="30px"><span>Geek_bc0291</span> 👍（0） 💬（0）<div>＃创建个目录
import os
# word文件所在路径
word_files_path = &#39;&#47;Users&#47;edz&#47;Desktop&#47;效率专栏&#47;文章2&#47;word样例文件&#39;
if os.path.isdir(word_files_path):
    print(word_files_path)
else:
    os.makedirs(word_files_path)
    print(&quot;create dir ok&quot;)</div>2021-12-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/0c/c438c5df.jpg" width="30px"><span>天国之影</span> 👍（0） 💬（0）<div>如果发现文档保存在上一层目录，可将代码做如下修改：
file_name = PurePath(invitation_path, replace_content[&#39;&lt;姓名&gt;&#39;]).with_suffix(&#39;.docx&#39;)
修改原因：
由于使用了with_name()函数，导致修改了最后的文件路径，从而导致保存在上一层目录，按照上述修改，可保证文件路径和文件名连在一起。</div>2021-12-07</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTICFHlYKsSkvShSGCxiaLydzPs0Om5YhH3VKPBKkWGOytaYFiaaldyR49hG70xKSMRa1ZhzSP1DFffA/132" width="30px"><span>nick</span> 👍（0） 💬（1）<div>邀请函那个代码能调通吗，其他两个调通了，是不是有什么问题</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/35/03/83a3d8e9.jpg" width="30px"><span>cathy2052</span> 👍（0） 💬（0）<div>  File &quot;&lt;ipython-input-9-724ba4cc277c&gt;&quot;, line 10
    merger_without_format(&#39;C:&#47;Users&#47;82695&#47;办公自动化课程&#47;文章2代码&#47;word样例文件&#47;绩效考核管理制度1.docx&#39;,&#39;C:&#47;Users&#47;82695&#47;办公自动化课程&#47;文章2代码&#47;word样例文件&#47;绩效考核管理制度2.docx&#39;)
                        ^
SyntaxError: invalid syntax</div>2021-02-28</li><br/>
</ul>