<h1 align="center">
  🎓 校园二手交易平台 <br>
  <sub><code>Campus Market</code></sub>
</h1>

<p align="center">
  <i>让闲置流动起来 —— 安全、便捷的校园 C2C 交易空间</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white&style=for-the-badge" alt="Django">
  <img src="https://img.shields.io/badge/Tailwind_CSS-v3-06B6D4?logo=tailwindcss&logoColor=white&style=for-the-badge" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/Alpine.js-3.x-8BC0D0?logo=alpine.js&logoColor=white&style=for-the-badge" alt="Alpine.js">
  <img src="https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white&style=for-the-badge" alt="SQLite">
</p>

---

## 📖 项目简介

校园二手交易平台是一个专为高校学生打造的 **C2C 闲置物品交易系统**，覆盖从发布到交易的完整闭环：

- 📸 **多图发布** — 拖拽上传 9 张图，拖拽排序，轮播展示
- 🔍 **搜索筛选** — 关键词高亮、价格区间、多维排序、热门标签
- ❤️ **收藏关注** — 商品收藏，心形切换，我的收藏管理
- 🛒 **交易订单** — 下单→确认→交易中→完成，状态时间线追踪
- 💬 **留言互动** — AJAX 留言/回复/删除，嵌套展示
- 🔔 **实时通知** — 铃铛角标，订单/留言推送，相对时间
- 👤 **个人主页** — 资料编辑、头像上传、统计面板
- 📱 **移动端适配** — 汉堡菜单、底部导航栏、固定操作栏

项目采用 **Django MTV 架构** + **Tailwind CSS** + **Alpine.js** 构建，注重前后端分离 API 设计、权限校验、UI 审美的平衡，设计风格参考闲鱼 App 网页版。

---

## 🧰 核心技术栈

| 层级 | 技术 | 说明 |
|:---|:---|:---|
| 🔙 后端框架 | **Django 5.2** | ORM、MTV 模式、用户认证、表单验证、JSON API |
| 🎨 前端样式 | **Tailwind CSS (CDN)** | 原子化 CSS，自定义动画（toast/fade/skeleton） |
| ⚡ 前端交互 | **Alpine.js 3.x (CDN)** | 轻量响应式框架：轮播、收藏、通知、Tab 切换 |
| 🗄️ 数据库 | **SQLite** | 零配置开发；索引优化，可平滑迁移至 MySQL/PostgreSQL |
| 📝 模板 | **Django Template Language** | 配合 Tailwind 实现组件化页面 + 自定义模板标签 |
| 🧩 图标 | **SVG Inline** | 轻量图标方案，无需额外字体库 |

---

## ✨ 功能清单

### 🔐 用户系统
- [x] 注册（用户名 + 密码，注册即自动登录，前端+后端双重校验）
- [x] 登录 / 注销（带 `?next=` 回跳，输入非空校验）
- [x] 注册时自动创建 UserProfile（信号机制 `get_or_create` 防竞态）
- [x] 个人资料编辑（头像、昵称、手机号、微信号、宿舍区、个人简介）
- [x] 头像上传圆形预览 + 前端即时预览 + 清除功能
- [x] 导航栏显示 `display_name`（昵称优先）

### 📦 商品模块
- [x] **多图上传**（拖拽/点击选择，最多 9 张，拖拽排序，缩略图预览）
- [x] 商品发布（标题、价格、描述、分类、多图）
- [x] 商品列表页（公开浏览，瀑布流卡片网格）
- [x] **图片轮播**（左右箭头 + 小圆点指示器 + 触屏滑动）
- [x] 商品详情页（左右分栏 / 移动端上下布局）
- [x] 我的商品管理（统计面板 5 指标 + 下架/上架/删除）
- [x] 商品状态机：在售 ⇄ 交易中 → 已售出 / 已下架
- [x] 浏览量统计（F 表达式防竞态）
- [x] 分类胶囊筛选（横向滚动 + 选中态黑白高亮）
- [x] **搜索增强**：排序下拉（5 种）、价格区间筛选、关键词 `<mark>` 高亮、热门搜索标签
- [x] **空搜索结果友好提示**（引导浏览全部/清除搜索）

### ❤️ 收藏系统
- [x] 心形按钮（Alpine.js 无刷新切换，实心红/空心灰，弹跳动画）
- [x] 收藏计数（商品卡片 + 详情页）
- [x] 「我的收藏」标签页（商品卡片网格 + 取消收藏）
- [x] 软删除机制（`is_active` 标记，保留收藏记录）

