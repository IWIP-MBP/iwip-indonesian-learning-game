# 🇮🇩 IWIP 印尼语学习与考核游戏化平台 (Indonesian Learning Platform)

面向企业外派及中方员工的**游戏化印尼语通关学习与 KPI 培训考核平台**。系统深度融合了 **Duolingo 式通关学习地图**、**Quizizz 式多样化互动题型**、**49 个常用与行政专项词汇库** 以及 **企业级 KPI 考核分析报表**。界面采用精致的 **iOS 磨砂玻璃 (Glassmorphism) 暗黑美学风格**。

---

## 🌟 核心特性

- **🎮 游戏化通关学习地图**：21 个课程节点（涵盖发音、日常问候、办公会议、安全生产、环保规范等），支持连击加成、经验值 (XP)、等级与通关锁机制。
- **📝 8 大智能题型与标准发音**：词汇选择、中印互译、填空、连线配对、对话拼图、语音辨析等题型，内置印尼语标准发音朗读与解析。
- **📚 49 大场景常用词汇专项学习**：涵盖宿管管理、食堂管理、车辆调度、物资仓储、行政办公室等专项企业词汇，支持“对照学习”与“听/读/写三维测试”。
- **📊 学习数据多维雷达图与看板**：ECharts 可视化呈现学员能力雷达图、学习活跃度热力图与部门横向对比。
- **⚙️ 企业级管理后台**：支持 Excel 批量导入员工花名册、一键导出 KPI 考核报表及自定义 Docker 容器端口配置。

---

## 🛠️ 技术架构

- **前端**：Vue 3 + Vite + Pinia + Bootstrap 5 + ECharts + SheetJS
- **后端**：Python Flask + SQLAlchemy + JWT 认证
- **数据库**：MySQL 8.0 / SQLite 3
- **容器化**：Docker & Docker Compose (Nginx + Backend + Database)

---

## 🚀 快速启动

### 使用 Docker Compose 运行 (推荐)

进入 `docker` 目录执行：

```bash
cd docker
docker compose up -d --build
```

- **前端访问**：`http://localhost:8080`
- **后端接口**：`http://localhost:5000`

---

## 🔑 默认管理员账号

- **工号 (Employee ID)**: `admin`
- **初始密码**: `123456`

---

## 📂 目录结构

```text
├── backend/            # Flask 后端服务 (Blueprints/Models/Utils)
├── database/           # 词汇题库 JSON 与初始化 SQL
├── docker/             # Dockerfile、docker-compose 与 Nginx 配置
├── frontend/           # Vue 3 前端工程代码
├── scripts/            # 题库自动生成与 PDF 词典解析脚本
└── requirements.txt    # Python 依赖清单
```

---

## 📄 许可证

MIT License
