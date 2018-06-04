@echo off

set strLinker=%SystemRoot%\Microsoft.NET\Framework\v2.0.50727\csc.exe
set strAppName=PaCodeToRegexUtil2017CS

echo %strLinker%
echo.

set strCmd=%strLinker% /target:exe /optimize %strAppName%.cs

echo #%strCmd%
%strCmd%

pause
