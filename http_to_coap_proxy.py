import asyncio
import logging
from aiocoap import Context, Message, Code
from aiohttp import web

# Конфигурация
COAP_SERVER = "coap://localhost"  # Адрес CoAP-сервера
HTTP_HOST = "127.0.0.1"  # Адрес HTTP-сервера
HTTP_PORT = 8080  # Порт HTTP-сервера

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def coap_request(method, path, payload=None):
    
    try:
        # Создаем CoAP-контекст
        context = await Context.create_client_context()

        # Формируем CoAP-запрос
        coap_code = {
            "GET": Code.GET,
            "POST": Code.POST,
            "PUT": Code.PUT,
            "DELETE": Code.DELETE,
        }.get(method, Code.GET)

        request = Message(code=coap_code, uri=f"{COAP_SERVER}{path}", payload=payload)

        logger.debug(f"Sending CoAP request: {request}")

        # Отправляем запрос и получаем ответ
        response = await context.request(request).response

        logger.debug(f"Received CoAP response: {response.code}, {response.payload}")

        # Возвращаем статус и тело ответа
        return response.code, response.payload
    except Exception as e:
        logger.error(f"CoAP request failed: {e}")
        raise

async def handle_http_request(request):
    
    try:
        # Получаем метод, путь и тело HTTP-запроса
        method = request.method
        path = request.path
        payload = await request.read() if method in ["POST", "PUT"] else None

        logger.debug(f"Received HTTP request: {method} {path}")

        # Конвертация HTTP-запроса в CoAP
        coap_code, coap_payload = await coap_request(method, path, payload)

        # Конвертация CoAP-ответа в HTTP
        return web.Response(status=int(coap_code), body=coap_payload)
    except Exception as e:
        logger.error(f"HTTP request handling failed: {e}")
        return web.Response(status=500, text=str(e))

async def start_http_server():
    
    app = web.Application()
    app.router.add_route("*", "/{path:.*}", handle_http_request)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, HTTP_HOST, HTTP_PORT)

    logger.info(f"HTTP-прокси запущен на http://{HTTP_HOST}:{HTTP_PORT}")
    await site.start()

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(start_http_server())