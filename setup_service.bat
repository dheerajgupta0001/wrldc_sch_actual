call nssm.exe install scada_sem_service "%cd%\run_server.bat"
call nssm.exe set scada_sem_service AppStdout "%cd%\logs\scada_sem_service.log"
call nssm.exe set scada_sem_service AppStderr "%cd%\logs\scada_sem_service.log"
call sc start scada_sem_service
rem call nssm.exe edit scada_sem_service