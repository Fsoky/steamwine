# steamwine
Example:


```py
import asyncio
from steamwine import Steam

api = Steam("API_KEY")


async def handler():
	friends = await api.user.friends(76561198982570889)

	for friend in friends.friends_list:
		usr = await api.user.get(friend.steam_id)
		print(usr.players[0].name)


asyncio.get_event_loop().run_until_complete(handler())
```
