set url=hostnameprovider
curl %url% > temp.txt
set /p final_hostname=<temp.txt
del temp.txt
if "%COMPUTERNAME%" != "%final_hostname%" (
    netdom renamecomputer %COMPUTERNAME% /Newname %final_hostname%
    shutdown -r -t 0
)
