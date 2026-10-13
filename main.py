#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学生生活管家 - 可运行入口脚本

用法：
    python main.py
    python main.py --demo
    python main.py --check

说明：
    无参数        启动交互模式
    --demo        用内置示例数据执行一轮完整流程（不进入交互）
    --check       只做语法/工具自检，不交互
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from student_life_manager import (
    StudentLifeManager,
    calc_priority,
    health_evaluate,
    generate_study_plan,
    recommend_meals,
    daily_summary,
    logger,
)


DEMO_INPUT = [
    "课表：高数课、英语课",
    "待办：数学作业、英语六级、阅读",
    "截止2026-10-14 22:00 截止2026-10-15 22:00 截止2026-10-16 22:00",
    "重要程度 5 3 2",
    "睡眠5小时 疲劳8 不适：头痛、失眠",
]


def self_check() -> int:
    logger.info("[--check] 开始自检")
    ok = True

    # 1. 语法/导入检查（import 成功即通过）
    print("[OK] 模块导入成功")

    # 2. calc_priority 正常调用
    try:
        res = calc_priority(["a", "b"], ["2026-10-14 22:00", "2026-10-15 22:00"], [5, 3])
        assert len(res) == 2
        print(f"[OK] calc_priority 正常调用，排序结果: {res[0]['task']} > {res[1]['task']}")
    except Exception as e:
        print(f"[FAIL] calc_priority: {e}")
        ok = False

    # 3. health_evaluate 正常调用
    try:
        res = health_evaluate(7.5, 2, [])
        assert res["risk_level"] in ("低风险", "中风险", "高风险")
        print(f"[OK] health_evaluate 正常调用，风险: {res['risk_level']}")
    except Exception as e:
        print(f"[FAIL] health_evaluate: {e}")
        ok = False

    # 4. 内置能力调用
    try:
        plan = generate_study_plan({"subjects": ["高数", "英语"]}, ["19:00-22:00"])
        assert plan["total_hours"] > 0
        print(f"[OK] generate_study_plan 正常，总时长: {plan['total_hours']}h")
        meals = recommend_meals("早餐", {"sleep_hours": 8, "fatigue_level": 1})
        assert len(meals) >= 3
        print(f"[OK] recommend_meals 正常，推荐 {len(meals)} 项")
        summary = daily_summary({"completed_tasks": ["x"], "sleep_hours": 7, "risk_level": "低风险"})
        assert "低风险" in summary
        print(f"[OK] daily_summary 正常")
    except Exception as e:
        print(f"[FAIL] 内置能力: {e}")
        ok = False

    print(f"\n自检结果: {'全部通过' if ok else '存在失败项'}")
    return 0 if ok else 1


def run_demo():
    logger.info("[--demo] 执行演示数据")
    mgr = StudentLifeManager()
    for line in DEMO_INPUT:
        print(f"\n>>> 输入: {line}")
        mgr._parse_input(line)
        mgr._execute_all_tasks()
    print("\n[演示完成]")


def main():
    if "--check" in sys.argv:
        sys.exit(self_check())
    elif "--demo" in sys.argv:
        run_demo()
    else:
        mgr = StudentLifeManager()
        mgr.run()


if __name__ == "__main__":
    main()
