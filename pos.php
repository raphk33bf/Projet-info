<?php

function id($id,$x,$y){
    $host="irioso.sql.free.fr";
    $database="irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";
    
    //récupération des entrées du script
	$json = file_get_contents('php://input');
	$obj = json_decode($json);

    $id = $obj->id ;
    $x = $obj->x ;
    $y = $obj->y ;

    $connexion = mysqli_connect($host,$user,$password,$port,$database);

    if(mysqli_errno($connexion)){
		echo('La connexion a échouée ! ');
    }

    else{
    }
        echo('CONNECté');
        $req = "INSERT INTO `pos` (`id`, `x`, `y`) VALUES (?,?,?)";
        $stmt = mysqli_prepare($connexion, $req);
        mysqli_stmt_bind_param($stmt, 'sss', $id, $x, $y);
	    mysqli_stmt_execute($stmt);
	    mysqli_commit($connexion);
        
    mysqli_close($connexion);

}

?>


