<?php
function insert_nv_obs(){
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
    $timestamp = $obj->timestamp;
    $essence = $obj->essence;
    $circonference = $obj->circonference;
    $mort = $obj->mort;
    $id_groupe = $obj->id_groupe;

    

    $connexion = mysqli_connect($host, $user, $password, $database, $port);

    if(mysqli_errno($connexion)){
       echo json_encode(array('error' => 'La connexion a échouée !'));
        
    }

    else {
        $req_max_id_obs = 'SELECT MAX(id_observations_arbres) AS max_id FROM observations_arbres';
        $result_max_id_obs = mysqli_query($connexion, $req_max_id_obs);

        if($result_max_id_obs){
            $row_max_id = mysqli_fetch_array($result_max_id_obs, MYSQLI_ASSOC);
            $max_id = $row_max_id['max_id'] + 1; // Incrémentation de l'ID pour la nouvelle observation

            // Nouvelle liaison entre l'arbre et l'observation
            $req_insert_id_obs= $connexion-> prepare("INSERT INTO `details_arbres` (`id_arbres`, `id_observations_arbres`) VALUES (?, ?)");
            $req_insert_id_obs-> bind_param("ii", $id, $max_id);
            $req_insert_id_obs->execute();

            // Insertion de la nouvelle observation
            $req_insert_obs = 'INSERT INTO observations_arbres (id,id_groupe, essence, latitude_estimee, longitude_estimee, circonference, mort, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)';
            $stmt_insert_obs = $connexion->prepare($req_insert_obs);
            $stmt_insert_obs->bind_param("ssssssss", $max_id, $id_groupe, $essence, $lat, $long, $circonference, $mort, $timestamp);
            $stmt_insert_obs->execute();

        }
    }
}


insert_nv_obs();
?>