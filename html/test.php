<?php
   
    
      // Opens directory
      $myDirectory=opendir("./.upload/gencat/");

      // Gets each entry
      while($entryName=readdir($myDirectory)) {
       $dirArray[]=$entryName;
      }
 
      // Finds extensions of files
 /*      function findexts($filename) {
       for ($i=0;$filename[$i]!=NULL;$i++){}
     $exts = $filename[$i];
       return $exts;
      } */
 
      // Closes directory
      closedir($myDirectory);
 
      // Counts elements in array
      $indexCount=count($dirArray);
 
      // Sorts files
      //sort($dirArray);
        rsort($dirArray);//sorting in descending order
     
      $flag=0;
      
      
      // (Randomly) Loops through the array of files
      for($index=rand(0,$indexCount); $index < $indexCount; $index++) {
       
       //Loops through the array of files
       //for($index=0; $index < $indexCount; $index++) {
       
       // Gets File Names
       $name=$dirArray[$index];
       $namehref=$dirArray[$index];	
     //  $ext = findexts($name);
     
       if (strlen($name)>='3'){
         $str_index=strval($index);
         $fileid = "inputFile".$str_index;
      //   echo($fileid);
         $inputid="inputFileUploadButton".$str_index;
         $inputlab="inputFileLabel".$str_index;
         
 
     
     if ($flag==0){
      // echo 'em
  
        echo("
       <audio autoplay id='audio' preload='auto' tabindex= '0' controls='' type='audio/mpeg'>
            <source src='.upload/gencat/$namehref'>
            Sorry, your browser does not support HTML5 audio.
           </audio>
         
 
       <ul id='playlist'>
           ");
        
            echo("
             
            <li class='active'>
          <a href='.upload/gencat/$namehref'>$name</a>
        ");
        echo("<div>
        <div class='input-group'>
          <div class='custom-file'>
            <input type='file' accept='audio/*' class='custom-file-input' id='$fileid' aria-describedby='inputGroupFileAddon04'>
            <label class='custom-file-label' id='$inputlab' for='$fileid'>Choose file</label>
          </div>
          ");
          echo("<div class='input-group-append'>
          <button class='btn btn-primary' type='button' id='$inputid' >Upload</button>
        </div>
      </div>
      <div class='progress'>
        <div id='progressbar' class='progress-bar bg-success' role='progressbar' style='width: 0%' aria-valuenow='0'
          aria-valuemin='0' aria-valuemax='100'></div>
      </div> 
      <script>
      var $fileid = document.getElementById('$fileid');
      var $inputlab = document.getElementById('$inputlab');
      var submitBtn = document.getElementById('$inputid');
      var progressBar = document.getElementById('progressbar');
      
      $fileid.addEventListener('change', function(){handleFileupload($fileid,$inputlab)});
      submitBtn.addEventListener('click', function(){uploadFile('$name',$fileid)});
      </script>
      
  <script src=file_upload.js'></script> "
     );
   
  
   
      $flag=1;
     }
     else{    
          // echo 'em
          echo("
           
            <li>
          <a href='./.upload/gencat/$namehref'>$name</a>
        </li>"
   );
   echo("<div>
   <div class='input-group'>
     <div class='custom-file'>
       <input type='file' accept='audio/*' class='custom-file-input' id='$fileid' aria-describedby='inputGroupFileAddon04'>
       <label class='custom-file-label' id='$inputlab' for='$fileid'>Choose file</label>
     </div>
     ");
     echo("<div class='input-group-append'>
     <button class='btn btn-primary' type='button' id='$inputid' >Upload</button>
   </div>
 </div>
 <div class='progress'>
   <div id='progressbar' class='progress-bar bg-success' role='progressbar' style='width: 0%' aria-valuenow='0'
     aria-valuemin='0' aria-valuemax='100'></div>
 </div> 
 <script>
 var $fileid = document.getElementById('$fileid');
 var $inputlab = document.getElementById('$inputlab');
 var submitBtn = document.getElementById('$inputid');
 var progressBar = document.getElementById('progressbar');
 
 $fileid.addEventListener('change', function(){handleFileupload($fileid,$inputlab)});
 submitBtn.addEventListener('click', function(){uploadFile('$name',$fileid)});
 </script>");
         }
        }
       }
   ?>
