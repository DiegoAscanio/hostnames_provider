curl hostnameprovider > temp.txt
set /p final_hostname=<temp.txt
del temp.txt
if not "%final_hostname%" == "" (
    if not "%COMPUTERNAME%" == "%final_hostname%" (
        netdom renamecomputer %COMPUTERNAME% /Newname %final_hostname% /force
        shutdown -r -t 10
    )
)
