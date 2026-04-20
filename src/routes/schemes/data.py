from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    ### Our Sended request should respect the following attributs:
    file_id : str
    chunk_size : Optional[int] = 200
    overlap_size : Optional[int] = 40
    do_reset : Optional[int] = 0 ## to start from zero again (we can use bool)
    
    
    
    