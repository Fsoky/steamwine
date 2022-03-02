import asyncio
from steamwine import Steam

api = Steam("B073992A27871F131E82FFE17CA788E5")


async def handler():
    friends = await api.users.friends(76561198982570889)

    for friend in friends.friends:
        usr = await api.users.get(friend.steam_id)
        print(usr.objects)


asyncio.get_event_loop().run_until_complete(handler())