### 🛒 订单系统
- [x] 完整订单生命周期：待确认 → 交易中 → 已完成 / 已取消
- [x] 「我想要」按钮（商品详情页，毛玻璃确认弹窗）
- [x] 商品状态自动联动：下单→交易中，取消→在售，完成→已售出
- [x] 「我的订单」页面（我买到的 / 我卖出的 标签切换）
- [x] 订单卡片：商品信息 + 对方昵称 + 状态标签 + **状态时间线**（横线+圆点）
- [x] 卖家操作：确认交易 / 拒绝 / 标记完成
- [x] 联系方式互见（确认后双方可查看对方手机/微信）
- [x] 取消原因记录 + 状态筛选胶囊

### 💬 留言系统
- [x] AJAX 留言列表（页面加载渲染，无需刷新）
- [x] 留言输入框（登录可见，字数 500 限制 + 实时计数）
- [x] 留言卡片：头像/昵称/时间/内容，楼层分割线
- [x] **嵌套回复**（`@用户名`，缩进 + 左边框）
- [x] 删除留言（作者或商品所有者可见，AJAX 无刷新）
- [x] 前端+后端双重校验

### 🔔 通知系统
- [x] 导航栏铃铛图标（Alpine.js 下拉面板）
- [x] 未读红色数字角标（>99 显示 99+）
- [x] 5 种通知类型：新留言 / 新订单 / 订单确认 / 取消 / 完成
- [x] 通知列表：类型图标 + 标题/内容/相对时间 + 已读/未读区分（蓝底/白底）
- [x] 点击跳转对应页面 + 自动标记已读
- [x] 「全部已读」按钮
- [x] 30 秒自动轮询未读数
- [x] 分页加载（每页 20 条）

### 🎨 UI/UX 增强
- [x] **卡片悬浮增强**：scale(1.05) + 旋转 2° + shadow-2xl + 快速预览按钮滑入
- [x] **Toast 消息通知**：顶部滑入，3 秒消失，成功绿/失败红/警告黄
- [x] **回到顶部**：滚动 > 500px 显示，平滑滚动
- [x] **骨架屏**：收藏列表 shimmer 动画占位
- [x] **图片模糊懒加载**：blur(10px) → loaded → 清晰（CSS filter transition）
- [x] **按钮微交互**：`active:scale-[0.97]` 按压反馈
- [x] 吸顶毛玻璃导航栏（`backdrop-blur-xl`）

### 📱 移动端适配
- [x] 汉堡菜单 + 展开搜索栏（`<768px`）
- [x] 底部固定导航栏（首页/发布/订单/我的 + 安全区适配）
- [x] 详情页底部固定操作栏（价格 + 我想要 + 联系卖家）
- [x] iOS 防缩放（输入框 16px）
- [x] 响应式卡片网格（2→3→4→5 列）
- [x] 详情页左右分栏自动上下布局
- [x] 轮播图触屏滑动

### 🛠️ Django Admin 后台
- [x] @admin.register 注册全部模型
- [x] 彩色状态圆角标签
- [x] 价格 ¥ 格式化、头像圆形预览
- [x] list_filter / search_fields / date_hierarchy

---

## 🧱 数据模型 (8 个)

| 模型 | 说明 | 关键字段 |
|:---|:---|:---|
| `Category` | 商品分类 | name, icon |
| `Goods` | 商品 | title, price, description, category, user, status, view_count |
| `GoodsImage` | 商品多图 | goods FK, image, sort_order |
| `UserProfile` | 用户资料 | user FK, avatar, nickname, phone, wechat, dormitory, bio |
| `Comment` | 商品留言 | goods FK, user FK, parent FK (self), content |
| `Favorite` | 商品收藏 | user FK, goods FK, is_active (UniqueConstraint) |
| `Order` | 交易订单 | buyer, seller, goods, order_no, status, price, cancel_reason |
| `Notification` | 站内通知 | recipient, sender, type, title, content, link, is_read |

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Git（可选）

### 本地运行

```bash
# 1. 克隆项目
git clone <your-repo-url>
cd Campus_market

# 2. 创建虚拟环境（推荐）
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. 安装依赖
pip install django

# 4. 数据库迁移
python manage.py makemigrations goods
python manage.py migrate

# 5. 创建超级管理员（用于访问 Admin 后台）
python manage.py createsuperuser

# 6. 导入种子数据（可选）
python seed_data.py

# 7. 启动开发服务器
python manage.py runserver
```

### 访问地址

| 地址 | 说明 |
|:---|:---|
| http://localhost:8000/ | 根路径，自动跳转到首页 |
| http://localhost:8000/goods/ | 商品列表（首页） |
| http://localhost:8000/goods/register/ | 用户注册 |
| http://localhost:8000/goods/login/ | 用户登录 |
| http://localhost:8000/goods/add/ | 发布商品 |
| http://localhost:8000/goods/my/ | 我的商品/收藏 |
| http://localhost:8000/goods/orders/ | 我的订单 |
| http://localhost:8000/goods/profile/edit/ | 编辑资料 |
| http://localhost:8000/admin/ | Django 管理后台 |

