import random

# 定义区域，BOSS 名称以及对应的权重
boss_by_region = {
    "蒙德": [
        ("无相之风", 4),
        ("无相之雷", 4),
        ("急冻树", 5),
        ("无相之冰", 4),
    ],
    "璃月": [
        ("无相之岩", 4),
        ("纯水精灵", 5),
        ("爆炎树", 5),
        ("古岩龙蜥", 5),
        ("层岩 遗迹巨蛇", 5),
        ("隐山猊兽", 5),
    ],
    "稻妻": [
        ("魔偶剑鬼", 5),
        ("无相之火", 4),
        ("恒常机关阵列", 5),
        ("无相之水", 4),
        ("雷音权现", 5),
        ("黄金王兽", 5),
        ("深海龙蜥之群", 5),
    ],
    "须弥": [
        ("掣电树", 5),
        ("翠翎恐蕈", 5),
        ("兆载永劫龙兽", 5),
        ("半永恒统辖矩阵", 5),
        ("无相之草", 4),
        ("风蚀沙虫", 5),
        ("深罪浸礼者", 5),
    ],
    "枫丹": [
        ("冰风组曲上", 5),
        ("冰风组曲下", 5),
        ("铁甲熔火帝皇", 5),
        ("实验性场力发生装置", 5),
        ("千年珍珠骏麟", 5),
        ("水型幻灵", 5),
        ("魔像督军", 5),
    ],
    "纳塔": [
        ("贪食匿叶龙山王", 5),
        ("金焰绒翼龙暴君", 5),
        ("秘源机兵·构型械", 5),
        ("深邃摹结株", 5),
    ]
}

# 自动生成完整的 BOSS 列表
boss_list = []
for region, bosses in boss_by_region.items():
    for boss, weight in bosses:
        boss_list.append((region, boss, weight))

# 总体力和单次所需体力
total_resin = 200  # 每天体力
boss_resin_cost = 40  # 每次消耗体力
draw_count = total_resin // boss_resin_cost  # 计算需要抽取的次数

# 提取权重
weights = [boss[2] for boss in boss_list]

# 按权重随机抽取 BOSS
selected_bosses = random.choices(boss_list, weights=weights, k=draw_count)

# 确保抽取结果不重复
unique_bosses = []
for boss in selected_bosses:
    if boss not in unique_bosses:
        unique_bosses.append(boss)
    if len(unique_bosses) == draw_count:
        break

# 输出结果
print("今天需要打的 Boss：")
for i, boss in enumerate(unique_bosses, 1):
    region, name, _ = boss  # 解包 BOSS 信息
    print(f"{i}. {region} {name}")

# 防止窗口闪退
input("\n按回车键退出程序...")
