<?php

function MAJ_arbre($id,$long,$lat){

    /* 
    IN <-- id arbre,long,lat
    OUT --> datas update arbre, insert into observations
    */

    $host="irioso.sql.free.fr";
    $database="irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";

    //récupération des entrées du script
    
	$json = file_get_contents('php://input');
	$obj = json_decode($json);

    $id = $obj->id;
    $long = $obj->long;
    $lat = $obj->lat;

    $connexion = mysqli_connect($host, $user, $password, $database, $port);

    if(mysqli_errno($connexion)){
       echo json_encode(array('error' => 'La connexion a échouée !'));
        
    }

    else {
        $req_data='SELECT latitude_estimee,longitude_estimee FROM arbres WHERE `id` = ' . $id;
        $result_select = mysqli_query($connexion, $req_data);
        if($result_select){

            $row = mysqli_fetch_array($result_select, MYSQLI_ASSOC);
            $lat_estimee = $row['latitude_estimee'];
            $long_estimee = $row['longitude_estimee'];

            $long_med= ($long + $long_estimee) / 2;
            $lat_med = ($lat + $lat_estimee) / 2;

    
            $req_update = 'UPDATE arbres SET latitude_estimee = ' . $lat_med . ', longitude_estimee = ' . $long_med . ' WHERE id = ' . $id;
            mysqli_query($connexion, $req_update);
        } 

     }

    

    mysqli_commit($connexion) ;
    mysqli_close($connexion);
}

MAJ_arbre($id,$long,$lat);



?>
