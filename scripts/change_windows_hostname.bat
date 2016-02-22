curl hostnameprovider > temp.txt
set /p final_hostname=<temp.txt
del temp.txt
if "%final_hostname%" != "" (
    if "%COMPUTERNAME%" != "%final_hostname%" (
        netdom renamecomputer %COMPUTERNAME% /Newname %final_hostname%
        shutdown -r -t 10
    )
)
