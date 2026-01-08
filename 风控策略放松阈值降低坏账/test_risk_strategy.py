import pandas as pd
import numpy as np
from risk_control_strategy import UserCreditData, RiskControlStrategy
from typing import Dict, List

# 读取模拟数据
def load_sample_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

# 将DataFrame行转换为UserCreditData对象
def create_user_data_from_row(row: pd.Series) -> UserCreditData:
    return UserCreditData(
        user_id=row['user_id'],
        age=row['age'],
        income=row['income'],
        credit_score=row['credit_score'],
        debt_to_income=row['debt_to_income'],
        loan_amount=row['loan_amount'],
        loan_term=row['loan_term'],
        employment_years=row['employment_years'],
        number_of_credit_lines=row['number_of_credit_lines'],
        late_payments=row['late_payments'],
        default_history=row['default_history'],
        industry=row['industry'],
        marital_status=row['marital_status'],
        education=row['education']
    )

# 运行风控策略测试
def run_strategy_test(data: pd.DataFrame) -> Dict[str, List[Dict]]:
    # 创建两种模式的风控策略
    strict_strategy = RiskControlStrategy(strict_mode=True)
    relaxed_strategy = RiskControlStrategy(strict_mode=False)
    
    # 存储结果
    strict_results = []
    relaxed_results = []
    
    # 对每个用户进行评估
    for _, row in data.iterrows():
        user_data = create_user_data_from_row(row)
        
        # 严格模式评估
        strict_result = strict_strategy.evaluate_loan_application(user_data)
        strict_results.append(strict_result)
        
        # 宽松模式评估
        relaxed_result = relaxed_strategy.evaluate_loan_application(user_data)
        relaxed_results.append(relaxed_result)
    
    return {
        'strict': strict_results,
        'relaxed': relaxed_results
    }

