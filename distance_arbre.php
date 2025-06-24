<?php

function distance_arbre($long_pers,$lat_pers){

    /* IN <-- long_pers,lat_pers
    OUT --> boolean,id : True if proximité arbre et son id */

    $host="irioso.sql.free.fr";
    $database="irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";

    //récupération des entrées du script
    
	$json = file_get_contents('php://input');
	$obj = json_decode($json);

    $long_pers = $obj->long ;
    $lat_pers = $obj->lat ;

    $connexion = mysqli_connect($host,$user,$password,$database,$port);

    if(mysqli_errno($connexion)){
        echo json_encode(array('error' => 'La connexion a échouée !'));
    }

    else{
        
    }

    $req_recup='SELECT latitude_estimee,longitude_estimee,id FROM arbres';
    $result_recup=mysqli_query($connexion, $req_recup);

    if($result_recup){
        while ($row = mysqli_fetch_array($result_recup, MYSQLI_ASSOC)) {
            $distance=sqrt(pow($long_pers-$row['longitude_estimee'],2) + pow($lat_pers-$row['latitude_estimee'],2));
            if($distance<= 1){
                $id=$row['id'];
                return(json_encode(['booleen' => TRUE, 'id' => $row['id']]))
            }
        }
    }

    else{
        echo json_encode(array('error' => 'bd vide !'));
    }

    mysqli_commit($connexion) ;
    mysqli_close($connexion);
    
    return FALSE;
}

distance_arbre($long_pers,$lat_pers);

?>