> 💡 也支持不带 `/goods/` 前缀的便捷短链接：`/register/`、`/login/`、`/logout/`、`/add/` 均会自动重定向到对应页面。

---

## 📡 API 端点一览

### 收藏
| 方法 | 路由 | 说明 |
|:---|:---|:---|
| POST | `/goods/<id>/favorite/` | 切换收藏（JSON 响应） |
| GET | `/goods/favorites/` | 我的收藏列表（JSON） |

### 订单
| 方法 | 路由 | 说明 |
|:---|:---|:---|
| POST | `/goods/<id>/order/create/` | 创建订单 |
| POST | `/goods/orders/<id>/confirm/` | 卖家确认 |
| POST | `/goods/orders/<id>/cancel/` | 取消订单（body: reason） |
| POST | `/goods/orders/<id>/complete/` | 标记完成 |
| GET | `/goods/orders/<id>/` | 订单详情 JSON |
| GET | `/goods/orders/` | 订单列表页 |

### 留言
| 方法 | 路由 | 说明 |
|:---|:---|:---|
| GET | `/goods/<id>/comments/` | 留言列表 JSON |
| POST | `/goods/<id>/comment/add/` | 添加留言（body: content, parent_id） |
| POST | `/goods/<id>/comment/delete/<cid>/` | 删除留言 |

### 通知
| 方法 | 路由 | 说明 |
|:---|:---|:---|
| GET | `/goods/notifications/` | 通知列表 JSON（`?page=N`） |
| GET | `/goods/notifications/unread/` | 未读数 `{unread: N}` |
| POST | `/goods/notifications/read/<id>/` | 标记已读 |
| POST | `/goods/notifications/read-all/` | 全部已读 |

---

## 📁 目录结构

```
Campus_market/
├── campus_market/                  # Django 项目配置
│   ├── settings.py                 # 全局配置 + 媒体文件 + 上传限制
│   ├── urls.py                     # 根路由
│   └── wsgi.py                     # WSGI 入口
│
├── goods/                          # 商品应用（核心业务）
│   ├── models.py                   # 8 个数据模型 + 信号
│   ├── admin.py                    # 管理后台注册与美化
│   ├── urls.py                     # 25+ 条应用路由
│   ├── apps.py                     # 应用配置
│   ├── views/                      # 视图层（按模块拆分）
│   │   ├── goods_views.py          #   商品 CRUD + 搜索筛选
│   │   ├── user_views.py           #   登录/注册 + 资料编辑
│   │   ├── comment_views.py        #   留言 API（树形结构）
│   │   ├── order_views.py          #   订单 API（完整生命周期）
│   │   ├── favorite_views.py       #   收藏 API（软删除）
│   │   └── notification_views.py   #   通知 API（分页+相对时间）
│   ├── services/                   # 业务逻辑层
│   │   ├── goods_service.py        #   商品删除（级联文件清理）
│   │   └── notification_service.py #   通知发送公共函数
│   ├── forms/                      # 表单层
│   │   ├── goods_form.py           #   商品表单 + 图片校验
│   │   └── profile_form.py         #   用户资料表单
│   ├── templatetags/               # 自定义模板标签
│   │   └── highlight_tags.py       #   关键词高亮 <mark>
│   └── templates/                  # 模板层（组件化）
│       ├── base.html               #   全局布局（Toast/回到顶部/骨架/底部导航）
│       ├── goods_list.html         #   首页（搜索/排序/筛选/高亮/热门标签）
│       ├── goods_detail.html       #   详情页（轮播/收藏/留言/下单/移动端操作栏）
│       ├── add_goods.html          #   发布页（多图拖拽上传/排序）
│       ├── my_goods.html           #   个人中心（5 指标/商品管理/收藏标签/骨架屏）
│       ├── my_orders.html          #   订单页（双标签/状态筛选/时间线）
│       ├── order_card.html         #   订单卡片组件（含状态时间线）
│       ├── user_profile.html       #   资料编辑页（头像预览/字数统计）
│       ├── login.html              #   登录页（Indigo 渐变）
│       └── register.html           #   注册页（Emerald 渐变）
│
├── media/                          # 用户上传文件
│   ├── goods/                      #   商品图片
│   └── avatars/                    #   用户头像
│
├── db.sqlite3                      # SQLite 数据库
├── seed_data.py                    # 种子数据脚本
├── manage.py                       # Django CLI 入口
├── .gitignore
└── README.md
```

---

## 📐 订单状态流转

```
买家创建 → [待确认] ──卖家确认──→ [交易中] ──卖家标记完成──→ [已完成]
    ↓ 买/卖家取消                  ↓ 买/卖家取消(需原因)      商品→已售出
  [已取消]                       [已取消]
  商品→恢复在售                   商品→恢复在售
```

---

