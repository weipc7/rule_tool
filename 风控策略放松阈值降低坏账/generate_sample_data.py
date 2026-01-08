import pandas as pd
import numpy as np
import random
from typing import List

# 配置参数
NUM_USERS = 1000
USER_ID_PREFIX = "USER_"

# 行业列表
INDUSTRIES = ["金融", "IT", "制造业", "零售", "教育", "医疗", "房地产", "其他"]

# 婚姻状况
MARITAL_STATUS = ["单身", "已婚", "离婚", "丧偶"]

# 教育程度
EDUCATION = ["博士", "硕士", "本科", "大专", "高中及以下"]

# 生成随机年龄
def generate_age() -> int:
    return random.randint(18, 70)

# 生成随机收入
def generate_income() -> float:
    # 收入分布：大部分在5000-20000之间，少数高收入
    if random.random() < 0.8:
        return round(random.uniform(5000, 20000), 2)
    else:
        return round(random.uniform(20000, 100000), 2)

# 生成随机信用分数
def generate_credit_score() -> int:
    # 信用分数分布：大部分在600-800之间
    if random.random() < 0.6:
        return random.randint(600, 750)
    elif random.random() < 0.85:
        return random.randint(750, 850)
    else:
        return random.randint(300, 600)

# 生成随机债务收入比
def generate_debt_to_income() -> float:
    # 债务收入比分布：大部分在0.2-0.5之间
    if random.random() < 0.7:
        return round(random.uniform(0.2, 0.5), 4)
    elif random.random() < 0.9:
        return round(random.uniform(0.5, 0.7), 4)
    else:
        return round(random.uniform(0.1, 0.2), 4)

# 生成随机贷款金额
def generate_loan_amount(income: float) -> float:
    # 贷款金额与收入相关，通常为年收入的1-5倍
    annual_income = income * 12
    return round(random.uniform(annual_income, annual_income * 5), 2)

# 生成随机贷款期限
def generate_loan_term() -> int:
    # 贷款期限：12-60个月
    return random.randint(12, 60)

# 生成随机工作年限
def generate_employment_years() -> int:
    # 工作年限分布：大部分在1-10年之间
    if random.random() < 0.7:
        return random.randint(1, 10)
    elif random.random() < 0.9:
        return random.randint(10, 20)
    else:
        return random.randint(0, 1)

# 生成随机信用行数
def generate_credit_lines() -> int:
    # 信用行数分布：大部分在1-5之间
    if random.random() < 0.7:
        return random.randint(1, 5)
    elif random.random() < 0.9:
        return random.randint(5, 10)
    else:
        return 0

# 生成随机逾期次数
def generate_late_payments(credit_score: int) -> int:
    # 逾期次数与信用分数负相关
    if credit_score >= 750:
        return random.randint(0, 1)
    elif credit_score >= 700:
        return random.randint(0, 2)
    elif credit_score >= 650:
        return random.randint(0, 3)
    elif credit_score >= 600:
        return random.randint(1, 5)
    else:
        return random.randint(3, 10)

# 生成随机违约历史
def generate_default_history(credit_score: int) -> int:
    # 违约历史与信用分数负相关
    if credit_score >= 750:
        return 0
    elif credit_score >= 700:
        return random.randint(0, 1)
    elif credit_score >= 650:
        return random.randint(0, 1)
    elif credit_score >= 600:
        return random.randint(0, 2)
    else:
        return random.randint(1, 3)

# 生成单个用户数据
def generate_user_data(user_id: str) -> dict:
    age = generate_age()
    income = generate_income()
    credit_score = generate_credit_score()
    debt_to_income = generate_debt_to_income()
    loan_amount = generate_loan_amount(income)
    loan_term = generate_loan_term()
    employment_years = generate_employment_years()
    number_of_credit_lines = generate_credit_lines()
    late_payments = generate_late_payments(credit_score)
    default_history = generate_default_history(credit_score)
    industry = random.choice(INDUSTRIES)
    marital_status = random.choice(MARITAL_STATUS)
    education = random.choice(EDUCATION)
    
    return {
        "user_id": user_id,
        "age": age,
        "income": income,
        "credit_score": credit_score,
        "debt_to_income": debt_to_income,
        "loan_amount": loan_amount,
        "loan_term": loan_term,
        "employment_years": employment_years,
        "number_of_credit_lines": number_of_credit_lines,
        "late_payments": late_payments,
        "default_history": default_history,
        "industry": industry,
        "marital_status": marital_status,
        "education": education
    }

# 生成所有用户数据
def generate_all_users(num_users: int) -> List[dict]:
    users = []
    for i in range(num_users):
        user_id = f"{USER_ID_PREFIX}{str(i+1).zfill(5)}"
        user_data = generate_user_data(user_id)
        users.append(user_data)
    return users

# 主函数
def main():
    print(f"正在生成 {NUM_USERS} 条用户信用数据...")
    
    # 生成数据
    users_data = generate_all_users(NUM_USERS)
    
    # 转换为DataFrame
    df = pd.DataFrame(users_data)
    
    # 保存到CSV文件
    output_file = "/Users/weipengcheng/Documents/trae_projects/20260108/风控策略放松阈值降低坏账/sample_credit_data.csv"
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"数据生成完成，保存到 {output_file}")
    print("\n数据概览：")
    print(df.head())
    print(f"\n数据集大小：{df.shape[0]} 行, {df.shape[1]} 列")
    print("\n信用分数分布：")
    print(df['credit_score'].describe())

if __name__ == "__main__":
    main()
