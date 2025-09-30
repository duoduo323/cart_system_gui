# cart_system_gui PyCharm
# password_tool Lenovo
# 2025/9/7 周日 下午1:42
import bcrypt
from tool_code.loggerOut import logger_file


class PasswordUtils:
    """密码加密工具类"""

    @staticmethod
    def hash_password(password: str) -> str:
        """
        使用bcrypt加密密码
        :param password: 明文密码
        :return: 加密后的密码
        """
        try:
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger_file('error', f"密码加密失败: {e}")
            raise

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        :param plain_password: 用户输入的明文密码
        :param hashed_password: 数据库中存储的加密密码
        :return: 是否匹配
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logger_file('error', f"密码验证失败: {e}")
            return False