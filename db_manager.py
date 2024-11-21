import sqlite3
from datetime import datetime, timedelta
from db_template import DB_BYTES
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
        支持 PyInstaller 打包后的 exe 和普通 Python 运行
        """

        # 确定数据库存储路径
        if getattr(sys, 'frozen', False):
            # 如果是 PyInstaller 环境，使用 _MEIPASS 读取嵌入的数据库
            base_path = sys._MEIPASS  # 临时路径
            db_filename = "genshin_boss_history.db"
            temp_db_path = os.path.join(base_path, db_filename)

            # 确保数据库文件存储在 exe 同级目录
            final_db_path = os.path.join(os.path.dirname(sys.executable), db_filename)

        else:
            # 普通 Python 环境，使用脚本所在目录
            base_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本路径
            db_filename = "genshin_boss_history.db"
            temp_db_path = os.path.join(base_path, db_filename)

            # 确保数据库文件存储在当前目录
            final_db_path = os.path.join(base_path, db_filename)

            

        # 如果数据库文件不存在，创建并写入嵌入的字节流
        if not os.path.exists(final_db_path):
             with open(final_db_path, "wb") as db_file:
                 db_file.write(DB_BYTES)

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
                        draw_date DATE
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
    def add_draw(boss_name):
        try:
            # 获取数据库路径
            db_path = PortableDatabaseManager.get_database_path()
                
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO boss_history (boss_name, draw_date) VALUES (?, ?)", 
                    (boss_name, datetime.now().date())
                )
                conn.commit()
                logging.info(f"成功记录BOSS: {boss_name}")
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
