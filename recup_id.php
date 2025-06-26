<?php


function recup_id(){

    /* 
    IN <-- nom,prenom 
    OUT --> id_grp,id_eleve 
    */

    $host="irioso.sql.free.fr";
    $database="irioso";
    $user = "irioso";
    $password = "963364";
    $port = "3306";

    //récupération des entrées du script
    
	$json = file_get_contents('php://input');
	$obj = json_decode($json);
    
    
    $nom = $obj->nom ;
    $prenom = $obj->prenom ;

    $connexion = mysqli_connect($host,$user,$password,$database,$port);

    if(mysqli_errno($connexion)){
		echo json_encode(array('error' => 'La connexion a échouée !'));
    } 

    
    /*if (!$obj || !isset($obj->long) || !isset($obj->lat)) {
    echo json_encode(['error' => 'Entrée JSON manquante ou invalide']);
    exit;
    }*/

    else{
		

        $stmt = $connexion->prepare("SELECT id, id_groupe FROM eleves WHERE nom like ? AND prenom like ?");
        $stmt->bind_param("ss", $nom, $prenom);
        $stmt->execute();
        $result = $stmt->get_result();  

        if($result){
            $row = $result->fetch_assoc();
            if ($row) {
                echo json_encode(array('id' => $row['id'], 'id_groupe' => $row['id_groupe']));
            } 
            else {
                echo json_encode(array('error' => 'Aucun résultat'));
            }
        } 
        else {
            echo json_encode(array('error' => 'ERREUR B.D !'));
        }
    }
    mysqli_commit($connexion) ;
    mysqli_close($connexion);


}

recup_id();

?>