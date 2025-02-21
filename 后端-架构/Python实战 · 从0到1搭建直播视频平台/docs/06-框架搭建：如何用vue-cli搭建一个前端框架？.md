你好，我是Barry。

上节课我们全面分析了平台功能模块和整体技术选型，我们最终会把项目做什么样子，想必你已经了然于胸了。

从今天开始，我们就要正式写代码了。我们先从前端开始，按现在前端项目的套路，第一步自然要先把平台的框架搭建起来，之后再进行各个功能页面的编写。

这节课我就结合一个HelloWorld的小案例，带你一起实操搭建。相信通过这节课的学习，你可以掌握从0搭建前端框架的能力，之后就能举一反三，利用框架搭建各类平台前端了。

话不多说，让我们一起来探索这有趣的搭建过程吧。

## 为什么我们要选择前后端分离？

动手搭建框架之前，我们得先来聊聊这个项目的开发模式。Python做全栈开发，其实有两种实现方式。一种就是前后端不分离的模式，通过Flask的模版语法来实现。但是这样做对前端的支持并不全面，另外大多数企业目前也摆脱了这样的模式。

另一种就是前后端分离的模式，这是现在企业项目里经常采用的开发方式。为什么现在后者更常用呢，我们还得从项目开发的进化过程说起。

在最初的项目开发过程中，公司没有明确的岗位划分。这意味着一个工程师既要实现后端代码，同时也要完成前端效果呈现的代码编写，具体关系你可以参考我画的这张示意图。
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/f5/72/8cbc5cb3.jpg" width="30px"><span>好困啊</span> 👍（0） 💬（1）<div>1. 动态效果：
   当用户将鼠标悬停在 Icon 上时，可以加入一些微动效来增加互动性。例如，Icon 可以轻微放大、旋转或改变颜色。

2. 提示功能：
   当用户悬停在 Icon 上时，可以显示一个小提示（例如，“点击返回首页”），指导用户进行操作。

3. 适应性设计：
   根据不同的页面背景，Icon 可以有多种颜色或版本。例如，对于深色背景的页面，可以使用白色版本的 Icon，而对于浅色背景的页面，则使用深色版本。

4. 响应式位置：
   在不同的设备和屏幕大小上，Icon 的位置可以稍作调整，确保用户在任何情况下都能轻松访问。

5. 集成其他功能：
   Icon 除了返回首页功能外，也可以通过长按或右键点击来展示一个小菜单，提供其他常用功能，如“帮助”、“设置”或“关于我们”。

6. 与其他元素的协调：
   确保 Icon 与页面上的其他元素在视觉上和功能上都能很好地协调。例如，如果页面上有一个导航栏，那么 Icon 应该与它在视觉风格和位置上都保持一致。

7. 历史版本展示：
   在特定的时间，如品牌周年庆，可以展示平台 Icon 的历史版本，增加品牌故事感和用户的参与感。

8. 节日主题：
   在特定的节日或活动期间，可以对 Icon 进行轻微的修改，增加节日氛围。例如，国庆节期间可以在 Icon 上添加国旗元素。

9. 加载动画：
   如果平台的某些页面需要加载时间，可以使用 Icon 作为加载动画的一部分，增强用户的等待体验。

10. 错误页面的导航：
   在“404”或其他错误页面上，Icon 可以作为一个明确的导航元素，帮助用户快速返回首页或其他关键页面。</div>2023-08-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/de/e927c333.jpg" width="30px"><span>浩荡如空气</span> 👍（0） 💬（1）<div>为什么不用最新的vue3</div>2023-08-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/da/d9/f051962f.jpg" width="30px"><span>浩仔是程序员</span> 👍（0） 💬（1）<div>对于思考题，可以把这部分抽象成一个公共组件，以达到复用的效果！

1. 环境的安装，vue2.0和vue3.0有什么区别呢
vue2.0
npm install vue-cli
vue3.0
npm install @vue&#47;cli

区别在于多了@，@可以指定具体的版本

2. macos系统使用npm安装的时候会出现没有权限报错
直接使用sudo就可以

3. 在npm install也会报错
实测mac前面加sudo即可，如果是m系列处理器需要npm install --ignore-scripts
</div>2023-06-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（0） 💬（2）<div>1. 思考题
可以创建一个公共组件的文件夹，专门放置要多处复用的组件，哪里需要就直接引入

2. 安装时候出现的一些坑的总结

