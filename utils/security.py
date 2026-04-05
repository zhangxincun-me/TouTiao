"""
from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=['auto'])


# 密码加密
def get_hashed_password(password: str):
    return pwd_context.hash(password)

#密码验证，verify 返回值是布尔型
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

"""


import bcrypt
from passlib.context import CryptContext

# --- 兼容性补丁：解决新版 bcrypt 各种不兼容问题 ---

# 1. 解决缺失 __about__ 属性问题
if not hasattr(bcrypt, "__about__"):
    class About:
        __version__ = bcrypt.__version__
    bcrypt.__about__ = About

# 2. 解决 72 字节强制校验导致的 ValueError
# 我们重新定义一个 hashpw，如果密码超过 72 字节就自动截断
_original_hashpw = bcrypt.hashpw
def patched_hashpw(password, salt):
    if isinstance(password, str):
        password = password.encode('utf-8')
    # 核心：如果超过 72 字节，只取前 72 位
    if len(password) > 72:
        password = password[:72]
    return _original_hashpw(password, salt)

# 把修改后的方法塞回 bcrypt 模块
bcrypt.hashpw = patched_hashpw
# -----------------------------------------------

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=['auto'])

# 密码加密
def get_hashed_password(password: str):
    return pwd_context.hash(password)

# 密码验证
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
    
