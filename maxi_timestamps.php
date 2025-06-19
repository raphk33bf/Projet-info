<?php

///FONCTIONS
function maxi_timestamp($n,$groupe,$connexion){
	$req = "select timestamp from data_gps where id_phone= ".$groupe." and timestamp<=".$n." order by timestamp desc"  ;
	$result = mysqli_query($connexion, $req);
	if($result){
 
        printf("<br> result est non vide <br>") ;
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return $row["timestamp"] ;
    }
    else{printf("<br> result est vide <br>") ;
	}
}

///PROGRAMME PRINCIPAL
function main() {

	$URL = "localhost" ;
	$user = "root" ;
	$password = "root" ;
	$db_name = "irioso" ;

	$groupe = 1 ;
	printf($groupe . '<br>') ;

	$connexion = mysqli_connect($URL,$user,$password,$db_name);

	if(mysqli_errno($connexion)){
		echo('La connexion a échouée ! ');
	}
	else{
		echo('Vous êtes connectés à votre base de données !<BR>');}
       

	$json = file_get_contents('php://input');
	$obj = json_decode($json);
	$n = $obj->timestamp;
	maxi_timestamp($n,$groupe,$connexion);
	
	mysqli_commit($connexion) ;
    mysqli_close($connexion);
}

main() ; 