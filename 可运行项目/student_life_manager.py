#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大学生生活管家完整Python系统
AGH自动拆解5个子任务：
①学习计划生成 ②三餐推荐 ③待办优先级排序 ④健康风险评估 ⑤每日总结

核心工具：
- calc_priority: 待办优先级计算
- health_evaluate: 健康风险评估

运行规则：
- 支持多轮对话交互，输入quit退出
- 日志记录保存至 agh_run_log.txt
"""

import json
import logging
import os
import re
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 日志配置
LOG_FILE = "agh_run_log.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("student_life_manager")


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class AGHTool:
    """AGH工具注册基类"""

    def __init__(self, name: str, description: str, parameters: dict):
        self.name = name
        self.description = description
        self.parameters = parameters

    def __repr__(self) -> str:
        return f"<AGHTool:{self.name}>"


class AGHToolRegistry:
    """AGH工具注册表"""

    def __init__(self):
        self._tools: Dict[str, AGHTool] = {}

    def register(self, tool: AGHTool) -> None:
        self._tools[tool.name] = tool
        logger.info("AGH注册工具: %s", tool.name)

    def get(self, name: str) -> Optional[AGHTool]:
        return self._tools.get(name)

    def list(self) -> List[AGHTool]:
        return list(self._tools.values())


def calc_priority(todos: List[Dict], deadlines: List[str], importance: List[int]) -> List[Dict]:
    """
    待办优先级计算工具
    输入: 待办列表、截止时间、任务重要程度
    输出: 排序后的优先级清单
    """
    if len(todos) != len(deadlines) or len(todos) != len(importance):
        raise ValueError("todos, deadlines, importance 长度必须一致")

    scored = []
    for i, task in enumerate(todos):
        deadline = deadlines[i]
        imp = importance[i]
        try:
            dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
            time_bonus = max(0, 24 - (dt - datetime.now()).total_seconds() / 3600) / 24
        except ValueError:
            time_bonus = 0.5
        score = imp * 0.6 + time_bonus * 0.4
        scored.append({
            "task": task,
            "deadline": deadline,
            "importance": imp,
            "score": round(score, 2),
            "rank": 0,
        })

    scored.sort(key=lambda x: (-x["score"], x.get("deadline", "")))
    for rank, item in enumerate(scored, start=1):
        item["rank"] = rank

    logger.info("calc_priority 处理 %d 条待办", len(scored))
    return scored


def health_evaluate(sleep_hours: float, fatigue_level: int, symptoms: List[str]) -> Dict:
    """
    健康评估工具
    输入: 睡眠时长、疲劳程度(0-10)、有无不适
    输出: 健康风险评估与建议
    """
    if sleep_hours < 0 or fatigue_level < 0:
        raise ValueError("sleep_hours 与 fatigue_level 不能为负数")
    risk_score = 0.0
    suggestions = []

    if sleep_hours < 6:
        risk_score += 3
        suggestions.append("睡眠不足6小时，建议今晚提前休息")
    elif sleep_hours < 8:
        risk_score += 1.5
        suggestions.append("睡眠一般，保持规律作息")
    else:
        suggestions.append("睡眠充足，继续保持")

    if fatigue_level >= 8:
        risk_score += 3
        suggestions.append("疲劳程度极高，建议暂停高强度学习，适当休息")
    elif fatigue_level >= 5:
        risk_score += 1.5
        suggestions.append("疲劳明显，建议安排短时休息")
    else:
        suggestions.append("疲劳程度较低，状态良好")

    if symptoms:
        risk_score += min(len(symptoms) * 0.5, 2)
        suggestions.append("存在不适症状: " + "、".join(symptoms) + "，必要时就医")

    if risk_score >= 6:
        risk_level = "高风险"
    elif risk_score >= 3:
        risk_level = "中风险"
    else:
        risk_level = "低风险"

    result = {
        "risk_level": risk_level,
        "risk_score": round(risk_score, 2),
        "suggestions": suggestions,
    }
    logger.info("health_evaluate 评估: %s (score=%.2f)", risk_level, risk_score)
    return result


def generate_study_plan(class_schedule: Dict, available_time: List[str]) -> Dict:
    """学习计划生成"""
    plan = []
    subjects = class_schedule.get("subjects", [])
    free_slots = available_time or ["19:00-22:00"]

    if not subjects:
        subjects = ["高数", "英语"]

    for slot in free_slots:
        m = re.match(r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})", slot)
        hours = 3.0
        if m:
            hours = max(0.5, (int(m.group(2)[:2]) - int(m.group(1)[:2])) % 24)
        for i, subj in enumerate(subjects):
            plan.append({
                "subject": subj,
                "slot": slot,
                "hours": round(hours / max(len(subjects), 1), 2),
            })

    logger.info("generate_study_plan 生成 %d 个学习项", len(plan))
    return {"plan": plan, "total_hours": round(sum(p["hours"] for p in plan), 2)}


def recommend_meals(meal_type: str, state: Dict) -> List[str]:
    """三餐推荐"""
    base = {
        "早餐": ["鸡蛋", "牛奶", "全麦面包"],
        "午餐": ["米饭", "瘦肉", "青菜"],
        "晚餐": ["面条", "豆腐", "水果"],
    }
    recs = list(base.get(meal_type, []))

    if state.get("sleep_hours", 8) < 6:
        recs.append("增加易消化食物，避免油腻")
    if state.get("fatigue_level", 0) >= 8:
        recs.append("补充优质蛋白和维生素")

    logger.info("recommend_meals(%s) 推荐 %d 项", meal_type, len(recs))
    return recs


def daily_summary(day_log: Dict) -> str:
    """每日总结"""
    lines = [
        f"日期: {day_log.get('date', _now_str())}",
        f"完成任务数: {len(day_log.get('completed_tasks', []))}",
        f"睡眠: {day_log.get('sleep_hours', '未记录')}h",
        f"健康风险: {day_log.get('risk_level', '未评估')}",
        "建议: " + day_log.get("suggestion", "保持当前节奏"),
    ]
    summary = "\n".join(lines)
    logger.info("daily_summary 生成完成")
    return summary


class StudentLifeManager:
    def __init__(self):
        self.registry = AGHToolRegistry()
        self.registry.register(AGHTool("calc_priority", "待办优先级计算", {
            "todos": "List[str]", "deadlines": "List[str]", "importance": "List[int]",
        }))
        self.registry.register(AGHTool("health_evaluate", "健康风险评估", {
            "sleep_hours": "float", "fatigue_level": "int", "symptoms": "List[str]",
        }))
        self.state = {
            "class_schedule": {},
            "todos": [],
            "deadlines": [],
            "importance": [],
            "health": {"sleep_hours": 8.0, "fatigue_level": 0, "symptoms": []},
        }

    def run(self):
        logger.info("===== 大学生生活管家启动 =====")
        print("欢迎使用大学生生活管家系统")
        print("输入 quit 退出\n")

        while True:
            print("请提供以下信息（可分多轮输入）:")
            print("1. 课表信息  2. 待办事项  3. 身体状态  4. quit退出")
            user_input = input("\n> ").strip()

            if not user_input:
                continue
            if user_input.lower() == "quit":
                logger.info("用户输入quit，退出程序")
                print("再见！")
                break

            self._parse_input(user_input)
            self._execute_all_tasks()

    def _parse_input(self, text: str):
        # 解析课表：提取“课表”之后的部分，再拆分科目（去掉末尾的“课”字和“表：”残留）
        if "课表" in text or "class" in text.lower():
            # 取“课表”之后的内容
            after = re.split(r"课表[:：]?|class[:：]?", text, flags=re.IGNORECASE)[-1]
            # 按逗号、顿号、分号拆分，过滤空值、去掉末尾“课”字、去掉可能的“表：”前缀
            raw_subjects = [s.strip() for s in re.split(r"[，、,;；]", after) if s.strip()]
            cleaned = []
            for s in raw_subjects:
                s = re.sub(r"^表[:：]?", "", s)  # 去掉“表：”残留
                if s.endswith("课"):
                    s = s[:-1]
                if s:
                    cleaned.append(s)
            self.state["class_schedule"]["subjects"] = cleaned or ["高数", "英语"]
        # 解析待办：提取“待办”之后的部分
        if "待办" in text or "todo" in text.lower():
            after = re.split(r"待办[:：]?|todo[:：]?", text, flags=re.IGNORECASE)[-1]
            tasks = [t.strip() for t in re.split(r"[，、,;；]", after) if t.strip()]
            self.state["todos"] = tasks
        # 解析截止时间
        if "截止" in text or "deadline" in text.lower():
            self.state["deadlines"] = re.findall(r"\d{4}-\d{2}-\d{2}(?: \d{2}:\d{2})?", text)
        # 解析重要程度
        if "重要" in text or "重要程度" in text:
            self.state["importance"] = [int(m) for m in re.findall(r"\d+", text)] or [3] * len(self.state["todos"])
        # 解析睡眠
        if "睡眠" in text:
            m = re.search(r"睡眠[:：]?\s*(\d+(?:\.\d+)?)", text)
            if m:
                self.state["health"]["sleep_hours"] = float(m.group(1))
        # 解析疲劳
        if "疲劳" in text:
            m = re.search(r"疲劳[:：]?\s*(\d+)", text)
            if m:
                self.state["health"]["fatigue_level"] = int(m.group(1))
        # 解析不适症状
        if "不适" in text or "症状" in text:
            after = re.split(r"不适[:：]?|症状[:：]?", text, flags=re.IGNORECASE)[-1]
            self.state["health"]["symptoms"] = [s.strip() for s in re.split(r"[，、,;；]", after) if s.strip()]

    def _execute_all_tasks(self):
        print("\n" + "=" * 40)
        print("AGH拆解执行5个子任务")
        print("=" * 40)

        plan = generate_study_plan(self.state["class_schedule"], ["19:00-22:00"])
        print("\n【①学习计划】")
        for item in plan["plan"]:
            print(f"  - {item['subject']}: {item['slot']}, 约{item['hours']}h")
        print(f"  总可用时长: {plan['total_hours']}h")

        for meal in ["早餐", "午餐", "晚餐"]:
            meals = recommend_meals(meal, self.state["health"])
            print(f"\n【②{meal}推荐】" + ", ".join(meals))

        if self.state["todos"]:
            todos = self.state["todos"]
            importance = list(self.state["importance"]) if self.state["importance"] else [3] * len(todos)
            default_deadline = f"{datetime.now().strftime('%Y-%m-%d')} 23:59"
            deadlines = list(self.state["deadlines"])
            while len(deadlines) < len(todos):
                deadlines.append(default_deadline)
            deadlines = deadlines[:len(todos)]
            while len(importance) < len(todos):
                importance.append(3)
            importance = importance[:len(todos)]
            ranked = calc_priority(todos, deadlines, importance)
            print("\n【③待办优先级】")
            for r in ranked:
                print(f"  #{r['rank']} {r['task']} (截止:{r['deadline']}, 重要度:{r['importance']}, 得分:{r['score']})")
        else:
            print("\n【③待办优先级】未提供待办事项")

        hr = health_evaluate(
            self.state["health"]["sleep_hours"],
            self.state["health"]["fatigue_level"],
            self.state["health"]["symptoms"],
        )
        print(f"\n【④健康风险评估】{hr['risk_level']} (score={hr['risk_score']})")
        for s in hr["suggestions"]:
            print(f"  建议: {s}")

        summary = daily_summary({
            "completed_tasks": self.state["todos"],
            "sleep_hours": self.state["health"]["sleep_hours"],
            "risk_level": hr["risk_level"],
            "suggestion": hr["suggestions"][0] if hr["suggestions"] else "保持当前节奏",
        })
        print(f"\n【⑤每日总结】\n{summary}\n")


def main():
    logger.info("开始执行 main()")
    mgr = StudentLifeManager()
    mgr.run()
    logger.info("===== 程序结束 =====")


if __name__ == "__main__":
    main()
