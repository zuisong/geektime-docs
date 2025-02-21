你好，我是陈博士。今天我们来探讨一下新能源汽车企业的实时车况监控业务的数据查询与优化。

随着新能源汽车市场的迅速扩张，实时车况监控成为了确保车辆安全运行的关键环节。通过查询，我们可以即时掌握每辆车的健康状态，包括电池性能、电机效率以及潜在故障，这有助于车企提前做出维护决策。

针对该场景，我整理了6张数据表以及对应的查询问题。针对这些查询问题，你可以了解到这些SQL该如何撰写。

## **数据表**

- 车辆基础信息表 vehicle\_base\_info  
  ![](https://static001.geekbang.org/resource/image/62/4b/622f7184aabb3f68ebb432ba05365e4b.jpg?wh=2100x1396)
- 实时位置信息表 vehicle\_location  
  ![](https://static001.geekbang.org/resource/image/4c/8e/4cb8b6e7dee4a97ede32213e25ef818e.jpg?wh=2106x1278)
- 电池状态表 battery\_status  
  ![](https://static001.geekbang.org/resource/image/88/92/88698f485c5a4d965a8788bea26c5e92.jpg?wh=2106x1510)
- 电机状态表 motor\_status  
  ![](https://static001.geekbang.org/resource/image/84/9a/849b662cb13a3c796a477fd173f8439a.jpg?wh=2110x1286)
- 故障告警表 vehicle\_alarm  
  ![](https://static001.geekbang.org/resource/image/60/5c/606b2ffae5fd2429a80d60a0e894865c.jpg?wh=2108x1364)

<!--THE END-->

- 行驶状态表 driving\_status  
  ![](https://static001.geekbang.org/resource/image/07/d4/07fd97cdd809198eecb6cab181099dd4.jpg?wh=2114x1620)

## **问题设定**

我从车辆实时监控查询、电池健康状态分析、故障分析统计、行驶里程统计、性能监控预警、驾驶行为分析、地理分布分析、SOC 变化趋势分析、车辆综合性能评估等维度设置了一些常见的查询问题，一起来看一下。

### **车辆实时监控查询**

查询指定车辆最近5分钟的实时状态，包括位置、电量、速度等信息。

```plain
SELECT
    v.vin,
    v.model_name,
    d.car_status,
    l.speed,
    l.latitude,
    l.longitude,
    b.soc as battery_level,
    b.voltage as battery_voltage,
    m.motor_speed,
    m.motor_temperature,
    l.collect_time
FROM vehicle_base_info v
LEFT JOIN vehicle_location l ON v.vehicle_id = l.vehicle_id
LEFT JOIN battery_status b ON v.vehicle_id = b.vehicle_id
LEFT JOIN motor_status m ON v.vehicle_id = m.vehicle_id
LEFT JOIN driving_status d ON v.vehicle_id = d.vehicle_id
WHERE v.vehicle_id = 'VH00000001'
AND l.collect_time >= DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 5 MINUTE), '%Y-%m-%d %H:%i:%s.%f')
ORDER BY l.collect_time DESC
LIMIT 1;
 
// 说明： DATE_FORMAT 函数用于格式化日期和时间数据，使其按照指定的格式输出。在这个SQL查询中，DATE_FORMAT 与 DATE_SUB 结合使用来计算过去5分钟的时间点。
```