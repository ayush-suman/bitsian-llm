sudo apt-get update
sudo apt-get install -yq supervisor python3-distutils python3-pip
pip install --upgrade pip virtualenv

sudo bash /opt/bitsian-ai/log-agent.sh --also-install

useradd -m -d /home/ayush231suman ayush231suman
virtualenv -p python3 /opt/bitsian-ai/venv
/bin/bash -c "source /opt/bitsian-ai/venv/bin/activate"
/opt/bitsian-ai/venv/bin/pip install -r /opt/bitsian-ai/requirements.txt

sudo chown -R ayush231suman:ayush231suman /opt/bitsian-ai

sudo cat > /etc/supervisor/conf.d/bitsian-ai.conf << EOF
[program:bitsianai]
directory=/opt/bitsian-ai
command=/opt/bitsian-ai/venv/bin/python3 main.py
autostart=true
autorestart=true
user=ayush231suman
environment=VIRTUAL_ENV="/opt/bitsian-ai/venv",PATH="/opt/bitsian-ai/venv/bin",HOME="/home/ayush231suman",USER="ayush231suman"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update


