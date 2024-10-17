import os
from datetime import datetime

def produto_imagem_path(instance, filename):   
    ext = filename.split('.')[-1]
    now = datetime.now()
    filename = f'{now.strftime("%Y%m%d%H%M%S")+f"{now.microsecond:06d}"}.{ext}'  
    return os.path.join('produtos', filename)