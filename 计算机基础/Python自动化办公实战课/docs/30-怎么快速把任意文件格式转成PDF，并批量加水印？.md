你好，我是尹会生。

在办公场景中，我们打交道最多的软件，要数Office的办公套件了，功能丰富且强大，使用方便。不过你可能也会发现，我们经常用于文字编辑的Word软件，它使用的docx扩展名的文件无论是在不同操作系统平台、不同的设备上，还是在内容安全性和格式的兼容性上，都没有PDF文件强大。Excel和PowerPoint中的文件也是如此。

例如：你需要把公司的合同范本发给其他公司审阅，为了保证文本不会被随意篡改，往往需要把Word或PowerPoint的文件转换为PDF文件，再通过邮件发给其他公司。而且，随着数字化转型的开始，原本在计算机上正常显示的表格，拿到手机上可能会缺少字体；也可能因为屏幕宽度不同，导致格式无法对齐；还可能会出现无法显示文字等格式问题。

不过这些问题呢，PDF统统可以解决。所以像是商业的条款、合同、产品介绍，既要保证安全，又要确保格式正确，如果你不想限制用户必须要用多宽的显示器，或者必须安装好特定的字体，才能看到你的Word、Excel、PowerPoint里的内容的话，那么使用PDF文件就是非常必要的了。

所以在今天这一讲中，我将带你学习如何把Word、Excel、PowerPoint的默认文件格式批量转换为PDF文件，并教你怎么给PDF文件增加水印，既保证样式美观，又确保文档的安全。
<div><strong>精选留言（13）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/0c/c438c5df.jpg" width="30px"><span>天国之影</span> 👍（3） 💬（1）<div>【增加水印章节】
pdf合并后会出现乱码，可以通过更换pyPDF4这个库解决这个问题
具体代码可参考：https:&#47;&#47;relph1119.github.io&#47;TechBooks-ReadingNote&#47;#&#47;python_office_automation&#47;section05</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/95/a2/2f07f7a3.jpg" width="30px"><span>小pawn爷</span> 👍（1） 💬（1）<div>没有HTML转PDF的安全方法？</div>2021-07-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/23/66/413c0bb5.jpg" width="30px"><span>LDxy</span> 👍（1） 💬（1）<div>COM编程接口是一种接口类型吗？</div>2021-04-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/68RYibsKbLuPxurBbxykcaOOkibk9HcRbricEkvUfx1QDMSibg4upTd4Bo5urWdfGvIbHj5uujlicltiadHxQDpI9bUg/132" width="30px"><span>ty</span> 👍（0） 💬（1）<div>有没有pdf转word
</div>2023-06-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（0） 💬（1）<div>def word2pdf(word_path, pdf_path):

    # 指定Word类型
    word = client.DispatchEx(&quot;Word.Application&quot;)
    # 使用Word软件打开a.doc
    file = word.Documents.Open(word_path, ReadOnly=1)
    # 文件另存为当前目录下的pdf文件
    file.SaveAs(pdf_path, FileFomat = 17)
    # 关闭文件
    file.Close()
    # 结束word应用程序进程   
    word.Quit()

请问老师，这段代码运行时会卡在    # 使用Word软件打开a.doc
    file = word.Documents.Open(word_path, ReadOnly=1) 不动 ，请问怎么解决？</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/11/1d/6ad7eb3c.jpg" width="30px"><span>Wang</span> 👍（0） 💬（2）<div>中文会出现，合并后会出现乱码</div>2021-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/aa/95/20e8a273.jpg" width="30px"><span>鏡墨山人</span> 👍（0） 💬（1）<div>自己的电脑从Microsoft Office换用WPS Office之后转换会出错，请问有什么解决的方法嘛？</div>2021-05-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ef/95/754df959.jpg" width="30px"><span>innovator琳</span> 👍（0） 💬（2）<div>Mac os 上怎么操作？</div>2021-04-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/1d/7d/368df396.jpg" width="30px"><span>somenzz</span> 👍（2） 💬（0）<div>代码里面有中文逗号，这种经过测试吗？</div>2021-08-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/1d/0c/c438c5df.jpg" width="30px"><span>天国之影</span> 👍（1） 💬（0）<div>“将PowerPoint 幻灯片转换为PDF”这一节中
会遇到报错&quot;TypeError: The Python instance can not be converted to a COM object&quot;
在文件另存为当前目录下的pdf文件，请改为下面代码
file.ExportAsFixedFormat(&#39;\\&#39;.join([pptdir, pdfname]), FixedFormatType=2, 
                             PrintRange=None)</div>2021-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2023-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/9a/ea/cfb28cda.jpg" width="30px"><span>阿牛</span> 👍（0） 💬（0）<div>文章源代码 写入新的pdf文件出错
错误提示`ValueError: I&#47;O operation on closed file: test.pdf`

解决办法：
把写入语句缩进到读取没有水印的with语句内</div>2022-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5d/26/e0452d6f.jpg" width="30px"><span>ycc</span> 👍（0） 💬（0）<div>请问linux下如何比较完美地实现word转pdf，使用lib office效果很差啊？</div>2022-06-23</li><br/>
</ul>