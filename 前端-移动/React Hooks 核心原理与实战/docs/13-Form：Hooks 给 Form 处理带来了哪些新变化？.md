你好，我是王沛。今天我们来聊聊如何在 React 中使用表单。

表单作为用户交互最为常见的形式，但在 React 中实现起来却并没有那么容易。甚至可以说，使用表单，是 React 开发中最为困难的一部分。

主要有两方面的原因。一方面，React 都是状态驱动，而表单却是事件驱动，比如点击按钮、输入字符等，都是一个个离散的事件。因此，一般来说我们都需要将这些独立的事件转换成一定的应用程序状态，最终来完成表单的交互。

另一方面，表单元素一般都有自己的内在状态，比如原生的 input 节点就允许用户输入，这就需要我们在元素状态和表单状态之间做同步。

要能够很好地处理这些问题，我们首先需要对**表单的机制**有深入的理解，然后再从 **React Hooks 的角度去思考问题的解决方案**。

所以在今天这节课，我会从这三个方面来讲。

- 首先，介绍 React 中使用表单的基本原理，帮助你理解受控组件和非受控组件的概念，以及各自的适用场景。
- 然后看看 Hooks 出现后，给表单处理带来了哪些思路上的新变化。
- 最后，我们会学习几个常见的开箱即用的 React 表单解决方案，让你在理解实现原理的基础上，可以选择最适合自己的开源方案。

## 在表单中使用 React 组件：受控组件和非受控组件
<div><strong>精选留言（9）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/1f/11/b1/4379e143.jpg" width="30px"><span>H</span> 👍（9） 💬（1）<div>1，reset直接使用setState就行。
2，可以对该API自定义一个hook，在该hook初始化一个success和warn，用于提示用户处理结果信息，
     在useCallback中处理发送请求的逻辑，useCallback依赖于外界name。
     若服务器无此name值，则提示用户  操作成功，且清空表单数据。
     若服务器有此name值，则向用户发出警告，
     将此hook引入到useForm钩子中，在setFieldValue进行setValues之前，进行接口查询操作！</div>2021-07-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/11/b8/2c/0f7baf3a.jpg" width="30px"><span>Change</span> 👍（0） 💬（1）<div>请教老师个问题，在ants 中，Form.List如何嵌套From.List，以及实现思路是怎样的。现在有个问题就是根据Form.List里的不同值显示不同的组件内容,涉及到多层Form.List的嵌套</div>2021-07-12</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/20/48/9e/9bbaa97d.jpg" width="30px"><span>Geek_fcdf7b</span> 👍（1） 💬（0）<div>没有formily吗？</div>2022-08-20</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/DYAIOgq83erIjcViatJ0npo1GiaDYEjlz5bS1VQmWvS2n9AzSLthQOSVDMVjv8sZ2zf2QNk74zpjyUrXWZFon9DQ/132" width="30px"><span>Geek_a77079</span> 👍（1） 💬（2）<div>老师，validators条件判断中如果以来fieldValues中的值该怎么处理？没有思路，在useMemo中加入以来会存在未定义先引用的bug提示</div>2021-12-15</li><br/><li><img src="" width="30px"><span>Free fall</span> 👍（1） 💬（0）<div>const setFieldValue = useCallback(
    (key, value) =&gt; {
      setValues((values) =&gt; ({
        ...values,
        [key]: value,
      }))

      if (validators[key]) {
        validators[key](value).then((res) =&gt; {
          setErrors((errors) =&gt; ({
            ...errors,
            [key]: res,
          }))
        })
      }
    },
    [validators],
  )

  const reset = useCallback(() =&gt; {
    setValues(initialValues)
  }, [initialValues])</div>2021-06-27</li><br/><li><img src="https://thirdwx.qlogo.cn/mmopen/vi_32/qoicvAvQjJPGOayUM51Y65KYbInW2ElhNoJmQUORX0stGYziaK3Dyic0Y6guhTvGibibbuJArtf5DMWg6ia5nXPR4RXg/132" width="30px"><span>Geek_ad92ae</span> 👍（1） 💬（1）<div>老师，你好。在用户二次修改表单时，一般需要通过网络请求历史的表单数据进行初始化，这种情况是不是可以把网络请求和数据初始化的逻辑封装在useform里面？</div>2021-06-24</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/0f/61/3b/abb7bfe3.jpg" width="30px"><span>siegfried</span> 👍（0） 💬（1）<div>sandbox是不是被删除了？</div>2022-04-17</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1d/3c/b4/60e20977.jpg" width="30px"><span>Wizard</span> 👍（0） 💬（0）<div>可以用lodash的debounce讓用戶輸入完成後500ms才檢查是否有錯誤
將範例修改成下面這樣就行了
import _ from &quot;lodash&quot;
const validateDebounceFunction = useCallback(
    _.debounce((name, value) =&gt; {
      if (validators[name]) {
        const errMsg = validators[name](value);
        setErrors((errors) =&gt; ({
          ...errors,
          [name]: errMsg || null
        }));
      }
    }, 500),
    [validators]
  );

  const setFieldValue = useCallback(
    (name, value) =&gt; {
      setValues((values) =&gt; ({
        ...values,
        [name]: value
      }));

      validateDebounceFunction(name, value);
    },
    [validateDebounceFunction]
  );</div>2021-09-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/13/92/d9/84c1de45.jpg" width="30px"><span>傻子来了快跑丶</span> 👍（0） 💬（0）<div>虽然这个 API 只支持通过函数执行进行验证，但是，我们很容易扩展支持更多的类型，比如正则匹配、值范围等等,这个能演示一下吗</div>2021-07-01</li><br/>
</ul>