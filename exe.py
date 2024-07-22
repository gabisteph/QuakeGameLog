import subprocess

# Executar os scripts simultaneamente
process1 = subprocess.Popen(['python', 'scripts/quakeGameLog.py'])
process2 = subprocess.Popen(['python', 'scripts/report.py'])

# Esperar ambos os processos terminarem
process1.wait()
process2.wait()
