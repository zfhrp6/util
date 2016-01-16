 pip list --outdated | awk '{print $1}' | xargs -I{} pip install -U {}
