你好，我是海纳。

在[第 7 节课](https://time.geekbang.org/column/article/774409)，我们实现了 Python 的两个基本的内建类型：整数和字符串，从而构建了虚拟机的最基本的对象系统。从这节课开始，我们来实现两个重要的基本内建类型，分别是列表（list）和字典（dict）。

我们先来研究如何实现列表。

## 列表的定义

Python 中的列表很像数组操作，可以支持对元素的插入、添加、删除等操作。实际上 Python 的 list 和 C++ STL 中的 vector 非常相似。区别在于，Python 的 list 允许它的元素是不同类型的。我们以一个例子来说明 list 的特性。

```python
# test_list.py
lst = [1, "hello"]

# result is [1, 'hello']
print(lst)
```

上面的代码定义了一个列表，这个列表包含了两个元素。第一个元素是整数 1，第二个元素是字符串 `“hello”`。第二行代码把这个列表打印了出来。

通过 show\_file 工具，我们能观察到 Python 为了定义列表引入了新的字节码。这节课我们的任务就是实现这些定义列表所用的字节码。

```plain
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 ('hello')
              4 BUILD_LIST               2
              6 STORE_NAME               0 (lst)

  4           8 LOAD_NAME                1 (print)
             10 LOAD_NAME                0 (lst)
             12 CALL_FUNCTION            1
             14 POP_TOP
             16 LOAD_CONST               2 (None)
             18 RETURN_VALUE
```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/13/58/b3/abb3256b.jpg" width="30px"><span>枫树_6177003</span> 👍（1） 💬（2）<div>KMP算法</div>2024-06-03</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/26/eb/d7/90391376.jpg" width="30px"><span>ifelse</span> 👍（0） 💬（0）<div>学习打卡</div>2024-10-28</li><br/>
</ul>