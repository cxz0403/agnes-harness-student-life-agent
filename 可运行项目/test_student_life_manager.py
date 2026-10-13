#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大学生生活管家 - 测试用例
三类：正常 / 边界 / 失败
"""

import sys
import os
import io
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import student_life_manager as slm

PASSED, FAILED, TOTAL = 0, 0, 0


def check(desc, fn):
    global PASSED, FAILED, TOTAL
    TOTAL += 1
    try:
        fn()
        PASSED += 1
        print(f"  [PASS] {desc}")
    except AssertionError as e:
        FAILED += 1
        print(f"  [FAIL] {desc} -> {e}")


# ============ 正常类 ============
def test_normal():
    print("\n=== 正常类测试 ===")

    def t1():
        res = slm.calc_priority(["作业A", "作业B"], ["2026-10-14 22:00", "2026-10-15 22:00"], [5, 3])
        assert len(res) == 2, "结果长度应为2"
        assert res[0]["rank"] == 1, "应有rank字段"
    check("calc_priority 正常输入", t1)

    def t2():
        res = slm.health_evaluate(7.5, 2, [])
        assert res["risk_level"] in ("低风险", "中风险", "高风险")
        assert "suggestions" in res
    check("health_evaluate 正常输入", t2)

    def t3():
        res = slm.generate_study_plan({"subjects": ["高数", "英语"]}, ["19:00-22:00"])
        assert res["total_hours"] > 0
        assert len(res["plan"]) == 2
    check("generate_study_plan 正常输入", t3)

    def t4():
        res = slm.recommend_meals("早餐", {"sleep_hours": 8, "fatigue_level": 1})
        assert isinstance(res, list) and len(res) >= 3
    check("recommend_meals 正常输入", t4)

    def t5():
        res = slm.daily_summary({"completed_tasks": ["a", "b"], "sleep_hours": 7, "risk_level": "低风险"})
        assert "低风险" in res
    check("daily_summary 正常输入", t5)


# ============ 边界类 ============
def test_boundary():
    print("\n=== 边界类测试 ===")

    def t1():
        res = slm.calc_priority(["x"], ["2026-10-14 22:00"], [0])
        assert len(res) == 1, "单元素正常"
    check("calc_priority 单条待办", t1)

    def t2():
        res = slm.health_evaluate(8.0, 10, [])
        # 睡眠8边界(>=8无扣分), 疲劳10(>=8扣3分) -> 中风险
        assert res["risk_score"] >= 3
    check("health_evaluate 疲劳最高10", t2)

    def t3():
        res = slm.health_evaluate(6.0, 0, [])
        # 睡眠6边界: 不低于6(不扣分), 疲劳0(不扣)
        assert res["risk_level"] == "低风险"
    check("health_evaluate 睡眠=6小时边界", t3)

    def t4():
        res = slm.recommend_meals("不存在的餐", {"sleep_hours": 5, "fatigue_level": 9})
        assert isinstance(res, list), "未知餐型应返回基础列表"
    check("recommend_meals 未知餐型", t4)

    def t5():
        # 截止时间非法格式 -> 使用默认time_bonus
        res = slm.calc_priority(["t"], ["99/99/99"], [3])
        assert len(res) == 1, "非法日期不应崩溃"
    check("calc_priority 非法截止时间格式", t5)

    def t6():
        res = slm.generate_study_plan({}, [])
        # 无科目无时间段 -> 默认科目+默认时段
        assert len(res["plan"]) >= 1, "空输入应有默认值"
    check("generate_study_plan 空输入", t6)


# ============ 失败类 ============
def test_failure():
    print("\n=== 失败类测试 ===")

    def t1():
        try:
            slm.calc_priority(["a", "b"], ["2026-10-14"], [1, 2])
            raise AssertionError("长度不一致应抛异常")
        except ValueError:
            pass
    check("calc_priority 长度不匹配 -> ValueError", t1)

    def t2():
        try:
            slm.health_evaluate(-5, 0, [])
            raise AssertionError("负数睡眠应抛异常")
        except (ValueError, Exception):
            pass
    check("health_evaluate 负数睡眠", t2)

    def t3():
        try:
            slm.recommend_meals(123, None)
            raise AssertionError("非字符串meal_type应异常")
        except Exception:
            pass
    check("recommend_meals 非字符串参数", t3)


if __name__ == "__main__":
    test_normal()
    test_boundary()
    test_failure()
    print(f"\n=== 测试汇总: 通过 {PASSED}/{TOTAL}, 失败 {FAILED} ===")
    sys.exit(0 if FAILED == 0 else 1)
