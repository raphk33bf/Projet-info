<?php

function recup_data_arbre(){

    /*IN <-- id arbre
    OUT --> most recent datas arbre*/

    $host="irioso.sql.free.fr";
    $database="irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";

    //récupération des entrées du script
    
	$json = file_get_contents('php://input');
	$obj = json_decode($json);

    $id = $obj->id;

    $connexion = mysqli_connect($host, $user, $password, $database, $port);


    if(mysqli_errno($connexion)){
       echo json_encode(array('error' => 'La connexion a échouée !'));
        
    }

    else{
        $req_data= $connexion->prepare("SELECT max(id_observations_arbres) from details_arbres WHERE id_arbres = ?");
        $req_data->bind_param("s", $id);
        $req_data->execute();
        $result_data = $req_data->get_result();


        if($result_data){
            $row = mysqli_fetch_array($result_data, MYSQLI_ASSOC);
            $req_obs=$connexion->prepare('SELECT essence,circonference,mort from observations_arbres WHERE id = ?');
            $req_obs->bind_param("s", $row['max(id_observations_arbres)']);
            $req_obs->execute();
            $result_obs = $req_obs->get_result();
            
            if($result_obs){
                $row_obs = mysqli_fetch_array($result_obs, MYSQLI_ASSOC);
                echo json_encode([
                    'essence' => $row_obs['essence'],
                    'circonference' => $row_obs['circonference'],
                    'mort' => $row_obs['mort']
                ]);
            } else {
                echo json_encode(['error' => 'Erreur lors de la récupération des données d\'observation']);
            }
    }
    mysqli_commit($connexion);
    mysqli_close($connexion);
    }
}

recup_data_arbre();

?>