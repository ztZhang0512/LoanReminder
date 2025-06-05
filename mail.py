import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import os

# 邮箱配置
sender = os.getenv('EMAIL_SENDER')     # 发件人邮箱
password = os.getenv('EMAIL_PASSWORD') # 发件人邮箱授权码
receiver = os.getenv('EMAIL_RECEIVER') # 收件人邮箱

# 设置贷款信息
total_loan = 260000  # 贷款总额
loan_start_date = datetime.date(2025, 7, 20)  # 开始还贷日期
monthly_payment_first = 2909.16  # 第一个月还款金额
monthly_payment_rest = 2534.68  # 第二个月起的还款金额
total_months = 120  # 总共还款期数

# 发送邮件函数
def send_email(subject, content):
    # 创建邮件内容
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(sender)
    message['To'] = Header(receiver)
    message['Subject'] = Header(subject)

    try:
        # 连接SMTP服务器并发送邮件
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(sender, password)
        server.sendmail(sender, [receiver], message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")
    finally:
        server.quit()

# 计算当前期数和剩余金额
def calculate_payment(current_date):
    months_passed = (current_date.year - loan_start_date.year) * 12 + current_date.month - loan_start_date.month
    current_month = months_passed + 1  # 当前是第几个月

    if current_month == 1:
        payment = monthly_payment_first
    else:
        payment = monthly_payment_rest

    remaining_amount = total_loan - sum([monthly_payment_first] + [monthly_payment_rest] * (current_month - 1))
    return current_month, payment, remaining_amount
# 主程序逻辑
if __name__ == '__main__':
    current_date = datetime.date.today()
    
    # 判断是否在首次还款日（2025-07-19）或之后，并且是每月19号
    if current_date >= datetime.date(2025, 7, 19) and current_date.day == 19:
        current_month, payment, remaining_amount = calculate_payment(current_date)
        
        if current_month <= total_months:
            subject = f'第{current_month}/{total_months}期还贷提醒'
            content = f'期数：{current_month}\n还款金额：{payment:.2f}元\n剩余金额：{remaining_amount:.2f}元'
            send_email(subject, content)
        else:
            print("已超过还款期数")
    else:
        print("未到还款日，不发送邮件")