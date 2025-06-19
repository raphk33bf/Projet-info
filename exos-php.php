<?php

function etoile($l){
    for ($n=1;$n<=$l;$n++){
    echo "*";
}
}


function trianglestars($l){
    for($n;$n<=$l;$n++){
    etoile($n);
    echo "<br>";
    }
}

function carrestars($l){
    $n=1;
    while ($n<=$l){
        etoile($l);
        echo "<br>";
        $n=$n+1;
    }
}

function losange($l){
    $c=0;
    $n=1;
    while($c<$l){
        $c=$c+1;
        $s=$l/2;
        if($c<=$s){
            echo "<center>";
            etoile($n);
            echo "<br>";
            $n++;
        }

        if($c>=$s){
            echo "<center>";
            etoile($n);
            echo "<br>";
            $n=$n-1;
        }
    }
}




$L = array(1, 2, 5, 9, 12, 4);

function maxlist($L){
    $max = $L[0];
    $s = count($L);

    for($i = 1; $i < $s; $i++) {
        if($max < $L[$i]){
            $max = $L[$i];
        }
    }

    echo $max;
}

function posavant($time){
    $URL = "localhost" ;
	$user = "root" ;
	$password = "root" ;
	$db_name = "module" ;

	printf($time . '<br>') ;

    $connexion = mysqli_connect($URL,$user,$password,$db_name);
	$connexion = new mysqli($URL,$user,$password,$db_name);

	if(mysqli_errno($connexion)){
		echo('La connexion a échouée ! ');
	}
	else{
		echo('Vous êtes connectÃ©s Ã  votre base de donnÃ©es !<BR>');}

        $req = 'SELECT timestamp FROM data_gps WHERE `id`= ' . $time ;	
    	printf($req .'<br>') ;
        $result = mysqli_query($connexion, $req);  

        if($result){
            while ($row = mysqli_fetch_array($result, MYSQLI_ASSOC)) {
            printf($row['timestamp'] . "<br>") ;
            }
        }

        else{
            print('Pas dans la bd !<br>');
        }
        
    mysqli_commit($connexion) ;
    mysqli_close($connexion);
    

}


function distance_lieu($id_phone,$id_lieu){
    $URL = "localhost" ;
	$user = "root" ;
	$password = "root" ;
	$db_name = "module" ;

    $lieu=array(0,0,0);
    $phone=array(0,0,0);

	printf($id_phone . '<br>') ;
    printf($id_lieu . '<br>');

    $connexion = mysqli_connect($URL,$user,$password,$db_name);

    if(mysqli_errno($connexion)){
		echo('La connexion a échouée ! ');
	}

	else{
		echo('Vous êtes connectÃ©s Ã  votre base de donnÃ©es !<BR>');}

        $req_lieu = 'SELECT nom,latitude,longitude FROM lieux_d_interet WHERE id= ' . $id_lieu ;	
    	printf($req_lieu .'<br>') ;
        $result_lieu = mysqli_query($connexion, $req_lieu);  

        if($result_lieu){
            while ($row = mysqli_fetch_array($result_lieu, MYSQLI_ASSOC)) {
            $lieu[0]=$row['longitude'];
            $lieu[1]=$row['latitude'];
            $lieu[2]=$row['nom'];
            }
        }

        else{
            print('Pas dans la bd !<br>');
        }
        
        $req_phone = 'SELECT timestamp,latitude,longitude FROM data_gps WHERE id =' . $id_phone ;
        printf($req_phone.'<br>');
        $result_phone = mysqli_query($connexion, $req_phone);

        if($result_phone){
            while($row=mysqli_fetch_array($result_phone,MYSQLI_ASSOC)){
                $phone[0]=$row['longitude'];
                $phone[1]=$row['latitude'];
                $phone[2]=$row['timestamp'];
            }
        }    

    

    $distance=sqrt(abs($phone[0]-$lieu[0])+abs($phone[1]-$lieu[1]));

    mysqli_commit($connexion) ;
    mysqli_close($connexion);

    echo($phone[2] .','. $lieu[2] .','.  $distance );

}


