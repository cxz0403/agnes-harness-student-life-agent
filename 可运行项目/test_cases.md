大学生生活管家 - 测试样例汇总
================================

文件位置：
  被测代码：D:\agnes\student_life_manager.py
  测试代码：D:\agnes\test_student_life_manager.py
  运行命令：python test_student_life_manager.py

测试日期：2026-10-13
测试汇总：通过 14/14，失败 0


一、正常类（5项）
----------------

[测试1] calc_priority 正常输入
  输入:
    todos     = ["作业A", "作业B"]
    deadlines = ["2026-10-14 22:00", "2026-10-15 22:00"]
    importance= [5, 3]
  预期:
    返回长度为2的排序清单，每项含 rank 字段，rank=1/2
  结果: PASS

[测试2] health_evaluate 正常输入
  输入:
    sleep_hours  = 7.5
    fatigue_level= 2
    symptoms     = []
  预期:
    返回 dict，含 risk_level(低风险/中风险/高风险) 与 suggestions
  结果: PASS

[测试3] generate_study_plan 正常输入
  输入:
    class_schedule = {"subjects": ["高数", "英语"]}
    available_time = ["19:00-22:00"]
  预期:
    返回2个学习项，total_hours > 0
  结果: PASS

[测试4] recommend_meals 正常输入
  输入:
    meal_type = "早餐"
    state     = {"sleep_hours": 8, "fatigue_level": 1}
  预期:
    返回 list，长度 >= 3
  结果: PASS

[测试5] daily_summary 正常输入
  输入:
    day_log = {"completed_tasks": ["a", "b"], "sleep_hours": 7, "risk_level": "低风险"}
  预期:
    返回文本，含 "低风险"
  结果: PASS


二、边界类（6项）
----------------

[测试6] calc_priority 单条待办
  输入:
    todos     = ["x"]
    deadlines = ["2026-10-14 22:00"]
    importance= [0]
  预期:
    正常返回1项，不崩溃
  结果: PASS

[测试7] health_evaluate 疲劳最高10
  输入:
    sleep_hours  = 8.0
    fatigue_level= 10
    symptoms     = []
  预期:
    睡眠8h边界(不扣分)，疲劳10(>=8扣3分) → risk_score >= 3（中风险）
  结果: PASS

[测试8] health_evaluate 睡眠=6小时边界
  输入:
    sleep_hours  = 6.0
    fatigue_level= 0
    symptoms     = []
  预期:
    睡眠恰好6小时(不低于6，不扣分)，疲劳0 → 低风险
  结果: PASS

[测试9] recommend_meals 未知餐型
  输入:
    meal_type = "不存在的餐"
    state     = {"sleep_hours": 5, "fatigue_level": 9}
  预期:
    不崩溃，返回基础列表
  结果: PASS

[测试10] calc_priority 非法截止时间格式
  输入:
    todos     = ["t"]
    deadlines = ["99/99/99"]
    importance= [3]
  预期:
    日期解析失败时使用默认 time_bonus，不崩溃
  结果: PASS

[测试11] generate_study_plan 空输入
  输入:
    class_schedule = {}
    available_time = []
  预期:
    使用默认科目与默认时段，plan 非空
  结果: PASS


三、失败类（3项）
----------------

[测试12] calc_priority 长度不匹配 -> ValueError
  输入:
    todos     = ["a", "b"]
    deadlines = ["2026-10-14"]
    importance= [1, 2]
  预期:
    抛出 ValueError("todos, deadlines, importance 长度必须一致")
  结果: PASS

[测试13] health_evaluate 负数睡眠
  输入:
    sleep_hours  = -5
    fatigue_level= 0
    symptoms     = []
  预期:
    抛出 ValueError("sleep_hours 与 fatigue_level 不能为负数")
  结果: PASS

[测试14] recommend_meals 非字符串参数
  输入:
    meal_type = 123
    state     = None
  预期:
    抛出异常（类型/None 校验）
  结果: PASS


汇总
----
正常类：5/5 通过
边界类：6/6 通过
失败类：3/3 通过
总计：14/14 通过，失败 0