# 分析结果
def analyze_results(results: Dict[str, List[Dict]]):
    # 提取结果
    strict_results = results['strict']
    relaxed_results = results['relaxed']
    
    # 计算严格模式统计
    strict_approved = sum(1 for r in strict_results if r['decision'] == '批准')
    strict_rejected = sum(1 for r in strict_results if r['decision'] == '拒绝')
    strict_approval_rate = strict_approved / len(strict_results) * 100
    
    # 计算宽松模式统计
    relaxed_approved = sum(1 for r in relaxed_results if r['decision'] == '批准')
    relaxed_rejected = sum(1 for r in relaxed_results if r['decision'] == '拒绝')
    relaxed_approval_rate = relaxed_approved / len(relaxed_results) * 100
    
    # 计算两种模式下的差异
    approval_rate_diff = relaxed_approval_rate - strict_approval_rate
    additional_approved = relaxed_approved - strict_approved
    
    # 计算风险分数分布
    strict_risk_scores = [r['risk_score'] for r in strict_results]
    relaxed_risk_scores = [r['risk_score'] for r in relaxed_results]
    
    strict_avg_risk = np.mean(strict_risk_scores)
    relaxed_avg_risk = np.mean(relaxed_risk_scores)
    
    # 计算高风险用户被批准的情况（调整阈值为60）
    def calculate_high_risk_approved(results_list: List[Dict], threshold: float = 60) -> int:
        return sum(1 for r in results_list if r['decision'] == '批准' and r['risk_score'] < threshold)
    
    strict_high_risk_approved = calculate_high_risk_approved(strict_results)
    relaxed_high_risk_approved = calculate_high_risk_approved(relaxed_results)
    
    # 计算潜在坏账率（基于风险分数和违约历史）
    def calculate_potential_default_rate(results_list: List[Dict]) -> float:
        approved_users = [r for r in results_list if r['decision'] == '批准']
        if not approved_users:
            return 0.0
        
        # 基于风险分数和违约历史估计违约概率（使用与收益计算相同的逻辑）
        total_default_prob = 0.0
        for user in approved_users:
            # 风险分数越低，违约概率越高
            risk_score = user['risk_score']
            default_history = user['user_data']['default_history']
            credit_score = user['user_data']['credit_score']
            
            # 使用与收益计算相同的违约概率映射
            if risk_score >= 85:
                base_default_prob = 0.005
            elif risk_score >= 80:
                base_default_prob = 0.01
            elif risk_score >= 75:
                base_default_prob = 0.02
            elif risk_score >= 70:
                base_default_prob = 0.035
            elif risk_score >= 65:
                base_default_prob = 0.05
            elif risk_score >= 60:
                base_default_prob = 0.08
            elif risk_score >= 55:
                base_default_prob = 0.12
            else:
                base_default_prob = 0.18
            
            # 结合信用分数调整违约概率
            if credit_score >= 750:
                base_default_prob *= 0.7
            elif credit_score >= 700:
                base_default_prob *= 0.85
            elif credit_score < 600:
                base_default_prob *= 1.2
            
            # 调整违约历史的影响
            if default_history > 0:
                base_default_prob *= (1 + default_history * 0.15)
            
            total_default_prob += base_default_prob
        
        return (total_default_prob / len(approved_users)) * 100
    
    strict_default_rate = calculate_potential_default_rate(strict_results)
    relaxed_default_rate = calculate_potential_default_rate(relaxed_results)
    
    # 输出分析结果
    print("=" * 60)
    print("风控策略效果分析")
    print("=" * 60)
    
    print(f"\n审批结果统计：")
    print(f"严格模式 - 批准: {strict_approved}, 拒绝: {strict_rejected}, 通过率: {strict_approval_rate:.2f}%")
    print(f"宽松模式 - 批准: {relaxed_approved}, 拒绝: {relaxed_rejected}, 通过率: {relaxed_approval_rate:.2f}%")
    print(f"宽松模式相对严格模式 - 通过率提升: {approval_rate_diff:.2f}%, 额外批准用户数: {additional_approved}")
    
    print(f"\n风险分数统计：")
    print(f"严格模式 - 平均风险分数: {strict_avg_risk:.2f}")
    print(f"宽松模式 - 平均风险分数: {relaxed_avg_risk:.2f}")
    
    print(f"\n高风险用户批准情况（风险分数 < 60）：")
    print(f"严格模式 - 高风险批准数: {strict_high_risk_approved}, 占批准比例: {(strict_high_risk_approved/strict_approved*100) if strict_approved > 0 else 0:.2f}%")
    print(f"宽松模式 - 高风险批准数: {relaxed_high_risk_approved}, 占批准比例: {(relaxed_high_risk_approved/relaxed_approved*100) if relaxed_approved > 0 else 0:.2f}%")
    
    print(f"\n潜在坏账率估计：")
    print(f"严格模式 - 潜在坏账率: {strict_default_rate:.2f}%")
    print(f"宽松模式 - 潜在坏账率: {relaxed_default_rate:.2f}%")
    
    # 计算优化效果
    print(f"\n优化效果分析：")
    if strict_approval_rate > 0:
        approval_gain = approval_rate_diff / strict_approval_rate * 100
        print(f"- 审批通过率提升比例: {approval_gain:.2f}%")
    
    if strict_default_rate > 0:
        default_increase = relaxed_default_rate - strict_default_rate
        default_increase_pct = (default_increase / strict_default_rate) * 100
        print(f"- 潜在坏账率增加: {default_increase:.2f}% ({default_increase_pct:.2f}%)")
    
    # 计算风险调整后收益
    # 进一步优化参数：基于实际银行信贷业务的合理参数
    def calculate_risk_adjusted_return(results_list: List[Dict]) -> float:
        approved_users = [r for r in results_list if r['decision'] == '批准']
        if not approved_users:
            return 0.0
        
        total_risk_adjusted_return = 0.0
        for user in approved_users:
            loan_amount = user['user_data']['loan_amount']
            risk_score = user['risk_score']
            default_history = user['user_data']['default_history']
            credit_score = user['user_data']['credit_score']
            
            # 基于风险分数的更合理违约概率映射
            # 风险分数80分对应1%违约概率，70分对应3%，60分对应8%，50分对应15%
            if risk_score >= 85:
                base_default_prob = 0.005
            elif risk_score >= 80:
                base_default_prob = 0.01
            elif risk_score >= 75:
                base_default_prob = 0.02
            elif risk_score >= 70:
                base_default_prob = 0.035
            elif risk_score >= 65:
                base_default_prob = 0.05
            elif risk_score >= 60:
                base_default_prob = 0.08
            elif risk_score >= 55:
                base_default_prob = 0.12
            else:
                base_default_prob = 0.18
            
            # 结合信用分数调整违约概率
            if credit_score >= 750:
                base_default_prob *= 0.7
            elif credit_score >= 700:
                base_default_prob *= 0.85
            elif credit_score < 600:
                base_default_prob *= 1.2
            
            # 调整违约历史的影响（合理的影响程度）
            if default_history > 0:
                base_default_prob *= (1 + default_history * 0.15)
            
            # 计算预期收益 - 使用更合理的信贷收益参数
            # 银行实际贷款利率通常在5-12%之间，此处使用8%作为平均收益率
            interest_rate = 0.08
            loan_term_months = user['user_data']['loan_term'] if 'loan_term' in user['user_data'] else 12
            
            # 计算等额本息月供
            monthly_rate = interest_rate / 12
            if monthly_rate == 0:
                monthly_payment = loan_amount / loan_term_months
            else:
                monthly_payment = loan_amount * monthly_rate * (1 + monthly_rate) ** loan_term_months / \
                               ((1 + monthly_rate) ** loan_term_months - 1)
            
            # 计算总收益（总利息收入）
            total_interest = monthly_payment * loan_term_months - loan_amount
            expected_revenue = total_interest
            
            # 计算预期损失 - 坏账损失率通常在60-80%之间，此处使用70%
            expected_loss = loan_amount * 0.7 * base_default_prob
            
            risk_adjusted_return = expected_revenue - expected_loss
            total_risk_adjusted_return += risk_adjusted_return
        
        return total_risk_adjusted_return
    
    strict_return = calculate_risk_adjusted_return(strict_results)
    relaxed_return = calculate_risk_adjusted_return(relaxed_results)
    
    print(f"\n风险调整后收益估计：")
    print(f"严格模式 - 总收益: {strict_return:,.2f} 元")
    print(f"宽松模式 - 总收益: {relaxed_return:,.2f} 元")
    print(f"宽松模式相对严格模式 - 收益变化: {(relaxed_return - strict_return):,.2f} 元")

# 主函数
def main():
    # 数据文件路径
    data_file = "/Users/weipengcheng/Documents/trae_projects/20260108/风控策略放松阈值降低坏账/sample_credit_data.csv"
    
    # 加载数据
    print("正在加载模拟数据...")
    data = load_sample_data(data_file)
    print(f"数据加载完成，共 {len(data)} 条记录")
    
    # 运行测试
    print("\n正在运行风控策略测试...")
    results = run_strategy_test(data)
    
    # 分析结果
    print("\n正在分析测试结果...")
    analyze_results(results)

if __name__ == "__main__":
    main()
