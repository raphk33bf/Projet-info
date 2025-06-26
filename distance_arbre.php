<?php

function distance_arbre(){

    /* IN <-- long_pers,lat_pers
    OUT --> boolean,id : True if proximité arbre et son id */

    $json = file_get_contents('php://input');
    $obj = json_decode($json);

    $long_pers = $obj->long;
    $lat_pers = $obj->lat;

    $host = "irioso.sql.free.fr";
    $database = "irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";

    /*
    if (!$obj || !isset($obj->long) || !isset($obj->lat)) {
    echo json_encode(['error' => 'Entrée JSON manquante ou invalide']);
    exit;
    }*/

    $connexion = mysqli_connect($host, $user, $password, $database, $port);

    if (mysqli_errno($connexion)) {
        echo json_encode(['error' => 'La connexion a échoué !']);
        exit;
    }

    $req_recup = 'SELECT latitude_estimee, longitude_estimee, id FROM arbres';
    $result_recup = mysqli_query($connexion, $req_recup);

    if ($result_recup) {
        while ($row = mysqli_fetch_array($result_recup, MYSQLI_ASSOC)) {
            $distance = sqrt(pow($long_pers - $row['longitude_estimee'], 2) + pow($lat_pers - $row['latitude_estimee'], 2));
            if ($distance <= 0.001) {
                echo json_encode(['booleen' => true, 'id' => $row['id']]);
                mysqli_close($connexion);
                exit;
            }
        }
    
    // Aucun arbre trouvé à proximité
    echo json_encode(['booleen' => false]);
    }   
    else {
    echo json_encode(['error' => 'Erreur lors de la requête B.D.']);
    }

    mysqli_close($connexion);
}

distance_arbre();

?>