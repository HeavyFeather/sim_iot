import asyncio
import aiocoap
import aiocoap.resource as resource

class HealthPulse(resource.Resource):
    async def render_get(self, request):
        payload = (
            "We are alive!".encode("ascii")
        )
        return aiocoap.Message(payload=payload, code=aiocoap.CONTENT)

class MulticastResource(resource.Resource):
    async def render_get(self, request):
        # Отправляем ответ на multicast-запрос
        payload = b"Hello from multicast server!"
        return aiocoap.Message(payload=payload, code=aiocoap.Code.CONTENT)

class ObservableResource(resource.ObservableResource):

    def __init__(self):

        super().__init__()
        self.counter = 0

    async def render_get(self, request):

        self.counter += 1
        payload = (
            f"counter {self.counter}".encode('utf-8')
        )
        return aiocoap.Message(payload=payload, code=aiocoap.Code.CONTENT)

    async def update_observation_count(self, count):
        
        if count:
            print(f"Observers: {count}")

class HttpProxyHandler(resource.Resource):

    def __init__(self):
        super().__init__()
        self.counter = 0

    async def render_get(self, request):
        # Возвращаем текущее значение счетчика
        payload = str(self.counter).encode('utf-8')
        return aiocoap.Message(payload=payload, code=aiocoap.Code.CONTENT)

    async def render_post(self, request):
        # Увеличиваем счетчик на 1
        self.counter += 1

        payload = str(self.counter).encode('utf-8')

        return aiocoap.Message(payload=payload, code=aiocoap.CHANGED)
        


async def server_():

    # создаём ресурс
    root = resource.Site()

    root.add_resource(["health"], HealthPulse())
    root.add_resource(['observation'], ObservableResource())  # Ресурс с поддержкой наблюдения
    root.add_resource(['multicast'], MulticastResource())
    root.add_resource(['counter'], HttpProxyHandler())
    

    await aiocoap.Context.create_server_context(root)

    await asyncio.get_running_loop().create_future()

asyncio.run(server_())

