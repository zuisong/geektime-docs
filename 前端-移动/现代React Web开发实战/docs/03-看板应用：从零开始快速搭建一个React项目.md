你好，我是宋一玮。从这节课开始，我们就进入到React Web应用开发的学习。

作为前端开发者，在学习一门新技术时最常用的方法是什么？Linux操作系统的创始人Linus大神有句名言：“口说无凭，放码过来。”没错儿，上手写代码确实是最有效的方式之一。

然而我也听到过不少吐槽：

- 前端开发不应该是一边写代码，一边刷新浏览器就够了吗？
- 为什么只想写几行代码，要配置一天的开发环境？
- 代码在别人那里跑的好好的，为什么我这里跑不起来了？
- 我改了几行代码，为什么页面没反应/就挂了？

我们需要了解一个现状，那就是现代前端开发早已结束了刀耕火种的时代，逐步向其他软件开发领域看齐。比如常被一起提到的后端开发领域，开发者们也常会抱怨配置开发环境又复杂又耗时间，同样的代码换个环境编译就会挂，等等。

现代前端的编译构建、依赖管理、CI/CD等工程化实践一应俱全，正如第1讲提到的，前端应用功能日益丰富、强大，这样的变化也是为了应对开发复杂度的攀升，但同时也带来了类似的痛点。我们即将要创建的React项目，就需要用到一系列工具链。不过这些技术，对于初学者来说确实有一定的门槛。

这时你可能会问到：“那我什么时候才可以上手写React代码？”
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/21/69/79/b4132042.jpg" width="30px"><span>🐑</span> 👍（7） 💬（0）<div>你好，我是咱们《现代React Web开发实战》的专栏编辑！课程中的相关代码我都放在了这里，你可以根据需要来学习👇

🌟https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban 这是oh-my-kanban项目源代码。

🌟https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;commits&#47;main 这个是03分步骤提交的commits。

