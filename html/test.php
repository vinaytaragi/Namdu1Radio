<?php
// $dirArray = array("x.wav", "y.wav", "x_comment.wav","x_comment2");
 $filename=array();
 $comments=array();
for($index=0; $index < count($dirArray); $index++){
  if (strpos($dirArray[$index], '_comment')==FALSE){
    
    array_push($filename,$dirArray[$index]);

  }
  else{
    
    array_push($comments,$dirArray[$index]);
  }

} 

$dirArray=array();
for($i=0;$i<count($filename);$i++){
  //echo(substr($filename[$i],0,-4));
 array_push($dirArray,$filename[$i]);
  for($j=0;$j<count($comments);$j++){ 
    //echo(strpos($comments[$j],substr($filename[$i],0,-4)));
    if(strpos($comments[$j],substr($filename[$i],0,-4))!==FALSE){
     // echo("hello");  
      array_push($dirArray,$comments[$j]);
    }

  }

}
// for($i=0;$i<count($dirArray);$i++){
//   echo($dirArray[$i]);

//   }




   ?>
