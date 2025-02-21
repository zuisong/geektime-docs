你好，我是Mike。

上一讲我们了解了Unsafe Rust的所属定位和基本性质，这一讲我们就来看看Rust FFI编程到底是怎样一种形式。

FFI是与外部语言进行交互的接口，在Safe Rust看来，它是不可信的，也就是说Rust编译不能保证它是安全的，只能由程序员自己来保证，因此在Rust里调用这些外部的代码功能就需要把它们包在 `unsafe {}` 中。

Rust和C有血缘关系，具有ABI上的一致性，所以**Rust和C之间可以实现双向互调，并且不会损失性能。**

## Rust调用C

我们先来看在Rust中如何调用C库的代码。

一般各个平台下都有 libm 库，它是操作系统基本的数学math库。下面我们以Linux为例来说明。下面的示例代码来自 [Rust By Example](https://doc.rust-lang.org/rust-by-example/std_misc/ffi.html)。

```plain
use std::fmt;

// 连接到系统的 libm 库
#[link(name = "m")]
extern {
    // 这是一个外部函数，计算单精度复数的方根
    fn csqrtf(z: Complex) -> Complex;
    // 计算复数的余弦值
    fn ccosf(z: Complex) -> Complex;
}

// 对unsafe调用的safe封装，从此以后，就按safe函数方式使用这个接口
fn cos(z: Complex) -> Complex {
    unsafe { ccosf(z) }
}

fn main() {
    // z = -1 + 0i
    let z = Complex { re: -1., im: 0. };

    // 调用m库中的函数，需要用 unsafe {} 包起来
    let z_sqrt = unsafe { csqrtf(z) };

    println!("the square root of {:?} is {:?}", z, z_sqrt);

    // 调用安全封装后的函数
    println!("cos({:?}) = {:?}", z, cos(z));
}

// 用 repr(C) 标注，定义Rust结构体的ABI格式，按C的ABI来
#[repr(C)]
#[derive(Clone, Copy)]
struct Complex {
    re: f32,
    im: f32,
}

// 实现复数的打印输出
impl fmt::Debug for Complex {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if self.im < 0. {
            write!(f, "{}-{}i", self.re, -self.im)
        } else {
            write!(f, "{}+{}i", self.re, self.im)
        }
    }
}
```
<div><strong>精选留言（10）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/0f/82/54/b9cd3674.jpg" width="30px"><span>小可爱(`へ´*)ノ</span> 👍（1） 💬（1）<div>跟完了，很值得的，老师功底很厚。</div>2024-03-08</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/18/ed/4d/7df516d5.jpg" width="30px"><span>一带一路</span> 👍（1） 💬（1）<div>Rust 与 Python 绑定未来可期！</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/0f/99/0d72321f.jpg" width="30px"><span>A0.何文祥</span> 👍（0） 💬（1）<div>老师，我根据文档https:&#47;&#47;pyo3.rs&#47;v0.20.2&#47;parallelism了解到，如果要在PyO3里Release GIL需要执行Python::allow_threads，咱们实例是不是遗漏了这一步，实际跑的还是single CPU core。</div>2024-01-31</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/8b/57/a3daeaae.jpg" width="30px"><span>tan</span> 👍（0） 💬（1）<div>window 观测时间： Measure-Command {python .\fib_rust.py}    。
ps: 为什么我在window10上测试 python自己写的函数只要 0.49s, 调用rust的需要12s
ps: 如果有同学不关心执行时间想要确定调用成功与否，需要`calc_fib` 把给这个函数返回值</div>2024-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/12/a2/4b/b72f724f.jpg" width="30px"><span>zxk</span> 👍（0） 💬（1）<div>C 语言中的 char 是一个 8bit 大小的类型，一个 char 可以覆盖 ASCII 码表；而在 Rust 中 char 是一个 Unicode 字符，使用 32bit（即 UTF-32）进行存储。

C 语言中的字符串其实就是一个 char 数组，并以 `\0` 作为结束标志；而 Rust 中的 String 是经过 UTF-8 编码后的字节数组，一个实际的字符对应一个或多个字节（UTF-8 是可变长编码），通过一个长度来得出字符串的结束位置。

若要将 C 语言的字符串类型映射到 Rust 中的类型，目前能想到两种方案：
1. C 端以 UTF-8 的方式编码存储字符串，并传递给 Rust； Rust 可以选择使用 CString 存储在转化，或者自行解析并注意 `\0` 的标识符；
2. C 端自由选择编码，在传给 Rust 时告诉 Rust 编码方式，并由 Rust 自行解码，并转为内部的 UTF-8 编码。</div>2024-01-20</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/17/2e/7e/a15b477c.jpg" width="30px"><span>Noya</span> 👍（0） 💬（1）<div>完结!</div>2024-01-04</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（2）<div>请问在 calc_fib 函数里，为什么 fib 的计算结果被丢弃，而返回 Ok(()) 呢？
</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/10/82/42/8b04d489.jpg" width="30px"><span>刘丹</span> 👍（0） 💬（3）<div>请问老师，pyproject.toml 这个文件是哪个工具需要的？ 我按本课教程操作，没有创建这个文件也能正常运行。</div>2024-01-01</li><br/><li><img src="" width="30px"><span>Geek_72807e</span> 👍（0） 💬（2）<div>基本跟完了老师的课程，还有哪些进阶内容或参考资料老师推荐一下？！</div>2024-01-01</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/16/9c/fb/7fe6df5b.jpg" width="30px"><span>陈卧虫</span> 👍（0） 💬（0）<div>真的讲的很好，我学习 rust 的第一课，谢谢老师🙏</div>2024-12-12</li><br/>
</ul>