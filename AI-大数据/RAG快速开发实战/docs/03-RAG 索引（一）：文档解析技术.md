> 本门课程为精品小课，不标配音频

你好，我是常扬。

在之前的课程中，我们了解到，RAG（检索增强生成）系统的首要步骤是索引（Indexing）流程中的文档解析。文档解析技术的本质在于将**格式各异、版式多样、元素多种**的文档数据，包括段落、表格、标题、公式、多列、图片等文档区块，转化为阅读顺序正确的字符串信息。“**Quality in, Quality out**” 是大模型技术的典型特征，高质量的文档解析能够从各种复杂格式的非结构化数据中提取出高精准度的信息，对RAG系统最终的效果起决定性的作用。

RAG系统的应用场景主要集中在专业领域和企业场景。这些场景中，除了关系型和非关系型数据库，更多的数据以 **PDF、TXT、Word、PPT、Excel、CSV、Markdown、XML、HTML** 等多种格式存储。尤其是PDF文件，凭借其统一的排版和多样化的结构形式，成为了最为常见的文档数据存储与交换格式。文档解析技术不仅需要支持上述所有常见格式，还需要特别强化对于PDF的解析能力，包括对电子档和扫描档的处理，支持多种版面形式的解析、不同类型版面元素的识别，并能够还原正确的阅读顺序。

此外，由于PDF文档往往篇幅巨大、页数众多，且企业及专业领域PDF文件数据量庞大，因此文档解析技术还需具备极高的处理性能，以确保知识库的高效构建和实时更新。
<div><strong>精选留言（11）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/14/13/48/55be9797.jpg" width="30px"><span>Joney Hsiao</span> 👍（1） 💬（2）<div>尝试过解析有图片的pdf文件，但是不理想，大模型输出“由于没有提供具体的图片内容，无法对图片进行分析。如果报告中有相关的图表或图像，请提供详细描述或上传图片，以便进一步分析。”

