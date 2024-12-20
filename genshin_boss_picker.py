import random
import logging
from datetime import datetime, timedelta
from db_manager import PortableDatabaseManager as DatabaseManager

# 配置日志
logging.basicConfig(
    level=logging.WARNING, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

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

class BossSelector:

    def __init__(self, 
                 total_resin=200, 
                 boss_resin_cost=40, 
                 max_repeats=3):
        self.total_resin = total_resin  # 每天总树脂
        self.boss_resin_cost = boss_resin_cost  #每次BOSS消耗树脂
        self.max_repeats = max_repeats  #每周最大重复次数
        self.boss_list = boss_list  # 直接使用全局的 boss_list

    # 随机抽取 BOSS
    def random_draw(self, excluded_bosses=None):
        """
        随机抽取BOSS，考虑最近一周的抽取历史和当天已抽取的BOSS
        
        :param excluded_bosses: 需要排除的BOSS名称列表
        :return: 选中的BOSS信息（地区、BOSS名称、权重）
        """
        recent_draws = DatabaseManager.get_recent_draws()
        excluded_bosses = excluded_bosses or set()
        
        # 筛选符合重复次数限制且未在当天抽取的BOSS
        available_bosses = [
            boss for boss in self.boss_list 
            if (recent_draws.get(boss[1], 0) < self.max_repeats and 
                boss[1] not in excluded_bosses)
        ]
        
        # 如果没有符合条件的BOSS，重置可用BOSS列表（但仍排除当天已抽取的）
        if not available_bosses:
            logging.warning("一周内可用BOSS不足，放宽周限制继续抽取。")
            available_bosses = [
                boss for boss in self.boss_list 
                if boss[1] not in excluded_bosses
            ]
            
        # 如果仍然没有可用BOSS，说明所有BOSS都被抽取过了
        if not available_bosses:
            logging.error("没有可用的BOSS可供抽取")
            return None
            
        # 根据权重随机选择
        weights = [boss[2] for boss in available_bosses]
        selected_boss = random.choices(available_bosses, weights=weights, k=1)[0]
        
        # 记录抽取结果
        DatabaseManager.add_draw(selected_boss[1], selected_boss[0])
        
        return selected_boss

    def select_bosses(self):
        """
        根据可用树脂选择不重复的BOSS
        """
        draw_count = self.total_resin // self.boss_resin_cost
        
        bosses = []
        excluded_bosses = set()  # 用于记录当天已抽取的BOSS
        
        for _ in range(draw_count):
            boss = self.random_draw(excluded_bosses)
            if boss is None:  # 如果没有可用BOSS了
                break
                
            bosses.append(boss)
            excluded_bosses.add(boss[1])  # 将已抽取的BOSS添加到排除列表
        
        return bosses

def main():
    try:
        # 初始化数据库
        DatabaseManager.init_db()

        # 查询当天记录
        today_draws = DatabaseManager.get_today_draw()

        today_date = DatabaseManager.get_first_draw_date()
        if not today_date:
            today_date = datetime.now().date()


        if today_draws:
            print(f"{today_date}")
            print("今日已抽取，结果如下：")
            for boss, region in today_draws:
                print(f"{region} {boss}")
        else:
            # 清理7天前的数据
            DatabaseManager.cleanup_old_data(days_to_keep=7)

            # 创建BOSS选择器
            selector = BossSelector()

            # 选择BOSS
            selected_bosses = selector.select_bosses()

            # 打印结果
            print("今日抽取结果：")
            for region, boss, _ in selected_bosses:
                print(f"{region} {boss}")

    except Exception as e:
        logging.error(f"程序执行发生错误: {e}")
    finally:
        input("\n按回车键退出程序...")

if __name__ == "__main__":
    main()