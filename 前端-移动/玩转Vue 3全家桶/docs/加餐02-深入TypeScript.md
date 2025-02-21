你好，我是大圣。

在讲组件化的进阶开发篇之前，我想在全家桶实战篇的最后，用一讲的篇幅，来专门聊一下TypeScript。希望你在学完这一讲之后，能对TypeScript有一个全面的认识。

另外，今天我会设置很多实战练习，一边阅读一边敲代码的话，学习效果更好。而且，这次加餐中的全部代码都是可以在线完成的，建议你打开[这个链接](https://www.typescriptlang.org/play?#code/FAehAJC+9Q66MA3lHnrQMhGGO5QgB6F+E9gnU0AByhZBKA)，把下面的每行代码都跟着敲一遍。

## TypeScript入门

对于TypeScript，你首先要了解的是，TypeScript 可以在JavaScript的基础上，对变量的数据类型加以限制。TypeScript 中最基本的数据类型包括布尔、数字、字符串、null、undefined，这些都很好理解。

在下面的代码中，我们分别定义了这几个数据类型的变量，你能看到，当我们把number类型的变量price赋值字符串时，就会报错，当我们把数组 me 的第一个元素 me\[0] 的值修改为数字时，也会报错。

```typescript
let courseName:string = '玩转Vue 3全家桶'
let price:number = 129
price = '89' //类型报错
let isOnline:boolean = true
let courseSales:undefined
let timer:null = null
let me:[string,number] = ["大圣",18]
me[0] = 1 //类型报错
```
<div><strong>精选留言（25）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（11） 💬（1）<div>不建议用中文变量名，其中一个原因是手敲的时候，需要来回转换中英文输入法。😅</div>2021-12-03</li><br/><li><img src="" width="30px"><span>require</span> 👍（4） 💬（1）<div>学得时候是typescript, 用的时候就变成了anyscript😂</div>2021-12-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/91/9d/ff31f7a1.jpg" width="30px"><span>山雨</span> 👍（2） 💬（1）<div>大圣老师，实战篇代码啥时候更新</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/ff/d1/7a4a6f4f.jpg" width="30px"><span>风一样</span> 👍（1） 💬（1）<div>请问老师，let todos:Ref = ref([{title:&#39;学习Vue&#39;,done:false}])这条语句中，用 Ref 和 不用 Ref，有什么区别呢？</div>2021-12-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/0c/eb/b101e3c6.jpg" width="30px"><span>Lanb Wang</span> 👍（0） 💬（1）<div>跟着敲了一遍，然后现在看自己敲得是啥子都不晓得
</div>2022-02-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/40/94/afd0919c.jpg" width="30px"><span>起風了</span> 👍（0） 💬（1）<div>想问一下type和interface有什么区别?什么时候用type,什么时候用interface?</div>2022-01-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/f9/78/0cb10cad.jpg" width="30px"><span>韩棒</span> 👍（0） 💬（1）<div>大圣老师 Ref在使用的时候有一个 “Ref”仅表示类型，但在此处却作为值使用-ts。是需要配置tsconfig.json吗？</div>2021-12-03</li><br/><li><img src="" width="30px"><span>2345</span> 👍（27） 💬（1）<div>个人不觉得中文变量能帮助理解。</div>2022-02-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/e9/42/1de79e71.jpg" width="30px"><span>南山</span> 👍（9） 💬（1）<div>type RecursivePartial&lt;T&gt; = {
  [P in keyof T]?:
    T[P] extends (infer U)[] ? RecursivePartial&lt;U&gt;[] :
    T[P] extends object ? RecursivePartial&lt;T[P]&gt; :
    T[P];
};</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/19/2c/47/b0931f00.jpg" width="30px"><span>江南烟雨时</span> 👍（7） 💬（0）<div>一看就会，一做就废。</div>2022-04-21</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（7） 💬（2）<div>有个地方挺神奇的哈，不打印你是不会理解这段代码的。

enum 课程评分 { 好, 非常好, 嘎嘎好 }
console.log(课程评分[&#39;好&#39;] === 0) &#47;&#47; true
console.log(课程评分[0] === &#39;好&#39;)  &#47;&#47; true

为啥课程评分[&#39;好&#39;] === 0 ， 又 课程评分[0] === &#39;好&#39; 呢？

console.log(课程评分) 

```
[LOG]: {
  &quot;0&quot;: &quot;好&quot;,
  &quot;1&quot;: &quot;非常好&quot;,
  &quot;2&quot;: &quot;嘎嘎好&quot;,
  &quot;好&quot;: 0,
  &quot;非常好&quot;: 1,
  &quot;嘎嘎好&quot;: 2
} 
```
原来如此~


</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/c8/4a/3a322856.jpg" width="30px"><span>ll</span> 👍（4） 💬（0）<div>ts 是 js 的 “超集” 其将 js 缺失的 “静态类型” 补上了，此外实现了一些“新的特性”，例如，函数重载。
js 原生不支持这种语言特性，是可以自己写代码实现的。而 ts 原生提供了这些“特性”，对于使用者的“成本” 就是要额外学习一些“新语法”。当熟悉这些新的写法后，我们在工程上收获的就是所谓“出错要趁早”，在“编译阶段”就发现错误，不用等到“运行时”发生错误，造成更大的损失。额外的，静态类型系统也给 lint 类插件提供了“技术支持”，使得在编写代码的时候得到更好的提示。

简单说，ts “让”我们的是更严格的写代码，“先要有，才能用，后边不能随心变”。是不是太“严格”了，是“严格”了，这也动态语言与静态语言是经常被争论的一个点。但 ts 在“灵活性”上也作了工作，比如所谓的泛型，以及一系列与之配套的API。

 当然只谈感受作用不是很大，要想用的好，还是要不断的实践。</div>2021-12-06</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/GPm0HkJtcItC1Cbo1Mh1giaQAibho4rp13Kpwv9BEAUW6SMXUXRwGUArskchaqrjy2TgwFwD9CltML5vXvSDiacFg/132" width="30px"><span>许强</span> 👍（1） 💬（0）<div>
 import { ref ,Ref} from &#39;vue&#39;
 interface Todo{ 
     title:string,
      done:boolean
 }
 let todos:Ref = ref([{title:&#39;学习Vue&#39;,done:false}])
 
这段代码貌似没使用到 Todo 这个接口把？</div>2023-01-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2a/fa/79/c5cfe88c.jpg" width="30px"><span>淡若清风过</span> 👍（1） 💬（0）<div>slots，attrs，emit这些是什么类型？</div>2022-06-21</li><br/><li><img src="" width="30px"><span>杨林山</span> 👍（1） 💬（0）<div>示例中Interface API的属性全都是固定接口名，那像restful方式的接口地址该如何定义呢？

get &#47;users&#47;:userId
</div>2022-04-11</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTIueaIvXNRZrZKtSt5oODLLrsYEa4txMhHE5PWibziawMApUiaOIWgvl7d0MC6S2AeKWPA5ictWeSdlbA/132" width="30px"><span>Geek_b2e48c</span> 👍（0） 💬（0）<div>我基本上是好几个弹窗封了一个组件，每个弹窗内容v-if渲染。我会定义一个弹窗的枚举区分，但是弹窗展示时调用getData函数获取数据的方法我就写成了策略模式，刚开始比较好用，但是后面getdata必须要写满所有的弹窗类型，否则会报错，有什么办法可以按需创建方法吗？</div>2023-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/55/28/66bf4bc4.jpg" width="30px"><span>荷兰小猪8813</span> 👍（0） 💬（1）<div>
type Partial1&lt;T&gt; = {
    [K in keyof T]?:T[K]
}

T[K] 这是个啥语法？？</div>2023-07-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/cd/f6/3224464a.jpg" width="30px"><span>前端队长</span> 👍（0） 💬（0）<div>type Partial1&lt;T&gt; = {
    [K in keyof T]?: T[K] extends object ? Partial1&lt;T[K]&gt; : T[K]
}
这样？</div>2022-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/22/db/44/fe39de59.jpg" width="30px"><span>恭喜恭喜 ！！！</span> 👍（0） 💬（0）<div>ts定义变量类型为undefined 或者null后还可以再重新赋值吗</div>2022-07-25</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/9b/9a/7c87614b.jpg" width="30px"><span>YK菌</span> 👍（0） 💬（0）<div>感觉大圣老师的语速是越来越快拉~~</div>2022-04-30</li><br/><li><img src="http://thirdwx.qlogo.cn/mmopen/vi_32/sgEfkeMSIIibeH4l0HS8uwM6PGY3DSHoW5tV9l1hDQ06tr3OnI7F545Wdxsh59rqOKnzjLUpCcEqic3P9zZbKzPQ/132" width="30px"><span>楼外楼</span> 👍（0） 💬（0）<div>下面的泛型可以理解，但是 ts的 extends 用法理解起来确实吃力</div>2022-04-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2c/27/8a/d65e34c4.jpg" width="30px"><span>木子初秋</span> 👍（0） 💬（0）<div>看了之后，终于看懂了TS开发的项目中有很多的运用泛型的地方，对于泛型的理解老师讲的太通透了。</div>2022-02-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/5b/9e/a8dec12d.jpg" width="30px"><span>cwang</span> 👍（0） 💬（0）<div>So Cool !</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/cd/ed/825d84ee.jpg" width="30px"><span>费城的二鹏</span> 👍（0） 💬（0）<div>太实用了，周末要亲手试试，避免用any，减少出错可能。</div>2021-12-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/14/3f/a8/8da58e53.jpg" width="30px"><span>海阔天空</span> 👍（0） 💬（0）<div>如果可以的话，在项目中引用ts还是很有必要的。对项目的规范和要求也相对提升。</div>2021-12-03</li><br/>
</ul>