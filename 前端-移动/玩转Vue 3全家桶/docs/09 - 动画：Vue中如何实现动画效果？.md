你好，我是大圣。

在上一讲中，我给你讲解了组件化设计的思路，有了组件，我们就可以积木式地搭建网页了。领会组件设计的思路后，小圣继续丰富了清单组件的功能，在组件的功能实现完毕后，我给他提出了一个新的要求，希望能有一些动画效果的加入，让这个应用显得不再这么生硬。

小圣自己琢磨以后，又找过来咨询我Vue 3中实现动画的方式，所以今天我就来跟你聊一下Vue中应该如何实现常见的过渡和动效。在讲解过程中，我们会继续给之前那个清单应用添砖加瓦，给它添加更多酷炫的玩法，让我们正式开始今天的学习吧。

## 前端过渡和动效

在讲Vue中的动效和过渡之前，我想先跟你聊一下前端的过渡和动效的实现方式。举个例子，假设我现在有这样一个需求：在页面上要有一个div标签，以及一个按钮，点击页面的按钮后，能够让div标签的宽度得到增加。

在下面的代码中，我们可以实现上面所说的这个效果。这段代码里，首先是一个div标签，我们使用width控制宽度。我们想要的前端效果是，每次点击按钮的时候，div标签的宽度都增加100px。

```xml
<template>

  <div class="box" :style="{width:width+'px'}"></div>
  <button @click="change">click</button>
</template>

<script setup>
import {ref} from 'vue'
let width= ref(100)
function change(){
  width.value += 100
}
</script>

<style>
.box{
  background:red;
  height:100px;
}
</style>
```
<div><strong>精选留言（30）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（62） 💬（6）<div>边看回顾学过和用过的动画知识，总结下：
      1. 为什么要用动画？
         首先肯定不是为了“炫技”，从产品的角度，个人觉得是为了“降低用户理解难度”，因为
         “动” 意味着有“生气”，比较“自然”。回想下日常生活中，碰到的人或事，如果比较“自
         然”是不是意味着比较“好搞”，比较“容易相处”。而我们用动画就是为了实现这样的效果。

         当然用户体验这种事，大公司应该专门有个UX部门，我们前端主要还是要以实现为主，
         工程师还是要“多、快、好、省”的把事情做成，这就涉及到动画的具体实现。

      2. 动画的实现
         个人觉得动画的实现就是CSS的事，JS实现动画也是动态改变某个元素的CSS属性。这个
         过程可以看下隔壁李兵老师的《浏览器工作原理与实践》其中的渲染流水线的论述，这
         里强调下，如果较关注的动画性能问题，还是从动画的本质理解起：

         动画的本质：“从哪里来，到哪里去，中间过程是怎么样的”。

         以本节第一段代码来说，从哪里来&quot;from&quot;，就是 box.width=100px；去哪&quot;to&quot;, 就是
         box.width += 100px；后面为了“动起来”，加了个中间过程，是用&quot;transition&quot;实现的，
         当然还有其他实现，深究还涉及到贝叶斯曲线函数，“弹簧函数”之类的技术实现。

         提下动画的性能问题，简单说就是，改变有些 CSS 属性会影响渲染流程，就是常说的
         “重排，重绘，合成”。提供两个资源，可以具体看下，改变哪些属性会触发。
         – https:&#47;&#47;csstriggers.com&#47;
         – https:&#47;&#47;gist.github.com&#47;paulirish&#47;5d52fb081b3570c81e3a

      3. Vue 组件化实现
         Vue 提供了&lt;transition&gt;, &lt;transition-group&gt;两个组件来帮助我们实现业务中的动画
         需求，大大的提高了我们的开发效率。

         很神奇，有需求的同学可以看看源码，看看怎么实现的，应该能学到不少知识。</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/3e/e4/11c66f44.jpg" width="30px"><span>我叫兽儿…</span> 👍（20） 💬（4）<div>动手实现清单删除动画的时候，踩了一个小坑，在此记录一下，代码如下：
