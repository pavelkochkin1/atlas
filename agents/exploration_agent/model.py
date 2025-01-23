from core.config import settings
from langchain_gigachat import GigaChat

gigachat_model = GigaChat(
    credentials=settings.GIGA_KEY,
    model="GigaChat",
    timeout=30,
    verify_ssl_certs=False,
    temperature=0.3,
)
