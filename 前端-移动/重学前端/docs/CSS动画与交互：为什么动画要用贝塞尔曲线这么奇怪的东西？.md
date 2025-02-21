你好，我是winter，今天我们来学习一下CSS的动画和交互。

在CSS属性中，有这么一类属性，它负责的不是静态的展现，而是根据用户行为产生交互。这就是今天我们要讲的属性。

首先我们先从属性来讲起。CSS中跟动画相关的属性有两个：animation和transition。

## animation属性和transition属性

我们先来看下animation的示例，通过示例来了解一下animation属性的基本用法:

```CSS
@keyframes mykf
{
  from {background: red;}
  to {background: yellow;}
}

div
{
    animation:mykf 5s infinite;
}
```

这里展示了animation的基本用法，实际上animation分成六个部分：

- animation-name 动画的名称，这是一个keyframes类型的值（我们在第9讲“CSS语法：除了属性和选择器，你还需要知道这些带@的规则”讲到过，keyframes产生一种数据，用于定义动画关键帧）；
- animation-duration 动画的时长；
- animation-timing-function 动画的时间曲线；
- animation-delay 动画开始前的延迟；
- animation-iteration-count 动画的播放次数；
- animation-direction 动画的方向。
<div><strong>精选留言（7）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（26） 💬（1）<div>const tweenFns = {
  linear: (from, to, t, d) =&gt; from + (to - from) * (t &#47; d)
}

&#47;**
 * only support &quot;linear&quot; timing-function
 * duration unit is &quot;ms&quot;
 * @param {HTMLElement} el
 * @param {({prop: String, value: String, duration: Number})[]} list
 *&#47;
function transitionTo(el, list) {
  let startTime
  let oldStyle = new Map()
  let newStyle = new Map()
  for (let prop of list) {
    oldStyle.set(prop.name, window.getComputedStyle(el)[prop.name])
  }
  for (let prop of list) {
    el.style[prop.name] = prop.value
  }
  for (let prop of list) {
    newStyle.set(prop.name, window.getComputedStyle(el)[prop.name])
  }
  for (let prop of list) {
    el.style[prop.name] = oldStyle.get(prop.name)
  }


  requestAnimationFrame(run)

  function run(time) {
    if (startTime == null) startTime = time
    let t = time - startTime
    let done = true
    for (let prop of list) {
      if (t &gt;= prop.duration) {
        el.style[prop.name] = newStyle.get(prop.name)
        continue
      }
      done = false
      let oldPropValue = oldStyle.get(prop.name)
      let newPropValue = newStyle.get(prop.name)
      if (prop.name === &#39;transform&#39;) {
        if (oldPropValue === &#39;none&#39;) oldPropValue = &#39;matrix(1, 0, 0, 1, 0, 0)&#39;
        if (newPropValue === &#39;none&#39;) newPropValue = &#39;matrix(1, 0, 0, 1, 0, 0)&#39;
      }
      el.style[prop.name] = generateNewStyle(oldPropValue, newPropValue, t, prop.duration, tweenFns.linear)
    }
    if (!done) requestAnimationFrame(run)
  }
}

function generateNewStyle(from, to, t, duration, tweenFn) {
  let fromExp = &#47;[\d.-]+&#47;g
  let toExp = &#47;[\d.-]+&#47;g
  let fromMatch
  let toMatch
  let result = &#39;&#39;
  let lastIndex = 0
  while (fromMatch = fromExp.exec(from)) {
    result += from.slice(lastIndex, fromMatch.index)
    toMatch = toExp.exec(to)
    result += tweenFn(+fromMatch[0], +toMatch[0], t, duration)
    lastIndex = fromExp.lastIndex
  }
  result += from.slice(lastIndex)
  return result
}</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/15/35/d0/f2ac6d91.jpg" width="30px"><span>阿成</span> 👍（21） 💬（3）<div>跟CSS的transition比，JS更加偏向指令式，而CSS更加偏向声明式，当然，这本身也是两门语言自身的特点，CSS用法简单直观，JS则在控制方面有更大的灵活性。

上面我只实现了 linear timing function（其他的函数实现网上大把大把的...），具体用法如下：
&lt;!DOCTYPE html&gt;
&lt;html lang=&quot;en&quot;&gt;
&lt;head&gt;
  &lt;meta charset=&quot;UTF-8&quot;&gt;
  &lt;title&gt;Document&lt;&#47;title&gt;
  &lt;style&gt;
    #ball {
      width: 100px;
      height: 100px;
      background: blue;
    }
  &lt;&#47;style&gt;
&lt;&#47;head&gt;
&lt;body&gt;
  &lt;div id=&quot;ball&quot;&gt;&lt;&#47;div&gt;

  &lt;script src=&quot;transition.js&quot;&gt;&lt;&#47;script&gt;
  &lt;script&gt;
    transitionTo(document.getElementById(&#39;ball&#39;), [
      {name: &#39;transform&#39;, duration: 1000, value: &#39;translate(400px, 200px) rotate(40deg)&#39;},
      {name: &#39;backgroundColor&#39;, duration: 1000, value: &#39;red&#39;},
      {name: &#39;width&#39;, duration: 1000, value: &#39;200px&#39;},
      {name: &#39;height&#39;, duration: 1000, value: &#39;200px&#39;}
    ])
  &lt;&#47;script&gt;
&lt;&#47;body&gt;
&lt;&#47;html&gt;</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/4d/fd/0aa0e39f.jpg" width="30px"><span>许童童</span> 👍（7） 💬（0）<div>这个课后练习有点难啊。希望老师可以带着大家过一遍。</div>2019-04-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/12/268826e6.jpg" width="30px"><span>Marvin</span> 👍（2） 💬（0）<div>&#47;&#47; 利用老师提供的贝塞尔曲线函数
    function timing_function(easing) {
        let resolve;
        if (easing === &#39;linear&#39;) resolve = generate(0, 0, 1, 1);
        else if (easing === &#39;ease&#39;) resolve = generate(0.25, 0.1, 0.25, 1);
        else if (easing === &#39;ease-in&#39;) resolve = generate(0.42, 0, 1, 1);
        else if (easing === &#39;ease-out&#39;) resolve = generate(0, 0, 0.58, 1);
        else if (easing === &#39;ease-in-out&#39;) resolve = generate(0.42, 0, 0.58, 1);
        else if (easing.indexOf(&#39;cubic-bezier&#39;) === 0) {
            let arr = easing.match(&#47;(?&lt;=\()(.*)(?=\))&#47;)[0].split(&quot;,&quot;);
            arr.map(item =&gt; { return Number(item); })
            resolve = generate(...arr);
        } else {
            resolve = generate(0, 0, 1, 1);
        }
        return resolve;
    }
    function transition(el,
                        target_value,
                        transition_property,
                        transition_duration,
                        transition_timing_function,
                        transition_delay) {

        let start = 0;
        let bezier = timing_function(transition_timing_function);
        let scale = 1 &#47; transition_duration;
        let targetArr = target_value.match(&#47;(\d*)(.*)&#47;);
        console.log(targetArr);

        function step(timestamp) {
            if (!start) start = timestamp;
            let progress = timestamp - start;
            let y = bezier(scale * progress); &#47;&#47; y轴的比例
            el.style[transition_property] = (Number(targetArr[1]) * y) + targetArr[2];
            if (progress &lt;= transition_duration)requestAnimationFrame(step);
        }
        setTimeout(() =&gt; {
            requestAnimationFrame(step)
        }, transition_delay);
    }



    let ball = document.getElementsByClassName(&quot;ball&quot;)[0];
    transition(ball, &quot;50px&quot;, &quot;font-size&quot;, 2000, &quot;liner&quot;, 1000);</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/97/c9/08fde78b.jpg" width="30px"><span>剑客不能说</span> 👍（2） 💬（1）<div>一脸懵逼状态看完的~</div>2019-09-27</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/60/12/268826e6.jpg" width="30px"><span>Marvin</span> 👍（0） 💬（0）<div>不是非常严谨的实现，但是差不多了。可以设置各种属性和时间曲线。
只支持数值+单位的形式例如：left: 200px 或者 font-size: 20px;

https:&#47;&#47;github.com&#47;OleileiA&#47;TransitionJs&#47;blob&#47;master&#47;transition.html</div>2020-08-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/c0/39/16340f72.jpg" width="30px"><span>zlxag</span> 👍（0） 💬（0）<div>交互没有？
</div>2020-06-09</li><br/>
</ul>