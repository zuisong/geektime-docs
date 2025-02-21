你好，我是海纳。

上一节课我们主要是实现了异常功能，并且实现了 StopIteration 异常，依赖它重构了 FOR\_ITER 循环。这一节课，我们就依赖于 StopIteration 异常来实现 Python 虚拟机中的另外一个重要功能——Generator。

## 自定义迭代器类

Python 中可以通过自定义迭代器类来实现迭代功能。其中包含了两个步骤，一个是新建一个迭代器对象，另一个是在这个迭代器对象执行迭代。

我们知道，使用 for 语句的时候，会涉及到两个字节码，分别是 GET\_ITER 和 FOR\_ITER。GET\_ITER 的作用是对一个可遍历对象，取得它的迭代器，FOR\_ITER 的作用是针对迭代器进行迭代。

Python 也提供了机制让我们可以手动实现这个功能，与 GET\_ITER 字节码等价的是 iter 函数，与 FOR\_ITER 等价的则是 next 方法。我们通过例子来说明这个问题。

```python
lst = [1, 2]
itor = iter(lst)

while True:
    try:
        print(next(itor))
    except StopIteration as e:
        break

for i in lst:
    print(i)
```

使用第 10 行和 11 行的 for 的写法的迭代过程，与第 4 行至第 8 行的 while 的写法是完全等价的。只是 for 循环隐藏掉了迭代器，而 while 循环则显式地持有一个迭代器。
<div><strong>精选留言（3）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/3b/59/44/727b90a8.jpg" width="30px"><span>冯某</span> 👍（0） 💬（0）<div>记录一下</div>2024-12-11</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-11-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/05/92/b609f7e3.jpg" width="30px"><span>骨汤鸡蛋面</span> 👍（0） 💬（0）<div>示例的foo 生成器函数是不是可以理解为：以为 foo() 返回的是一个或多个 数字，实际返回的是一个Generator，foo函数成了Generator 的一部分，在Generator.__next__ 执行时被触发。这也是python 让人迷惑和有魅力的地方，代码执行着执行着，类型就改了。 </div>2024-07-17</li><br/>
</ul>