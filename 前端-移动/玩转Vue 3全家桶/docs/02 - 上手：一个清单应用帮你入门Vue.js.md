你好，我是大圣，欢迎进入课程导读篇的第二讲。

在上一讲中，我带你了解了前端框架的基本发展历史。在为什么要学Vue框架这个问题上，相信你现在已经有了自己的答案。那么从今天开始，我们正式进入上手学Vue 的阶段。

我们的专栏课程会通过故事的形式展开。故事的主角小圣是一名刚入行的前端工程师，在校期间学了点HTML、CSS和JavaScript，但是不太懂框架。我是他的经理，会手把手教他在Vue.js这个框架里打怪升级。

小圣在学习Vue的过程中碰到的各种问题，同样也可能是你会碰到的问题。所以，在我带着你一起解决小圣面临的问题的同时，你的很多问题也会迎刃而解。

今天是小圣第一天入职，他只知道团队的项目是用Vue.js开发的，但并不熟悉Vue的具体技术细节，所以我决定带他先做一个清单应用，先在整体上熟悉这个框架。当然了，我在这里带小圣做的清单应用，更多的是一种模拟的场景，并不需要对号入座到真实的工作场景下。毕竟在真实的工作场景下，可能小圣一进公司就上实际的项目了。

如果你已经很熟悉Vue开发了，可以直接粗略地把本讲过一遍，直奔下一讲。在那里，我会带你梳理Vue 3的新特性，相信这些新特性会让你对Vue 3产生新的期待。
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/2a/f5/7a/7351b235.jpg" width="30px"><span>ch3cknull</span> 👍（101） 💬（7）<div>交作业：
仅前端缓存：在unmount组件时，将 组件的 data 存到 localStorage ，mount组件时取出。

如果后端有接口的话，可以在unmount时，同步到后端，挂载时请求接口

考虑用户体验，如果离线在线都可修改，可以考虑给todo的每一项加个最后修改时间，挂载时把本地缓存数据和接口数据合并，当冲突时，只留下最新数据</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/70/71/4ca18f1e.jpg" width="30px"><span>www</span> 👍（57） 💬（7）<div>全选按钮使用 set 和 get 进行处理，真是妙啊。
这一个方法就值了🎫了</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（38） 💬（6）<div>思考题：这个涉及到页面状态保存，方法有很多，大概两类：
1. 本地储存：
a. localstorage
b. workers
c. router，也可以存到 route 中
d. 存到本地文件
2. 服务端：这个就是将状态保存到服务器，通过 axios 等方式和服务器交换数据等</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/58/a1/1b387762.jpg" width="30px"><span>老杨头</span> 👍（13） 💬（4）<div>交作业 ：
通过watch监听数据变更并存储到localStorage中，然后在mounted时加载数据

watch: {
            todos: {&#47;&#47;监听数据变更
                handler(newVal, oldVal) {
                    console.info(&quot;todos-&gt;change&quot;)
                    &#47;&#47;TODO::原来是在unmount时才保存的，但unmount代码没有执行，所以换成wathc了，不知道为什么unmount没有执行
                    localStorage.setItem(&quot;todos&quot;, JSON.stringify(this.todos))
                },
                deep: true
            }
        },
        mounted() {
            &#47;&#47;加载数据
            var todos = localStorage.getItem(&quot;todos&quot;);
            if(todos) {
                this.todos = JSON.parse(todos);
            }
        },
        unmounted() {
            &#47;&#47;保存数据
            localStorage.setItem(&quot;todos&quot;, JSON.stringify(this.todos))
        },

