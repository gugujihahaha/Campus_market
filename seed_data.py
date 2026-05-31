"""
校园二手交易平台 · 数据填充脚本
创建丰富的分类、商品示例数据与占位图片
"""

import os
import sys
import random
from io import BytesIO

# 强制 UTF-8 输出（Windows GBK 兼容）
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_market.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.images import ImageFile
from goods.models import Category, Goods

import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'goods')
os.makedirs(MEDIA_ROOT, exist_ok=True)


def create_category(icon, name):
    """创建或更新分类"""
    # 先尝试通过 name 查找（处理可能的编码差异）
    qs = Category.objects.filter(name=name)
    if qs.exists():
        cat = qs.first()
        cat.icon = icon
        cat.save()
        return cat
    return Category.objects.create(icon=icon, name=name)


def generate_placeholder_image(width, height, color, text="", save_path=None):
    """用 PIL 生成彩色渐变占位图，模拟真实商品照片"""
    img = Image.new('RGBA', (width, height), (240, 240, 240, 255))
    draw = ImageDraw.Draw(img)

    # 双色渐变背景（模拟真实场景）
    color2 = tuple(max(0, c - 60) for c in color)
    for y in range(height):
        ratio = y / height
        r = int(color[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color[2] * (1 - ratio) + color2[2] * ratio)
        for x in range(width):
            img.putpixel((x, y), (r, g, b, 255))

    # 中心大号 emoji / 文字
    if text:
        try:
            # 尝试用 emoji 作为大图标
            draw_large_centered_text(draw, text, width, height)
        except:
            pass

    # 轻微模糊，更像真实照片
    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))

    if save_path:
        img = img.convert('RGB')
        img.save(save_path, 'JPEG', quality=85)
    return img


def draw_large_centered_text(draw, text, width, height):
    """在图片中心绘制大号文字/图标"""
    # 用 PIL 简单方式：先尝试绘制一个白色圆底
    cx, cy = width // 2, height // 2
    radius = min(width, height) // 4
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        fill=(255, 255, 255, 180),
        outline=(255, 255, 255, 220),
        width=3,
    )
    # 再绘制文字（emoji 可能不渲染，用简单符号替代方案）
    pass


