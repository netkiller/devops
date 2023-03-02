<?php

$id = $_GET['id'];
$type = $_GET['type'];
$message = $_GET['message'];
$zentao = new Zentao();
if($id){
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
    function task($id, $message){

        try {
            $this->conn = new PDO("mysql:host=$this->host;dbname=zentao",$this->username, $this->password);
            $id =ltrim($id, '0');
            $sql = "update zt_task set consumed=estimate, `left`=0, status='done', finishedDate=now() where id='".$id."'";
        //    print($sql);
            $count = $this->conn->exec($sql);
            
            if($message){
                $comment = "insert into zt_action(objectType,objectID,product,project,execution,actor,action,date,comment,extra,`read`,vision,efforted) select 'task','".$id."',',1,', project, execution, 'gitlab','commented',now(),'".$message."','','1','rnd','0' from zt_task where id=".$id;
                $status = $this->conn->exec($comment);
            }
        //print("$count rows.\n");
    
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
                $comment = "insert into zt_action(objectType,objectID,product,project,execution,actor,action,date,comment,extra,`read`,vision,efforted) select 'bug','".$id."',',1,', project, execution, 'gitlab','commented',now(),'".$message."','','1','rnd','0' from zt_task where id=".$id;
                $status = $this->conn->exec($comment);
            }
        //print("$count rows.\n");
    
        }
        catch(PDOException $e){
            echo $e->getMessage();
        }
    
    }
}


