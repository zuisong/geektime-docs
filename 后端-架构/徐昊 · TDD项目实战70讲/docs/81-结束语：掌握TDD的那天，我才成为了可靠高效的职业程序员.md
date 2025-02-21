你好，我是徐昊。今天要对线段编辑器这个项目做一个收尾，同时也是我们整门课程的一个收尾。

## 线段编辑器最终的结果

目前，线段编辑器的代码是这样的：

```plain
import Konva from "konva";
export class LineEditor extends Konva.Group {
    private line?: Konva.Line
    private pointsCount: number = 0
    attach(line: Konva.Line) {
        this.line = line
        line.on('pointsChange', () => {
            this.update()
        })
        this.update()
    }
    update() {
        let points = this.line!.points()
        let previous = -1
        for (let i = 0; i < points.length / 2; i++) {
            this.get(i, 'anchor').setAttrs({x: points[i * 2], y: points[i * 2 + 1]})
            if (previous !== -1)
                this.get(i, 'control').setAttrs({
                    x: points[previous * 2] + (points[i * 2] - points[previous * 2]) / 2,
                    y: points[previous * 2 + 1] + (points[i * 2 + 1] - points[previous * 2 + 1]) / 2
                })
            previous = i
        }
        for (let i = points.length / 2; i < this.pointsCount; i++) {
            this.findOne(`.${i}-anchor`).destroy()
            this.findOne(`.${i}-control`).destroy()
        }
        this.pointsCount = points.length / 2
    }
    private get(index: number, type: string) {
        return this.findOne(`.${index}-${type}`) || this.create(index, type)
    }
    private create(index: number, type: string) {
        let point = new Konva.Circle({name: `${index}-${type}`, radius: 10, draggable: true})
        if (type === 'anchor') {
            point.on('dragmove', (e) => {
                let points = this.line!.points()
                points[index * 2] = e.target.x()
                points[index * 2 + 1] = e.target.y()
                this.line!.points(points)
            }).on('dblclick', (e: Konva.KonvaEventObject<MouseEvent>) => {
                let points = this.line!.points()
                points.splice(index * 2, 2)
                this.line!.points(points)
            })
        } else {
            point.on('dragmove', (e) => {
                let points = this.line!.points()
                points.splice(index * 2, 0, e.target.x(), e.target.y())
                this.line!.points(points)
            })
        }
        this.add(point)
        return point
    }
}

```
<div><strong>精选留言（2）</strong></div><ul>
<li><img src="https://static001.geekbang.org/account/avatar/00/11/1d/de/62bfa83f.jpg" width="30px"><span>aoe</span> 👍（5） 💬（0）<div>原来真实的 TDD 开发中是首选简单快速的方法实现，见机行事</div>2022-09-13</li><br/><li><img src="https://static001.geekbang.org/account/avatar/00/1f/e0/54/c2a1abbc.jpg" width="30px"><span>王鸿轩</span> 👍（2） 💬（0）<div>期待与徐昊老师再会，听徐昊老师分享和写代码是一种非常愉悦的享受。</div>2023-12-30</li><br/>
</ul>