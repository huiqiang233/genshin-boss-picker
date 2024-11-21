import sqlite3
from datetime import datetime, timedelta
import os
import sys
import logging
import tempfile
import shutil

# 日志配置
logging.basicConfig(
    level=logging.WARNING, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

class PortableDatabaseManager:
    @staticmethod
    def get_database_path():
        """
        获取数据库文件路径
        支持 PyInstaller 打包后的 exe 数据库文件存储在用户的 AppData 目录,和普通 Python 运行
        """
        # 数据库文件名
        db_filename = "genshin_boss_history.db"

        if getattr(sys, 'frozen', False):
            # 如果是 PyInstaller 环境
            appdata_path = os.getenv('APPDATA')  # 获取用户 AppData\Roaming 目录
            if not appdata_path:
                raise EnvironmentError("无法获取用户的 AppData 路径")

            # 确定数据库最终路径
            final_db_path = os.path.join(appdata_path, "genshin_boss_picker", db_filename)

            # 确保 AppData 子目录存在
            os.makedirs(os.path.dirname(final_db_path), exist_ok=True)

            # 如果数据库文件不存在，则从临时目录复制或创建
            if not os.path.exists(final_db_path):
                base_path = sys._MEIPASS  # PyInstaller 的临时路径
                temp_db_path = os.path.join(base_path, db_filename)

                if os.path.exists(temp_db_path):
                    shutil.copy(temp_db_path, final_db_path)
                else:
                    open(final_db_path, "w").close()  # 创建空文件
        else:
            # 普通 Python 环境：数据库存储在脚本同级目录
            base_path = os.path.dirname(os.path.abspath(__file__))
            final_db_path = os.path.join(base_path, db_filename)

            # 如果数据库文件不存在，则创建空文件
            if not os.path.exists(final_db_path):
                open(final_db_path, "w").close()

        return final_db_path
        

    # 初始化数据库
    @staticmethod
    def init_db():
        try:
            # 获取数据库路径
            db_path = PortableDatabaseManager.get_database_path()
                
            # 连接数据库
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS boss_history (
                        boss_name TEXT,
                        draw_date DATE,
                        region TEXT
                    )
                """)
                # 为提高查询效率，添加索引
                cursor.execute(
                    "CREATE INDEX IF NOT EXISTS idx_boss_date ON boss_history(boss_name, draw_date)"
                )
                conn.commit()
                logging.info(f"数据库初始化成功：{db_path}")
        except sqlite3.Error as e:
            logging.error(f"数据库初始化失败: {e}")
            raise

    # 添加抽取记录
    @staticmethod
    def add_draw(boss_name, region):
        try:
            # 获取数据库路径
            db_path = PortableDatabaseManager.get_database_path()
                
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO boss_history (boss_name, draw_date, region) VALUES (?, ?, ?)", 
                    (boss_name, datetime.now().date(), region)
                )
                conn.commit()
                logging.info(f"成功记录BOSS: {region} {boss_name}")
        except sqlite3.Error as e:
            logging.error(f"记录BOSS失败: {e}")

    # 查询一周内的抽取记录
    @staticmethod
    def get_recent_draws():
        try:
            # 获取数据库路径
            db_path = PortableDatabaseManager.get_database_path()
                
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                one_week_ago = datetime.now().date() - timedelta(days=7)
                cursor.execute("""
                    SELECT boss_name, COUNT(*) 
                    FROM boss_history 
                    WHERE draw_date >= ? 
                    GROUP BY boss_name
                """, (one_week_ago,))
                result = dict(cursor.fetchall())
                logging.info(f"查询一周内抽取记录成功，共 {len(result)} 个BOSS")
                return result
        except sqlite3.Error as e:
            logging.error(f"查询抽取记录失败: {e}")
            return {}

    @staticmethod
    def get_today_draw():
        try:
            db_path = PortableDatabaseManager.get_database_path()
            today = datetime.now().date()
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT boss_name, region FROM boss_history 
                    WHERE draw_date = ?
                """, (today,))
                result = cursor.fetchall()
                return result  # 返回 (boss_name, region) 列表
        except sqlite3.Error as e:
            logging.error(f"查询当天记录失败: {e}")
            return []

        
    # 清理过期数据
    @staticmethod
    def cleanup_old_data(days_to_keep=7):
        try:
            db_path = PortableDatabaseManager.get_database_path()
            cutoff_date = datetime.now().date() - timedelta(days=days_to_keep)
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    DELETE FROM boss_history
                    WHERE draw_date < ?
                """, (cutoff_date,))
                conn.commit()
                logging.info(f"成功清理早于 {cutoff_date} 的数据")
        except sqlite3.Error as e:
            logging.error(f"清理数据失败: {e}")

    # 获取当天第一个 BOSS 的写入日期
    @staticmethod
    def get_first_draw_date():
        try:
            db_path = PortableDatabaseManager.get_database_path()
            
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                # 查询当天最早的日期
                cursor.execute("""
                    SELECT draw_date 
                    FROM boss_history
                    WHERE draw_date = (SELECT MIN(draw_date) FROM boss_history)
                    LIMIT 1
                """)
                result = cursor.fetchone()
                return result[0] if result else None  # 返回日期或 None
        except sqlite3.Error as e:
            logging.error(f"查询第一条记录日期失败: {e}")
            return None


