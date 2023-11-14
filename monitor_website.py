import os

import requests
import smtplib
import paramiko
import linode_api4
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')

def monitor_application():
    response = requests.get('http://139.144.70.22:8080/')

    try:
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Website is down, fix it!')
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, "Subject: SITE DOWN \n Fix the issue!")

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname='139.144.70.22:8080', username='root')
            stdin, stdout, stderr = ssh.exec_command('docker start c3e706bc905e')
            print(stdout.readlines())
            ssh.close()
    except Exception as ex:
        print(f'Connection error happened: {ex}')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, "Subject: SITE DOWN \n Application not accessible at all!")

        client = linode_api4.linode_client(LINODE_TOKEN)
        server = client.load(linode_api4.Instance, 24920590)
        server.reboot()


schedule.every(5).minutes.do(monitor_application())
