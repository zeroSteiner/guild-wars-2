#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gw2/account.py
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

import collections

import gw2.currencies
import gw2.rest
import gw2.tools

TradingPostPrice = collections.namedtuple('TradingPostPrice', ('buy', 'sell'))

class AccountProperty(object):
	def __init__(self, api):
		if isinstance(api, str):
			api = gw2.rest.GuildWars2ApiV2(token=api)
		if not isinstance(api, gw2.rest.GuildWars2ApiV2):
			raise TypeError('api needs to be a GuildWars2ApiV2 instance')
		self._api = api
		self.refresh()

	def refresh(self):
		raise NotImplemented()

class AccountTransactions(AccountProperty):
	__slots__ = ('_api', '_items_info', '_items_prices', 'bought', 'buying', 'selling', 'sold')
	def refresh(self):
		self.bought = self._api.commerce_transactions_history_buys()
		self.buying = self._api.commerce_transactions_current_buys()
		self.selling = self._api.commerce_transactions_current_sells()
		self.sold = self._api.commerce_transactions_history_sells()

		item_ids = set()
		for records in (self.bought, self.buying, self.selling, self.sold):
			for item in records:
				item_ids.add(item['item_id'])
		self._items_info = self._api.items(ids=item_ids)
		self._items_prices = gw2.tools.index_by(self._api.commerce_prices(ids=item_ids), 'id')

	def item_by_id(self, item_id):
		for item in self._items_info:
			if item['id'] == item_id:
				return item
		raise ValueError('id not found')

	def item_by_name(self, item_name):
		for item in self._items_info:
			if item['name'] == item_name:
				return item
		raise ValueError('name not found')

	def item_price_by_id(self, item_id):
		price = self._items_prices[item_id]
		price = TradingPostPrice(
			buy=gw2.currencies.Coins(price['buys']['unit_price']),
			sell=gw2.currencies.Coins(price['sells']['unit_price']))
		return price

	def item_price_by_name(self, item_name):
		item_id = self.item_by_name(item_name)['id']
		return self.item_price_by_id(item_id)

class AccountWallet(AccountProperty):
	__slots__ = ('_api', 'coin', 'gem', 'guild_commendation', 'karma', 'laurel', 'transmutation_charge')
	def refresh(self):
		gw2_currencies = self._api.currencies()
		gw2_currencies = gw2.tools.index_by(self._api.currencies(gw2_currencies), 'id')
		wallet_contents = dict(zip(self.__slots__, (None for _ in self.__slots__)))
		wallet = self._api.account_wallet()
		for item in wallet:
			currency_name = gw2_currencies[item['id']]['name'].lower().replace(' ', '_')
			if not currency_name in wallet_contents:
				continue
			if currency_name == 'coin':
				item['value'] = gw2.currencies.Coins(item['value'])
			setattr(self, currency_name, item['value'])

class Account(object):
	__slots__ = ('_api',)
	def __init__(self, api):
		if isinstance(api, str):
			api = gw2.rest.GuildWars2ApiV2(token=api)
		if not isinstance(api, gw2.rest.GuildWars2ApiV2):
			raise TypeError('api needs to be a GuildWars2ApiV2 instance')
		self._api = api

	@property
	def characters(self):
		character_names = self._api.characters()
		return gw2.tools.index_by(self._api.characters(character_names), 'name')

	@property
	def coins(self):
		wallet = gw2.tools.index_by(self._api.account_wallet(), 'id')
		return gw2.currencies.Coins(wallet[1]['value'])

	@property
	def transactions(self):
		return AccountTransactions(self._api)

	@property
	def wallet(self):
		return AccountWallet(self._api)
