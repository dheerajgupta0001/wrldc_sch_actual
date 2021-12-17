call nssm.exe install sch_drawal_service "%cd%\run_server.bat"
call nssm.exe set sch_drawal_service AppStdout "%cd%\logs\sch_drawal_service.log"
call nssm.exe set sch_drawal_service AppStderr "%cd%\logs\sch_drawal_service.log"
call sc start sch_drawal_service
rem call nssm.exe edit scada_sem_service