原来是在unmount时才保存的，但unmount代码没有执行，所以换成wathc了，不知道为什么unmount没有执行</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fb/0b/6362a743.jpg" width="30px"><span>杨村长</span> 👍（12） 💬（1）<div>交作业：将数据存入localStorage，刷新时再取出来展现
1.保存：watch一下todoList，变化存入
2.读取：data设置为localStorage中读出的数据</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（12） 💬（1）<div>打卡
1. 保存时机，在unmount的生命周期进行保存
2. 使用浏览器客户端存储，如sessionStorage，LocalStorage等api保存，保存时添加时间戳用于比对新老数据，使用服务端保存接口，将数据持久化到数据库，考虑接口请求失败时重试机制和友好提示
3. 客户端存储在在data定义时直接从localStorage等获取，服务端接口在created周期请求获取数据并给data赋值
4.考虑保存失败的情况，可以监听数据变化做自动保存</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/23/a6/88858c72.jpg" width="30px"><span>mixiuu</span> 👍（11） 💬（2）<div>仅刷新页面，并不会出发unmounted生命周期，在仅刷新页面的场景下可以在created生命周期里监听beforeunload事件，如果有todos，存入localstorage中</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/ad/24/c6b763b4.jpg" width="30px"><span>桃子-夏勇杰</span> 👍（6） 💬（2）<div> {{active}}  &#47; {{all}} 这里为什么要做成2个属性而不是直接做个1个属性呢？</div>2021-10-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/d7/3d/4b44d2ff.jpg" width="30px"><span>付帅帅</span> 👍（6） 💬（1）<div>目前能想到的持久化方案： 一个是借助后端让数据入库，还有就是 localStorage 这种浏览器本地持久化</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/2c/04/62765a5a.jpg" width="30px"><span>洪布斯</span> 👍（5） 💬（1）<div>在给输入框绑定事件 `addTodo` 时，把 `keydown` =&gt; `keyup` 是不是更合适，`keydown` 在按键按下时，会一直触发事件。或者做一个非空判断也可～</div>2021-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c9/f9/39492855.jpg" width="30px"><span>阿阳</span> 👍（5） 💬（1）<div>这一节看了好几遍，尤其是对于allDone这个计算属性，和v-model的结合使用，真是妙极了。以前走了不少弯路，没想到这个全选功能，实现的如此优雅。继续坚持学习。</div>2021-10-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（5） 💬（1）<div>学习任何框架，都可以以这个To do List为起始点。</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/0e/d9/e61ce097.jpg" width="30px"><span>郭纯</span> 👍（4） 💬（1）<div>两种方式 客户端持久化 或者 服务端持久化 .

客户端：localStorage  sessionStorage web sql cookie indexedDB
服务端：提供接口 客户端提交数据请求. </div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/bb/9e/eeac9445.jpg" width="30px"><span>肆水流歌</span> 👍（3） 💬（1）<div>看了大家的留言，我发现我只会localstorage，是我太菜了</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/76/3d/8120438b.jpg" width="30px"><span>3.141516</span> 👍（3） 💬（1）<div>之前学过小程序，发现微信小程序应该就是借鉴 vue 的风格，数据驱动、for、if 等等</div>2021-10-20</li><br/><li><img src="" width="30px"><span>Geek_be2349</span> 👍（3） 💬（1）<div>使用 localStorage 保存数据</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/95/21cb848b.jpg" width="30px"><span>柒月</span> 👍（2） 💬（1）<div>老师，为什么全选（数据变化），可以触发 set(), 不懂，这里的get() set() ，和 proxy 有关吗？</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/3a/e2/c48bd3b7.jpg" width="30px"><span>Kevin</span> 👍（2） 💬（1）<div>一个移动端的人来学习了下，从移动端的视觉来回答一下作业吧：
有两个方式来保存数据：
1、本地
2、远端

1、本地的方案，应该是一些本地cache的api调用；
2、远端：可以是服务端、也可使本地有rpc调用的服务；

其他考虑：
如何写的问题，也就是内存值和备份值的同步问题，可以考虑类似三级缓存的故事：
a）内存中修改后触发 本地cache
b）本地cache 触发remote的修改
c）需要对任务队列进行管理，避免数据同步失败；
</div>2021-11-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/c8/09/b34b1473.jpg" width="30px"><span>鱼腩</span> 👍（2） 💬（1）<div>尝试着用组合式API，在&lt;script setup&gt;  声明 
   state=reactive({对象}) ;
   const a,b,c =  toRefs(  );  
