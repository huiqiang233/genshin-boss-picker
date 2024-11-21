import random
from db_manager import init_db, add_draw, get_recent_draws

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

# 随机抽取 BOSS
def random_draw(boss_list, max_repeats=3):
    recent_draws = get_recent_draws()
    available_bosses = [
        boss for boss in boss_list if recent_draws.get(boss[1], 0) < max_repeats
    ]
    if not available_bosses:  # 如果没有符合条件的 BOSS
        print("一周内所有 BOSS 都已抽取超过三次，放宽限制继续抽取。")
        available_bosses = boss_list  # 忽略限制，重新启用所有 BOSS
    weights = [boss[2] for boss in available_bosses]
    selected_boss = random.choices(available_bosses, weights=weights, k=1)[0]
    add_draw(selected_boss[1])  # 记录抽取结果
    return selected_boss

# 主程序
if __name__ == "__main__":
    init_db()

    print("今日抽取结果：")
    for _ in range(draw_count):
        region, boss, _ = random_draw(boss_list)
        print(f"{region} {boss}")

    # 防止窗口闪退
    input("\n按回车键退出程序...")
