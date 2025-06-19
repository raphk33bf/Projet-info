<?php


function recup_id($nom,$prenom){

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
		echo('La connexion a échouée ! ');
    }

    else{
		}

        $stmt = $connexion->prepare("SELECT id, id_groupe FROM eleves WHERE nom = ? AND prenom = ?");
        $stmt->bind_param("ss", $nom, $prenom);
        $stmt->execute();
        $result = $stmt->get_result();  

        if($result){
            $row = $result->fetch_assoc();
	        echo(json_encode(array('id' => $row['id'], 'id_groupe' => $row['id_groupe'])));

            $stmt->close();
        }

        else{
            ECHO('ERREUR B.D !<br>');
        }
        
    mysqli_commit($connexion) ;
    mysqli_close($connexion);


}

recup_id($nom,$prenom);

?>
