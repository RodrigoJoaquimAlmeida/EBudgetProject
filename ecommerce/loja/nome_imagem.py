import os
from datetime import datetime
import random

def produto_imagem_path(instance, filename):   
    ext = filename.split('.')[-1]
    now = datetime.now()
    random_num = random.randint(1000, 9999)
    filename = f'{now.strftime("%Y%m%d%H%M%S")+f"{now.microsecond:06d}_{random_num}"}.{ext}'  
    return os.path.join('produtos', filename)