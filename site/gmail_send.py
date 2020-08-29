import smtplib
from email.mime.text import MIMEText

def sendmail(send_email,recv_email,password,title,content,send_name=None,recv_name=None):
    # 만일 보내는 사람, 받는 사람 이름이 없으면 이메일로 대체
    if send_name is None:
        send_name = send_email
    if recv_name is None:
        recv_name = recv_email

    # sendEmail = "구글ID@gmail.com"
    # recvEmail = "받는 이메일"
    # password = "구글 비밀번호"

    smtpName = "smtp.gmail.com" 
    smtpPort = 587 #smtp 포트 번호

    msg = MIMEText(content) 

    msg['Subject'] = title
    msg['From'] = send_name
    msg['To'] = recv_name
 

    s=smtplib.SMTP( smtpName , smtpPort ) #메일 서버 연결
    s.starttls() #TLS 보안 처리
    s.login( send_email , password ) #로그인
    s.sendmail( send_email, recv_email, msg.as_string() )
    s.close() #smtp 서버 연결 종료 

# 테스트
if __name__ == "__main__":
    title = "제목"
    content = "내용"
    send_email = "real.light.bot@gmail.com"
    password = "rkdgmlwl70"
    recv_email = "real.light.manager@gmail.com"
    sendmail(send_email,recv_email,password,title,content)
