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
            echo('Mise à jour de l\'arbre avec ID ' . $id . ' effectuée avec succès.');
        } 

        $req_max_id_obs = 'SELECT MAX(id_observations_arbres) AS max_id FROM observations_arbres';
        $result_max_id_obs = mysqli_query($connexion, $req_max_id_obs);

        if($result_max_id_obs){
            $row_max_id = mysqli_fetch_array($result_max_id_obs, MYSQLI_ASSOC);
            $max_id = $row_max_id['max_id'] + 1; // Incrémentation de l'ID pour la nouvelle observation

            // Nouvelle liaison entre l'arbre et l'observation
            $req_insert_id_obs= $connexion-> "INSERT INTO `details_arbres` (`id_arbres`, `id_observations_arbres`) VALUES ('1', '2')";
            $req_insert_id_obs-> bind_param("ii", $id, $max_id);
            $req_insert_id_obs->execute();


            $req_update_obs = 'UPDATE observations_arbres SET latitude_estimee = ' . $lat . ', longitude_estimee = ' . $long . ' WHERE id = ' . $max_id;
            mysqli_query($connexion, $req_update_obs);

        
        
        else {
            echo json_encode(array('error' => 'id !'));
            return;
        }

       
        }

    }

    mysqli_commit($connexion) ;
    mysqli_close($connexion);
}

MAJ_arbre($id,$long,$lat);



?>