## 📱 移动端布局断点

| 断点 | 宽度 | 布局变化 |
|:---|:---|:---|
| 默认 | < 480px | 2 列卡片网格 / 详情页上下布局 |
| `sm` | ≥ 640px | 3 列卡片 |
| `md` | ≥ 768px | 桌面导航栏恢复 / 底部导航栏隐藏 / 详情页左右分栏 |
| `lg` | ≥ 1024px | 4 列卡片 |
| `xl` | ≥ 1280px | 5 列卡片 |

---

## 📅 更新日志

### 2026-06-11 — 路由修复 + 注册登录加固

- ✅ 根路径 `/` 自动重定向到 `/goods/`（避免首页 404）
- ✅ 便捷短链接：`/register/`、`/login/`、`/logout/`、`/add/` 自动跳转
- ✅ 配置 `LOGIN_URL` / `LOGIN_REDIRECT_URL` / `LOGOUT_REDIRECT_URL`（修复 `@login_required` 跳转到不存在的 `/accounts/login/` 问题）
- ✅ 修复 `ALLOWED_HOSTS` 为空的问题
- ✅ 注册视图加固：用户名非空/3-20字符/仅允许字母数字下划线连字符，密码非空/≥6字符，捕获创建异常
- ✅ 登录视图加固：用户名和密码非空校验
- ✅ UserProfile 信号改用 `get_or_create` 防竞态，确保所有用户自动拥有资料
- ✅ 所有已存在用户补全 UserProfile 数据

### 2026-06-11 — 移动端适配 + UI 增强

- ✅ 移动端汉堡菜单 + 展开搜索栏
- ✅ 底部固定导航栏（安全区适配 + 当前页高亮）
- ✅ 商品详情页底部固定操作栏
- ✅ iOS 防缩放（input/textarea/select 16px）
- ✅ Toast 消息通知（滑入/自动消失/三色）
- ✅ 回到顶部按钮（>500px 渐显）
- ✅ 卡片悬浮增强（scale+rotate+shadow+快速预览）
- ✅ 骨架屏（shimmer 动画）
- ✅ 图片模糊懒加载（blur→清晰 transition）

### 2026-06-11 — 站内通知系统

- ✅ Notification 模型（5 种类型）
- ✅ 铃铛图标 + 未读角标（30s 轮询）
- ✅ 通知触发：留言/下单/确认/取消/完成
- ✅ 相对时间显示 + 分页加载

### 2026-06-11 — 完整订单系统

- ✅ Order 模型（6 字段 + 4 索引 + 唯一订单号）
- ✅ 状态流转：待确认→交易中→已完成/已取消
- ✅ 「我想要」按钮 + 毛玻璃确认弹窗
- ✅ 我的订单页面（双标签 + 状态筛选 + 时间线）
- ✅ 联系方式互见

### 2026-06-11 — 收藏系统

- ✅ Favorite 模型（软删除 + 联合唯一约束）
- ✅ 心形按钮（Alpine.js 无刷新切换 + 弹跳动画）
- ✅ 我的收藏标签页 + 卡片网格

### 2026-06-11 — 留言互动

- ✅ Comment parent FK 嵌套回复
- ✅ AJAX 加载/添加/删除（无刷新）
- ✅ 回复 @用户名 + 缩进左边框

### 2026-06-11 — 搜索增强

- ✅ 排序下拉（5 种：默认/价格升降/最新/最多浏览）
- ✅ 价格区间筛选
- ✅ 关键词 `<mark>` 高亮 + 热门搜索标签
- ✅ 空搜索结果友好引导

### 2026-06-10 — 多图上传 + 个人资料

- ✅ GoodsImage 模型（一对多 + sort_order）
- ✅ 9 张拖拽上传 + 缩略图排序 + DataTransfer API
- ✅ 商品详情页轮播图（触屏滑动）
- ✅ UserProfile 扩展（nickname/phone/wechat/bio）
- ✅ 个人资料编辑页

### 2026-05-31 — 业务闭环 (v0.4.0)

- 鉴权页面 UI 现代化
- 个人主页重构（统计面板 + 商品管理）
- 搜索 & 分类过滤激活

### 2026-05-31 — 商品详情页 & 发布表单 (v0.3.0)

- 左右分栏详情页
- 联系卖家毛玻璃弹窗
- 发布表单 UI 重写

### 2026-05-31 — 全局 UI 重塑 (v0.2.0)

- 吸顶毛玻璃导航
- Hero 横幅 + 分类胶囊
- 卡片悬浮动画

### 2026-05-31 — 项目初始化 (v0.1.0)

- 数据模型建立
- Admin 后台美化
- 基础 CRUD

---

<p align="center">
  <sub>Built with ❤️ using Django · Tailwind CSS · Alpine.js · Campus Market © 2026</sub>
</p>
