<?php

///FONCTIONS
function maxi_timestamp($n,$groupe,$connexion){
	$req = "select timestamp from data_gps where id_phone= ".$groupe." and timestamp<=".$n." order by timestamp desc"  ;
	$result = mysqli_query($connexion, $req);
	if($result){
 
        printf("<br> result est non vide <br>") ;
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return $row["timestamp"] ;
    }
    else{printf("<br> result est vide <br>") ;
	}
}
//
function mini_timestamp($n,$groupe,$connexion){
	$req = "select timestamp from data_gps where id_phone= ".$groupe." and timestamp>=".$n." order by timestamp asc"  ;
	$result = mysqli_query($connexion, $req);
	if($result){
 
        printf("<br> result est non vide <br>") ;
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return $row["timestamp"] ;
    }
    else{printf("<br> result est vide <br>") ;
	}
}
//ditance entre les duex points
function localisation($n,$groupe,$connexion){
	$req="select longitude,latitude from data_gps where id_phone= ".$groupe." and timestamp= ".$n;
	$result = mysqli_query($connexion, $req);
	if($result){
 
        printf("<br> result est non vide <br>") ;
        $row = $result->fetch_array(MYSQLI_ASSOC);
        return [$row["longitude"], $row["latitude"]];
       	 	
    }
    else{printf("<br> result est vide <br>") ;
	}
}

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
        return $meter;
    }

function position_x($n, $groupe,$connexion){
	$maxt=maxi_timestamp($n,$groupe,$connexion);
	$mint=mini_timestamp($n,$groupe,$connexion);
	$loc_maxt= localisation($maxt,$groupe,$connexion);
	$loc_mint= localisation($mint,$groupe,$connexion);
	$distance= distance($loc_maxt[1], $loc_maxt[0], $loc_mint[1], $loc_mint[0], $unit = 'k');
	$duree=$maxt-$mint;
	if ($duree == 0 || $distance == 0) {
		echo "Position fixe (aucun mouvement ou même timestamp).<br>";
		return;
	}
	$duree_x=$n-$maxt;
	$distance_x=$duree_x*$distance/$duree;
	$longitude_x=($distance_x/$distance)*($loc_mint[0]-$loc_maxt[0])+$loc_maxt[0];
	$latitude_x=($distance_x/$distance)*($loc_mint[1]-$loc_maxt[1])+$loc_maxt[1];
	echo "Position interpolée au timestamp $n : longitude : $longitude_x, latitude : $latitude_x<br>";
	return [$n,$longitude_x,$latitude_x];
	
}

function vitesse($n,$groupe,$connexion){
	$mint=mini_timestamp($n,$groupe,$connexion);
	$mint10=mini_timestamp($n+10,$group,$connexion);
	$loc_mint= localisation($mint,$groupe,$connexion);
	$loc_mint10= localisation($n+10,$groupe,$connexion);
	$distance= distance($loc_mint10[1], $loc_mint10[0], $loc_mint[1], $loc_mint[0], $unit = 'k');
	$duree=$mint10-$mint;
	if ($duree == 0 || $distance == 0) {
		echo "Position fixe (aucun mouvement ou même timestamp).<br>";
		return;
	}
	$vitesse=$distance/$duree;
	print($vitesse); // vitesse en m/s
	return $vitesse;
}



function deter_moyen($n1,$n2,$groupe,$connexion){
	$n=$n1;
	
	$moyen= array();
	while ($n<=$n2) {
		$v=(vitesse($n,$groupe,$connexion)/1000)*3600;  // vitesse en km/h
		if ($v<=1){
			$moyen['arret']=$n;
		}
		elseif ($v<=6){
			$moyen['marche']=$n;
		}
		elseif ($v<=15){
			$moyen['course']=$n;
		}
		elseif ($v<=25){
			$moyen['vélo']=$n;
		}
		else{
			$moyen['bus']=$n;
		}
		$n+=10;
	}
	print($moyen);
	intervalle_transport($n,$moyen,$connexion);
}
		
function intervalle_transport($n,$tab,$connexion){
	$moyen0=array_search($n, $tab);
	$tab_change=array();
	$tab_change[$moyen0]=$n;
	foreach($tab AS $cle => $valeur) {
		if ($cle!=$moyen0){
			$tab_change[$cle]=$valeur;
			$moyen0=$cle;
		}
	}
    print($tab_change);	
		
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