直接用 npm install -g @vue&#47;cli  好像目前是安装的是 Vue CLI 4.x 的版本
根据文档如果想拉取2.x版本的，需要再安装一个桥接：
npm install -g @vue&#47;cli-init
再执行 vue init webpack my-project


环境变量配置后出现 npm ERR 报错
可以&quot; 进入 C 盘 - 用户 - 删除 .npmrc 文件 &quot;</div>2023-06-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/55/6c/cad715eb.jpg" width="30px"><span>Archer</span> 👍（0） 💬（1）<div>如果使用flask前后端不分离的话，可以用父子模板的方法，构建一个父模板里面是公共显示部分比如导航栏之类的，然后在子模板继承父模板再做独立的页面开发。不知道VUE是不是类似的方法。</div>2023-05-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（1）<div> 还有一个问题： 我没有http:&#47;&#47;localhost:8080&#47;#&#47; ，我访问本地url只显示http:&#47;&#47;localhost:8080</div>2023-05-12</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTI7Bm7xdbwqoWPaDwqn6WESYL5QY8X8r3Q1P7UEIeDWictxJWEIJLluhIDHF7b0wFpbiav3gYToBBYg/132" width="30px"><span>Geek_840593</span> 👍（0） 💬（1）<div>请问我们这次的项目用的是Vue CLI 3.x版本还是Vue CLI 2.x版本呀？ 就前面安装脚手架来看，2.x和3.x就不一样，比如vue init 命令已经被移除了，取而代之的是 vue create 命令，在 Vue CLI 3.x 版本中，dev 脚本已经被替换成了 serve 脚本，安装过程好痛苦</div>2023-05-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/09/98/397c2c81.jpg" width="30px"><span>贾维斯Echo</span> 👍（0） 💬（1）<div>有几种不同的方式可以实现在每个页面上显示平台 icon 并让其链接回首页：

1.固定在网站的导航栏或工具栏上，这样无论用户在浏览哪个页面，都可以方便地访问首页。这个导航栏可以是网站的主要导航栏或者一个专门的工具栏，它可以包含其他有用的链接或功能。

2.将平台 icon 放在每个页面的页脚或页眉，这样用户在浏览页面的底部或顶部时，也可以轻松访问首页。

3.也可以将平台 icon 放在页面的固定位置，例如左上角或右上角。这样，当用户滚动页面时，icon 会保持在视图中,用户需要返回的时候就回去了。</div>2023-05-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/25/87/f3a69d1b.jpg" width="30px"><span>peter</span> 👍（0） 💬（2）<div>Q1：安装的vue-cli只对项目有效吗？ 比如在项目study1这个目录下面执行vue-cli的安装命令，那么，安装后的vue-cli对其他项目有效吗？

Q2：在一个目录下面执行vue-cli的安装命令，安装成功后，该目录下面并没有文件，还是空目录。难道vue-cli没有安装在此目录下面吗？

Q3：执行npm install失败，后面执行npm run dev也失败
Step1: 执行命令：npm install --global vue-cli，成功
Step2：执行：vue –V，成功，（刚开始有错误，搜索后解决）
Step3: 执行：vue init webpack my-project2，成功（vue init webpack my-project2）
Step4：执行：npm install, 失败
npm WARN saveError ENOENT: no such file or directory, 
open &#39;E:\Javaweb\study\videolive\front\study2\package.json&#39;
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN enoent ENOENT: no such file or directory, open &#39;E:\Javaweb\study\videolive\front\study2\package.json&#39;
npm WARN study2 No description
npm WARN study2 No repository field.
npm WARN study2 No README data
npm WARN study2 No license field.

但项目根目录下面有两个文件：package.json和package-lock.json。

后面执行npm install的错误信息：
npm run dev
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path E:\Javaweb\study\videolive\front\study2\package.json
注：1 VSCode版本：1.65；2 node版本是v14.18.1，对应的NPM版本是 6.14.15；3 没有创建环境变量NODE_PATH，也没有在环境变量path追加%NODE_PATH%。</div>2023-05-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/8f/88/3814fea5.jpg" width="30px"><span>安静点</span> 👍（0） 💬（1）<div>我觉得可以讲Icon固定在左上角，或者固定在导航栏或菜单栏上，再或者以浮动按钮的形式展现
点击跳转首页这个需要绑定函数之类的吧。</div>2023-05-05</li><br/>
</ul>