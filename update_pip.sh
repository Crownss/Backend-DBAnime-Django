#run command below for update all depedencies
#USAGE $sh update_pip.sh
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U