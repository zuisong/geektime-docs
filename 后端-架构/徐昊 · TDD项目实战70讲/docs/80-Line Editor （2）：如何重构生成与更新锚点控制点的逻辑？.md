你好，我是徐昊。今天我们继续使用TDD的方式实现一个线段编辑器。

## 回顾任务与代码

目前代码为：

```plain
import Konva from "konva";
export class LineEditor extends Konva.Group {
    private line?: Konva.Line
    attach(line: Konva.Line) {
        let points = line.points()
        let previous = -1
        for (let i = 0; i < points.length / 2; i++) {
            this.add(new Konva.Circle({name: `${i}-anchor`, radius: 10, x: points[i * 2], y: points[i * 2 + 1]}))
            if (previous !== -1)
                this.add(new Konva.Circle({
                    name: `${i}-control`, radius: 10,
                    x: points[previous * 2] + (points[i * 2] - points[previous * 2]) / 2,
                    y: points[previous * 2 + 1] + (points[i * 2 + 1] - points[previous * 2 + 1]) / 2
                }))
            previous = i
        }
        this.line = line
        line.on('pointsChange', () => {
            this.update()
        })
    }
    update() {
        let points = this.line!.points()
        let previous = -1
        for (let i = 0; i < points.length / 2; i++) {
            this.findOne(`.${i}-anchor`).setAttrs({x: points[i * 2], y: points[i * 2 + 1]})
            if (previous !== -1)
                this.findOne(`.${i}-control`).setAttrs({
                    x: points[previous * 2] + (points[i * 2] - points[previous * 2]) / 2,
                    y: points[previous * 2 + 1] + (points[i * 2 + 1] - points[previous * 2 + 1]) / 2
                })
            previous = i
        }
    }
}

```
<div><strong>精选留言（1）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/10/65/21/101a7075.jpg" width="30px"><span>davix</span> 👍（1） 💬（1）<div>老師，實際開發時，會實現了這些任務還看不到頁面啥樣嗎？
TDD時每完成一個任務是不是也結合一個手工UI測試？要不那些 .on 啊，.fire啊，哪些參數啥都不知道生沒生效。最後少刪一些線等情況沒有實際看到UI，單純頭腦想也很容易忽略。</div>2022-09-19</li><br/>
</ul>