function distance_arbre($long_pers,$lat_pers,$long_a,$lat_a){

    $distance=sqrt(abs($long_pers-$long_a)+abs($lat_a-$lat_pers));
    $distance_max=1;
    if ($distance<=$distance_max){
        return TRUE;
    }

    else{
        return FALSE;
    }
}

function inser_nv_arbre($long,$lat,$time_obs,$circo,$essence,$grpe,$mort,$nom_image){
   
    $req_inser='INSERT INTO `observations_arbres` (`id`, `id_groupe`, `timestamp`, `latitude_estimee`, `longitude_estimee`, `essence`, `circonference`, `nom_image`, `mort`) 
    VALUES (NULL,'. $grpe. ','. $time_obs .','. $lat . ',' . $long . ',' . $essence . ',' . $circo . ','. $nom_image . ',' . $mort.')';
    
    mysqli_query($connexion,$req_inser);    
}



function inser_arbre($long,$lat,$time_obs,$circo,$essence,$grpe,$mort,$nom_image){


    $URL = "localhost" ;
	$user = "root" ;
	$password = "root" ;
	$db_name = "module" ;

    $connexion = mysqli_connect($URL,$user,$password,$db_name);

    if(mysqli_errno($connexion)){
		echo('La connexion a échouée ! ');
	}

	else{
		echo('Vous êtes connectÃ©s Ã  votre base de donnÃ©es !<BR>');}

        $recup = 'SELECT id,latitude,longitude FROM arbres';
    	printf($recup .'<br>');
        $result_recup = mysqli_query($connexion, $recup);  

        if($result_recup){
            while ($row = mysqli_fetch_array($result_recup, MYSQLI_ASSOC)){
                if(distance_arbre($lat,$long,$row['latitude'],$row['longitude'])==TRUE){

                    $req_details='SELECT id_observations_arbres FROM details_arbres WHERE id_arbres='. $row['id'] ;
                    printf($row['id']. '<br>');
                    printf($req_details. '<br>');
                    $result_details=mysqli_query($connexion, $req_details);
                    
                    if($result_details){

                        while($row_req=mysqli_fetch_array($result_details,MYSQLI_ASSOC)){
                            $id_observation=$row_req['id_observations_arbres'];
                            printf($row_req['id_observations_arbres']);
                        }
                    
                        $med_lat=($lat+$row['latitude'])/2;
                        $med_long=($long+$row['longitude'])/2;

                        if($id_observation){
                            $req_obs='UPDATE observations_arbres SET  latitude_estimee='. $med_lat .', longitude_estimee='. $med_long. ' WHERE id='. $id_observation ;
                            printf($req_obs. '<br>');
                            $op_req=mysqli_query($connexion,$req_obs);

                            $req_test='SELECT timestamp,essence,circonference FROM observations_arbres WHERE id='. $id_observation ;
                            $resultat_test=mysqli_query($connexion,$req_test);

                            while($row_test=mysqli_fetch_array($resultat_test, MYSQLI_ASSOC)){

                                if(is_null($row_test['timestamp'])==TRUE){

                                    $req_inser='UPDATE observations_arbres SET timestamp='. $time_obs.'WHERE id='. $id_observation;
                                    mysqli_query($connexion,$req_inser);
                                }
                                if(is_null($row_test['essence'])==TRUE){

                                    $req_inser='UPDATE observations_arbres SET essence='. $essence .'WHERE id='. $id_observation;
                                    mysqli_query($connexion,$req_inser);
                                }
                                if(is_null($row_test['circonference'])==TRUE){

                                    $req_inser='UPDATE observations_arbres SET circonference='. $circo .'WHERE id='. $id_observation;
                                    mysqli_query($connexion,$req_inser);
                                }

                                
                            }
                        }
                        
                        else{
                            printf('erreur');
                        }
                    }


                    else{
                        echo('ERREUR');
                    }
                }

                else{
                    echo('arbre pas dans bd , enregistrement en cours');

                    inser_nv_arbre($long,$lat,$time_obs,$circo,$essence,$grpe,$mort,$nom_image);
                }
            }

        mysqli_commit($connexion) ;
        mysqli_close($connexion);

        }


}


inser_arbre(0,1,111,null,null,null,null,null);

?>