🌟https:&#47;&#47;gitee.com&#47;evisong&#47;geektime-column-oh-my-kanban&#47;releases&#47;tag&#47;v0.3.0 这个是03的完整代码。</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ac/62/37912d51.jpg" width="30px"><span>东方奇骥</span> 👍（11） 💬（2）<div>跟着老师一起写，Typescript版本：https:&#47;&#47;github.com&#47;worldluoji&#47;front-end&#47;blob&#47;main&#47;react&#47;my-app&#47;src&#47;components&#47;board&#47;board.tsx</div>2022-08-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/61/98/0d6b499d.jpg" width="30px"><span>船长</span> 👍（5） 💬（3）<div>老师好，问下这里 setTodoList 时为什么要用函数写？直接写有什么问题吗？
（不能贴图，我上传了图床）
![20220907QgBXtq](http:&#47;&#47;picbed.tanguangzhi.com&#47;uPic&#47;20220907QgBXtq)</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/4f/39/791d0f5e.jpg" width="30px"><span>学习前端-react</span> 👍（5） 💬（1）<div>请问：什么是受控组件？是不是指的是value值是传入的然后触发的事件去更新value？</div>2022-08-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/58/9d/91d795cf.jpg" width="30px"><span>ZENG</span> 👍（3） 💬（7）<div>做的时候加了一个input框自动焦点的功能：
const inputRef = useRef();
  useEffect(() =&gt; {
    inputRef.current.focus()
  })</div>2022-08-26</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/c8/04/fed4c1ad.jpg" width="30px"><span>若川</span> 👍（3） 💬（10）<div>学到了新的node版本管理工具 fnm。

Windows 用户安装 VSCode 后，命令行终端默认就有 code 命令了~可以 code -h 查看帮助信息。</div>2022-08-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/52/0e/c5ff46d2.jpg" width="30px"><span>CondorHero</span> 👍（2） 💬（1）<div>以前只用过 nvm，这回了解了 fnm，借助它去调研了下 Node.js 管理器，然后一下子打开了 Node.js 管理器的大门，什么 nvm、n、fnm、Volta、nvs 等等，一圈看下来还是 fnm 香 ，速度快、更好的跨平台、像 nvm 一样的 API 简洁度，瞬间把 nvm 卸了装上 fnm😄</div>2022-08-25</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTKaOTc2Lx04iackJhiaOYjBQccVsyzYUrGzibeJw2G5eQez1XmnOianUTD4hFZkQWpVdLVS8ogBIxibffg/132" width="30px"><span>muzzy</span> 👍（1） 💬（1）<div>老师 现在还推荐使用cra去创建react的应用么 还是直接用vite去创建</div>2023-07-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（1） 💬（2）<div>老师你好，请问在更新组件状态时，这样使用：
    setTodoList((currentTodoList) =&gt; [
      { title, status: new Date().toDateString() },
      ...currentTodoList,
    ]);
这时候传入的是一个回调函数，这种使用方法能讲一下吗？</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/46/72/98d9723e.jpg" width="30px"><span>Ccccceilui</span> 👍（1） 💬（2）<div>执行完

brew install fnm
和
fnm install --lts
命令后

npx
和
yarn
命令并不存在啊？</div>2022-08-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/29/c3/791d0f5e.jpg" width="30px"><span>渣渣辉</span> 👍（0） 💬（1）<div>对于0经验react的新手来说很受用。这节课看了1个点。</div>2023-07-18</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJZmm5lWL0PlSEdluyDYtmyTvkHW7kSqJbsT40SZGnuFVUBDrICBlXgB53PeB8cOxuEs88PPk4feg/132" width="30px"><span>童童</span> 👍（0） 💬（1）<div>源码怎么clone不下来？提示“The authenticity of host xxxx can&#39;t be established. Please make sure you have the correct access rights.”</div>2023-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/3c/88/6bef27d6.jpg" width="30px"><span>大神博士</span> 👍（0） 💬（1）<div>复制出来代码都是加减号，不能从样式上去区分新旧代码吗；太难受了</div>2023-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/42/ed42e7cd.jpg" width="30px"><span>simoom</span> 👍（0） 💬（1）<div>使用npx create-react-app@latest my-app才成功的, 建议更新</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/60/42/ed42e7cd.jpg" width="30px"><span>simoom</span> 👍（0） 💬（1）<div>现在好像变了, 建议修改文章

cqy:react&#47; $ npx create-react-app oh-my-kanban                                                                                                                                                                                                                       [22:46:28]

You are running `create-react-app` 4.0.3, which is behind the latest release (5.0.1).

We no longer support global installation of Create React App.

Please remove any global installs with one of the following commands:
- npm uninstall -g create-react-app
- yarn global remove create-react-app

The latest instructions for creating a new app can be found here:
https:&#47;&#47;create-react-app.dev&#47;docs&#47;getting-started&#47;

npm notice
npm notice New patch version of npm available! 8.19.2 -&gt; 8.19.3
npm notice Changelog: https:&#47;&#47;github.com&#47;npm&#47;cli&#47;releases&#47;tag&#47;v8.19.3
npm notice Run npm install -g npm@8.19.3 to update!
npm notice</div>2022-11-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/88/a1/a78990c4.jpg" width="30px"><span>永不放弃</span> 👍（0） 💬（1）<div>前面看板列的 CSS .kanban-column &gt; ul { flex: 1; flex-basis: 0; overflow: auto; }，保证了卡片增减不会改变页面高度，而是自动出现滚动条。  我这边这样设置了，但是没有局部自动滚动图，都是整屏的。这个是啥原因？老师  .kanban-column &gt; ul {
  flex: 1;
  flex-basis: 0;
  margin: 1rem;
  padding: 0;
  overflow: auto;
}
</div>2022-10-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/88/a1/a78990c4.jpg" width="30px"><span>永不放弃</span> 👍（0） 💬（1）<div>新手打开学习，环境已配置，项目已创建，已跑通，已跟着代码实现。 https:&#47;&#47;github.com&#47;yj229201093&#47;oh-my-kanban</div>2022-10-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erb3HxekfsIdQumoyJVicmOuvibm0DqIiaCNHeESJdic3t1eIXAplplMicOnmLzibI19uiagdXm8qgZftHbw/132" width="30px"><span>Geek_45e28f</span> 👍（0） 💬（1）<div>        &lt;section className=&quot;kanban-column column-todo&quot;&gt;
          &lt;h2&gt;待处理&lt;&#47;h2&gt;
          &lt;ul&gt;
            {
              new Array(10).fill(&#39;&#39;).map((index) =&gt; {
                &lt;li className=&quot;kanban-card&quot;&gt;
                  &lt;div className=&quot;card-title&quot;&gt;开发任务-{index + 1}&lt;&#47;div&gt;
                  &lt;div className=&quot;card-status&quot;&gt;22-05-22 18:15&lt;&#47;div&gt;
                &lt;&#47;li&gt;
                }
              )
            }
          &lt;&#47;ul&gt;
        &lt;&#47;section&gt;
