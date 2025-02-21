你好，我是月影。在课程正式开始之前，我想先和你聊聊可视化是什么，Web前端和可视化的区别，以及可视化领域中非常重要的工具。了解了这些基本的东西，对我们的学习是非常有帮助的。

前段时间因为新型冠状病毒，我们每天都在关注疫情信息。不知道你有没有注意过这些疫情信息的展示方式。

[![](https://static001.geekbang.org/resource/image/5a/d8/5ad44fe26f7eb1b2132a041a2e62a2d8.png?wh=1434%2A739 "来源：北京大学可视化与可视分析实验室")](https://vis.ucloud365.com/ncov/china_stat/#/)

我们看到的疫情图大概都会通过上面这个信息图的样子展示出来。这种信息图与普通的网页看上去差别非常大，我们没办法用传统的Web开发技术实现这样的“网页”。没错，这是一个与传统Web开发完全不一样的领域，叫做**数据可视化**（Data Visualization）。

其实，除了“疫情地图”之外，我们平时见到的很多东西，都是通过数据可视化来实现的。比如，每年淘宝“双十一”的可视化数据大屏、各种平台的年度账单等等。

那你可能要问了，可视化到底是什么呢？

如果要给可视化下一个定义，我觉得应该是这样的：**可视化是将数据组织成易于为人所理解和认知的结构，然后用图形的方式形象地呈现出来的理论、方法和技术**。实现可视化有两个关键要素，一个是数据，另一个是图形。如果要考虑在计算机上呈现，那还要加上交互。

## Web前端与可视化有什么区别？

据我所知，很多同学在工作中因为产品需求要呈现图表，而不知不觉从Web开发进入了可视化领域。但因为不了解它们之间的核心区别，或多或少都会遇到一些棘手的问题。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLicryBoLjDicckia0c5bkOoAlYoR2I9NMK8BiaD7HCGxhS1eM9YSfDuUJuZC90uwv9FvHIVSsBoxFgZw/132" width="30px"><span>MwumLi</span> 👍（26） 💬（1）<div>我一直以为程序员不只是掳码的工具人，特别是前端程序员，把语言文字需求视觉化，仿佛创造一个新世界，你就是造物主，学习可视化，会让这个造物主的权力更大</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/f6/0d/e16dff4e.jpg" width="30px"><span>瑞泉</span> 👍（16） 💬（1）<div>客户经常说看过哪家的可视化很炫酷，真正自己做的时候总感觉元素布局有问题，或者根据数据设计的展示很别扭，无法真正展示数据的特点，老师有没有什么方法介绍一下</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/20/7d/2a5c137c.jpg" width="30px"><span>秋谷</span> 👍（15） 💬（2）<div>之所以学习图形化，其实就是被‘表象’给吸引到了，各种层出不穷的视觉效果，以及看到某个厉害的作品的时候，总是会感叹一下，牛批啊，这也是我们前端写的诶，所以自己也想体验一下这种感觉。另外学习图形化的难点，相信很多小伙伴应该都有这样的感受吧，我数学不行，会不会太复杂之类的疑问，希望月影大大能够解惑一下。</div>2020-06-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIJxWVk7Gq9LBHFjWu1rxfWxqUwqicqkicxIBtliaEyHeXolVElpN7weZWqeZeY3lbRKCZ8AJbkq8MZA/132" width="30px"><span>越夜鸣</span> 👍（12） 💬（3）<div>随着硬件设备计算存储能力的提升，网络带宽速度的提升，以及不断提升的视觉及交互需求，觉着3d可视化是一种趋势。

国内的3d引擎，大多都不支持真正的阴影，法向量贴图，

而three直接进行业务开发比较困难，大量的时间用在在场景搭建上，就是缺少一个可视化的场景搭建编辑器。

另外有的引擎，生态圈不成熟，论坛里讨论的也比较少，没有专业的技术问答区。

针对业务开发的3d可视化，老师有没有推荐的3d引擎or框架？</div>2020-06-29</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/52/36/18f5d218.jpg" width="30px"><span>zcdll</span> 👍（12） 💬（1）<div>感觉 前端 可以扩展边界到 任何和 显示 相关的领域，包括1-在什么设备上显示 2-用什么技术显示 3-显示什么图像。
这也是我转行到前端最重要的原因，图像，图形的魔力大大滴</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/be/b7/638b5d30.jpg" width="30px"><span>白泗小林</span> 👍（9） 💬（9）<div>最近做一个需求是将很多小的病理切片拼成一个大图，能放大缩小倍数还能在图片上做标记的需求。老师有没有推荐的现成的库可以使用？</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/82/dc/5dbbe598.jpg" width="30px"><span>coolseaman</span> 👍（6） 💬（1）<div>有过基于echarts的复杂图表的开发经历，需要经过非常复杂巧妙的配置项才得以实现。echarts社区也有非常多的案例可供参考。
但是图表的库的限制还是非常大，掌握可视化技术，可以提供更多具有交互功能的图表解决方案。</div>2020-07-06</li><br/><li><img src="" width="30px"><span>GISer</span> 👍（6） 💬（3）<div>一直从事webgis开发，自从做了第一个大屏系统后，被一些图标给惊艳到了，从此更热衷于数据可视化开发，从简单的2d展示到3d展示，挑战一个接一个，从最开始的canvas到webgl，学习过程中走了不少弯路，跟着大神系统的学习一下，希望看openlayers和cesium更轻松些。</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/5f/58/f58ad899.jpg" width="30px"><span>大梦一场</span> 👍（5） 💬（2）<div>我还期待月影大大教教我canvas的一些基础和高级用法，但我更想学的是绘制的数学和算法，比如支付宝的芝麻信用分展现这种如何绘制，思路啥的</div>2020-06-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/70/83/36ab65ec.jpg" width="30px"><span>keke</span> 👍（4） 💬（2）<div>我想着学完后给公司的订单系统做一个可视化的数据大屏，不知道能不能实现～</div>2020-06-28</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eriaIgoPa8abNTaUm7o6oa6mvL9iagRTdD1vhovWPyfiaS82f409Sz3kMFzYLNa4ibnHagA7M33l8XnIQ/132" width="30px"><span>Bufan</span> 👍（4） 💬（1）<div>老师，你好，学习图形学有啥推荐的书籍吗</div>2020-06-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cc/cf/1c19ad6d.jpg" width="30px"><span>陈启年</span> 👍（4） 💬（1）<div>问：“你为什么想要学习可视化呢？”
答：做为从影视行业过来的人，对影视语言和三维建模有着天然的喜好。做了好几年前端后感觉有些荒废，想着怎么样才能把他们打通、结合起来。
曾经负责一个图表库模块（要求不引入现成的图表库看），使用dom或svg加上动画感觉卡的不行，改成canvas后又苦于任意形状下判断边界。后来就使用svg卡勉强实现。
问：“你觉得在学习的过程中有什么难点？”
完全不同的技术栈听着挺吓人的，希望多些真实案例，多多加餐😄</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/90/4656119a.jpg" width="30px"><span>拖鞋</span> 👍（4） 💬（1）<div>我想学这个想学好多年了，终于有大佬开课了</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b9/cc/80f6bf88.jpg" width="30px"><span>浮生若梦</span> 👍（4） 💬（1）<div>echarts也有custom的接口支持客户定制一些比较特别的图形，在视觉效果上基本可以实现d3的效果，但是动画的定制比较弱。另外，老师说的各种库可以结合工作使用场景深入说下具体区别吗？是否开源（免费）？最炫能实现什么效果？性能瓶颈？还有就是工作中怎么结合多个技术之长实现某一效果（比如echarts结合d3甚至webgl， 或者某地图结合canvas和webgl）？比如mapbox是国外地图的佼佼者，他跟国内开源的maptalks有什么区别？cesium for js是比较专业的gis地图，如果做三维城市，他除了性能自身做过优化比别的地图强之外，视觉效果较弱？</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/43/8a/9380fe92.jpg" width="30px"><span>KeilingZhuang</span> 👍（3） 💬（1）<div>我觉得数据可视化是一门艺术，把原本复杂的数据用生动有趣的方式展现出来，方便人们快速理解数据背后的含义。

请问大佬学习：在前端数据可视化领域里，数学会是最终决定实力的瓶颈吗？</div>2020-08-10</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/f1/18/63b9bd3c.jpg" width="30px"><span>宁康</span> 👍（3） 💬（1）<div>学习图形化技术不仅是扩展自己在web前端方面的知识面，同时我想图形化技术学好了，以后VR和AR方面也会很有用处。</div>2020-06-22</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erKbqXs1LibG8xNSJLfibacKZibtOJERzVVGLKUII7BtxYjjtwHiaEQtKicFPHabJwQRN6yfdqxfbDA8icA/132" width="30px"><span>amose</span> 👍（2） 💬（1）<div>由于一直在做BI报表开发，就默认属于可视化范畴。对我来说，可视化难点一个在于数据呈现和解读，另一个在于设计审美</div>2020-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/a9/662318ab.jpg" width="30px"><span>我母鸡啊！</span> 👍（2） 💬（2）<div>我之前自学webgl，看到three.js网站有很多很炫的例子，但是自己却不知道怎么去实现，后来问了人说要有ui建模什么的，感觉更不懂了。。。 不知道学完课程会不会对这些知识有一点理解
我为什么想学可视化，因为我觉得前端不应该只局限于页面，5g都来了，前端能在浏览器里做更酷的事情才对</div>2020-07-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/17/54/d1e9265f.jpg" width="30px"><span>LiSkysunCHN</span> 👍（2） 💬（1）<div>毕业后刚开始做全栈开发，后期接触可视化（少儿编程），然后对可视化方向喜欢的一发不可收拾，现在主要做了人工智能领域中人脸、OCR的较多可视化尝试，越来越爱！最初认为可视化就是Canvas 2D，随着需要解决的问题越来越多，渐渐去学习图形学知识、webgl、计算几何等知识。</div>2020-07-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b6/eb/5a8f95a0.jpg" width="30px"><span>Action</span> 👍（2） 💬（1）<div>老师，我想问问阿里的dataV是不是 都是可视化工程师做的。我做类似的项目，用vue也能做出来。不过像你说的 cavas之类的 貌似还没用到，引入的 echarts图标库，动态配置文件达到配置效果</div>2020-06-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/91/07/f270f35f.jpg" width="30px"><span>多读书</span> 👍（2） 💬（1）<div>在vue中highcharts和echart中如何实现3d效果</div>2020-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/36/11/d386b10f.jpg" width="30px"><span>温同学</span> 👍（2） 💬（1）<div>平时最多用echart完成可视化，修改一下配置。难点:普通做多了，定制化3d建模，粒子效果 用的three 脑壳痛 不知道怎么学习</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/9f/5b/87fa1e23.jpg" width="30px"><span>变成海的话</span> 👍（2） 💬（1）<div>经常有些分不清web前端开发和可视化开发的界限，也思考过两者的价值区别，有些迷茫，很多时候同样的东西，用传统前端的html和css可以解决，用可视化的canvas和svg也可以实现，就有些迷，到底该选哪个了。学习这门课，其实主要有两个目的，一个是为了知识，一个是为了延伸自己对可视化的价值和方向的思考</div>2020-06-23</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/ia2p5TE3N9AjcTcZK2ibgVYSTlUcklTCkWBibqRrGy9Yp5DtdmJOIyTO4ZP4LE5a3y3B2rURM81t8s7o2QMibj8LuQ/132" width="30px"><span>没事撸代码</span> 👍（2） 💬（1）<div>为啥要学可视化？
认为可视化是未来很可期的一个方向，加上自己也比较有兴趣。
难点：
数学知识？图形学，应该会涉及到很多矩阵计算的数学知识把，自己忘的完完的了</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/21/8c/e7241683.jpg" width="30px"><span>墨白™</span> 👍（2） 💬（1）<div>想要学习可是的目标是找出一个技术上的突破点。我将工程师能力分成3块来评价：
1. 技术能力
2. 项目管理能力
3. 团队管理能力

目前我在团队中第2项完成的不错，目前急需增加第1项，第3项需要根据团队发展来做出相应的变动，需要等待好的时机。</div>2020-06-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/57/05/6e0193b5.jpg" width="30px"><span>新哥</span> 👍（2） 💬（1）<div>可以每节课都留点思考题或布置点作业，不然我太懒了</div>2020-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/01/dd/169c2c54.jpg" width="30px"><span>小甘</span> 👍（1） 💬（1）<div>为什么要学习可视化呢？ 
1. 做了几年前端，感觉已经到了瓶颈期。 希望借助可视化技术深入一门技术，突破瓶颈期。
2. 目前的新基建等概念能对工业互联网、物联网等领域产生强有力的推动。个人认为可视化在这两方面有很大的应用场景。如：智慧工厂、物联网传感器可视化等等。</div>2020-12-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/73/c1/2f56a514.jpg" width="30px"><span>Hayho</span> 👍（1） 💬（1）<div>canvas 3d和webgl有什么区别</div>2020-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/38/29/9377bb13.jpg" width="30px"><span>孔孔熊</span> 👍（1） 💬（1）<div>平时的工作就是用在利用类似echart的图表库做数据展示的web开发，但是经常会有困惑，比如可视化也可以让后端工程师或有极少量前端经验的工程师用BI Tool更丰富的图表代替，而不需要有丰富前端经验的工程师去调用图表库或其他途径开发。所以想从这门课里学习到数据可视化的更多可能性，更强化自己的技术，不只是调用改写图表库，以及可能可以解决我对可视化技术选择上的一些困惑</div>2020-07-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/17/10/ff08859a.jpg" width="30px"><span>躺着看云飘</span> 👍（1） 💬（1）<div>之前的工作内容是web前端, 新公司正好在做可视化大屏的项目. 未来的发展发现一直困扰我很久, 邂逅了这门课程, 感觉打开了新世界的大门, 想把可视化作为自己未来的发展发现, 深入下去</div>2020-07-04</li><br/>
</ul>