&lt;ul v-if=&quot;todolist.length&quot;&gt;
      &lt;transition-group name=&quot;list&quot; tag=&quot;ul&quot;&gt;
        &lt;li v-for=&quot;(item, index) in todolist&quot; :key=&quot;index&quot;&gt;
          &lt;input type=&quot;checkbox&quot; v-model=&quot;item.checked&quot; &#47;&gt;
          &lt;span&gt;{{ item.title }}&lt;&#47;span&gt;
          &lt;span @click=&quot;deleteItem($event, index)&quot; class=&quot;delete&quot;&gt;x&lt;&#47;span&gt;
        &lt;&#47;li&gt;
      &lt;&#47;transition-group&gt;
    &lt;&#47;ul&gt;
这里for循环我使用了index作为key，导致删除某一个li时，动画总是作用到最后一个li上。看了半天发现index会随着li的删除而变化，比如：我删除了第三个li，但是第四个会立马补上变成第三个，后面的li会依次向前补位，导致动画错乱。解决方式就是使用唯一的不会变的值作为key，比如id.

愿共同学习，共同进步！</div>2021-11-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/0e/3a/24b79152.jpg" width="30px"><span>Justin</span> 👍（12） 💬（5）<div>想請問一下

function enter(el,done){
     document.body.offsetHeight 
     el.style.transform = `translate(0,0)` 
     el.addEventListener(&#39;transitionend&#39;, done)
}
 document.body.offsetHeight 這一行的作用是什麼？
感謝</div>2021-11-05</li><br/><li><img src="" width="30px"><span>Geek_0c8aff</span> 👍（8） 💬（5）<div>&#47;&#47; bug, 删除todo的最后一项，加入垃圾桶的动画位置不对（0,0），以下是我的修改。
function removeTodo(e: any, i: number) {
      animate.el = e.target
      animate.show = true
      setTimeout(()=&gt;{
        todos.value.splice(i, 1)
      },100)
    }</div>2021-11-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/ec/68/06d59613.jpg" width="30px"><span>柒月</span> 👍（8） 💬（7）<div>页面切换动画的时候，要求路由组件必须要有个根元素包裹，不然动画不生效的。
https:&#47;&#47;stackoverflow.com&#47;questions&#47;65553121&#47;vue-3-transition-renders-non-element-root-node-that-cannot-be-animated</div>2021-11-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/75/4f/e22e91b2.jpg" width="30px"><span>雪狼</span> 👍（6） 💬（1）<div>课程非常棒，在学习过程中提几个建议

1、部分代码能加点注释更方便理解，比如enter函数
2、css没有写全，比如垃圾筐的，这倒也不是大问题
3、如果每讲，最后能有一个本讲完整的实例代码贴到最后，更方便查看
4、动画需要一个root节点包裹才能生效，课程中没有体现出来的</div>2021-12-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/f2/58/c5153d1d.jpg" width="30px"><span>Zachy</span> 👍（6） 💬（2）<div>&#47;&#47; 强迫症下把删除动画精准还原到垃圾桶位置，暂时没加抛物线，否则效果更佳。
const {animate,beforeEnter, enter, afterEnter,removeTodo}  = useAnimation();

function useAnimation(){
  let animate = reactive({
    show: false,
    el: null,
  });
  const dustbin ={ 
    el:null,
    pos:[],
    init(queryStr){
      this.el = document.querySelector(queryStr);
      this.getPos();
    },
    getPos(){
      const { left, top} = this.el.getBoundingClientRect();
      this.pos[0] = left;
      this.pos[1] = top;
    }
  }
  function beforeEnter(el) {
    let dom = animate.el;
    let rect = dom.getBoundingClientRect();
    const  aniEl=  document.querySelector(&#39;.animate&#39;);
    &#47;&#47;动画元素 调整到dustbin的位置,也可以css直接写精准位置
    aniEl.style.left = `${dustbin.pos[0]}px`; 
    aniEl.style.top= `${dustbin.pos[1]}px`;
    &#47;&#47;计算并赋值偏移量
    let dx = dustbin.pos[0] - rect.left;
    let dy = dustbin.pos[1] - rect.top;
    el.style.transform = `translate(-${dx}px, ${dy*-1}px)`;
  }
  function enter(el, done) {
    document.body.offsetHeight;
    el.style.transform = `translate(0,0)`;
    el.addEventListener(&quot;transitionend&quot;, done);
  }
  function afterEnter(el) {
    animate.show = false;
    el.style.display = &quot;none&quot;;
  }
function removeTodo(e,i){
      animate.el = e.target
      animate.show = true
      todos.value.splice(i, 1);
      dustbin.init(&#39;.dustbin&#39;);
    }
  return {animate,beforeEnter,enter,afterEnter,removeTodo}
}</div>2021-11-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1c/6b/91/168e10a1.jpg" width="30px"><span>bugu</span> 👍（6） 💬（5）<div>问一个问题：列表动画那一部分transition-group ，设置 tag 的作用是什么呢？我尝试去掉tag，没有看出什么差异。
还有下面move的动画设定
.flip-list-move {
  transition: transform 2s ease;
}
我尝试修改和删除，也没有看出什么差异。

请帮忙指定一下，谢谢老师和各位同学</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/90/ddb4aba4.jpg" width="30px"><span>微妙</span> 👍（4） 💬（1）<div>el.style.transform = `translate(-${x}px, ${y}px)` 
模板字符串中当x为负数时会被识别为 --xpx，导致transform识别不出而变为 translate(0px, 0px);
应先计算好x、y的值，然后在模板字符串内赋值</div>2021-11-08</li><br/><li><img src="" width="30px"><span>Geek_1ecc87</span> 👍（3） 💬（2）<div>为什么要在v-for li中指定key添加任务的时候动画才会生效？</div>2022-01-14</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/7icj7X67vvABNjC284ichONicn6PFeZSUAdclWKr8FJIHfWUzx6azxPuDcCNODV8ZmqXMAUibvJZiaXsYxKCmtJfxkg/132" width="30px"><span>于三妮</span> 👍（2） 💬（1）<div>请问那个红叉叉是什么格式的，这种图片要哪里找</div>2021-11-16</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/58/ba171e09.jpg" width="30px"><span>小胖</span> 👍（2） 💬（2）<div>反馈个bug,最近一条todo删除，y坐标的值会为0</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/58/ba171e09.jpg" width="30px"><span>小胖</span> 👍（2） 💬（1）<div>大圣老师，问下，在enter函数里面为什么需要添加一行document.body.offsetHeight，我尝试，不添加这句动画就不会生效；
</div>2021-11-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/01/ea/d0be0574.jpg" width="30px"><span>笑叹尘世</span> 👍（2） 💬（1）<div>let x = window.innerWidth - rect.left - 60
弱弱的问一下这个60是哪里的来的数值？</div>2021-11-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/eb/af/e49af9a8.jpg" width="30px"><span>JC.彦</span> 👍（2） 💬（1）<div>let dom = animate.el为什么获取的是要删除的li元素？</div>2021-11-08</li><br/><li><img src="" width="30px"><span>Geek_a84b8d</span> 👍（2） 💬（1）<div>思考题 可以在@keyframes move多设置几个百分比和对应的top值</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/c3/58/ba171e09.jpg" width="30px"><span>小胖</span> 👍（2） 💬（1）<div>我想问下大圣老师，这些个字体图标是有什么vs插件么？</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/56/ea/32608c44.jpg" width="30px"><span>giteebravo</span> 👍（7） 💬（0）<div>
列表动画那一部分，tag 的目的是给 li 渲染一个 ul 父元素，且要给 v-for 指定一个 key 属性，否则动画是不会有效果的。</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/e2/d8/913105f5.jpg" width="30px"><span>Summer夏</span> 👍（4） 💬（0）<div>&lt;ul v-if=&quot;todos.length&quot;&gt; 这个v-if不去掉的话  列表删除完后再新增第一条是没有动画的。</div>2022-04-28</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（2） 💬（0）<div>打卡
1. 使用animate.css的shake动画改变弹窗元素的classname
2. 使用transition组件，分别在enter，leave设置对应的特定类名样式
 3.使用transition的js对应的钩子实现</div>2021-11-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/30/55/ae/de8cf97c.jpg" width="30px"><span>Soffio</span> 👍（1） 💬（0）<div>思考题：
 &lt;span :class=&quot;[&#39;dustbin&#39;, { shake: isDel }]&quot;&gt;🗑️&lt;&#47;span&gt;

.shake {
  animation: shake 0.82s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes shake {
  10%,
  90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%,
  80% {
    transform: translate3d(2px, 0, 0);
  }

  30%,
  50%,
  70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%,
  60% {
    transform: translate3d(4px, 0, 0);
  }
}
1、点击删除的时候，通过一个布尔值添加抖动的类，开启个定时器跟图标走向垃圾桶的时长一样，定时器里面把布尔值设置true，然后nextTick的时候把布尔值设为false。</div>2022-09-04</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTLok8xc4lQfDjjxDUF6iatEUYibVqYeGRU22EtIO3xcgjSvuO7vKwfKSc3cGoNOicp1icQlC2vOKaIGmw/132" width="30px"><span>Geek_27b6ec</span> 👍（1） 💬（0）<div>最后一个垃圾桶的完整代码有么</div>2022-02-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/04/1c/7899bab4.jpg" width="30px"><span>南城</span> 👍（1） 💬（0）<div>过渡我到觉得实用率一般，其实接口效能，缓存上去了用户体感就好了，动画的过渡还不如状态中间状态确定性开的更符合用研。不过学是真学到了，我也不常用</div>2022-02-05</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/16/0b/18dce773.jpg" width="30px"><span>HAYWAEL</span> 👍（1） 💬（0）<div>思考题

@keyframes shake {

    0%,
    100% {
        transform: translateX(0)
    }

    10% {
        transform: translateX(-9px)
    }

    20% {
        transform: translateX(8px)
    }

    30% {
        transform: translateX(-7px)
    }

    40% {
        transform: translateX(6px)
    }

    50% {
        transform: translateX(-5px)
    }

    60% {
        transform: translateX(4px)
    }

    70% {
        transform: translateX(-3px)
    }

    80% {
        transform: translateX(2px)
    }

    90% {
        transform: translateX(-1px)
    }
}</div>2022-01-05</li><br/><li><img src="" width="30px"><span>一起</span> 👍（1） 💬（0）<div>请问为什么在 afterEnter这个函数中，不设置el.style.display这句代码，动画会在结束时会停顿一两秒才消失？</div>2021-11-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/7d/4d/d98865b2.jpg" width="30px"><span>老实人Honey</span> 👍（0） 💬（0）<div>代码能不能跑起来呢 有点怀疑</div>2023-11-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/0d/21bf48eb.jpg" width="30px"><span>NULL</span> 👍（0） 💬（0）<div>为什么好像新输入的第一项……动画效果没有实现 o_O 要从第二项开始才有预期的效果？！

参考：
https:&#47;&#47;vuejs.org&#47;guide&#47;built-ins&#47;transition.html#transition-on-appear
若对初始状态希望获得同样的过渡效果，只需&lt;transition-group appear&gt;直接添加 appear 属性即可。

可全体离开、消失的情况，还未完善过渡补齐……
</div>2023-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/0d/21bf48eb.jpg" width="30px"><span>NULL</span> 👍（0） 💬（0）<div>好像发现为什么列表动画那部分中，从【暂无数据】状态来新添加【第一条】&lt;li&gt;时，这第一条&lt;li&gt;没有如后续列表项那样明显的动画效果呢？
是因为这里存在【暂无数据】这行&lt;div&gt;的消失，而……显得第一条出现的动效在视觉上不易察觉呢？还是在动效运行逻辑上还有这一丝bug不足？</div>2023-09-02</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/5b/25/d78cc1fe.jpg" width="30px"><span>都市夜归人</span> 👍（0） 💬（0）<div>```html
&lt;template&gt;
	&lt;div&gt;
		&lt;span class=&quot;dustbin&quot;&gt;🗑&lt;&#47;span&gt;
		&lt;div class=&quot;animate-wrap&quot;&gt;
			&lt;Transition @before-enter=&quot;beforeEnter&quot; @enter=&quot;enter&quot; @after-enter=&quot;afterEnter&quot;&gt;
				&lt;div class=&quot;animate&quot; v-show=&quot;animate.show&quot;&gt;📋&lt;&#47;div&gt;
			&lt;&#47;Transition&gt;
		&lt;&#47;div&gt;
		&lt;input type=&quot;text&quot; v-model=&quot;title&quot; @keydown.enter=&quot;addTodo&quot; &#47;&gt;
		&lt;button v-if=&quot;active &lt; all&quot; @click=&quot;clear&quot;&gt;清理&lt;&#47;button&gt;
		&lt;div v-if=&quot;todos?.length&quot;&gt;
			&lt;TransitionGroup name=&quot;flip-list&quot; tag=&quot;ul&quot;&gt;
				&lt;li v-for=&quot;(todo, i) in todos&quot; :key=&quot;todo.title&quot;&gt;
					&lt;input type=&quot;checkbox&quot; v-model=&quot;todo.done&quot; &#47;&gt;
					&lt;span :class=&quot;{ done: todo.done }&quot;&gt;{{ todo.title }}&lt;&#47;span&gt;
					&lt;span class=&quot;remove-btn&quot; @click=&quot;removeTodo($event, i)&quot;&gt;❌&lt;&#47;span&gt;
				&lt;&#47;li&gt;
			&lt;&#47;TransitionGroup&gt;
		&lt;&#47;div&gt;
		&lt;div v-else&gt;暂无数据&lt;&#47;div&gt;
		&lt;div&gt;
			全选&lt;input type=&quot;checkbox&quot; v-model=&quot;allDone&quot;&gt;
			&lt;span&gt;{{ active }} &#47; {{ all }}&lt;&#47;span&gt;
		&lt;&#47;div&gt;
	&lt;&#47;div&gt;
	&lt;Transition name=&quot;modal&quot;&gt;
		&lt;div class=&quot;info-wrapper&quot; v-if=&quot;showModal&quot;&gt;
			&lt;div class=&quot;info&quot;&gt;
				请输入内容
			&lt;&#47;div&gt;
		&lt;&#47;div&gt;
	&lt;&#47;Transition&gt;
&lt;&#47;template&gt;
&lt;script setup&gt;
import { ref, reactive, computed } from &quot;vue&quot;;
debugger
let animate = reactive({
	show: false, el: null
})

function beforeEnter(el) {
	debugger
	let dom = animate.el
	let rect = dom.getBoundingClientRect()
	let x = window.innerWidth - rect.left - 60
	let y = rect.top - 10
	el.style.transform = `translate(-${x}px, ${y}px)`
}
function enter(el, done) {
	document.body.offsetHeight
	el.style.transform = `translate(0,0)`
	el.addEventListener(&#39;transitionend&#39;, done)
}
function afterEnter(el) {
	animate.show = false
	el.style.display = &#39;none&#39;
}

import { useTodos } from &#39;.&#47;useTodos.js&#39;;
let { title, todos, addTodo, clear, active, all, allDone, showModal, removeTodo } = useTodos();
&lt;&#47;script&gt;
```
上面的代码在chrome和edge浏览器中都没有出现购物车的动画效果
</div>2023-08-14</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/8a/8a/7c1baa25.jpg" width="30px"><span>buoge</span> 👍（0） 💬（0）<div>“...清单应用其他代码” 请问下这个语法时什么意思？注释？</div>2023-05-12</li><br/>
</ul>