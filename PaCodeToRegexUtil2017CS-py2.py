#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python 2.7
#

import re, os

class PaCodeToRegexUtil():
	WordChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
	WriteChars = [' ', '\t', '\r', '\n']
	SpecialChars = '^$[](){}.*?+|\\'
	EOP = ['+', '-', '*', '/', '~', '|']
	DOP = ['++', '--', '**', '==', '//', '||', '&&', '$$']
	StrChars = ['"', '\'']

	def __init__(self):
		self._word  = 0
		self._spec  = 0
		self._space = 0
		self.StrChar = None # '"'
		self._string = 0

		self.ns = 0

	def _show(self):
		print self.ns, 'flag=', self._word, self._spec, self._space, self._string, ' self.StrChar=', self.StrChar
		self.ns += 1

	def _switch(self, n):
		self._space  = 1 if n==0 else 0
		self._spec   = 1 if n==1 else 0
		self._word   = 1 if n==2 else 0
		self._string = 1 if n==4 else 0
		# self.StrChar = '"'
		# self._show()

	def toRegexStringEx(self, s):

		_cache = []
		w_st = -1

		i, c, l = 0, 0, len(s)

		for ch in s:

			def prevCh():
				# print 'prevCh()', s[i - 1], s
				return s[i - 1] if i > 0 else None

			# print prevCh(), ch, self._string, self.StrChar, not self._string and ch in self.StrChars and prevCh() != '\\'
			if not self._string and ch in self.StrChars: # and prevCh() != '\\':
				# print '~' * 30
				w_st = i
				self.StrChar = ch
				self._switch(4)
				# self._show()

			else:

				if self._string:

					if ch == self.StrChar and prevCh() != '\\':

						self.StrChar = None
						self._switch(0)
						# self._show()
						# print 's[w_st : i] =' + s[w_st : i + 1]
						_cache.append( s[w_st : i + 1] )

				else:

					if c > 0:

						c -= 1

					else:

						c = 0

						if ch in self.WordChars:
							if self._word == 0:
								w_st = i
							self._switch( 2 )

						else:
							if self._word:
								_cache.append( s[w_st : i] )

							if ch in self.WriteChars:
								self._switch( 0 )
							else:

								if i < l - 1:
									ch2 = s[i + 1]
									ss = ch + ch2
									if ss in self.DOP or ch2 == '=' and ch in self.EOP:
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

		# _split = '-' * 30
		# print _split + '\n' + '\n'.join( _cache ) + '\n' + _split
		return _target


os.system('cls')

ctru = PaCodeToRegexUtil()

_source = (
	'for (var i = 0, ls = A_strNoCheckPage.length; i < ls; i++) {',
	'function callInit_OK(){',
	'url: "/ConnectorService/BSFunctionPermission",',
	'return $(\'<div/>\').text(s).html();',
	'inndertext = jqHtmlEncode( inndertext );',
	'if(v == \'\\xa0\' || v == null) v = \'&#160;\'',
	'return $.jgrid.htmlEncode( val || "\\xa0" );',
	'thead += "<div title=\\"" + $.jgrid.htmlEncode( title ) + "\\" id=\'jqgh_" + ts.p.id + "_" + ts.p.colModel[i].name + "\' " + tdc + ">" + $.jgrid.htmlEncode( ts.p.colNames[i] );',
	"_ctx.setCookie('markedDateTime', (new Date).toGMTString(), {'path':'/' ,'expires': 1 });",
	'var unloadDateTimePrev = new Date( $$.cookie(\'markedDateTime\') || 0 );'
	)


for l in _source:
	print '=' * 30
	print l
	r = ctru.toRegexStringEx( l )
	# ctru._show()
	print r
	_m = re.findall( r, l )
	print _m
	# if _m: print _m[0]

# _demo1 = (
# 	'thead += "<div title=\\""+ $.jgrid.htmlEncode( title ) + "\\" id=\'jqgh_" + ts.p.id + "_" + ts.p.colModel[i].name + "\' " + tdc + ">" + $.jgrid.htmlEncode( ts.p.colNames[i] );',
# 	'thead += "<div title=\\""+$.jgrid.htmlEncode(title)+"\\" id=\'jqgh_"+ts.p.id+ "_" + ts.p.colModel[i].name + "\' " + tdc + ">" + $.jgrid.htmlEncode( ts.p.colNames[i] );',
# 	'thead += "<div title=\\""+$.jgrid.htmlEncode(title)+"\\" id=\'jqgh_"+ts.p.id+"_"+ts.p.colModel[i].name+"\' "+ tdc + ">" + $.jgrid.htmlEncode( ts.p.colNames[i] );',
# 	'thead += "<div title=\\""+$.jgrid.htmlEncode(title)+"\\" id=\'jqgh_"+ts.p.id+"_"+ts.p.colModel[i].name+"\' "+tdc+">"+$.jgrid.htmlEncode(ts.p.colNames[i] );',
# 	'thead += "<div title=\\""+$.jgrid.htmlEncode(title)+"\\" id=\'jqgh_"+ts.p.id+"_"+ts.p.colModel[i].name+"\' "+tdc+">"+$.jgrid.htmlEncode(ts.p.colNames[i]);',
# )

# r = ctru.toRegexStringEx( _demo1[0] )
# for l in _demo1:
# 	print re.findall( r, l )
