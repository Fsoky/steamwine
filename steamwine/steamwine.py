from typing import Union, List

import json
import asyncio
import aiohttp

from dataclasses import dataclass

from .utils import *


class User:

	def __init__(self, api_key, format):
		self.default_params = {
			"key": api_key,
			"format": format
		}

	async def friends(self, steam_id: int, *, relationship: str="friend"):
		self.default_params["steamid"] = steam_id
		self.default_params["relationship"] = relationship

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/ISteamUser/GetFriendList/v0001/", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					friends_list = FriendsList(data)
					
					for obj in data["friendslist"]["friends"]:
						friends_object = FriendsData(
							obj["steamid"],
							obj["relationship"],
							obj["friend_since"]
						)
						friends_list.friends.append(friends_object)

					return friends_list
				else:
					return response.text

	async def get(self, steam_ids: Union[List[str], int]):
		"""In Development"""

		if not isinstance(steam_ids, list):
			steam_ids = [steam_ids]
		self.default_params["steamids"] = steam_ids

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					users_list = UserResponse(data)

					for obj in data["response"]["players"]:
						users_object = UserResponseData(
							obj["steamid"],
							obj["communityvisibilitystate"],
							obj["profilestate"],
							obj["personaname"],
							obj["commentpermission"],
							obj["profileurl"],
							Avatar(
								obj["avatar"],
								obj["avatarmedium"],
								obj["avatarfull"],
								obj["avatarhash"]
							),
							obj["lastlogoff"],
							obj["personastate"],
							obj["realname"],
							obj["primaryclanid"],
							obj["timecreated"],
							obj["personastateflags"]
						)
						users_list.players.append(users_object)

					return users_list
				else:
					return response.text

	async def achievements(self, steam_id: int, app_id: int):
		self.default_params["steamid"] = steam_id
		self.default_params["appid"] = app_id

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					achievements_list = Achievements(
						data,
						data["playerstats"]["steamID"],
						data["playerstats"]["gameName"],
						data["playerstats"]["success"]
					)

					for obj in data["playerstats"]["achievements"]:
						achievements_object = AchievementsData(
							obj["apiname"],
							obj["achieved"],
							obj["unlocktime"]
						)
						achievements_list.achievements.append(achievements_object)

					return achievements_list
				else:
					return response.text

	async def bans(self, steam_ids: int):
		self.default_params["steamids"] = steam_ids

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/ISteamUser/GetPlayerBans/v1", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					bans_list = PlayerBans(data)

					for obj in data["players"]:
						bans_object = PlayerBansData(
							obj["SteamId"],
							obj["CommunityBanned"],
							obj["VACBanned"],
							obj["NumberOfVACBans"],
							obj["DaysSinceLastBan"],
							obj["NumberOfGameBans"],
							obj["EconomyBan"]
						)
						bans_list.players.append(bans_object)

					return bans_list
				else:
					return response.text

	async def group_list(self, steam_id: int):
		# what's this?
		self.default_params["steamid"] = steam_id

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/ISteamUser/GetUserGroupList/v1", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					return data
				else:
					return response.text

	async def resolve_vanity_url(self, url: str):
		# what's this?
		self.default_params["vanityurl"] = url

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					return data
				else:
					return response.text


class Service:

	def __init__(self, api_key, format):
		self.default_params = {
			"key": api_key,
			"format": format
		}

	async def owned_games(self, steam_id: int, *, include_appinfo: str=None, include_played_free_games: str=None, appids_filter: list=None):
		self.default_params["steamid"] = steam_id

		if include_appinfo is not None:
			self.default_params["include_appinfo"] = include_appinfo
		if include_played_free_games is not None:
			self.default_params["include_played_free_games"] = include_played_free_games
		if appids_filter is not None:
			self.default_params["appids_filter"] = appids_filter

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					owned_games_list = OwnedGames(data, data["response"]["game_count"])

					for obj in data["response"]["games"]:
						owned_games_object = OwnedGamesData(
							obj["appid"],
							PlaytimeForever(
								obj["playtime_forever"],
								obj["playtime_windows_forever"],
								obj["playtime_mac_forever"],
								obj["playtime_linux_forever"]
							)
						)
						owned_games_list.games.append(owned_games_object)

					return owned_games_list
				else:
					return response.text

	async def recently_played_games(self, steam_id: int, *, count: int=2):
		self.default_params["steamid"] = steam_id
		self.default_params["count"] = count

		async with aiohttp.ClientSession() as session:
			async with session.get("http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/", params=self.default_params) as response:
				if self.default_params["format"] == "json":
					data = await response.json()
					recently_played_games_list = RecentlyPlayedGames(data, data["response"]["total_count"])

					for obj in data["response"]["games"]:
						recently_played_games_object = RecentlyPlayedGamesData(
							obj["appid"],
							obj["name"],
							obj["playtime_2weeks"],
							obj["img_icon_url"],
							obj["img_logo_url"],
							PlaytimeForever(
								obj["playtime_forever"],
								obj["playtime_windows_forever"],
								obj["playtime_mac_forever"],
								obj["playtime_linux_forever"]
							)
						)
						recently_played_games_list.games.append(recently_played_games_object)

					return recently_played_games_list
				else:
					return response.text


@dataclass
class Labeler:

	user: object
	service: object


class Steam:

	def __new__(cls, api_key, format="json"):
		return Labeler(
			User(api_key, format),
			Service(api_key, format)
		)