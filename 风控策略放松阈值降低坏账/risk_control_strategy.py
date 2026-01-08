import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class UserCreditData:
    """
    用户信用数据类，存储用户的各种信用相关信息
    """
    def __init__(self, user_id: str, age: int, income: float, credit_score: int, 
                 debt_to_income: float, loan_amount: float, loan_term: int, 
                 employment_years: int, number_of_credit_lines: int, 
                 late_payments: int, default_history: int, 
                 industry: str, marital_status: str, education: str):
        """
        初始化用户信用数据
        
        Args:
            user_id: 用户ID
            age: 年龄
            income: 月收入
            credit_score: 信用分数
            debt_to_income: 债务收入比
            loan_amount: 申请贷款金额
            loan_term: 贷款期限（月）
            employment_years: 工作年限
            number_of_credit_lines: 信用行数
            late_payments: 逾期次数
            default_history: 违约历史次数
            industry: 行业
            marital_status: 婚姻状况
            education: 教育程度
        """
        self.user_id = user_id
        self.age = age
        self.income = income
        self.credit_score = credit_score
        self.debt_to_income = debt_to_income
        self.loan_amount = loan_amount
        self.loan_term = loan_term
        self.employment_years = employment_years
        self.number_of_credit_lines = number_of_credit_lines
        self.late_payments = late_payments
        self.default_history = default_history
        self.industry = industry
        self.marital_status = marital_status
        self.education = education
        
        # 计算月供
        self.monthly_payment = self._calculate_monthly_payment()
        # 计算月供收入比
        self.payment_to_income = self.monthly_payment / self.income if self.income > 0 else 0
        
    def _calculate_monthly_payment(self) -> float:
        """
        简单计算月供（等额本息）
        假设年利率为5%
        """
        annual_interest_rate = 0.05
        monthly_rate = annual_interest_rate / 12
        if monthly_rate == 0:
            return self.loan_amount / self.loan_term
        return self.loan_amount * monthly_rate * (1 + monthly_rate) ** self.loan_term / \
               ((1 + monthly_rate) ** self.loan_term - 1)


