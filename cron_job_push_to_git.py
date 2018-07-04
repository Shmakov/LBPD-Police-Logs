import subprocess
import os

current_path = os.path.dirname(os.path.realpath(__file__))
pdf_logs_path = current_path + "/pdf_logs/"

os.chdir(current_path)
subprocess.run(['git', 'pull'])
os.chdir(pdf_logs_path)
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', 'cron job: new log file(s)'])
subprocess.run(['git', 'push'])