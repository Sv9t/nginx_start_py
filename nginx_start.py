import paramiko, time, requests, datetime

host = '192.168.1.37'
urls = 'http://'
host_url = '{}{}'.format(urls, host)
default_put = '/etc/nginx/conf.d/'
default_time = datetime.datetime.now()
default_put_time = '{}default.{}'.format(default_put, default_time)
user = 'root'
psw = 'root'
port = 22
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def command():
    stdin, stdout, stderr = ssh.exec_command('service nginx start',timeout=10)
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print("SSH - ждем 3 сек")
            time.sleep(3)
    
def restart_nginx():
    stdin, stdout, stderr = ssh.exec_command('service nginx restart',timeout=10)
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print("SSH - ждем 3 сек")
            time.sleep(3)
    
       
def sftp_conf():
    sftp = ssh.open_sftp()
    for i in sftp.listdir('/etc/nginx/conf.d/'):
        time.sleep(2)
        if "default.conf" in i:
            sftp.posix_rename('/etc/nginx/conf.d/default.conf', default_put_time)
            sftp.put(r'C:\Users\Ivanov\Documents\default.conf', '/etc/nginx/conf.d/default.conf')
            time.sleep(2)
            print("SSH - успешно, default.conf переименован и заменен")
            break
    else:   
        sftp.put(r'C:\Users\Ivanov\Documents\default.conf', '/etc/nginx/conf.d/default.conf')
        print("SSH - успешно, default.conf не было, залит")


def sftp_index():
    sftp = ssh.open_sftp()
    sftp.put(r'C:\Users\Ivanov\Documents\index.html', '/usr/share/nginx/html/index.html')
    time.sleep(2)
    print('SSH - успешно залит index.html')

def main():
    try:
        ssh.connect(hostname=host, port=port, username=user, password=psw, timeout=10)
        command()     #запускаем nginx, ждем ответ после запуска команды
        while True:
            try:
                r = requests.get(host_url, timeout=2)
                if r.ok:
                    print('Все в норме!')
                    sftp_index()
                    time.sleep(2)
                    ssh.close()
                    print('Можно работать')
                    break
                else:
                    print(r.status_code)
            except Exception as exption:
                print('Страница не существует!\n', exption)
                sftp_conf()
                time.sleep(2)
                restart_nginx()
                continue
    except Exception as e:
        print(e)
        ssh.close()
       
#Вызов всей функции
if __name__ == '__main__':
    main()