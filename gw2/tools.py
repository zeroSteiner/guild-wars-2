#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gw2/tools.py
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

import json

from gw2.currencies import Coins
from gw2.rest import GuildWars2ApiV2

import dateutil.parser

def create_item_name_cache(progress_callback=None, api=None):
	api = api or GuildWars2ApiV2()
	item_ids = api.items()
	item_names = {}
	chunk = 50
	total_items = len(item_ids)
	for i in range(0, total_items, chunk):
		items = api.items(ids=item_ids[i:i + chunk])
		for item in items:
			item_names[item['name']] = item['id']
		if progress_callback:
			progress_callback(i, total_items)
	return item_names

def index_by(items, key, value=None):
	index = {}
	for i in items:
		i_key = i[key]
		if value is None:
			i_value = i
		else:
			i_value = i[value]
		index[i_key] = i_value
	return index

def parse_timestamp(ts):
	return dateutil.parser.parse(ts)

def trade_profit(buy_price, sell_price):
	buy_price = float(buy_price)
	sell_price = float(sell_price)
	margin = sell_price - (sell_price * 0.15)
	margin -= buy_price
	return Coins(margin)
