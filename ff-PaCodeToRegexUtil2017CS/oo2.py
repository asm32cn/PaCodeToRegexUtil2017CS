#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
#

import re

_source = 'function   callInit_OK() {'
_source = 'for (var i = 0, ls = A_strNoCheckPage.length; i < ls; i++) {'

_source2 = (
	'function  callInit_OK(){',
	'function callInit_OK(){',
	'function callInit_OK() {',
	'function callInit_OK( ){',
	'function callInit_OK (){',
	'function callInit_OK ( ){ ',
	'function callInit_OK ( ) { '
	)

class RegexUtil():
	WordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
	WriteChars = [' ', '\t', '\r', '\n']
	SpecialChars = '^$[](){}.*?+\\'
	OP = [['+', '-', '*', '/', '~', '|'], '=']
	OPS = ['++', '--', '**', '==', '//']

	def __init__(self):
		self.word  = 0
		self.spec  = 0
		self.space = 0

	def _show(self):
		print 'flag=', self.word, self.spec, self.space

	def _switch(self, n):
		self.word  = 1 if n==2 else 0
		self.spec  = 1 if n==1 else 0
		self.space = 1 if n==0 else 0
		# self._show()

	def toRegexString(self, s):

		_cache = []

		flag = 1
		word = 0
		last = None

		for ch in s:
			if ch in self.WriteChars:
				flag = 0
			else:
				flag = 1

			last = _cache[-1] if len( _cache ) else None
			if flag:
				if ch in self.WordChars:
					word = 1
				else:
					word = 0
					if last != '\\s+':
						_cache.append('\\s*')
				if ch in self.SpecialChars:
					_cache.append('\\')
				_cache.append(ch)
			elif ch in self.WriteChars and last in self.WordChars:
				_cache.append('\\s+')

		# _target = ''.join( _cache )
		return ''.join( _cache )

	def toRegexStringEx(self, s):

		_cache = []
		_cacheElement = []

		# word = 0
		w_st = -1
		w_ed = -1

		# space = 0
		s_st = -1
		s_ed = -1

		i = 0

		for ch in s:

			if ch in self.WordChars:
				if self.word == 0:
					w_st = i
				self._switch( 2 )

			else:
				if self.word:
					w_ed = i
					_cacheElement.append( s[w_st : w_ed] )
				self.word = 0

				if ch in self.WriteChars:
					if self.space == 0:
						s_st = i
					self._switch( 0 )
				else:
					if self.space:
						s_ed = i
					self.space = 0

					# if ch not in self.WriteChars and ch not in self.WordChars:
					_cacheElement.append( ch )
					self._switch( 1 )

			_cache.append( ch )

			i += 1

		print '\n'.join( _cacheElement )
		return ''.join( _cache )

ru = RegexUtil()

_target = ru.toRegexStringEx( _source )

ru._show()

print re.findall( 'for\s+\(var\s+i\s+=\s*0\s*\,\s*ls\s*=\s*A_strNoCheckPage\s*\.length\s*;\s*i\s*<\s*ls\s*;\s*i\s*\+\s*\+\s*\)\s*{', _source )
print _target

# print re.findall( _target, _source )

for l in _source2:
	print l
	# print re.findall( _target, l )
