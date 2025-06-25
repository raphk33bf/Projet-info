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

    if(mysqli_errno($connexion)){
       echo json_encode(array('error' => 'La connexion a échouée !'));
        
    }

    else{
        $req_data="SELECT max(id_observations_arbres) from details_arbres WHERE id_arbres = " . $id;
        $result_data=mysqli_query($connexion, $req_data);

        if($result_data){
            $row = mysqli_fetch_array($result_data, MYSQLI_ASSOC);

            $req_obs='SELECT essence,circonference,mort from observations_arbres WHERE id_observations_arbres = ' . $row['max(id_observations_arbres)'];
            $result_obs = mysqli_query($connexion, $req_obs);
            
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
}

recup_data_arbre();
?>