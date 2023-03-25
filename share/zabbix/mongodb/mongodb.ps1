# Zabbix wrapper for mongodb running on local MS Windows
# UserParameter=mongodb.status[*],powershell -NoProfile -ExecutionPolicy Bypass -File C:\zabbix\scripts\mongodb.ps1 $1 $2 $3 $4 $5

param(
[string] $arg1,
[string] $arg2,
[string] $arg3,
[string] $arg4,
[string] $arg5
)

# Replace here : exact path to mongo.exe
$MONGO_BIN="C:\Program Files\MongoDB\Server\3.4\bin\mongo.exe"

$MONGO_CMD="";
$ParameterList = (Get-Command -Name $MyInvocation.InvocationName).Parameters;
foreach ($key in $MyInvocation.BoundParameters.keys)
{
    $value = (get-variable $key).Value 
	$MONGO_CMD="$MONGO_CMD.$value"
}
$MONGO_CMD="db.serverStatus()$MONGO_CMD"


# Replace here : database host, port, and name
invoke-expression '& "$MONGO_BIN" localhost:27017/admin --eval "$MONGO_CMD" --quiet' 
