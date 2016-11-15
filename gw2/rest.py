#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gw2/rest.py
#
#  Copyright 2015 Spencer McIntyre <zeroSteiner@gmail.com>
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following disclaimer
#    in the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of the  nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import requests

class ApiError(Exception):
	pass

def _flatten_ids(ids):
	if isinstance(ids, (list, set, tuple)):
		ids = map(str, ids)
		ids = ','.join(ids)
	elif ids is not None:
		ids = str(ids)
	return ids

class GuildWars2ApiV2(object):
	url_base = 'https://api.guildwars2.com/v2/'
	__slots__ = ('_token',)
	def __init__(self, token=None):
		self._token = token

	def __repr__(self):
		return "<{0} token={1!r} >".format(self.__class__.__name__, self._token)

	def _request(self, method, params=None):
		headers = {}
		if self._token:
			headers['Authorization'] = "Bearer {0}".format(self._token)
		response = requests.get(self.url_base + method, headers=headers, params=params)
		if not response.ok:
			raise ApiError()
		return response.json()

	def account(self):
		return self._request('account')

	def account_bank(self):
		return self._request('account/bank')

	def account_dyes(self):
		return self._request('account/dyes')

	def account_inventory(self):
		return self._request('account/inventory')

	def account_materials(self):
		return self._request('account/materials')

	def account_minis(self):
		return self._request('account/minis')

	def account_skins(self):
		return self._request('account/skins')

	def account_wallet(self):
		return self._request('account/wallet')

	def achievements(self, ids=None):
		return self._request('achievements', params={'ids': _flatten_ids(ids)})

	def achievements_daily(self):
		return self._request('achievements/daily')

	def achievements_daily_tomorrow(self):
		return self._request('achievements/daily/tomorrow')

	def achievements_groups(self, ids=None):
		return self._request('achievements/groups', params={'ids': _flatten_ids(ids)})

	def achievements_categories(self, ids=None):
		return self._request('achievements/categories', params={'ids': _flatten_ids(ids)})

	def build(self):
		return self._request('build')

	def characters(self, ids=None):
		return self._request('characters', params={'ids': _flatten_ids(ids)})

	def colors(self, ids=None):
		return self._request('colors', params={'ids': _flatten_ids(ids)})

	def commerce_exchange_coins(self, quantity=100):
		return self._request('commerce/exchange/coins', params={'quantity': quantity})

	def commerce_exchange_gems(self, quantity=100):
		return self._request('commerce/exchange/gems', params={'quantity': quantity})

	def commerce_listings(self, ids=None):
		return self._request('commerce/listings', params={'ids': _flatten_ids(ids)})

	def commerce_prices(self, ids=None):
		return self._request('commerce/prices', params={'ids': _flatten_ids(ids)})

	def commerce_transactions_current_buys(self):
		return self._request('commerce/transactions/current/buys')

	def commerce_transactions_current_sells(self):
		return self._request('commerce/transactions/current/sells')

	def commerce_transactions_history_buys(self):
		return self._request('commerce/transactions/history/buys')

	def commerce_transactions_history_sells(self):
		return self._request('commerce/transactions/history/sells')

	def continents(self, ids=None):
		return self._request('continents', params={'ids': _flatten_ids(ids)})

	def continents_floors(self, continent_id, ids=None):
		return self._request("continents/{0}/floors".format(continent_id), params={'ids': _flatten_ids(ids)})

	def continents_floors_regions(self, continent_id, floor_id, ids=None):
		return self._request("continents/{0}/floors/{1}/regions".format(continent_id, floor_id), params={'ids': _flatten_ids(ids)})

	def continents_floors_regions_maps(self, continent_id, floor_id, region_id, ids=None):
		return self._request("continents/{0}/floors/{1}/regions/{2}/maps".format(continent_id, floor_id, region_id), params={'ids': _flatten_ids(ids)})

	def continents_floors_regions_maps_sectors(self, continent_id, floor_id, region_id, map_id, ids=None):
		return self._request("continents/{0}/floors/{1}/regions/{2}/maps/{3}/sectors".format(continent_id, floor_id, region_id, map_id), params={'ids': _flatten_ids(ids)})

	def continents_floors_regions_maps_pois(self, continent_id, floor_id, region_id, map_id, ids=None):
		return self._request("continents/{0}/floors/{1}/regions/{2}/maps/{3}/pois".format(continent_id, floor_id, region_id, map_id), params={'ids': _flatten_ids(ids)})

	def continents_floors_regions_maps_tasks(self, continent_id, floor_id, region_id, map_id, ids=None):
		return self._request("continents/{0}/floors/{1}/regions/{2}/maps/{3}/tasks".format(continent_id, floor_id, region_id, map_id), params={'ids': _flatten_ids(ids)})

	def currencies(self, ids=None):
		return self._request('currencies', params={'ids': _flatten_ids(ids)})

	def files(self, ids=None):
		return self._request('files', params={'ids': _flatten_ids(ids)})

	def items(self, ids=None):
		return self._request('items', params={'ids': _flatten_ids(ids)})

	def legends(self, ids=None):
		return self._request('legends', params={'ids': _flatten_ids(ids)})

	def maps(self, ids=None):
		return self._request('maps', params={'ids': _flatten_ids(ids)})

	def materials(self, ids=None):
		return self._request('materials', params={'ids': _flatten_ids(ids)})

	def minis(self, ids=None):
		return self._request('minis', params={'ids': _flatten_ids(ids)})

	def professions(self, ids=None):
		return self._request('professions', params={'ids': _flatten_ids(ids)})

	def pvp_games(self, ids=None):
		return self._request('pvp/games', params={'ids': _flatten_ids(ids)})

	def pvp_stats(self):
		return self._request('pvp/stats')

	def quaggans(self, ids=None):
		return self._request('quaggans', params={'ids': _flatten_ids(ids)})

	def recipes(self, ids=None):
		return self._request('recipes', params={'ids': _flatten_ids(ids)})

	def recipes_search_input(self, ids=None):
		return self._request('recipes/search', params={'input': _flatten_ids(ids)})

	def recipes_search_output(self, ids=None):
		return self._request('recipes/search', params={'output': _flatten_ids(ids)})

	def skills(self, ids=None):
		return self._request('skills', params={'ids': _flatten_ids(ids)})

	def skins(self, ids=None):
		return self._request('skins', params={'ids': _flatten_ids(ids)})

	def specializations(self, ids=None):
		return self._request('specializations', params={'ids': _flatten_ids(ids)})

	def titles(self, ids=None):
		return self._request('titles', params={'ids': _flatten_ids(ids)})

	def tokeninfo(self):
		return self._request('tokeninfo')

	def traits(self, ids=None):
		return self._request('traits', params={'ids': _flatten_ids(ids)})

	def worlds(self, ids=None):
		return self._request('worlds', params={'ids': _flatten_ids(ids)})
