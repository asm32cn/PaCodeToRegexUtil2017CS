#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
#

import re, os

class RegexUtil():
	WordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
	WriteChars = [' ', '\t', '\r', '\n']
	SpecialChars = '^$[](){}.*?+|\\'
	OP = [['+', '-', '*', '/', '~', '|'], '=']
	OPS = ['++', '--', '**', '==', '//', '||', '&&', '$$']

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

	def toRegexStringEx(self, s):

		_cache = []
		w_st = -1

		i, c, l = 0, 0, len(s)

		for ch in s:

			if c > 0:

				c -= 1

			else:

				c = 0

				if ch in self.WordChars:
					if self.word == 0:
						w_st = i
					self._switch( 2 )

				else:
					if self.word:
						_cache.append( s[w_st : i] )

					if ch in self.WriteChars:
						self._switch( 0 )
					else:

						if i < l - 1:
							ch2 = s[i + 1]
							ss = ch + ch2
							if ss in self.OPS or ch2 == self.OP[1] and ch in self.OPS[0]:
								_cache.append( ss )
								c = 1
							else:
								_cache.append( ch )
						else:
							_cache.append( ch )

						self._switch( 1 )

			i += 1

		def isWord(ss):
			for ch in ss:
				if ch not in self.WordChars:
					return False
			return True

		def fixedData(s):
			return ''.join( [ '\\' + ch if ch in self.SpecialChars else ch for ch in s ] )

		_target = ''
		l = len(_cache)
		for i in xrange( l ):
			_target += fixedData( _cache[i] )
			_target += '\\s+' if ( i < l - 1 and isWord(_cache[i]) and isWord(_cache[i + 1]) ) else '\\s*';

		print '-' * 30 + '\n' + '\n'.join( _cache )
		return _target


os.system('cls')

ru = RegexUtil()

_source = (
	'for (var i = 0, ls = A_strNoCheckPage.length; i < ls; i++) {',
	'function callInit_OK(){',
	'url: "/ConnectorService/BSFunctionPermission",',
	'return $(\'<div/>\').text(s).html();',
	'inndertext = jqHtmlEncode( inndertext );',
	'if(v == \'\\xa0\' || v == null) v = \'&#160;\'',
	'return $.jgrid.htmlEncode( val || "\xa0" );',
	'thead += "<div title=\\"" + $.jgrid.htmlEncode( title ) + "\\" id=\'jqgh_" + ts.p.id + "_" + ts.p.colModel[i].name + "\' " + tdc + ">" + $.jgrid.htmlEncode( ts.p.colNames[i] );',
	"_ctx.setCookie('markedDateTime', (new Date).toGMTString(), {'path':'/' ,'expires': 1 });",
	'var unloadDateTimePrev = new Date( $$.cookie(\'markedDateTime\') || 0 );'
	)


for l in _source:
	r = ru.toRegexStringEx( l )
	print '=' * 30
	ru._show()
	print l
	print r
	print re.findall( r, l )
