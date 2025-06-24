<?php


function ajout_arbre($max_id,$id_groupe, $time, $lat, $long, $essence, $circo, $nom_img, $mort){

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
    $time = $obj->timestamp
    $nom_img = $obj->nom_img

    if(mysqli_errno($connexion)){
        echo json_encode(array('error' => 'La connexion a échouée !'));
    }

    else{
        
    }

    $req_insert_id_obs= $connexion-> "INSERT INTO `observations_arbres` 
    (`id`, `id_groupe`, `timestamp`, `latitude_estimee`, `longitude_estimee`, `essence`, `circonference`, `nom_image`, `mort`) 
    VALUES (?,?,?,?,?,?,?,?,?)";
    $req_insert_id_obs-> bind_param("iiiiiiiii", $max_id,$id_groupe, $time, $lat, $long, $essence, $circo, $nom_img, $mort);
    $req_insert_id_obs->execute();

    mysqli_commit($connexion) ;
    mysqli_close($connexion);
}


ajout_arbre($max_id,$id_groupe, $time, $lat, $long, $essence, $circo, $nom_img, $mort);

?>