class RiskAssessment:
    """
    风险评估类，用于计算用户的多维度风险分数
    """
    def __init__(self):
        # 各维度权重配置 - 调整权重，提高信用分数和债务情况的权重
        self.weights = {
            'credit_score': 0.35,
            'debt_to_income': 0.25,
            'payment_to_income': 0.15,
            'employment_years': 0.08,
            'late_payments': 0.08,
            'default_history': 0.05,
            'demographics': 0.04
        }
        
        # 行业风险系数（示例）
        self.industry_risk = {
            '金融': 1.0,
            'IT': 0.9,
            '制造业': 1.1,
            '零售': 1.2,
            '教育': 0.8,
            '医疗': 0.85,
            '房地产': 1.3,
            '其他': 1.0
        }
        
        # 教育程度风险系数
        self.education_risk = {
            '博士': 0.7,
            '硕士': 0.8,
            '本科': 0.9,
            '大专': 1.0,
            '高中及以下': 1.2
        }
    
    def calculate_credit_score_risk(self, credit_score: int) -> float:
        """
        计算信用分数风险（0-1，越高风险越大）
        """
        if credit_score >= 750:
            return 0.02
        elif credit_score >= 700:
            return 0.1
        elif credit_score >= 650:
            return 0.2
        elif credit_score >= 600:
            return 0.35
        elif credit_score >= 550:
            return 0.55
        else:
            return 0.8
    
    def calculate_debt_risk(self, debt_to_income: float) -> float:
        """
        计算债务收入比风险（0-1，越高风险越大）
        """
        if debt_to_income < 0.3:
            return 0.03
        elif debt_to_income < 0.4:
            return 0.15
        elif debt_to_income < 0.5:
            return 0.3
        elif debt_to_income < 0.6:
            return 0.5
        elif debt_to_income < 0.7:
            return 0.7
        else:
            return 0.9
    
    def calculate_payment_risk(self, payment_to_income: float) -> float:
        """
        计算月供收入比风险（0-1，越高风险越大）
        """
        if payment_to_income < 0.2:
            return 0.03
        elif payment_to_income < 0.3:
            return 0.15
        elif payment_to_income < 0.4:
            return 0.3
        elif payment_to_income < 0.5:
            return 0.5
        else:
            return 0.75
    
    def calculate_employment_risk(self, employment_years: int) -> float:
        """
        计算就业年限风险（0-1，越高风险越大）
        """
        if employment_years >= 10:
            return 0.05
        elif employment_years >= 5:
            return 0.2
        elif employment_years >= 2:
            return 0.4
        elif employment_years >= 1:
            return 0.6
        else:
            return 0.8
    
    def calculate_payment_history_risk(self, late_payments: int) -> float:
        """
        计算逾期记录风险（0-1，越高风险越大）
        """
        if late_payments == 0:
            return 0.05
        elif late_payments <= 2:
            return 0.2
        elif late_payments <= 5:
            return 0.5
        elif late_payments <= 8:
            return 0.7
        else:
            return 0.9
    
    def calculate_default_risk(self, default_history: int) -> float:
        """
        计算违约历史风险（0-1，越高风险越大）
        """
        if default_history == 0:
            return 0.1
        elif default_history == 1:
            return 0.4
        elif default_history == 2:
            return 0.7
        else:
            return 0.9
    
    def calculate_demographic_risk(self, age: int, industry: str, education: str) -> float:
        """
        计算人口统计学风险（0-1，越高风险越大）
        """
        # 年龄风险
        if age >= 25 and age <= 55:
            age_risk = 0.3
        elif age >= 18 and age < 25:
            age_risk = 0.7
        elif age > 55 and age <= 65:
            age_risk = 0.5
        else:
            age_risk = 1.0
        
        # 行业风险
        industry_risk = self.industry_risk.get(industry, 1.0)
        
        # 教育风险
        education_risk = self.education_risk.get(education, 1.0)
        
        # 综合人口统计学风险
        demographic_risk = (age_risk + industry_risk + education_risk) / 3
        return min(demographic_risk, 1.0)
    
    def calculate_overall_risk_score(self, user_data: UserCreditData) -> Tuple[float, Dict[str, float]]:
        """
        计算综合风险分数（0-100，越高风险越小）
        
        Returns:
            综合风险分数, 各维度风险分数
        """
        # 计算各维度风险（0-1，越高风险越大）
        credit_score_risk = self.calculate_credit_score_risk(user_data.credit_score)
        debt_risk = self.calculate_debt_risk(user_data.debt_to_income)
        payment_risk = self.calculate_payment_risk(user_data.payment_to_income)
        employment_risk = self.calculate_employment_risk(user_data.employment_years)
        payment_history_risk = self.calculate_payment_history_risk(user_data.late_payments)
        default_risk = self.calculate_default_risk(user_data.default_history)
        demographic_risk = self.calculate_demographic_risk(user_data.age, user_data.industry, user_data.education)
        
        # 各维度风险字典
        risk_dimensions = {
            'credit_score_risk': credit_score_risk,
            'debt_risk': debt_risk,
            'payment_risk': payment_risk,
            'employment_risk': employment_risk,
            'payment_history_risk': payment_history_risk,
            'default_risk': default_risk,
            'demographic_risk': demographic_risk
        }
        
        # 计算加权平均风险（越高风险越大）
        weighted_risk = sum(risk * weight for risk, weight in zip(risk_dimensions.values(), self.weights.values()))
        
        # 改进的风险分数转换：使用更平滑的非线性转换，使分数分布更合理
        # 调整转换公式，使分数范围更符合预期（50-95）
        risk_score = 50 + (1 - weighted_risk) * 45
        
        # 对风险分数进行调整，设置更合理的范围
        adjusted_risk_score = max(40, min(95, risk_score))
        
        return round(adjusted_risk_score, 2), risk_dimensions