def download_or_generate_image(goods_id, category_icon, index):
    """下载真实占位图，失败则用 PIL 生成"""
    filename = f"goods_{goods_id}_{index}.jpg"
    save_path = os.path.join(MEDIA_ROOT, filename)

    # 如果已存在，直接返回
    if os.path.exists(save_path):
        return filename

    # 尝试从 picsum 下载
    try:
        resp = requests.get(
            f"https://picsum.photos/600/450?random={goods_id * 100 + index}",
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if resp.status_code == 200:
            img = Image.open(BytesIO(resp.content))
            img = img.convert('RGB')
            img.save(save_path, 'JPEG', quality=85)
            print(f"  [download] {filename} from picsum.photos")
            return filename
    except Exception as e:
        print(f"  [warn] picsum download failed: {e}")

    # 降级：PIL 生成彩色占位图
    colors = [
        (220, 180, 140),  # 暖棕
        (140, 180, 220),  # 蓝灰
        (180, 220, 180),  # 绿
        (220, 200, 160),  # 米黄
        (200, 180, 220),  # 淡紫
        (160, 200, 220),  # 青
        (220, 160, 180),  # 粉
        (180, 220, 200),  # 薄荷
        (240, 200, 160),  # 杏
        (200, 220, 240),  # 浅蓝
    ]
    color = colors[goods_id % len(colors)]
    generate_placeholder_image(600, 450, color, category_icon, save_path)
    print(f"  [generated] {filename}")
    return filename


# ==================== 主流程 ====================

print("=" * 60)
print("校园二手 · 数据填充")
print("=" * 60)

# ── 1. 清理旧数据 ──
print("\n[1/4] 清理旧数据...")
Goods.objects.all().delete()
Category.objects.all().delete()
print("  已清除所有商品和分类")

# ── 2. 创建分类 ──
print("\n[2/4] 创建商品分类...")
categories_data = [
    ("📱", "手机数码"),
    ("💻", "电脑办公"),
    ("📚", "书籍教材"),
    ("👔", "服饰鞋包"),
    ("🏠", "生活用品"),
    ("🎮", "游戏动漫"),
    ("🎵", "音乐乐器"),
    ("🏃", "运动户外"),
    ("🎨", "文具用品"),
    ("🔌", "电器配件"),
    ("🪴", "绿植花卉"),
    ("🍜", "零食特产"),
]
categories = []
for icon, name in categories_data:
    cat = create_category(icon, name)
    categories.append(cat)
    print(f"  {icon} {name}  (id={cat.id})")

# ── 3. 确保有用户 ──
print("\n[3/4] 检查用户...")
from django.contrib.auth.hashers import make_password

users = list(User.objects.filter(is_staff=False))
if len(users) < 2:
    # 创建测试用户
    test_users = [
        ("xiaoming", "小明", "xiaoming123"),
        ("xiaohong", "小红", "xiaohong123"),
        ("daxuezhang", "大学长", "daxuezhang123"),
    ]
    for uname, _, pwd in test_users:
        if not User.objects.filter(username=uname).exists():
            User.objects.create_user(username=uname, password=pwd)
            print(f"  创建用户: {uname} / {pwd}")
    users = list(User.objects.filter(is_staff=False))
else:
    print(f"  已有 {len(users)} 个普通用户")

for u in users:
    # 确保每个用户都有 UserProfile
    from goods.models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=u)
    if created or not profile.dormitory:
        dorms = ["南区3栋", "北区5号楼", "东区1栋", "西区7号楼", "研究生公寓A", "留学生公寓"]
        contacts = ["WeChat: campus_" + u.username, "QQ: 123456789", "手机: 138****5678"]
        profile.dormitory = random.choice(dorms)
        profile.contact_info = random.choice(contacts)
        profile.save()
        print(f"  更新 {u.username} 的个人资料")
print(f"  共 {len(users)} 个用户参与数据生成")

# ── 4. 创建商品 ──
print("\n[4/4] 创建示例商品...")

