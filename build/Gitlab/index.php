<?php
/* ========================================
 * Author: netkiller<netkiller@msn.com>
 * Homepage: http://www.netkiller.cn
 * ========================================
 */
 
define("TOKEN", "");
if($_SERVER['HTTP_X_GITLAB_TOKEN'] != TOKEN){
        error_log("failed token");
        exit(0);
}

$cmd = null;
if($data = file_get_contents('php://input')) {
	error_log( $data );
	try {
		$payloads = json_decode($data);
		$branch	= "development"	;
		$project = $payloads->project->name;
		$group	= $payloads->project->namespace;

		if($payloads->ref == "refs/heads/master") {
			$branch = "production";
			// disable production
			exit();
		}
		if($payloads->ref == "refs/heads/testing") {
			$branch = "testing";
		}
			
		if($payloads->ref === 'refs/heads/development'){
			$branch = "development";
		}

		//$cmd="sudo -u www -i  /srv/deploy/deploy.sh $group $branch $project";
		$cmd="/srv/deploy/deploy.sh $group $branch $project";
		$result=system($cmd);

		error_log($cmd);
		error_log($result);

	} catch(Exception $ex) {
		error_log($ex);
	}
} else {
	error_log("failed request");
} 
?>
