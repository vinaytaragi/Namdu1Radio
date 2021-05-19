<?php
    
     // Opens directory
     $myDirectory=opendir("./.upload/gencat");
     
for ($x = 0; $x <= 10; $x++) {
  echo ("<div>
  <div class='input-group'>
    <div class='custom-file'>
      <input type='file' accept='audio/*' class='custom-file-input' id='inputFile' aria-describedby='inputGroupFileAddon04'>
      <label class='custom-file-label' id='inputFileLabel' for='inputFile'>Choose file</label>
    </div>
    <div class='input-group-append'>
      <button class='btn btn-primary' type='button' id='inputFileUploadButton' disabled='true'>Upload</button>
    </div>
  </div>
  <div class='progress'>
    <div id='progressbar' class='progress-bar bg-success' role='progressbar' style='width: 0%' aria-valuenow='0'
      aria-valuemin='0' aria-valuemax='100'></div>
  </div> ");
}
?> 