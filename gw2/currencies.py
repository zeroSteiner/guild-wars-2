#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gw2/currencies.py
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

import operator

class Coins(object):
	__slots__ = ('_value')
	def __init__(self, copper=0, silver=0, gold=0):
		copper = int(copper)
		copper += silver * 100
		copper += gold * 10000
		self._value = copper

	def __int__(self):
		return self._value

	def __add__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		self._value = operator.add(self._value, other)
		return self

	def __cmp__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		return cmp(self._value, other)

	def __div__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		self._value = operator.div(self._value, other)
		return self

	def __float__(self):
		return float(self._value)

	def __floordiv__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		self._value = operator.floordiv(self._value, other)
		return self

	def __mod__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		self._value = operator.mod(self._value, other)
		return self

	def __mul__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		self._value = operator.mul(self._value, other)
		return self

	def __repr__(self):
		return "<{0} ({1}) >".format(self.__class__.__name__, self.to_string(self._value))

	def __str__(self):
		return self.to_string(self._value)

	def __sub__(self, other):
		if isinstance(other, self.__class__):
			other = other._value
		self._value = operator.sub(self._value, other)
		return self

	@classmethod
	def from_string(cls, coins):
		copper = 0
		modifier = 1
		if coins.startswith('-'):
			coins = coins[1:]
			modifier = -1
		coins = coins.split(' ')
		for token in coins:
			if not token:
				continue
			if token.endswith('c'):
				copper += int(token[:1])
			elif token.endswith('s'):
				copper += int(token[:1]) * 100
			elif token.endswith('g'):
				copper += int(token[:1]) * 10000
			else:
				raise ValueError("unknown token: '{0}'".format(token))
		copper *= modifier
		return cls(copper)

	@staticmethod
	def to_string(coins):
		if isinstance(coins, Coins):
			coins = coins._value
		negative = coins < 0
		coins = abs(coins)
		copper = coins % 100
		coins //= 100
		silver = coins % 100
		coins //= 100
		gold = coins
		value = []
		if gold:
			value.append("{0:,}g".format(gold))
		if silver or gold:
			value.append("{0}s".format(silver))
		value.append("{0}c".format(copper))
		value = ' '.join(value)
		if negative:
			value = '-' + value
		return value
