


# 字典
dic = {"a": 1, "b": 2, "c": 3}

# 函数：准备接收关键字参数
def func(a,b,c):
    print(a,b,c)

# ✅ 正确：**dic 把字典拆成 a=1,b=2,c=3 传进去
func(**dic)