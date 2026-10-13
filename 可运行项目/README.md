# 大学生生活管家 Python 系统

这是一个可直接运行的 Python 作品。系统接收用户输入的课表、待办事项和身体状态，并自动执行 5 个子任务：

1. 学习计划生成
2. 三餐推荐
3. 待办优先级排序
4. 健康风险评估
5. 每日总结

## 核心自定义工具

- `calc_priority`：输入待办列表、截止时间、任务重要程度，输出排序后的优先级清单。
- `health_evaluate`：输入睡眠时长、疲劳程度、有无不适，输出健康风险评估与建议。

## 运行环境

- Python 3.8 或更高版本
- 无第三方依赖

## 目录结构

```text
.
├── README.md
├── requirements.txt
├── check.bat
├── main.py
├── run.bat
├── run_tests.bat
├── student_life_manager.py
├── test_student_life_manager.py
├── test_cases.md
├── agh_run_log.txt
└── __pycache__/
```

## 启动方式

Windows 双击或运行：

```powershell
run.bat
```

手动运行主程序：

```powershell
python main.py
python student_life_manager.py
```

无交互演示模式：

```powershell
python main.py --demo
```

自检模式：

```powershell
python main.py --check
check.bat
```

运行测试：

```powershell
python test_student_life_manager.py
```

或一键执行测试脚本：

```powershell
run_tests.bat
```

## 交互说明

程序启动后，可分多轮输入：

- 课表：例如 `课表：高数课、英语课`
- 待办：例如 `待办：数学作业、英语六级、阅读`
- 截止时间：例如 `截止2026-10-14 22:00 截止2026-10-15 22:00 截止2026-10-16 22:00`
- 重要程度：例如 `重要程度 5 3 2`
- 身体状态：例如 `睡眠5小时 疲劳8 不适：头痛、失眠`
- 退出：输入 `quit`

每轮输入后，系统会执行全部 5 个子任务，并生成：

- 学习计划
- 三餐推荐
- 待办优先级
- 健康风险评估
- 每日总结

## 日志说明

程序运行时会在当前目录生成：

```text
agh_run_log.txt
```

其中保存完整运行记录，包括工具注册、学习计划生成、三餐推荐、待办优先级排序、健康评估和每日总结等关键日志。

## 测试说明

测试文件：

```text
test_student_life_manager.py
```

测试覆盖三类：

- 正常类：标准输入、常规输出
- 边界类：单条待办、疲劳度最大值、睡眠 6 小时边界、未知餐型、非法截止时间、空输入
- 失败类：长度不匹配、负数睡眠、非字符串参数

测试文档：

```text
test_cases.md
```

## 验证结果

当前作品已验证：

- Python 语法检查通过
- 主程序可运行
- 测试样例 14/14 通过
- 日志文件可正常生成
