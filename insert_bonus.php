<?php

function insert_bonus(){

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
    $time = $obj->timestamp;
    $id_bonus = 2; // ID du bonus à insérer, ici c'est le bonus pour l'observation d'un arbre
    $id_groupe = 2; // ID du groupe, ici c'est le groupe "Tous les groupes" (à adapter si nécessaire)

    $connexion = mysqli_connect($host, $user, $password, $database, $port);

    /*if (!$obj || !isset($obj->long) || !isset($obj->lat)) {
    echo json_encode(['error' => 'Entrée JSON manquante ou invalide']);
    exit;
    }*/

    if(mysqli_errno($connexion)){
       echo json_encode(array('error' => 'La connexion a échouée !'));
        
    }



    else {
        $req_select_time="select max(timestamp) from observations_arbres,details_arbres where id=id_observations_arbres and id_arbres = ?";
        $stmt = $connexion->prepare($req_select_time);
        $stmt->bind_param("s", $id);
        $stmt->execute();
        $result_select = $stmt->get_result();
        if($result_select){
            $row = mysqli_fetch_array($result_select, MYSQLI_ASSOC);
            $last_obs_time = $row['max(timestamp)'];

            

            if ($time-$last_obs_time >= 60*60*24*2){
                // Insertion deu bonus
                $req_insert_bonus = "INSERT INTO bonus_obtenus(id_bonus,id_groupe,timestamp) VALUES (?,?,?)";
                $stmt_insert = $connexion->prepare($req_insert_bonus);
                $stmt_insert->bind_param("sss", $id_bonus,$id_groupe,$time);
                $stmt_insert->execute();
                $id_obs = $stmt_insert->insert_id;
                echo json_encode(['booleen' => true]);
                
                
            } 
            
            else {
                echo json_encode(['booleen' => false]);
            }
    
     
    mysqli_commit($connexion) ;
    mysqli_close($connexion);   }
    }

}

insert_bonus();

?>