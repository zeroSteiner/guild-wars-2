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

from gw2 import currencies
from gw2 import rest
from gw2 import tools

AccountWallet = collections.namedtuple(
	'AccountWallet',
	(
		'coin',
		'gem',
		'guild_commendation',
		'karma',
		'laurel',
		'transmutation_charge'
	)
)

class Account(object):
	__slots__ = ('_api',)
	def __init__(self, api):
		if isinstance(api, str):
			api = rest.GuildWars2ApiV2(token=api)
		if not isinstance(api, rest.GuildWars2ApiV2):
			raise TypeError('api needs to be a GuildWars2ApiV2 instance')
		self._api = api

	@property
	def characters(self):
		character_names = self._api.characters()
		return tools.index_by(self._api.characters(character_names), 'name')

	@property
	def coins(self):
		wallet = tools.index_by(self._api.account_wallet(), 'id')
		return currencies.Coins(wallet[1]['value'])

	@property
	def wallet(self):
		gw2_currencies = self._api.currencies()
		gw2_currencies = tools.index_by(self._api.currencies(gw2_currencies), 'id')
		wallet_contents = dict(zip(AccountWallet._fields, (None for _ in AccountWallet._fields)))
		wallet = self._api.account_wallet()
		for item in wallet:
			currency_name = gw2_currencies[item['id']]['name'].lower().replace(' ', '_')
			if not currency_name in wallet_contents:
				continue
			if currency_name == 'coin':
				item['value'] = currencies.Coins(item['value'])
			wallet_contents[currency_name] = item['value']
		return AccountWallet(**wallet_contents)