语法也没报错。。。但是也没打印出任何东西。</div>2022-09-26</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erb3HxekfsIdQumoyJVicmOuvibm0DqIiaCNHeESJdic3t1eIXAplplMicOnmLzibI19uiagdXm8qgZftHbw/132" width="30px"><span>Geek_45e28f</span> 👍（0） 💬（1）<div>老师，array.map()里的箭头函数不是应该是 () =&gt; {}吗？
为什么 ()=&gt;{}不会显示任何东西，反而()=&gt;()才会把无须列表打印出来？</div>2022-09-26</li><br/><li><img src="" width="30px"><span>智能-杨晋</span> 👍（0） 💬（1）<div>老师，如果就是要在父组件里面改变todoList 给 todoList插入一跳数据呢？(数据不往子组件迁移)
</div>2022-09-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/98/b1/f89a84d0.jpg" width="30px"><span>wu526</span> 👍（0） 💬（1）<div>老师，我按文章中的步骤操作时, 在最后 没有将 &quot;组件外面的todoList 数组改为 state 转移到组件内部&quot;, 也就是直接使用 const todoList = [{...}]这种方式, 回车时新项目也添加成功了，React 的相关信息时 &quot;react&quot;: &quot;^18.2.0&quot;, &quot;react-dom&quot;: &quot;^18.2.0&quot;,  &quot;react-scripts&quot;: &quot;5.0.1&quot;。麻烦老师解惑一下，非常感谢老师。</div>2022-09-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b4/f5/aec0f0c0.jpg" width="30px"><span>whoami</span> 👍（0） 💬（2）<div>mac版本下是不是用n也可以</div>2022-09-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1b/6b/c6/4cc776a7.jpg" width="30px"><span>百里</span> 👍（0） 💬（1）<div>到flex: 1; flex-basis: 0;这里就卡住了。
重新学习后发现，可以改为 flex: 0px;</div>2022-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（0） 💬（1）<div>一步一步的做，反复的看，好有收获，夯实基础，加深对开发思想的理解。</div>2022-09-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/99/13/2b325b02.jpg" width="30px"><span>学会用实力去谈条件</span> 👍（0） 💬（2）<div>有交流群嘛，方便问题反馈和沟通</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1a/99/13/2b325b02.jpg" width="30px"><span>学会用实力去谈条件</span> 👍（0） 💬（2）<div>$fnm --version输出fnm 1.31.1，说明fnm安装成功了，但是在执行 fnm install --lts时输出Installing Node v16.17.0 (x64)后就报错了
error: Can&#39;t download the requested binary: Can&#39;t extract the file: failed to unpack `&#47;Users&#47;xxx&#47;Library&#47;Application Support&#47;fnm&#47;node-versions&#47;.downloads&#47;.tmpYF3No7&#47;node-v16.17.0-darwin-x64&#47;bin&#47;node`

是需要配置国内的镜像加速器（开了梯子也是如此）
官网也没做过多介绍：https:&#47;&#47;github.com&#47;Schniz&#47;fnm

顺便推荐一款VSCode好用的插件：AppWorks</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1e/b0/2d/dd070a55.jpg" width="30px"><span>sello</span> 👍（0） 💬（1）<div>
老师，请问 eval &quot;$(fnm env --use-on-cd)&quot; 这行命令是做什么的</div>2022-08-30</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q3auHgzwzM7D1LViadpKva62AYrvTy0tHFVaiaUUHFhw3Cqgrvj6kufayoOSJ9IcgL5viamlhhbIwhFtL0vMu35aA/132" width="30px"><span>Geek_0c843c</span> 👍（0） 💬（1）<div>不用typescrpt讲吗</div>2022-08-30</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/46/f5/f2ad6692.jpg" width="30px"><span>小新</span> 👍（0） 💬（2）<div>install code 没找到</div>2022-08-29</li><br/><li><img src="" width="30px"><span>Sweety Gan</span> 👍（0） 💬（1）<div>老师，请问你的代码仓库地址可以发下吗</div>2022-08-25</li><br/>
</ul>