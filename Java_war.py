import paramiko


class OneKey:
    #定义远程对象
    def __init__(self, hostname, username, password, port=22):
        self.ssh_fd = paramiko.SSHClient()
        self.ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.ssh_fd.connect(hostname, username=username, password=password, port=port)

        #定义远程文件传输对象
        self.transport = paramiko.Transport(hostname, port)
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def exec_cmd(self, cmd):
        stdin, stdout, stderr = self.ssh_fd.exec_command(cmd)
        return stdout.channel.recv_exit_status() == 0

    def copy_file(self, local_src, remote_src):
        self.exec_cmd('touch' + remote_src)
        self.sftp.put(local_src, remote_src)

    def kill_process_by_port(self, port):
        cmd = 'lsof - i:' + str(port)
        stdin, stdout, stderr = self.ssh_fd.exec_command(cmd)
        lines = stdout.readlines()
        if len(lines)>0:
            pid = lines[1].split()[1]

    def __enter__(self):
        return  self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ssh_fd.close()
        self.transport.close()


with OneKey('192.168.150.146', 'root', 'admin') as ssh:
    ssh.exec_cmd('rm -rf /usr/java/apache-tomcat-7.0.103/webapps/webRgSQL.war')
    ssh.exec_cmd('rm -rf /usr/java/apache-tomcat-7.0.103/webapps/webRgSQL')
    ssh.copy_file('C:/Users/asus/Desktop/webRgSQL.war', '/usr/java/apache-tomcat-7.0.103/webapps/webRgSQL.war')
    ssh.kill_process_by_port(8080)
    ssh.exec_cmd('source /etc/profile; /usr/java/apache-tomcat-7.0.103/bin/statup.sh')