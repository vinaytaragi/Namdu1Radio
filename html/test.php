<?php
    
     // Opens directory
     $myDirectory=opendir("./.upload/gencat");
     
     function findexts($filename) {
        for ($i=0;$filename[$i]!=NULL;$i++){}
      $exts = $filename[$i-1];
        return $exts;
       }

     // Gets each entry
     while($entryName=readdir($myDirectory)) {
      $dirArray[]=$entryName;
     }
     echo implode(" ",$dirArray);
     ?>