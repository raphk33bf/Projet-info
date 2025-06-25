<?php


function ajout_arbre(){

    /*IN<-- datas arbres
    OUT --> datas insertion into observations_arbre*/
    
    $host = "irioso.sql.free.fr";
    $database = "irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";

    // Récupération des entrées du script
    $json = file_get_contents('php://input');
    $obj = json_decode($json);
    
    $connexion = mysqli_connect($host, $user, $password, $database, $port);
    
    $essence = $obj->essence;
    $circo = $obj->circonference;
    $id_groupe = $obj->id_groupe;
    $mort = $obj->mort;
    $lat = $obj->lat;
    $long = $obj->long;
    $time = $obj->timestamp;
    $nom_img = $obj->nom_img;

    if(mysqli_errno($connexion)){
        echo json_encode(['error' => 'La connexion a échouée !']);
    }

    else{
        
    }
    // Récupération de l'ID maximum dans la table arbres
    $req_max_id = "SELECT MAX(id) AS max_id FROM arbres";
    $result_max_id = mysqli_query($connexion, $req_max_id);
    if ($result_max_id) {
        $row = mysqli_fetch_assoc($result_max_id);
        $max_id_arbres = $row['max_id'] + 1; // Incrémentation de l'ID maximum
    } else {
        echo json_encode(['error' => 'Erreur lors de la récupération de l\'ID maximum']);
        mysqli_close($connexion);
        exit;
    }


    // Insertion dans la table arbres
    $req_insert_id = $connexion-> prepare("INSERT INTO `arbres` 
    (`id`, `essence_estimee`, `latitude_estimee`, `longitude_estimee`)
    VALUES (?,?,?,?)");
    $req_insert_id-> bind_param("ssss", $max_id_arbres, $essence, $lat, $long);
    $req_insert_id->execute();
    
    mysqli_commit($connexion) ;

    //insertion des points dans la table
    $req_insert_bonus="insert into bonus_obtenus (id_groupe,id_bonus,timestamp) values (?,?,?)";
    $req_insert_bonus = $connexion-> prepare($req_insert_bonus);
    $req_insert_bonus-> bind_param("sss", , $id_groupe, 2, $time);
    $req_insert_bonus->execute();

    mysqli_commit($connexion) ;



    // Récupération de l'ID maximum dans la table observations_arbres
    $req_max_id_obs = "SELECT MAX(id) AS max_id FROM observations_arbres";
    $result_max_id_obs = mysqli_query($connexion, $req_max_id_obs);
    if ($result_max_id_obs) {
        $row = mysqli_fetch_assoc($result_max_id_obs);
        $max_id_obs = $row['max_id'] + 1; // Incrémentation de l'ID maximum
    } 

    // Insertion dans la table details_arbres
    $req_insert_id_details = $connexion-> prepare("INSERT INTO `details_arbres` 
    (`id_arbres`, `id_observations_arbres`)
    VALUES (?,?)");
    $req_insert_id_details-> bind_param("ss", $max_id_arbres, $max_id_obs);
    $req_insert_id_details->execute();
    
    mysqli_commit($connexion) ;

    // Insertion dans la table observations_arbres
    $req_insert_id_obs= $connexion-> prepare("INSERT INTO `observations_arbres` 
    (`id`, `id_groupe`, `timestamp`, `latitude_estimee`, `longitude_estimee`, `essence`, `circonference`, `nom_image`, `mort`) 
    VALUES (?,?,?,?,?,?,?,?,?)");
    $req_insert_id_obs-> bind_param("sssssssss", $max_id_obs, $id_groupe, $time, $lat, $long, $essence, $circo, $nom_img, $mort);
    $req_insert_id_obs->execute();

    mysqli_commit($connexion) ;
    mysqli_close($connexion);
}


ajout_arbre();

?>