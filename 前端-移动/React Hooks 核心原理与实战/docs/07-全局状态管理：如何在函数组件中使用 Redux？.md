你好，我是王沛。今天我们来聊聊怎么在函数组件中使用Redux。

Redux 作为一款状态管理框架啊，是公认的React 开发中最大的一个门槛，但同时呢，它也是 React 开发人员必须掌握的一项技能。因为只有熟练应用 Redux，你才能更加灵活地使用 React，来从容应对大型项目的开发难题。

这里我要说句题外话。Redux诞生于 2015 年，也就是React 出现之后一年多。虽然一开始是由第三方开发者开源，不是 Facebook 官方，但是也迅速成为了最为主流的 React 状态管理库。而且，之后 Redux 跟它的开发者 Dan Abbramov 和 Andrew Clark 一起，都被 Facebook 收编，成为 React 官方生态的一部分。侧面可以看到 Redux 在React 中的重要作用。

需要说明的是，Redux 作为一套独立的框架，虽然可以和任何 UI 框架结合起来使用。但是因为它基于不可变数据的机制，可以说，基本上就是为 React 量身定制的。

不过你可能会说，Redux 上手比较难，该怎么办呢？的确是这样，因Redux引入了一些新的编程思想，还有比较繁琐的样板代码，确实带来了一定的上手难度。