class RiskControlStrategy:
    """
    风控策略类，用于执行风控规则和决策
    """
    def __init__(self, strict_mode: bool = False):
        """
        初始化风控策略
        
        Args:
            strict_mode: 是否为严格模式（True为严格模式，False为宽松模式）
        """
        self.strict_mode = strict_mode
        self.risk_assessment = RiskAssessment()
        
        # 根据模式设置不同的阈值
        self._set_thresholds()
    
    def _set_thresholds(self):
        """
        根据模式设置不同的风控阈值
        """
        if self.strict_mode:
            # 严格模式阈值
            self.thresholds = {
                'minimum_credit_score': 620,
                'maximum_debt_to_income': 0.50,
                'maximum_payment_to_income': 0.35,
                'minimum_employment_years': 1,
                'maximum_late_payments': 3,
                'maximum_default_history': 1,
                'minimum_risk_score': 60
            }
        else:
            # 宽松模式阈值（放宽标准）
            self.thresholds = {
                'minimum_credit_score': 580,         # 降低40分
                'maximum_debt_to_income': 0.60,     # 提高10个百分点
                'maximum_payment_to_income': 0.45,   # 提高10个百分点
                'minimum_employment_years': 0,      # 允许刚工作
                'maximum_late_payments': 6,         # 增加3次
                'maximum_default_history': 1,       # 允许1次违约历史
                'minimum_risk_score': 55            # 降低5分
            }
    
    def check_hard_rules(self, user_data: UserCreditData) -> Tuple[bool, List[str]]:
        """
        检查硬性规则
        
        Returns:
            是否通过硬性规则, 未通过规则列表
        """
        failed_rules = []
        
        if user_data.credit_score < self.thresholds['minimum_credit_score']:
            failed_rules.append(f"信用分数低于阈值({self.thresholds['minimum_credit_score']})")
        
        if user_data.debt_to_income > self.thresholds['maximum_debt_to_income']:
            failed_rules.append(f"债务收入比高于阈值({self.thresholds['maximum_debt_to_income']})")
        
        if user_data.payment_to_income > self.thresholds['maximum_payment_to_income']:
            failed_rules.append(f"月供收入比高于阈值({self.thresholds['maximum_payment_to_income']})")
        
        if user_data.employment_years < self.thresholds['minimum_employment_years']:
            failed_rules.append(f"工作年限低于阈值({self.thresholds['minimum_employment_years']})")
        
        if user_data.late_payments > self.thresholds['maximum_late_payments']:
            failed_rules.append(f"逾期次数超过阈值({self.thresholds['maximum_late_payments']})")
        
        if user_data.default_history > self.thresholds['maximum_default_history']:
            failed_rules.append(f"违约历史超过阈值({self.thresholds['maximum_default_history']})")
        
        return len(failed_rules) == 0, failed_rules
    
    def evaluate_loan_application(self, user_data: UserCreditData) -> Dict:
        """
        评估贷款申请
        
        Returns:
            评估结果字典
        """
        # 计算综合风险分数
        risk_score, risk_dimensions = self.risk_assessment.calculate_overall_risk_score(user_data)
        
        # 检查硬性规则
        hard_rules_passed, failed_rules = self.check_hard_rules(user_data)
        
        # 改进的决策逻辑：引入风险调整机制
        decision = "拒绝"
        decision_reason = ""
        
        if hard_rules_passed:
            if risk_score >= self.thresholds['minimum_risk_score']:
                decision = "批准"
                decision_reason = "通过硬性规则检查，且综合风险分数达标"
            else:
                # 风险分数接近阈值时，考虑其他补偿因素
                if risk_score >= self.thresholds['minimum_risk_score'] - 5:
                    # 检查是否有补偿因素
                    has_compensating_factors = False
                    
                    # 高收入补偿
                    if user_data.income > 20000:
                        has_compensating_factors = True
                    # 长期工作稳定性补偿
                    elif user_data.employment_years > 5:
                        has_compensating_factors = True
                    # 良好的教育背景补偿
                    elif user_data.education in ["本科", "硕士", "博士"]:
                        has_compensating_factors = True
                    # 低贷款金额补偿
                    elif user_data.loan_amount < 50000:
                        has_compensating_factors = True
                    
                    if has_compensating_factors:
                        decision = "批准"
                        decision_reason = "风险分数接近阈值，但有补偿因素（高收入/长期工作/良好教育/低贷款金额）"
                    else:
                        decision = "拒绝"
                        decision_reason = f"综合风险分数低于阈值({self.thresholds['minimum_risk_score']})，且无补偿因素"
                else:
                    decision = "拒绝"
                    decision_reason = f"综合风险分数低于阈值({self.thresholds['minimum_risk_score']})"
        else:
            # 检查是否有强补偿因素可以突破硬性规则
            has_strong_compensating_factors = False
            strong_factors = []
            
            # 极高信用分数
            if user_data.credit_score >= 750:
                has_strong_compensating_factors = True
                strong_factors.append("极高信用分数")
            # 极高收入
            if user_data.income > 50000:
                has_strong_compensating_factors = True
                strong_factors.append("极高收入")
            # 长期稳定工作
            if user_data.employment_years > 10:
                has_strong_compensating_factors = True
                strong_factors.append("长期稳定工作")
            
            if has_strong_compensating_factors and len(failed_rules) <= 1:
                decision = "批准"
                decision_reason = f"未完全通过硬性规则检查({', '.join(failed_rules)})，但有强补偿因素({', '.join(strong_factors)})"
            else:
                decision = "拒绝"
                decision_reason = f"未通过硬性规则检查: {', '.join(failed_rules)}"
        
        # 构建结果
        result = {
            'user_id': user_data.user_id,
            'decision': decision,
            'decision_reason': decision_reason,
            'risk_score': risk_score,
            'risk_dimensions': risk_dimensions,
            'strict_mode': self.strict_mode,
            'thresholds': self.thresholds,
            'user_data': {
                'age': user_data.age,
                'income': user_data.income,
                'credit_score': user_data.credit_score,
                'debt_to_income': user_data.debt_to_income,
                'loan_amount': user_data.loan_amount,
                'monthly_payment': user_data.monthly_payment,
                'payment_to_income': round(user_data.payment_to_income, 4),
                'employment_years': user_data.employment_years,
                'late_payments': user_data.late_payments,
                'default_history': user_data.default_history
            }
        }
        
        return result
