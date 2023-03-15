<?php
$id = $_GET['id'];
$type = $_GET['type'];
$zentao = new Zentao();

$func = $_GET['func'];

if($func == 'close'){

    $zentao->close($id, $type);
    exit();
}

if($id){
    $message = $_GET['message'];
    if($type == 'task'){
        $zentao->task($id,$message);
    }elseif($type == 'bug'){
        $zentao->bug($id,$message);
    }

}else{
    exit();
}
class Zentao {
    public $host = "localhost";
    public $username = "root";
    public $password = "123456";
    public $conn = null;

    function __construct() {

    }
    function close($id,$type){
        try {
            $this->conn = new PDO("mysql:host=$this->host;dbname=zentao",$this->username, $this->password);
            $id =ltrim($id, '0');
            if($type == 'task'){
                $sql = "update zt_task set status='closed', closedBy='devops', closedDate=now() where status='done' and id='".$id."'";
            }
            if($type == 'bug'){
                $sql = "update zt_bug set status='closed', closedBy='devops', closedDate=now() where status='resolved' and id='".$id."'";
            }

            $status = $this->conn->exec($sql);
            print("$id, $status");

        }
        catch(PDOException $e){
            echo $e->getMessage();
        }
        
    }
    function task($id, $message){

        try {
            $this->conn = new PDO("mysql:host=$this->host;dbname=zentao",$this->username, $this->password);
            $id =ltrim($id, '0');
            // $sql = "update zt_task set consumed=estimate, `left`=0, status='done', finishedDate=now() where id='".$id."'";
            $sql = "update zt_task set status='doing', estStarted=now() where status='wait' and id='".$id."'";
        //    print($sql);
            $task = $this->conn->exec($sql);

            if($message){
                //$comment = "insert into zt_action(objectType,objectID,product,project,execution,actor,action,date,comment,extra,`read`,vision,efforted) select 'task','".$id."',',1,', project, execution, 'gitlab','commented',now(),'".$message."','','1','rnd','0' from zt_task where id=".$id;
                $comment = "insert into zt_action(objectType,objectID,product,project,actor,action,date,comment,extra,`read`,efforted) select 'task','".$id."',',1,', project, 'gitlab','commented',now(),'".$message."','','1','0' from zt_task where id=".$id;
                $action = $this->conn->exec($comment);
                $effort = "insert into zt_effort(objectType,objectID,product,project,account,work,date,`left`,consumed,begin,end) select 'task', id ,'',project,assignedTo,name, now(),0,estimate,'0000','0000' from zt_task where id=".$id;
                $effort = $this->conn->exec($effort);
            }
            print("$task, $action, $effort");

        }
        catch(PDOException $e){
            echo $e->getMessage();
        }
    }

    function bug($id, $message){

        try {
            $this->conn = new PDO("mysql:host=$this->host;dbname=zentao",$this->username, $this->password);
            $id =ltrim($id, '0');
            $sql = "update zt_bug set status='resolved', confirmed='1',resolution='fixed',resolvedBuild='trunk', resolvedDate=now() where id='".$id."'";
        //    print($sql);
            $count = $this->conn->exec($sql);
            if($message){
                //$comment = "insert into zt_action(objectType,objectID,product,project,execution,actor,action,date,comment,extra,`read`,vision,efforted) select 'bug','".$id."',',1,', project, execution, 'gitlab','commented',now(),'".$message."','','1','rnd','0' from zt_task where id=".$id;
                $comment = "insert into zt_action(objectType,objectID,product,project,actor,action,date,comment,extra,`read`,efforted) select 'bug','".$id."',',1,', project, 'gitlab','commented',now(),'".$message."','','1','0' from zt_task where id=".$id;
                $status = $this->conn->exec($comment);
                $effort = "insert into zt_effort(objectType,objectID,product,project,account,work,date,`left`,consumed,begin,end) select 'bug', id ,product,project,assignedTo,title, now(),0,1,'0000','0000' from zt_bug where id=".$id;
                $status = $this->conn->exec($effort);
            }
        //print("$count rows.\n");

        }
        catch(PDOException $e){
            echo $e->getMessage();
        }

    }
}