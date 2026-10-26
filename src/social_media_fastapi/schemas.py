from pydantic import BaseModel


class PostBase(BaseModel):
    """ This model describes the data you API accepts from client """
    title: str
    content: str
    is_published: bool = True
