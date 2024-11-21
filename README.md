# Genshin Boss Picker  
*原神体力随机 BOSS 抽取工具*  

## 项目简介  
Genshin Boss Picker 是一个为《原神》玩家设计的小工具，帮助玩家根据每天的体力值随机选择需要挑战的材料BOSS，同时支持根据BOSS所在区域和自定义权重进行抽取。  

该工具旨在让玩家的游戏体验更具随机性，同时节省手动选择目标的时间。  

---

## 功能特色  
- **随机抽取 BOSS**：根据每日体力值自动计算抽取次数，并随机选择挑战目标。  
- **支持权重配置**：玩家可以为不同的 BOSS 设置权重，提高某些 BOSS 的出现概率。  
- **区域分类**：BOSS 按照所在区域分类，抽取结果会显示地名和具体 BOSS 名称。  
- **可自定义数据**：支持修改 BOSS 列表和权重信息，方便扩展。  

---

## 使用方法  
小白使用带图形界面的程序直接访问[链接](https://github.com/huiqiang233/genshin-boss-picker/releases)
1. 确保你的系统已安装Python（推荐版本 3.7 及以上）。  
2. 下载或克隆本项目代码：

   ```bash
   git clone https://github.com/huiqiang233/genshin-boss-picker.git
   cd genshin-boss-picker
   ```
3. 编辑代码中的 boss_by_region，根据需要自定义BOSS名称、区域和权重。
运行程序：

   ```bash
   python genshin_boss_picker.py
   ```
4. 程序将输出今日需要挑战的随机 BOSS 列表。

---

## 贡献指南
欢迎大家为项目贡献代码或建议！你可以通过提交 Issue 或 Pull Request 与我联系。
