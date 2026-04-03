<div align="center">

# 导师.skill

> *"那你相当于这周啥也没干啊"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

还在因为摸鱼一周、组会不知道汇报什么而忐忑吗？<br>
还在看到导师一皱眉，就开始心跳加速、脑子空白吗？<br>
还在被批完以后只剩情绪，根本复盘不出问题到底出在哪吗？<br>

**导师.skill，把导师蒸馏成 skill，提前模拟你的每一次组会。**

<br>

提供你的聊天记录、组会反馈、汇报稿、PPT、截图，加上你对导师的印象<br>
我们会把这些材料整理成一套可运行的结构：<br>
**Part A — Meeting Memory（组会记忆）+ Part B — Pressure Persona（高压画像）**<br>
生成一个能提前预判导师会怎么批、怎么问、怎么打断你的组会生存辅助器

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [项目结构](#项目结构) · [致敬--引用](#致敬--引用) · [English](README_EN.md)

</div>

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
# 安装到当前项目（在 git 仓库根目录执行）
mkdir -p .claude/skills
git clone https://github.com/Wkk13/mentor-skill.claude/skills/create-mentor

# 或安装到全局（所有项目都能用）
git clone https://github.com/Wkk13/mentor-skill ~/.claude/skills/create-mentor
```


### 依赖（可选）

```bash
pip install -r requirements.txt
```

当前可选依赖主要用于部分图片元信息读取。只做文本类组会预演时，通常不装也能用。

---

## 使用

在 Claude Code 中输入：

```bash
/create-mentor
```

然后按提示输入：

* 导师称呼或代号
* 你最怕的组会场景
* 导师最常怎么批你、怎么追问你
* 你这次汇报最怕被抓住的点
* 可选材料：聊天记录、组会反馈、PPT、笔记、截图

完成后用 `/{slug}` 调用该导师 Skill，开始组会预演。

### 它能帮你做什么

* 提前模拟导师会怎么批你
* 预测本次组会最容易被抓的点
* 生成“批评 - 应对 - 补救动作”预案
* 帮你把一段容易挨批的话改得更稳
* 在你慌的时候分清楚：这是内容漏洞，还是恐惧放大

### 管理命令

| 命令 | 说明 |
|------|------|
| `/create-mentor` | 创建导师 Skill |
| `/list-mentors` | 列出所有导师 Skill |
| `/{slug}` | 调用完整 Skill（模拟导师批评、追问与应对辅助） |
| `/{slug}-memory` | 查看组会记忆模式（高频批评、危险点、情绪触发） |
| `/{slug}-persona` | 查看高压画像模式（导师施压风格与提问路径） |
| `/mentor-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-mentor {slug}` | 删除 |

---

## 效果示例

> 输入：`我的导师组会上特别喜欢先说“你这个没有讲清楚”，然后开始追问定义、实验和意义。我一被打断就会慌。`

**场景一：预测组会会被怎么批**

```text
用户         ❯ 如果我这周就按现在这版 PPT 去讲，我导师最可能先抓什么？

导师.skill   ❯ 他大概率不会耐心听你铺垫完。

               他更像是会在你讲到第二页的时候直接打断：
               “所以你这周到底做了什么？别给我念 PPT，先说结论。”

               然后如果你还在绕，他下一句多半就是：
               “你讲了半天背景，是因为结果拿不出手，还是因为你自己也没想清楚？”

               你现在最危险的地方不是“结果还不够多”，而是“问题定义和结论对不上”。
               换句话说，你这版 PPT 很容易给他一种感觉：
               看起来很忙，实际上没讲明白自己到底推进了什么。
```

**场景二：模拟导师追问**

```text
用户         ❯ 那你来扮演我导师问我

导师.skill   ❯ 好，我先按你导师最常见的路径来：

               1. 你这周到底推进了什么？不要跟我汇报你有多忙，我只听结果。
               2. 这个结果能说明什么？如果说明不了，你为什么还敢把它放在这里？
               3. 你到底是在验证一个假设，还是只是把能跑的东西都跑了一遍？
               4. 你现在这页最核心的信息是什么？如果你自己一句话说不出来，就别指望别人替你总结。
               5. 下周你准备补哪个关键实验？别再跟我说“继续看看”，这不是计划，这是拖延。
```

**场景三：被批以后帮你整理应对**

```text
用户         ❯ 他今天又说我“看起来很忙，但不像有推进”

导师.skill   ❯ 这句话批的不是你忙不忙，而是你没有把“投入”翻译成“有效进展”。

               你下次不要先报过程，先报这三件事：
               1. 这周验证了什么
               2. 哪个假设被支持或被排除
               3. 下一步具体补什么

               你现在缺的不是更努力的语气，而是更像结果汇报的结构。
```

---

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 微信聊天记录 | WeChatMsg / 留痕 / PyWxDump 导出 | 推荐，重点提取导师的批评方式和你的回应 |
| QQ 聊天记录 | txt / mht 导出 | 适合保留较久的师生沟通记录 |
| 组会反馈 / 批注 | 截图 / Markdown / TXT | 最能提取高频批评和追问路径 |
| 汇报稿 / PPT | Markdown / PDF / 图片 | 用于识别本次汇报的危险点 |
| 照片 | JPEG/PNG（含 EXIF） | 可辅助整理时间线与会议上下文 |
| 口述/粘贴 | 纯文本 | 即使没有完整材料，也能先生成初版 |

### 生成的 Skill 结构

每个导师 Skill 由两部分组成：

| 部分 | 内容 |
|------|------|
| **Part A — Meeting Memory** | 高频批评库、追问路径、危险信号、有效/无效应对、情绪触发点 |
| **Part B — Pressure Persona** | 导师的施压风格、关注焦点、可接受回应、踩雷表达与应对建议 |

运行逻辑：`收到汇报内容 → Pressure Persona 判断导师会怎么开刀 → Meeting Memory 补充真实组会案例 → 输出批评预判、应对策略和推荐表达`

### 适合的使用场景

* 组会前一晚不知道该怎么讲
* 怕导师突然追问，想先演练一轮
* 被批完以后想复盘“他到底在批什么”
* 想把“我怕导师”拆成更具体的风险点
* 想提前准备一套被打断后的回应话术

### 进化机制

* **追加资料** → 找到更多聊天记录/组会记录/PPT → 自动分析增量 → merge 进对应部分
* **对话纠正** → 说“他不会这么追问”→ 写入 Correction 层，立即生效
* **版本管理** → 每次更新自动存档，支持回滚

---

## 项目结构

本项目遵循 [AgentSkills](https://agentskills.io) 开放标准：

```text
create-mentor/
├── SKILL.md                    # skill 入口（官方 frontmatter）
├── prompts/                    # Prompt 模板
│   ├── intake.md               #   对话式信息录入
│   ├── memory_analyzer.md      #   组会记忆提取
│   ├── persona_analyzer.md     #   高压画像提取
│   ├── memory_builder.md       #   memory.md 生成模板
│   ├── persona_builder.md      #   persona.md 结构模板
│   ├── merger.md               #   增量 merge 逻辑
│   └── correction_handler.md   #   对话纠正处理
├── tools/                      # Python 工具
│   ├── wechat_parser.py        # 微信聊天记录解析
│   ├── qq_parser.py            # QQ 聊天记录解析
│   ├── social_parser.py        # 社交媒体内容解析
│   ├── photo_analyzer.py       # 照片元信息分析
│   ├── skill_writer.py         # Skill 文件管理
│   └── version_manager.py      # 版本存档与回滚
├── mentors/                    # 生成的导师 Skill
├── docs/PRD.md
├── NOTICE.md
├── INSTALL.md
├── requirements.txt
└── LICENSE
```

---

## 注意事项

* **原材料质量决定还原度**：真实组会记录 + 聊天记录 + PPT > 仅凭口述
* 建议优先提供：
  1. **被批得最惨的那次组会**：最能暴露导师的真实施压路径
  2. **导师的原话**：比“他大概就是这个意思”更有价值
  3. **你卡壳的部分**：最能定位你的真实恐惧触发点
  4. **本次汇报稿/PPT**：最适合直接做预判和改写
* 这个 Skill 的重点是帮你更有准备地面对导师，不是替代真实学术判断
* 批评预判是为了降低恐惧，不是为了放大恐惧

---

### 推荐的聊天记录导出工具

以下工具为独立的开源项目，本项目不包含它们的代码，仅在解析器中适配了它们的导出格式：

- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** — 微信聊天记录导出（Windows）
- **[PyWxDump](https://github.com/xaoyaoo/PyWxDump)** — 微信数据库解密导出（Windows）
- **留痕** — 微信聊天记录导出（macOS）

## 致敬 & 引用

本项目并不是从零开始凭空出现的。

本项目架构灵感来源于：
- **[同事.skill](https://github.com/titanwings/colleague-skill)**（by titanwings）— 首创"把人蒸馏成 AI Skill"的双层架构
- **[前任.skill](https://github.com/therealXiaomanChu/ex-partner-skill)**（by therealXiaomanChu）— 将双层架构迁移到了亲密关系场景
导师.skill 在这些开源创意的基础上，把场景进一步收敛到了：
* 导师压力
* 组会恐惧
* 批评预判
* 追问模拟
* 应对策略生成

也就是说，它关心的不是“导师是谁”本身，而是：

**面对这个导师时，我怎么活过组会。**



本项目当前采用 [MIT License](LICENSE)，并遵循 [AgentSkills](https://agentskills.io) 开放标准，兼容 Claude Code。

---

### 写在最后

> “很多人怕导师，不是因为导师真的不可战胜，而是因为不知道下一句会被捅哪里。”

如果未知是恐惧的来源，那么预演就是最便宜的止痛药。

这个 Skill 不会替你做实验，不会替你写论文，也不会替你去开组会。

但它至少可以帮你在真正坐到会议室之前，先把最糟糕的那一轮在本地跑一遍。

先被它批一次。
先被它追问一次。
先把那句最容易让你慌的话，改成你能接得住的话。



MIT License © [therealXiaomanChu](https://github.com/therealXiaomanChu)