请问应该如何从哪点开始优化？
</div>2024-12-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/0a/a4/828a431f.jpg" width="30px"><span>张申傲</span> 👍（1） 💬（1）<div>第3讲打卡~</div>2024-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/66/d0/2fb761be.jpg" width="30px"><span>Jaycee-张少同</span> 👍（1） 💬（1）<div>实际工作场景中我认为pdf doc docx文件元素是构建字符切块的主要类型，另也可加入ppt演示文件内的文本字符。严格说我认为excel表格文件应当是份属db gpt的事情。不过事事无绝对，欢迎探讨</div>2024-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/f1/1f/c5064ee5.jpg" width="30px"><span>JMGAO</span> 👍（0） 💬（2）<div>linux下解析文件类型pdf&#47;txt&#47;csv 能够成功，解析md&#47;docx&#47;ppt&#47;xml&#47;html等提示 zipfile.BadZipFile: File is not a zip file
```
File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;unstructured&#47;partition&#47;text_type.py&quot;, line 270, in exceeds_cap_ratio
    if sentence_count(text, 3) &gt; 1:
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;unstructured&#47;partition&#47;text_type.py&quot;, line 219, in sentence_count
    sentences = sent_tokenize(text)
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;unstructured&#47;nlp&#47;tokenize.py&quot;, line 56, in sent_tokenize
    _download_nltk_packages_if_not_present()
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;unstructured&#47;nlp&#47;tokenize.py&quot;, line 41, in _download_nltk_packages_if_not_present
    tagger_available = check_for_nltk_package(
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;unstructured&#47;nlp&#47;tokenize.py&quot;, line 29, in check_for_nltk_package
    nltk.find(f&quot;{package_category}&#47;{package_name}&quot;, paths=paths)
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;nltk&#47;data.py&quot;, line 551, in find
    return find(modified_name, paths)
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;nltk&#47;data.py&quot;, line 538, in find
    return ZipFilePathPointer(p, zipentry)
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;nltk&#47;data.py&quot;, line 391, in __init__
    zipfile = OpenOnDemandZipFile(os.path.abspath(zipfile))
  File &quot;&#47;root&#47;workspace&#47;mingjian&#47;env_rag&#47;lib&#47;python3.10&#47;site-packages&#47;nltk&#47;data.py&quot;, line 1020, in __init__
    zipfile.ZipFile.__init__(self, filename)
  File &quot;&#47;usr&#47;lib&#47;python3.10&#47;zipfile.py&quot;, line 1272, in __init__
    self._RealGetContents()
  File &quot;&#47;usr&#47;lib&#47;python3.10&#47;zipfile.py&quot;, line 1339, in _RealGetContents
    raise BadZipFile(&quot;File is not a zip file&quot;)
```</div>2025-01-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/cd/10/1b38a2f9.jpg" width="30px"><span>大胡</span> 👍（0） 💬（1）<div>另外，csv文件也存在一个gbk编码错误</div>2024-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/cd/10/1b38a2f9.jpg" width="30px"><span>大胡</span> 👍（0） 💬（1）<div>此处问题较多。下面是一个下载问题，有什么好办法吗？
Resource punkt_tab not found.
  Please use the NLTK Downloader to obtain the resource:
  &gt;&gt;&gt; import nltk
  &gt;&gt;&gt; nltk.download(&#39;punkt_tab&#39;)
    For more information see: https:&#47;&#47;www.nltk.org&#47;data.html
  Attempted to load tokenizers&#47;punkt_tab&#47;english&#47;</div>2024-12-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3c/68/9b/d53ebac5.jpg" width="30px"><span>Grain Buds</span> 👍（0） 💬（1）<div>课程代码顺利跑通，但是生成结果准确性不足呢？生成回答中，有关金融业的部分并没有提取到，仅做了简略描述</div>2024-11-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/db/95/daad899f.jpg" width="30px"><span>Seachal</span> 👍（0） 💬（1）<div>第3讲打卡~</div>2024-11-15</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/3b/d0/e5/0a3ee17c.jpg" width="30px"><span>kevin</span> 👍（0） 💬（1）<div>在windows下运行，csv可以解析，但doc一解析系统就挂了，也不知道怎么回事，装了LibreOffice 24.8</div>2024-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4c/aa/37705e4e.jpg" width="30px"><span>影明</span> 👍（0） 💬（1）<div>在windows下运行，csv可以解析，但docx报错：
文档 .&#47;data_lesson3\test.csv 的部分内容为: 案例名称: 制造业的数字化转型
公司背景: 制造业案例介绍了一家成立于20世纪初的德国老牌汽车制造公司，拥有悠久的历史和丰富的制造经验。面对日益激烈的市场竞争和消费者需求的变化，公司意识到传统制造模式...
文档 test.csv 的总字符数: 1262
文档 test.csv 分割的文本Chunk数量: 3
soffice failed to convert to format docx:MS Word 2007 XML with code 0
Error: source file could not be loaded
Traceback (most recent call last):
  File &quot;c:\Users\yingm\LAB\PycharmProjects\rag_app\rag_app_lesson3.py&quot;, line 238, in &lt;module&gt;
    main()
  File &quot;c:\Users\yingm\LAB\PycharmProjects\rag_app\rag_app_lesson3.py&quot;, line 227, in main
    index, chunks = indexing_process(&#39;.&#47;data_lesson3&#39;, embedding_model)
  File &quot;c:\Users\yingm\LAB\PycharmProjects\rag_app\rag_app_lesson3.py&quot;, line 93, in indexing_process
    document_text = load_document(file_path)
  File &quot;c:\Users\yingm\LAB\PycharmProjects\rag_app\rag_app_lesson3.py&quot;, line 55, in load_document
    documents = loader.load()  # 加载文档
 ......
    elements = func(*args, **kwargs)
  File &quot;C:\Users\yingm\.conda\envs\rag_env_39\lib\site-packages\unstructured\partition\docx.py&quot;, line 160, in partition_docx
    opts = DocxPartitionerOptions.load(
  File &quot;C:\Users\yingm\.conda\envs\rag_env_39\lib\site-packages\unstructured\partition\docx.py&quot;, line 222, in load
    return cls(**kwargs)._validate()
  File &quot;C:\Users\yingm\.conda\envs\rag_env_39\lib\site-packages\unstructured\partition\docx.py&quot;, line 376, in _validate
    raise FileNotFoundError(f&quot;no such file or directory: {repr(self._file_path)}&quot;)
FileNotFoundError: no such file or directory: &#39;C:\\Users\\yingm\\AppData\\Local\\Temp\\tmpij10aiti\\test.docx&#39;</div>2024-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/78/3e/f60ea472.jpg" width="30px"><span>grok</span> 👍（3） 💬（2）<div>组里有个项目需要处理合同pdf（扫描件&#47;英文），主要难点是夹杂的特殊字符和希腊字母。效果不达标。
已尝试：
Adobe, Nitro, Azure Doc intelligence, GPT4o, ensemble of doc intelligence + gpt4o&#47;V
下一步打算尝试：
AWS Textract, Google Vision API, Nougat, Texify, Tesseract&#47;pytesseract</div>2024-09-01</li><br/>
</ul>