发现Script代码里面，通过 toRefs返回的，必须用 a.value来赋值，才可以保留响应式效果；
而 state.a 则不需要，底层应该是由于reactive内部对get,set进行处理；而toRefs返回的是ref类型，还有computed返回的也是ref。。。。难怪说vue3+ts+volar真香，类型检查真心不能缺</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/2f/f4adcb41.jpg" width="30px"><span>。。。</span> 👍（2） 💬（1）<div>我是新手，应该怎么代码练习下这个小app。
ps:vue 要在vs code中安装引入下吧，还不会</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/23/49/bf/4936c58b.jpg" width="30px"><span>吴晨辉</span> 👍（2） 💬（1）<div>课后作业：
本人背景：纯后端来学前端
思路：将数据缓存在浏览器页面刷新后不清除的地方（可以是后端，也可以是浏览器本地储存）
如果是后端，那么需要绑定一个后端接口，刷新页面重新获取数据
如果是浏览器本地储存，我觉得vue本身可以去做这件事，只需要给我们开放一个参数是否缓存本地
最好的方案是两个都做，这样后端卡住前端还能流畅显示</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fd/01/8d4a247c.jpg" width="30px"><span>就不吃苹果</span> 👍（2） 💬（1）<div>将数据存储到storage里面，在created的时候从浏览器本地获取数据吗？</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/73/ff/3e30f1c6.jpg" width="30px"><span>嘿吼</span> 👍（1） 💬（1）<div>&quot;但是有一个额外的要求，就是列表中没有标记为完成的某一项列表数据时，这个按钮是不显示的。&quot;

大圣老师，建议这句话改一下，结合代码，可以知道是什么意思，单看这句话还是又点绕。

：但是有一个额外的要求，就是列表中没有可以标记为完成的数据时，这个按钮是不显示的。</div>2021-11-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/bb/47/b60ae3eb.jpg" width="30px"><span>你好，阳光</span> 👍（1） 💬（1）<div>我测试发现在unmount时存data并不一定能把最新的状态保存下来，在update的时候才可以</div>2021-11-06</li><br/><li><img src="" width="30px"><span>Geek_140133</span> 👍（1） 💬（1）<div>文档+声音的方式真是赞，比视频自由、轻松、方便。
作业：localStorage</div>2021-10-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/f4/0a/02ecee7a.jpg" width="30px"><span>女干部</span> 👍（1） 💬（1）<div>大圣果然讲的有意思的多，
让我一个crud boy拾起了vue的兴趣</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（1） 💬（2）<div>
老师晚上好！
`Vue.createApp(App).mount(&#39;#app&#39;)`
这一句总是会提示一个错误：
`Uncaught TypeError: Vue.createApp is not a function`</div>2021-10-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/fb/c1/ecb11a80.jpg" width="30px"><span>By:小新</span> 👍（1） 💬（1）<div>首先采用vuex进行app运行时数据状态保存
然后再卸载组件之前拦截，将vuex的状态持久化到
localStorage</div>2021-10-20</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83eq6UjL0SBicZgyKzsAnCf08l0MibyqxsCecSVXa3tKvSDeDG6XRe1ngziaChRiaRcA0kzOlIwfcnNZvwg/132" width="30px"><span>Alias</span> 👍（1） 💬（1）<div>“jquery -&gt; vue&#47;react: 不要再思考页面的元素怎么操作，而是要思考数据是怎么变化的。这就意味着，我们只需要操作数据，至于数据和页面的同步问题，框架会帮我们处理”</div>2021-10-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/02/10/e81e6791.jpg" width="30px"><span>cx</span> 👍（1） 💬（1）<div>监听todos的数据，然后通过缓存的方式解决</div>2021-10-20</li><br/>
</ul>