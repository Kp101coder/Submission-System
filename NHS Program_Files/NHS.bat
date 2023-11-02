::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCyDJGyX8VAjFDBEHVTTAE+/Fb4I5/jHwcK0nV4IVu82a5zS1bqyEPIc7VfleKkL33Zfi/ctHwhdagGXQCcH52dBuQQ=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFDBEHVTTAE+/Fb4I5/jHwcK0nV4IVu82a5zS1bqyDsggqnbxd5skxWlTl8VMPxReagWqfAp6rHZH1g==
::YB416Ek+ZW8=
::
::
::978f952a14a936cc963da21a135fa983
cd Program_Files
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit
jre\bin\java.exe -splash:"Assets\ahsSplash.gif" "LoadingScreen.java"
jre\bin\java.exe -jar "program.jar"
taskkill /IM python.exe
exit