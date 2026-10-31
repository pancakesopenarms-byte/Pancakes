import sys
import requests

print(sys.executable)
print(sys.version)
print(sys.platform)

for module_name, module_path in sys.modules.items():
    print(module_name, module_path)