但是你不要担心，今天这节课，我会通过具体的例子带你上手Redux。而且我会讲解 Redux 要解决什么问题，引入了什么样的新概念，争取能从本质上去理解 Redux 的理念和使用方法，提高你举一反三的能力。
<div><strong>精选留言（22）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/f2/4f/59bd4141.jpg" width="30px"><span>Isaac</span> 👍（8） 💬（7）<div>老师，redux 如何和自定义 hooks 很好的结合起来？
比如常见的获取一个列表，我封装成一个 useList 的自定义 hook，那么就可以在多个组件中使用 useList。但是每次 useList() 的时候，都会触发接口调用，获取到的数据源组件之间无法共享。
</div>2021-06-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/11/b1/4379e143.jpg" width="30px"><span>H</span> 👍（8） 💬（2）<div>请问老师在这个专栏更新完之后还有没有其他的计划》
学习老师的每一篇文章以及视频都有醍醐灌顶，任脉打通的感觉。
很期待老师接着出一个关于解读react源码的课程，很期待，很期待。
不知道老师除了react的专栏和视屏还有没有其它的课程，很想很想跟着去学习学习。</div>2021-06-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/3b/43/dedbfc4c.jpg" width="30px"><span>Redmi_18117543951</span> 👍（1） 💬（1）<div>终于知道啥是异步Action了，之前被名字吓住，学过才发现原来实际上很简单呀</div>2021-07-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/d1/ad/1aed3dec.jpg" width="30px"><span>小飞侠</span> 👍（0） 💬（2）<div>小结里面，最后一个词有错别字（∩▽∩），既能=&gt;技能</div>2022-03-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/fa/21/abb7bfe3.jpg" width="30px"><span>Vongola</span> 👍（0） 💬（1）<div>const data = useSelectore(state =&gt; state.data);
这里应该是useSelector吧？</div>2021-08-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/10/34/705572e6.jpg" width="30px"><span>陈芳</span> 👍（0） 💬（1）<div>在 react-redux 的实现中，为了确保需要绑定的组件能够访问到全局唯一的 Redux Store，利用了 React 的 Conext 机制去存放 Store 的信息。
应该是Context</div>2021-07-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/fc/c3/0991edfc.jpg" width="30px"><span>闲闲</span> 👍（0） 💬（1）<div>老师我有两个问题麻烦问下，
1、如果项目里面状态值特别多，业务比较复杂，感觉redux就很容易造成一些不知道哪里引起的重复渲染，导致组件频繁渲染，这个问题有啥好的办法吗？
2、使用redux，怎么实现A请求完了再发B请求呢？</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/51/4d/0aceadde.jpg" width="30px"><span>腾挪</span> 👍（30） 💬（0）<div>给极客时间网页版提一个建议，强烈建议网页版也能像手机端一样，对写得好的文章进行点赞👍。本文写得通俗易懂，说明王老师水平很高，值得赞。</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/bd/ec/cc7abf0b.jpg" width="30px"><span>L</span> 👍（4） 💬（2）<div>总感觉redux这套已经过时了。样板代码之类的实在是太多太繁琐了。同样是这种统一管理数据的方式，vuex就比他好很多。感觉现在很多玩的都是约定式</div>2021-06-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/5d/22/6e78881e.jpg" width="30px"><span>Aaron</span> 👍（4） 💬（0）<div>可以通过在action添加其他字段，如payload来传递需要加减的数值</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/2c/0f7baf3a.jpg" width="30px"><span>Change</span> 👍（3） 💬（1）<div>老师问个问题，redux toolkit和redux有啥区别，在项目用哪个更方便一些</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/4a/97/414d0e39.jpg" width="30px"><span>kotumato</span> 👍（3） 💬（0）<div>function counterReducer(state = initialState, action) {
    switch (action.type) {
        case &#39;counter&#47;incremented&#39;: return {value: state.value + action.payload}
        case &#39;counter&#47;decremented&#39;: return {value: state.value - action.payload}
        default: return state
    }
}
const incrementAction = { type: &#39;counter&#47;incremented&#39;, payload: 10 };
store.dispatch(incrementAction); &#47;&#47; 计数器加 10
const decrementAction = { type: &#39;counter&#47;decremented&#39;,  payload: 10 };
store.dispatch(decrementAction); &#47;&#47; 计数器减 10</div>2021-06-08</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/Q0j4TwGTfTJVpGfkkH8rqC7nTmX8DlTZ3lMQpCic3a7rjUTXqnzv5bhXfQwQ15SxJF5CETbVegcHFbQNc4XfGyA/132" width="30px"><span>Geek_9b9b7e</span> 👍（1） 💬（0）<div>为什么要异步action?老师的答案是：“发送请求获取数据并进行错误处理这个逻辑是不可重用的。假设我们希望在另外一个组件中也能发送同样的请求，就不得不将这段代码重新实现一遍。“

也就是说，redux-thunk 要做的就是【把这段代码实现一遍】。

就是下面这段代码：
    &#47;&#47; 请求发送时
    dispatch({ type: &#39;FETCH_DATA_BEGIN&#39; });
    fetch(&#39;&#47;some-url&#39;).then(res =&gt; {
      &#47;&#47; 请求成功时
      dispatch({ type: &#39;FETCH_DATA_SUCCESS&#39;, data: res });
    }).catch(err =&gt; {
      &#47;&#47; 请求失败时
      dispatch({ type: &#39;FETCH_DATA_FAILURE&#39;, error: err });
    });

为了redux-thunk能重复使用这段代码，我们还需要定义一个 actionCreator 函数，用来返回这段代码。

我们为啥不直接使用自定义hooks呢，hooks的主要功能不就是”代码复用“。

例如：
useUserList(dispatch =&gt; {
    return useCallback(() =&gt; {
        &#47;&#47; 请求发送时
    dispatch({ type: &#39;FETCH_DATA_BEGIN&#39; });
    fetch(&#39;&#47;some-url&#39;).then(res =&gt; {
      &#47;&#47; 请求成功时
      dispatch({ type: &#39;FETCH_DATA_SUCCESS&#39;, data: res });
    }).catch(err =&gt; {
      &#47;&#47; 请求失败时
      dispatch({ type: &#39;FETCH_DATA_FAILURE&#39;, error: err });
    }), [dispatch]);
    });
}) </div>2022-03-07</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/ed/23/73af9e5c.jpg" width="30px"><span>山丘smith18651579836</span> 👍（1） 💬（0）<div>为什么不用usecontext</div>2022-01-23</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/db/ba/304a9a4a.jpg" width="30px"><span>Juntíng</span> 👍（1） 💬（0）<div>Hooks 的出现，结合 context API，用管理全局状态更加简洁易懂，只是在数据流变更机制上不容易捕获，但是却比 Redux 带来的代码复杂度的增加、样板代码过多，不易于阅读上来说我更加偏爱 hooks + ContextAPI 。</div>2021-06-22</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/28/66/d5/f36495bd.jpg" width="30px"><span>81</span> 👍（1） 💬（1）<div>异步操作需要传递数据的时候，可以这样操作嘛？dispath((dispatch,playload)=&gt;{fetch(&quot;&#47;some-url&quot;，{playload}).then(dispatth({type:&quot;&#47;update&#47;msg&quot;,playload}))})；。 是在dipatch派发的函数中的第二个参数位置传数据  第一个参数位置 写dispatch？</div>2021-06-18</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/fc/0f/df9edecd.jpg" width="30px"><span>小灰</span> 👍（1） 💬（0）<div>
import { createStore } from &#39;redux&#39;

&#47;&#47; 定义 Store 的初始值
const initialState = { value: 0 }

&#47;&#47; Reducer，处理 Action 返回新的 State
function counterReducer(state = initialState, action) {
  switch (action.type) {
    case &#39;counter&#47;incremented&#39;:
      return { value: state.value + 1 }
    case &#39;counter&#47;decremented&#39;:
      return { value: state.value - 1 }
    case &#39;counter&#47;add&#39;: 
      return {
          ...state,
          value: stat.value + action.data
      }
    default:
      return state
  }
}

&#47;&#47; 利用 Redux API 创建一个 Store，参数就是 Reducer
const store = createStore(counterReducer)

&#47;&#47; Store 提供了 subscribe 用于监听数据变化
store.subscribe(() =&gt; console.log(store.getState()))

&#47;&#47; 计数器加 1，用 Store 的 dispatch 方法分发一个 Action，由 Reducer 处理
const incrementAction = { type: &#39;counter&#47;incremented&#39; };

store.dispatch(incrementAction);
&#47;&#47; 监听函数输出：{value: 1}

&#47;&#47; 计数器减 1
const decrementAction = { type: &#39;counter&#47;decremented&#39; };
store.dispatch(decrementAction)
&#47;&#47; 监听函数输出：{value: 0}

const add = (data)=&gt;({type: &#39;counter&#47;add&#39;, data});
store.dispatch(add(5));</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/2b/e4/af/f8cf4bc2.jpg" width="30px"><span>Light 胖虎</span> 👍（0） 💬（0）<div>这样写可以吗，老师。在定义action对象的时候增加一个字段用来存储每次计算的步长（默认为1）
&#47;&#47; 定义 Store 的初始值const initialState = { value: 0，step: 1 }
function counterReducer(state = initialState, action) 
{ switch (action.type) { 
case &#39;counter&#47;incremented&#39;: return { value: state.value + action.step || 1} 
case &#39;counter&#47;decremented&#39;: return { value: state.value - action.step || 1 } 
default: return state 
}}


return (
 dispatch({ type: &#39;counter&#47;incremented&#39;,action: 2 })} &gt;+ {count}
 dispatch({ type: &#39;counter&#47;decremented&#39; })} &gt;-
)}</div>2021-12-28</li><br/><li><img src="" width="30px"><span>Geek_dbfc78</span> 👍（0） 💬（0）<div>使用action对象属性作为 表现层 -&gt; 数据层 参数传递的入口，实现动态值的加减</div>2021-10-09</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/29/05/6f/6a47d5b7.jpg" width="30px"><span>君</span> 👍（0） 💬（0）<div>有个问题
假设我页面有表单
表单控件复用程度很大
如何更优雅的管理
1、表单数据源
2、表单鉴权
3、表单鉴权后的数据再次过滤应对不同场景
4、表单初始值确定，同步和异步的情况
5、维护一个表单值准备好的状态并以此为准界定初始查询

感觉表单这一块还是蛮好玩的</div>2021-07-06</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/c0/99/259a412f.jpg" width="30px"><span>Geeker</span> 👍（0） 💬（0）<div>理解了异步 action</div>2021-06-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/2d/d4/76ffbdfc.jpg" width="30px"><span>珍惜眼前人</span> 👍（0） 💬（2）<div>老师，请教下：‘’同组件多个实例的状态共享：某个页面组件初次加载时，会发送请求拿回了一个数据，切换到另外一个页面后又返回。这时数据已经存在，无需重新加载。设想如果是本地的组件 state，那么组件销毁后重新创建，state 也会被重置，就还需要重新获取数据。‘’

关于这点，我觉得如果切换页面返回后，相当于重新加载这个页面，又会进入到初始化的状态，就会重新请求数据呢？</div>2021-06-08</li><br/>
</ul>