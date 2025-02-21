你好，我是杨文坚。

上节课，我们围绕运营平台Node.js服务的功能特点，学习了数据库方案设计，以及如何优雅实现数据库的快速初始化。同时，也提到一个项目观点：数据库的设计等于是业务功能的设计，所以只要数据库设计好了，业务功能设计也就基本成型。

今天这节课，我们也秉承这个观点，基于上节课设计的“员工用户表”来实现用户的注册和登录的功能（为了描述方便，“员工用户”我们就都简称为“用户”）。

一般，Web平台涉及用户操作的功能，都必须匹配相应的用户注册和登录的功能，才能规范用户的操作权限，避免产生业务数据污染，保证平台流程有条不紊地自动运行。那么如何实现运营平台的注册和登录功能呢？

只有数据库的员工用户表是远远不够的，我们需要基于员工用户表，设计“注册和登录的功能逻辑”。

## 如何设计注册和登录的功能逻辑？

用户注册和登录功能逻辑的设计，其实并不复杂，重点是理清功能点的每个步骤的逻辑。

我们先看用户注册的功能逻辑链路，我画了一张图。

![图片](https://static001.geekbang.org/resource/image/53/1e/53b85a43222daf4e5f8a4c77ae62951e.jpg?wh=1920x1080)

可以看出，注册功能的主要逻辑可以分成三步。

- 第一步，用户输入和提交“待注册”账号密码。这一步中，功能上要辅助用户校验用户名称是否符合规范，同时，要辅助用户校验两次密码是否一致。
- 第二步，用户提交注册信息，处理注册逻辑。这时候要平台判断账号是否存在，判断是否能注册，并处理注册结果。如果用户名称已存在，就准备好失败提示结果，如果用户名称不存在，就注册用户信息。
- 第三步，处理注册后的结果。如果用户注册成功，就自动跳转到登录页面，如果用户注册失败，显示失败原因，提醒用户如何改正。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/3e/19/ed6d0796.jpg" width="30px"><span>蒙</span> 👍（2） 💬（1）<div>加解密可以直接用node的加密函数不用jwt吗，
用jwt加解密有什么额外好处吗</div>2023-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-09-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/92/6d/becd841a.jpg" width="30px"><span>escray</span> 👍（0） 💬（0）<div>在本课附带的源码中，如果分别启动前后端

npm run dev:work-front
npm run dev:work-server

首页是可以出来的，但是在后台会有一个报错

12:21:39 PM [vite] Internal server error: Failed to resolve import &quot;@my&#47;components&#47;css&#47;index.css&quot; from &quot;packages&#47;work-front&#47;src&#47;pages&#47;home&#47;index.ts&quot;. Does the file exist?

好像是组件引用的问题，那个 index.css 文件是存在的，从代码里面也能够链接到 css 文件。

不知道有没有人遇到类似的问题，是否有解决办法？

另外就是用 pnpm i 来编译整个项目的时候，执行到

 &gt; vite-node .&#47;scripts&#47;build-dts.ts

还是会有 Error: TypeScript类型描述文件构建失败！

JSX element implicitly has type &#39;any&#39; because no interface &#39;JSX.IntrinsicElements&#39; exists.

在网上找了一下，大部分的办法是和 react 相关的，一般会推荐再次安装 @types&#47;react，或者重启 TypeScript 服务，感觉不太合适。

后来遇到的错误是

[less] Unrecognised input
2:35:34 PM [vite] Internal server error: [less] Unrecognised input
  Plugin: vite:css
  File: &#47;Users&#47;zhaorui&#47;Study&#47;professional&#47;SourceCode&#47;VueStudy&#47;vue3-course&#47;chapter&#47;21&#47;packages&#47;work-front&#47;src&#47;pages&#47;sign-in&#47;sign-in.vue:103:9
  2  |    &lt;DynamicForm
  3  |      class=&quot;sign-up-form&quot;
  4  |      :model=&quot;model&quot;
     |           ^
  5  |      :fieldList=&quot;fieldList&quot;
  6  |      @finish=&quot;onFinish&quot;
</div>2024-01-16</li><br/>
</ul>