# 商品模板库 (title, price_range, description, category_index, status)
goods_templates = [
    # --- 手机数码 ---
    ("iPhone 14 Pro 256G 暗紫色 国行在保", (4500, 6200),
     "2024年6月购入，国行正品，全套配件齐全。屏幕无划痕，边框轻微使用痕迹，电池健康度91%。因换了16 Pro所以出掉，支持当面验机。",
     0, 0),
    ("华为 Mate 60 Pro 雅丹黑 12+512G", (3800, 5500),
     "去年双十一京东购入，卫星通信功能好用！无拆无修无进水，原装配件都在。送一个UAG防摔壳和一个原装快充头。",
     0, 0),
    ("小米14 Ultra 白色 16G+1T", (3200, 4500),
     "毕业出闲置，拍照很牛的机子，徕卡影像。买了半年不到，几乎全新，一直贴膜戴套使用。",
     0, 1),
    ("AirPods Pro 2代 USB-C接口", (800, 1200),
     "2024年购买，用了不到一年。降噪功能完好，耳机无磕碰。充电仓有轻微划痕，配件齐全。",
     0, 0),
    ("iPad Air 5 星光色 64G WiFi版", (2500, 3500),
     "考研结束出iPad，买来只用来看网课和做笔记，屏幕完美，电池循环不到50次。送一支第三方触控笔。",
     0, 0),

    # --- 电脑办公 ---
    ("MacBook Air M2 午夜色 8+256G", (5000, 6800),
     "2023年底购入，轻度办公使用。电池循环仅80次，外观99新无磕碰。原装充电器和数据线都在，盒子也保留着。",
     1, 0),
    ("ThinkPad X1 Carbon Gen 11 i7-1355U", (4000, 5500),
     "公司配了新电脑所以出这台。商务旗舰轻薄本，980g超轻，键盘手感无敌。16G内存+512G SSD，2.8K OLED屏幕。",
     1, 0),
    ("罗技 MX Master 3S 无线鼠标 黑色", (280, 450),
     "买来用了两个月，手不太适应大鼠标所以出。静音按键，MagSpeed滚轮手感极佳，支持USB-C快充。",
     1, 0),
    ("LG 27寸 4K显示器 27UP850N", (1500, 2200),
     "毕业离校出显示器，Type-C一线连接笔记本超方便。4K分辨率IPS面板，自带音箱，适合设计和剪辑。",
     1, 1),

    # --- 书籍教材 ---
    ("《算法导论》第三版 英文原版", (80, 150),
     "CS必修课教材，几乎全新，只有前两章有少量笔记。经典中的经典，准备出给学弟学妹。",
     2, 0),
    ("《深入理解计算机系统》CSAPP 第三版", (60, 120),
     "考研408必备，书角有轻微折痕但不影响阅读。内页干净无涂画，附送自己整理的笔记电子版。",
     2, 0),
    ("2025考研政治英语数学全程资料", (30, 80),
     "考研上岸出全部资料，包含肖秀荣精讲精练+1000题、张宇18讲、黄皮书真题等。部分书有笔记但不影响使用。",
     2, 0),
    ("《C++ Primer Plus》第六版 中文版", (40, 75),
     "大一C++课买的，看了前一半。书很厚内容全面，适合零基础入门。几乎全新，光盘还在。",
     2, 1),

    # --- 服饰鞋包 ---
    ("Nike Air Force 1 '07 白色 42码", (350, 550),
     "买大了半码所以出，只穿了3次几乎全新。经典纯白配色，百搭神器。鞋盒配件齐全。",
     3, 0),
    ("Jansport 双肩包 经典款 黑色", (100, 200),
     "用了两年但非常耐造，除了底部轻微磨损外其他完好。容量大，装15.6寸笔记本没问题。",
     3, 0),

    # --- 生活用品 ---
    ("九阳小型电煮锅 1.5L 带蒸笼", (40, 90),
     "宿舍神器！功率小不跳闸，煮面煮粥热牛奶都很方便。毕业出，用了不到一年，配件齐全。",
     4, 0),
    ("MUJI 无印良品 超声波香薰机 白色", (150, 280),
     "朋友送的生日礼物，用了半年左右。外观简约颜值高，可以当小夜灯用。送一瓶甜橙精油。",
     4, 0),
    ("可折叠床上桌 带USB风扇和阅读灯", (30, 65),
     "冬天宿舍神器，不用下床就能写作业看剧。可调节高度和角度，折叠后不占空间。",
     4, 1),
    ("三层收纳抽屉柜 白色 带滚轮", (25, 50),
     "放在宿舍桌下刚好，装衣服杂物都好用。抽屉顺滑不卡，搬家便宜出。",
     4, 0),

    # --- 游戏动漫 ---
    ("Nintendo Switch OLED 白色 国行", (1200, 1700),
     "2024年购入，玩的频率不高。屏幕完美无烧屏，Joy-Con无漂移。带塞尔达旷野之息+王国之泪两个卡带。",
     5, 0),
    ("PS5 DualSense 手柄 星辰红", (250, 380),
     "买了两个手柄，这个基本没用过。自适应扳机和触觉反馈体验很棒，PC也能用。",
     5, 0),
    ("初音未来 韶华Ver. 手办 全新未拆", (280, 420),
     "B站会员购预定的，收到后发现自己没地方摆了😂 八角尖尖全新未拆封，带特典明信片。",
     5, 0),

    # --- 音乐乐器 ---
    ("YAMAHA F310 民谣吉他 41寸", (400, 650),
     "大一参加吉他社买的，后来太忙没坚持下来。琴弦最近换过，送调音器+变调夹+吉他包。",
     6, 0),
    ("JBL GO3 便携蓝牙音箱 迷彩绿", (120, 200),
     "防水防尘，洗澡听歌神器。音质在这个价位真的很能打，续航约5小时。",
     6, 0),

    # --- 运动户外 ---
    ("YONEX 天斧AX100ZZ 羽毛球拍 4U", (350, 500),
     "校队训练用的备用拍，现在换了新拍所以出。拍框有一处掉漆但不影响使用，刚换了BG80线26磅。",
     7, 0),
    ("Keep 瑜伽垫 加厚10mm NBR材质", (25, 50),
     "买来在宿舍练瑜伽/拉伸用，基本全新。NBR材质回弹好，送一个收纳绑带。",
     7, 0),
    ("小米手环8 NFC版 亮黑色", (100, 180),
     "换了Apple Watch所以出。续航一周左右，NFC刷门禁公交很方便。表带有使用痕迹但不影响佩戴。",
     7, 0),

    # --- 文具用品 ---
    ("Pilot 百乐78G+ 钢笔 F尖 透明示范", (50, 100),
     "笔圈入门神器，书写顺滑不刮纸。只上过一次墨，基本全新。送一瓶Pilot黑色墨水。",
     8, 0),
    ("国誉 Campus 活页本 B5 40页", (15, 30),
     "日本进口，纸质顺滑不洇墨。买了太多本用不完，全新未使用，带活页夹。",
     8, 0),

    # --- 电器配件 ---
    ("Anker 安克 氮化镓充电器 65W 三口", (80, 150),
     "一个充全部：两个Type-C + 一个USB-A，支持笔记本、平板、手机同时充电。体积小巧出差神器。",
     9, 0),
    ("绿联 Type-C扩展坞 7合1", (100, 180),
     "HDMI+3个USB+SD卡+PD充电，轻薄本必备。铝合金外壳散热好，用了半年功能正常。",
     9, 0),

    # --- 绿植花卉 ---
    ("多肉组合盆栽 6棵精品多头", (20, 50),
     "宿舍养的多肉，品种有桃蛋、熊童子、生石花等。带陶瓷盆和铺面石，好养耐旱。",
     10, 0),

    # --- 零食特产 ---
    ("三只松鼠 坚果大礼包 未拆封", (40, 80),
     "过年收到太多吃不完😂 全新未拆封，保质期到2026年底。包含夏威夷果、腰果、巴旦木等。",
     11, 0),
]

created = 0
for i, (title, price_range, desc, cat_idx, status) in enumerate(goods_templates):
    user = random.choice(users)
    price = round(random.uniform(*price_range), 2)
    # 价格取整好看一点
    if price > 100:
        price = round(price / 10) * 10  # 取整到10
    elif price > 50:
        price = round(price / 5) * 5      # 取整到5

    goods = Goods.objects.create(
        title=title,
        price=price,
        description=desc.strip(),
        category=categories[cat_idx],
        user=user,
        status=status,
        view_count=random.randint(10, 350),
    )

    # 下载/生成商品图片
    icon = categories[cat_idx].icon
    img_filename = download_or_generate_image(goods.id, icon, i)
    goods.image = f"goods/{img_filename}"
    goods.save()

    status_label = "在售" if status == 0 else "交易中"
    print(f"  [{status_label}] {icon} {title[:30]}...  ¥{price}  by {user.username}")

    created += 1

# ── 收尾 ──
print(f"\n{'=' * 60}")
print(f"✅ 完成！共创建/更新 {len(categories)} 个分类、{created} 件商品")
print(f"   图片存放目录: {MEDIA_ROOT}")
print(f"{'=' * 60}")
