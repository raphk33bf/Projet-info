<?php

///FONCTIONS
//on souhaite connaitre notre localisation a un timestamp donné qui n'exista pas forcément dans la base de donnees

//recuperation du timestamp existant juste avant le timestamp donne
function maxi_timestamp($n,$groupe,$connexion){
	$req = "select timestamp from data_gps where id_phone= ".$groupe." and timestamp<=".$n." order by timestamp desc"  ;
	$result = mysqli_query($connexion, $req);
	if($result){
 
       
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return $row["timestamp"] ;
    }
    else{printf("<br> result est vide <br>") ;
	}
}
//recuperation du timestamp existant juste apres le timestamp donne
function mini_timestamp($n,$groupe,$connexion){
	$req = "select timestamp from data_gps where id_phone= ".$groupe." and timestamp>=".$n." order by timestamp asc"  ;
	$result = mysqli_query($connexion, $req);
	if($result){
 
      
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return $row["timestamp"] ;
    }
    else{printf("<br> result est vide <br>") ;
	}
}
//renvoie notre localisation a un timestamp qui existe dans la base de donnees
function localisation($n,$groupe,$connexion){
	$req="select longitude,latitude from data_gps where id_phone= ".$groupe." and timestamp= ".$n;
	$result = mysqli_query($connexion, $req);
	if($result){
 
       
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return [$row["longitude"], $row["latitude"]];
       	 	
    }
    else{printf("<br> result est vide <br>") ;
	}
}
//renvoie la distance entre deux points donnes à partir de leurs coordonnées
function distance($lat1, $lng1, $lat2, $lng2, $unit = 'k') {
        $earth_radius = 6378137;   // Terre = sphère de 6378km de rayon
        $rla1 = deg2rad($lat1);
        $rlo1 = deg2rad($lng1);
        $rla2 = deg2rad($lat2);
        $rlo2 = deg2rad($lng2);
        $dlo = ($rlo2 - $rlo1) / 2;
        $dla = ($rla2 - $rla1) / 2;
        $a = (sin($dla) * sin($dla)) + cos($rla1) * cos($rla2) * (sin($dlo) * sin($dlo));
        $d = 2 * atan2(sqrt($a), sqrt(1 - $a));
        //
        $meter = ($earth_radius * $d);
        if ($unit == 'k') {
            return $meter / 1000;
        }
        return $meter; // ditance en km
    }
//renvoie les cordonnees associées au timestamp (pas forcément existant) donné
function position_x($n, $groupe,$connexion){
	$maxt=maxi_timestamp($n,$groupe,$connexion);
	$mint=mini_timestamp($n,$groupe,$connexion);
	$loc_maxt= localisation($maxt,$groupe,$connexion);
	$loc_mint= localisation($mint,$groupe,$connexion);
	$distance= distance($loc_maxt[1], $loc_maxt[0], $loc_mint[1], $loc_mint[0], $unit = 'k');
	$duree=$maxt-$mint;
	if ($duree == 0 || $distance == 0) {
		$localisation=localisation($n,$groupe,$connexion);
		print($localisation);
		return;
	}
	$duree_x=$n-$maxt;
	$distance_x=$duree_x*$distance/$duree;
	$longitude_x=($distance_x/$distance)*($loc_mint[0]-$loc_maxt[0])+$loc_maxt[0];
	$latitude_x=($distance_x/$distance)*($loc_mint[1]-$loc_maxt[1])+$loc_maxt[1];
	echo "Position interpolée au timestamp $n : longitude : $longitude_x, latitude : $latitude_x<br>";
	return [$n,$longitude_x,$latitude_x];
	
}
/// calcule la vitesse en km/h entre un timestamp et 10sec plus tard

function vitesse($n,$groupe,$connexion){
	$mint=mini_timestamp($n,$groupe,$connexion);
	$mint10=mini_timestamp($n+10,$groupe,$connexion);
	$loc_mint= localisation($mint,$groupe,$connexion);
	$loc_mint10= localisation($mint10,$groupe,$connexion);
	$distance= distance($loc_mint10[1], $loc_mint10[0], $loc_mint[1], $loc_mint[0], $unit = 'k');
	$duree=$mint10-$mint;
	if ($duree == 0 || $distance == 0) {
		echo "Position fixe (aucun mouvement ou même timestamp).<br>";
		return;
	}
	$vitesse=$distance/$duree*3600;
	print($vitesse.'<br>'); // vitesse en km/h
	return $vitesse;
}


/// renvoie un tableau associatif avec comme clé le timestamp du début et comme valeur le moyen de transport utilisé pour un intervalle de 10sec suivant le timestamp
function deter_moyen($n1,$n2,$groupe,$connexion){
	$n=$n1;
	$moyen= array();
	while ($n<=$n2) {
		$v=vitesse($n,$groupe,$connexion);  // vitesse en km/h
		if ($v<=1){
			$moyen[$n]='arret';
		}
		elseif ($v<=6){
			$moyen[$n]='marche';
		}
		elseif ($v<=15){
			$moyen[$n]='course';
		}
		elseif ($v<=25){
			$moyen[$n]='velo';
		}
		elseif($v>25){
			$moyen[$n]='bus';
		}
		$n+=10;
	}
	print_r($moyen);
	print('<br>') ; 
	$m=$n1;
	intervalle_transport($m,$moyen,$connexion);
}
/// Renvoie un tableau avec le timestamps de début d'utilisation d'un moyen de transport, puis quand ca change de moyen : nouvelle clé qui correspond au timestamp de changement de moyen associé au nouveau moyen comme valeur
function intervalle_transport($n,$tab,$connexion){
	$moyen0=$tab[$n];
	$tab_change=array();
	$tab_change[$n]=$moyen0;
	foreach($tab AS $cle => $valeur) {
		if ($valeur!=$moyen0){
			$tab_change[$cle]=$valeur;
			$moyen0=$valeur;
		}
	}
    print_r($tab_change);	
		
}		
		
		
		
	

///PROGRAMME PRINCIPAL
function main() {

	$URL = "localhost" ;
	$user = "root" ;
	$password = "root" ;
	$db_name = "irioso" ;

	$groupe = 1 ;
	printf($groupe . '<br>') ;

	$connexion = mysqli_connect($URL,$user,$password,$db_name);

	if(mysqli_errno($connexion)){
		echo('La connexion a échouée ! ');
	}
	else{
		echo('Vous êtes connectés à votre base de données !<BR>');}
       



	deter_moyen(1748874462 ,1748874522 ,$groupe,$connexion);
	mysqli_commit($connexion) ;
    mysqli_close($connexion);
}

main() ;    


	
?>
