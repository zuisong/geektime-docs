你好，我是王喆。

上节课，我们明确了推荐系统要解决的基本问题，清楚了深度学习推荐系统的技术架构，这节课我们开始走进实战。

作为程序员，我相信你肯定听过，甚至可能还很认同Linux之父Linus Torvalds的那句话“Talk is cheap.Show me the code.”。我也一样，所以只讲解理论知识不是这门课的风格，我希望你通过这门课的学习，不仅能构建出一棵深度学习推荐系统的知识树，还能动手实现出一个看得见、摸得着、能操作、能修改的推荐系统。

所以今天，**你跟着我的讲解，只需要花三十分钟的时间，就能将一套完整的深度学习推荐系统，Sparrow RecSys（随着课程的进行，我们会逐渐补充新的模块），在你自己的电脑上运行起来**。这也是我们这门课最终要实现的深度学习推荐系统。

## 废话不多说，直接运行

废话不多说，我们先把Sparrow RecSys安装运行起来。因为我已经把项目相关的所有代码（代码还会随着课程进行持续更新）、数据都整理到GitHub的开源项目中，所以你不需要额外安装任何的支持软件，也不需要额外下载任何数据。

这样，整个安装过程就跟“把大象装进冰箱“一样，只需要三步，就是打开冰箱门，把大象装进去，关上冰箱门。“翻译”成咱们的过程就是，从GitHub中clone代码，在本地以maven project的形式安装，运行RecSysServer主函数启动推荐服务器。接下来，我们详细地解释一下这三个步骤。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/24/2e/f9/c0a6232c.jpg" width="30px"><span>Capricornus</span> 👍（62） 💬（12）<div>MAC OS系统
1.下载IDEA（https:&#47;&#47;www.jetbrains.com&#47;idea&#47;download&#47;#section=mac）
2.下载JDK（https:&#47;&#47;www.oracle.com&#47;java&#47;technologies&#47;javase-jdk15-downloads.html）
3.安装IDEA和JDK（JDK的路径~&#47;Library&#47;Java&#47;JavaVirtualMachines&#47;openjdk-15.0.1-1）
4.打开IDEA，打开File-&gt;Project Strucure-&gt;Project-&gt;Project JDK(我的好像会自动识别)。若没有识别（显示jdk15.1）,点击三角号，自己添加，步骤Add SDK-&gt;JDK-&gt;选择上面提到的JDK路径选择。
5.在pom.xml点击右键，设置为maven project-&gt;&#39;Reload project&#39;。耐心等待，这个很费时间。
6.然后找到SparrowRecSys&#47;src&#47;main&#47;java&#47;com&#47;SparrowRecSys&#47;online&#47;RecSysServer,右击选择&quot;Run &#39;RecSysServer.main()&#39;&quot;,程序就执行起来了.
7.浏览器中键入http:&#47;&#47;localhost:6010&#47;</div>2020-12-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/2d/bb/8bd1b6e1.jpg" width="30px"><span>挖掘机</span> 👍（12） 💬（6）<div>windows下搭建推荐系统的步骤
1. 使用的vscode作为IDE
2. 编译命令为mvn package assembly:single
3. 我的web root uri在源代码里总是为空，稍微改了一下，这里是为了绕过去，也请指导的高手告诉正确方法
RecSysServer.java中49行改成了绝对路径
URI webRootUri = URI.create(&quot;file:&#47;D:&#47;Work&#47;RecommendationSystem&#47;Sparrow&#47;SparrowRecSys&#47;target&#47;classes&#47;webroot&#47;&quot;);
4. 运行java -jar target\SparrowRecSys-1.0-SNAPSHOT-jar-with-dependencies.jar即刻成功</div>2020-12-21</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/ibbg35VbtSTXrcBE1AWgwXAHmKBjru5HzSzEUaxiaTeahQqDVxr4ZATHibn67aanoMmT4uG34PNRv3norpmOqjwMw/132" width="30px"><span>嘿人</span> 👍（40） 💬（1）<div>王老师您好，我学习的时候就是经常把握不好“使用者”的度，碰到什么都想扎进去研究，导致很容易陷入‘局部极小值’，请问怎么把握这个度呢？</div>2020-12-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/c9/f8/72955ef9.jpg" width="30px"><span>浣熊当家</span> 👍（38） 💬（7）<div>因为没有项目经验，想知道git clone到本地之后，怎么运行这个Maven project呢？油管上有没有类似的demo可以看看，老师能出一下小的录屏么？万分感谢。。第一步就卡住了。。</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/8c/bd/3570d4c9.jpg" width="30px"><span>Hhha爲</span> 👍（34） 💬（1）<div>老师您好，我查阅了网上的一些博客资料，大多认为协同过滤这样的传统方法应该是在召回层。，不过在您的图里是在排序（精排）层，可以问一下这样分类的理由是什么吗？谢谢！</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/52/40/e57a736e.jpg" width="30px"><span>pedro</span> 👍（27） 💬（2）<div>暂时没有去跑项目，先尝试回答问题二吧，对于一个电影爱好者而言，从我的角度出发，一个能够取悦我的，电影推荐系统，必须满足我在电影种类，演员，电影内容，电影质量上的需求，要说什么最有帮助，我觉得应该是用户历史浏览记录。</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/84/f6/999c663d.jpg" width="30px"><span>Don</span> 👍（20） 💬（2）<div>召回有优化之后，排序并不能捕捉到召回新增的特征，在排序后召回的优化点弱化很多，这种一般怎么处理？比如：召回有话增加了性别+年龄的特征，但是排序层没有用这维特征，导致根据该特征召回的内容排序后都在靠后位置没有机会曝光</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/8e/67/afb412fb.jpg" width="30px"><span>Sam</span> 👍（15） 💬（6）<div>## 上个旧版本有些链接失效，现在补上这个新的，而且更新了步骤。
win7下 搭建 推荐系统 的步骤：
1. 第1步骤：下载IDEA。
https:&#47;&#47;www.jetbrains.com&#47;idea&#47;download&#47;#section=windows

2. 第2步骤：如何下载和配置JDK1.8（一定要JDK1.8）
https:&#47;&#47;www.cnblogs.com&#47;hejh&#47;p&#47;11276434.html

3.第3步骤：IDEA配置JDK1.8（一定要JDK1.8）
https:&#47;&#47;blog.csdn.net&#47;liluo_2951121599&#47;article&#47;details&#47;78484776

4. 第4步骤：window下安装scala步骤
https:&#47;&#47;www.cnblogs.com&#47;onlyxx&#47;p&#47;5168882.html

4.1 第4.1步骤：Scala安装问题找不到主类的（不要安装在有空格的路径）
https:&#47;&#47;blog.csdn.net&#47;weekdawn&#47;article&#47;details&#47;94625067

4.2 第4.2步骤：Scala2.11要匹配JDK1.8，否则出问题
https:&#47;&#47;blog.csdn.net&#47;yulutian&#47;article&#47;details&#47;80566728

5. 第5步骤：IDEA配置Scala
https:&#47;&#47;www.cnblogs.com&#47;starzy&#47;p&#47;10461038.html

6. 第6步骤：win7安装hadoop spark
https:&#47;&#47;www.jianshu.com&#47;p&#47;9f40fe1b6587

7. 第7步骤：安装Redis
https:&#47;&#47;www.cnblogs.com&#47;liuqingzheng&#47;p&#47;9831331.html

大功告成，如果安装过程有问题的同学，请留言，我们一起解决！~^^</div>2021-06-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTK6mh3xlaMoGtWjmVJh2LutdLcQcPbKNjRlVru3bx8ynPhgwuGhhdzTkwEMoXbvBtgkcDSfom1kZg/132" width="30px"><span>夜雨声烦</span> 👍（15） 💬（6）<div>JAVA小白 mac os系统 安装Sparrow Recsys时的历程：
1，安装java8和scala2.11
网上有很多参考教程。
安装Java8：https:&#47;&#47;blog.csdn.net&#47;irokay&#47;article&#47;details&#47;71374426
遇到的&#47;etc&#47;profile是readonly的情况，解决方法是更改该文件的权限，增加写权限：775.https:&#47;&#47;blog.csdn.net&#47;good007boy&#47;article&#47;details&#47;88659162
安装scale：https:&#47;&#47;blog.csdn.net&#47;u012373815&#47;article&#47;details&#47;53231292
遇到的问题，在执行scala的时候出现“scala [ERROR] Failed to construct terminal; falling back to unsupported”，应该是跟iterm2起了什么冲突，解决方案：https:&#47;&#47;blog.csdn.net&#47;merrily01&#47;article&#47;details&#47;102823539
2，安装、打开IDEA
略过
3，执行文件
在pom.xml点击右键，设置为maven project-&gt;&#39;Reload project&#39;
配置SDK：在File-&gt;Project Structure-&gt;Project配置Project SDK
然后找到SparrowRecSys&#47;main&#47;java&#47;online&#47;RecSysServer,右击选择&quot;Run &#39;RecSysServer.main()&#39;&quot;,程序就执行起来了
浏览器输入http:&#47;&#47;localhost:6010&#47;，就可以看到SparrowRecSys首页</div>2020-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/7e/0c/9ba6ba1b.jpg" width="30px"><span>明月</span> 👍（12） 💬（2）<div>老师，这是需要去了解一下java吗，在校生做推荐系统还是用Python</div>2020-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/9b/93/0d0be616.jpg" width="30px"><span>何去何从</span> 👍（10） 💬（1）<div>老师您好！因为之前工作没有过推荐系统相关的项目经验，如果后期有机会面试相关岗位，能否把这个项目写到简历中当做一个项目经验呢？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/24/16/a4/7aaa136f.jpg" width="30px"><span>海</span> 👍（7） 💬（2）<div>老师，马上就要秋招找工作了。时间问题只学习了python，感觉学习java体系来不及了，为了找工作想在scala系和pyspark系取舍一下。请问pyspark等用python调大数据相关技术在工业界运用广吗？</div>2020-12-29</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIyPicbmtsfhaIh4rD9pv43gTscicqoo7hwgaSaN2GmjSwCso5Gw0ARiaZbQCzEspBB37mSxxnAiahEdw/132" width="30px"><span>悠悠我心</span> 👍（7） 💬（1）<div>运行起来了，还没仔细看代码，期待</div>2020-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/0d/da/8a744899.jpg" width="30px"><span>wolong</span> 👍（7） 💬（2）<div>大佬您好！我这边大概从事搜索、广告、推荐的工作也大概有六七年的光景，我有几个一直困扰的问题希望您能抽时间帮忙解答。
1.现在关于实时广告点击率预估，业界主流的深度学习解决方案是怎样的思路？
2.深度强化学习在推荐行业目前的应用主要瓶颈在那些点？</div>2020-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/a2/da/a8a32113.jpg" width="30px"><span>太子长琴</span> 👍（6） 💬（1）<div>用户特征，尤其是行为特征，比如点击记录，有效浏览时长，点评记录，点评结果
物品特征，主演，类型，评分</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/ee/0e/833a346f.jpg" width="30px"><span>zly</span> 👍（5） 💬（1）<div>请问作为应届生想找推荐系统的工作，除了python以外更推荐学习什么语言呢（看到有的企业需要C++&#47;C，有的要Java），转专业小白有点迷茫</div>2020-12-15</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIHq3CYG3iaEwF2eXZYclCwJlKlg3jeFic8pgYwmITDhvMxYPuFfhI43386TvqoBTpyL88dUYK1Q7FQ/132" width="30px"><span>didishuibulou</span> 👍（5） 💬（8）<div>并没有看到“为你推荐页”，是在哪里啊？</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/25/72/73/d707c8be.jpg" width="30px"><span>MutouMan</span> 👍（4） 💬（1）<div>请问下使用tensorflow而不是pytorch是有什么技术原因吗？主要对tensorflow不太熟悉，想知道是不是需要学习tensorflow作为学习推荐系统的主力框架。谢谢</div>2021-04-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/9A1GRhjFcicWeSs9SmA1ib7Ft0017LLdgIw6o9q1hzmD7rX8PYTHZ2gaC3xn0CdlGriaoGPqpqGDk7UTjfZTHKrHg/132" width="30px"><span>PatrickPro2</span> 👍（4） 💬（1）<div>老师，我想基于你这套框架写一个自己的推荐系统项目，但我想用spring boot去做，而不是套在jetty上，这样做可以吗？</div>2021-01-28</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83epLVNa7usiaACLpwTu3hBUf9oeHPT2HMHRuyydwibNHGKUDBwayJrsdurZdOrRloZLqFIiaUz0ZaS1fA/132" width="30px"><span>Geek_260fe9</span> 👍（4） 💬（1）<div>老师您好，我之前只接触过python的项目，完全没有做过java，请问我如果想尽快入门java开发，从而能手动实现您这个项目，您有什么建议吗？</div>2021-01-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/36/59/010b3e60.jpg" width="30px"><span>神经蛙</span> 👍（4） 💬（1）<div>老师，您好，从百面机器学习、知乎和深度学习推荐系统，一路追过来。感谢您的分享，正在看近期的课。如果以后有更加深入的课程，希望在知乎上广而告之啊。

思考题
1.
数据部分
com.wzhe.sparrowrecsys.offline.spark.featureeng 特征工程
com.wzhe.sparrowrecsys.offline.spark.embedding 各种Embedding的数据处理

模型部分
com.wzhe.sparrowrecsys.offline.spark.evaluate.Evaluator 离线模型评估
com.wzhe.sparrowrecsys.offline.spark.model.CollaborativeFiltering 离线模型训练、预测
com.wzhe.sparrowrecsys.online.model 加载离线模型进行相关性计算，排序。

在线服务部分
com.wzhe.sparrowrecsys.online.datamanager.DataManager 在线数据管理 包括电影、评分、用户等类，还有Redis客户端类
com.wzhe.sparrowrecsys.online.recprocess 为你推荐、相似电影的处理类，调用模型类计算相关性
com.wzhe.sparrowrecsys.online.service 提供各个页面的HTTP服务，包括getMovie, getUser, getSimilarMovie, getRecommendation, getRecForYou

2.
基于用户观影行为：近期用户的观影片名、类别、导演、主演等，观看时长，用户历史的观影各类别比例
基于用户的社交行为：点赞、点踩、评论、分享。（分为正向和负向，调整推荐结果）
基于内容：观看同类型电影的人群的近期观影记录</div>2020-11-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/2b/df/ad9ff39b.jpg" width="30px"><span>且将酒作歌</span> 👍（3） 💬（1）<div>windows环境下，vscode + wsl2目前配置成功
wsl2系统为Ubuntu18.04（安装参考：https:&#47;&#47;docs.microsoft.com&#47;zh-cn&#47;windows&#47;wsl&#47;install-win10）
具体环境信息：
1、java: 1.8.0_301；2、scala: 2.11.8；3、flink: 1.11.3；4、spark:2.4.8;
5、Python: 3.7.6；6、Tensorflow：2.3.3
（安装参考：https:&#47;&#47;www.cnblogs.com&#47;lian1995&#47;p&#47;14882763.html）
可能需要将文件下载到windows，再将文件转移到wsl2系统路径，在 Windows 资源管理器的地址栏中输入 \\wsl$，会显示所有已安装的 WSL 目录，然后根据需要进行操作。
步骤如下：
1、在wsl2中安装好Java、scala、flink、spark、Aanaconda3等软件
2、在VScodes上安装好Remote WSL、Python等插件。
3、在wsl2命令框中输入&quot;code .&quot;，可能会报file permissions相关问题，可以参考：https:&#47;&#47;p3terx.com&#47;archives&#47;problems-and-solutions-encountered-in-wsl-use-2.html解决
4、在wsl2中安装完maven后，参考@挖掘机的方法输入mvn package assembly:single。可能会报错OutOfMemoryError系列问题。可以在终端中输入export MAVEN_OPTS=&quot;-Xmx4096M -Xss1024M -XX:MetaspaceSize=512M -XX:MaxMetaspaceSize=1024M -XX:+CMSClassUnloadingEnabled&quot;，如果不行，继续加内存。
5、继续参考@挖掘机的方法，将RecSysServer.java中46行改成了绝对路径
URI webRootUri = URI.create(&quot;home&#47;work&#47;RecommendationSystem&#47;Sparrow&#47;SparrowRecSys&#47;target&#47;classes&#47;webroot&#47;&quot;);
路径根据自己的实际情况而定。改完后重新输入mvn package assembly:single。
6、运行java -jar target\SparrowRecSys-1.0-SNAPSHOT-jar-with-dependencies.jar，收工。</div>2021-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/90/1a/5006d3be.jpg" width="30px"><span>Allen.Wu</span> 👍（3） 💬（1）<div>代码是Java的😓，，老师Python适合工业级推荐系统吗</div>2020-09-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/47/5b/cc9977ca.jpg" width="30px"><span>Eric</span> 👍（3） 💬（1）<div>这么多33节讲不完吧</div>2020-09-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/ec/8e/80ecba15.jpg" width="30px"><span>知行</span> 👍（2） 💬（1）<div>之前有幸读了王喆老师的大作，然后邮件提了一点自己的想法，得到了王老师的肯定，太荣幸了。 对于电影推荐场景，要想做到个性化，可能需要用户的属性，比如年龄、性别、学历、工作、资产状况。以及用户的行为序列特征，比如用户的点击、收藏、负反馈、停留时常等</div>2021-08-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/bd/eb/132cf10a.jpg" width="30px"><span>acedar</span> 👍（2） 💬（1）<div>找到RecSysServer，然后run，这个RecSysServer的目录写的太含糊了，完整的路径是：SparrowRecSys&#47;src&#47;main&#47;com.sparrowrecsys&#47;online&#47;RecSysServer, 
一开始找了半天也没找到这个位置，为避免大家也碰到这个问题，故分享出来，希望大家少走弯路。</div>2021-05-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/b5/8b/92549066.jpg" width="30px"><span>Geek_8183d5</span> 👍（2） 💬（1）<div> jdk一定要使用java8的版本：https:&#47;&#47;www.oracle.com&#47;java&#47;technologies&#47;javase&#47;javase-jdk8-downloads.html</div>2021-03-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/21/14/9c/793a7c63.jpg" width="30px"><span>Damon</span> 👍（2） 💬（1）<div>把项目打成jar包上传到服务器之后，执行jar包后在浏览器访问页面发现找不到文件，经排查应该是找不到index.html文件，用解压文件打开jar包发现这个文件是存在的，百度之后应该是jar包加载文件要用动态InputStream的方式，即InputStream in = this.getClass().getResourceAsStream(&quot;&#47;webroot&#47;index.html&quot;);，但是这个怎么传入Resource，即context.setBaseResource(Resource.newResource(webRootUri))，找了几天一直没有解决。本人没有java基础，没有找到解决方案。</div>2021-03-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/46/f4/93b1275b.jpg" width="30px"><span>Alan</span> 👍（2） 💬（1）<div>我是MacOS系统：
第一步：下载安装jdk8与IDE，推荐jdk8与IDEA（安装步骤省略，谷歌一下）；
第二步：从IDEA打开从github下载好的SparrowRecSys项目，会发现pom.xml很多环境配置错误（不急，正常）；
第三步：项目文件pom.xml点击右键，设置为maven project-&gt;&#39;Reload project&#39;。请耐心等待，这个很费时间，你会发现pom.xml错误慢慢减少（期间先看看源代码或先听老师教程），完成
第四步：找到SparrowRecSys&#47;src&#47;main&#47;java&#47;com&#47;SparrowRecSys&#47;online&#47;RecSysServer,右击选择&quot;Run &#39;RecSysServer.main()&#39;&quot;,程序就执行起来了.
第五步：浏览器中键入http:&#47;&#47;localhost:6010&#47;</div>2021-03-01</li><br/><li><img src="" width="30px"><span>王嘉伟</span> 👍（2） 💬（3）<div>如果运行scala程序有困难的同学，项目里已经有python实现的版本了，可以把相应的依赖通过pip装完就能运行了</div>2021-01-04</li><br/>
</ul>