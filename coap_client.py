import asyncio
import aiocoap

async def health_check():
    protocol = await aiocoap.Context.create_client_context()

    request = aiocoap.Message(code=aiocoap.GET, uri="coap://localhost/health")

    try: 
        response = await protocol.request(request).response
    except Exception as e:
        print("Fail to fetch resource [-]")
        print(e)
    else:
        print(f"Gained message: {response.code} - {response.payload}")

async def get_counter():

    protocol = await aiocoap.Context.create_client_context()

    request = aiocoap.Message(code=aiocoap.GET, uri="coap://localhost/counter")

    try: 
        response = await protocol.request(request).response
    except Exception as e:
        print("Fail to fetch resource [-]")
        print(e)
    else:
        print(f"Gained message: {response.code} - {response.payload}")

async def inc_counter():

    protocol = await aiocoap.Context.create_client_context()

    request = aiocoap.Message(code=aiocoap.Code.POST, uri='coap://localhost/counter')
    response = await protocol.request(request).response
    print(f"Counter after increment: {response.payload.decode()}")

async def observe_resource():

    # Создаем контекст клиента
    context = await aiocoap.Context.create_client_context()

    # Создаем запрос с наблюдением
    request = aiocoap.Message(code=aiocoap.Code.GET, uri='coap://localhost/observation', observe=0)

    # Отправляем запрос и подписываемся на изменения
    pr = context.request(request)
    response = await pr.response  # Первый ответ
    print(f"Initial response: {response.payload.decode()}")

    async for response in pr.observation:
        print(f"Observation update: {response.payload.decode()}")

# Multicast запрос
async def send_multicast():
    # Создаем контекст клиента
    context = await aiocoap.Context.create_client_context()

    # Создаем multicast-запрос
    request = aiocoap.Message(code=aiocoap.Code.GET, uri='coap://localhost/multicast')  # Групповой адрес для CoAP

    # Отправляем запрос и ожидаем ответов
    try:
        response = await context.request(request).response
        print(f"Response: {response.payload.decode()}")
    except Exception as e:
        print(f"Failed to fetch response: {e} [-]")


async def obs():        
    # Запускаем наблюдение за ресурсом
    observer_task = asyncio.create_task(observe_resource())

    # Ожидаем завершения наблюдения (можно прервать вручную)
    await observer_task

def client_():

    asyncio.run(send_multicast())
    asyncio.run(get_counter())
    asyncio.run(inc_counter())
    asyncio.run(health_check())
    asyncio.run(obs())

client_()