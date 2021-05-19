<html>
 <head>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <style type="text/css">
    #playlist,audio{background:#666;width:400px;padding:20px;}
    .active a{color:#5DB0E6;text-decoration:none;}
    li a{color:#eeeedd;background:#333;padding:5px;display:block;}
    li a:hover{text-decoration:none;}
  </style>
  
 </head>
 <body>
  <div id="topMenu" style="display:flex; flex-direction: row;">
	<a href="/MediaUpload/gallery.php" style="padding: 10px; background-color: #000000; color: #ffffff">Visual Gallery</a>
	<a href="/MediaUpload/upload.html" style="padding: 10px; background-color: #000000; color: #ffffff">Upload Image/Video</a>
  </div>
  <center>
   <div > <img src="wallpaper.jpg" style="width:100%;height:70%"> </div>
   <br>	
   <font size="10px">  Programs </font> 

   <br><br>	
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
	
	if ($flag==0){
	 // Print 'em
 
  	 print("
	  <audio autoplay id='audio' preload='auto' tabindex= '0' controls='' type='audio/mpeg'>
           <source src='.upload/gencat/$namehref'>
           Sorry, your browser does not support HTML5 audio.
          </audio>
		

	  <ul id='playlist'>
     	 ");
      	 print("
      	  
           <li class='active'>
 	    <a href='.upload/gencat/$namehref'>$name</a>
       ");
       print("<div>
       <div class='input-group'>
         <div class='custom-file'>
           <input type='file' accept='audio/*' class='custom-file-input' id='inputFile' aria-describedby='inputGroupFileAddon04'>
           <label class='custom-file-label' id='inputFileLabel' for='inputFile'>Choose file</label>
         </div>
         ");
         print("<div class='input-group-append'>
         <button class='btn btn-primary' type='button' id='inputFileUploadButton' disabled='true'>Upload</button>
       </div>
     </div>
     <div class='progress'>
       <div id='progressbar' class='progress-bar bg-success' role='progressbar' style='width: 0%' aria-valuenow='0'
         aria-valuemin='0' aria-valuemax='100'></div>
     </div> 
     <script>
     var inputFile = document.getElementById('inputFile');
     var inputFileLabel = document.getElementById('inputFileLabel');
     var submitBtn = document.getElementById('inputFileUploadButton');
     var progressBar = document.getElementById('progressbar');
 
     inputFile.addEventListener('change', handleFileupload);
     submitBtn.addEventListener('click', uploadFile);
 
     function handleFileupload(e) {
       const file = this.files[0];
       inputFileLabel.innerHTML = file.name;
       submitBtn.disabled = false;
     }
 
 
     function uploadFile() {
       var file = inputFile.files[0];
       // alert(file.name+' | '+file.size+' | '+file.type);
       var formdata = new FormData();
       formdata.append('file1', file);
       var simple = '$name';
       formdata.append('finalname',simple.split('.')[0]+'comment'+Date(Date.now).replaceAll(':','')+'.'+file.name.split('.')[1])
       console.log(formdata.get('finalname'));
       var ajax = new XMLHttpRequest();
       ajax.upload.addEventListener('progress', progressHandler, false);
       ajax.addEventListener('load', completeHandler, false);
       ajax.addEventListener('error', errorHandler, false);
       ajax.addEventListener('abort', abortHandler, false);
       ajax.open('POST', 'MediaUpload/file_upload_parser.php'); // http://www.developphp.com/video/JavaScript/File-Upload-Progress-Bar-Meter-Tutorial-Ajax-PHP
       //use file_upload_parser.php from above url
       ajax.send(formdata);
     }
 
     function progressHandler(event) {
       //_('loaded_n_total').innerHTML = 'Uploaded ' + event.loaded + ' bytes of ' + event.total;
       var percent = (event.loaded / event.total) * 100;
       progressBar.setAttribute('style', 'width:' + Math.round(percent)+'%');
       progressBar.setAttribute('aria-valuenow',Math.round(percent));
       progressBar.innerHTML=Math.round(percent)+'%';
       console.log(percent);
       //_('status').innerHTML = Math.round(percent) + '% uploaded... please wait';
     }
 
     function completeHandler(event) {
       //_('status').innerHTML = event.target.responseText;
       alert('Upload successful');
       progressBar.innerHTML = ''; //wil clear progress bar after successful upload
       progressBar.setAttribute('style', 'width: 30px  ');
       window.location = './index.php'
     }
 
     function errorHandler(event) {
       alert('Upload Failed');
     }
 
     function abortHandler(event) {
       alert('Upload Aborted');
     }
 
   </script>
    ");
	 $flag=1;
	}
	else{      
         // Print 'em
         print("
          
           <li>
	     <a href='./.upload/gencat/$namehref'>$name</a>
	   </li>"
  );
  print("<div>
  <div class='input-group'>
    <div class='custom-file'>
      <input type='file' accept='audio/*' class='custom-file-input' id='inputFile' aria-describedby='inputGroupFileAddon04'>
      <label class='custom-file-label' id='inputFileLabel' for='inputFile'>Choose file</label>
    </div>
    ");
    print("<div class='input-group-append'>
    <button class='btn btn-primary' type='button' id='inputFileUploadButton' disabled='true'>Upload</button>
  </div>
</div>
<div class='progress'>
  <div id='progressbar' class='progress-bar bg-success' role='progressbar' style='width: 0%' aria-valuenow='0'
    aria-valuemin='0' aria-valuemax='100'></div>
</div> 
<script>
var inputFile = document.getElementById('inputFile');
var inputFileLabel = document.getElementById('inputFileLabel');
var submitBtn = document.getElementById('inputFileUploadButton');
var progressBar = document.getElementById('progressbar');

inputFile.addEventListener('change', handleFileupload);
submitBtn.addEventListener('click', uploadFile);

function handleFileupload(e) {
  const file = this.files[0];
  inputFileLabel.innerHTML = file.name;
  submitBtn.disabled = false;
}


function uploadFile() {
  var file = inputFile.files[0];
  // alert(file.name+' | '+file.size+' | '+file.type);
  var formdata = new FormData();
  formdata.append('file1', file);
  var simple = '$name';
  formdata.append('finalname',simple.split('.')[0]+'comment'+Date(Date.now).replaceAll(':','')+'.'+file.name.split('.')[1])
  console.log(formdata.get('finalname'));
  var ajax = new XMLHttpRequest();
  ajax.upload.addEventListener('progress', progressHandler, false);
  ajax.addEventListener('load', completeHandler, false);
  ajax.addEventListener('error', errorHandler, false);
  ajax.addEventListener('abort', abortHandler, false);
  ajax.open('POST', 'MediaUpload/file_upload_parser.php'); // http://www.developphp.com/video/JavaScript/File-Upload-Progress-Bar-Meter-Tutorial-Ajax-PHP
  //use file_upload_parser.php from above url
  ajax.send(formdata);
}

function progressHandler(event) {
  //_('loaded_n_total').innerHTML = 'Uploaded ' + event.loaded + ' bytes of ' + event.total;
  var percent = (event.loaded / event.total) * 100;
  progressBar.setAttribute('style', 'width:' + Math.round(percent)+'%');
  progressBar.setAttribute('aria-valuenow',Math.round(percent));
  progressBar.innerHTML=Math.round(percent)+'%';
  console.log(percent);
  //_('status').innerHTML = Math.round(percent) + '% uploaded... please wait';
}

function completeHandler(event) {
  //_('status').innerHTML = event.target.responseText;
  alert('Upload successful');
  progressBar.innerHTML = ''; //wil clear progress bar after successful upload
  progressBar.setAttribute('style', 'width: 30px  ');
  window.location = './index.php'
}

function errorHandler(event) {
  alert('Upload Failed');
}

function abortHandler(event) {
  alert('Upload Aborted');
}

</script>");
        }
       }
      }
      
    ?>
      
</center>
	
   </ul> 	

 </body>
 <script
    type="text/javascript"
    src="./jquery-1.7.js"
    
  ></script>

  <script type="text/javascript">


    $(window).load(function(){
      
    var audio;
    var playlist;
    var tracks;
    var current;

    init();
    function init(){
       	current = 0;
	audio = $('#audio');
    	playlist = $('#playlist');
    	tracks = playlist.find('li a');
    	len = tracks.length - 1;
    	audio[0].volume = .90;
    	playlist.find('a').click(function(e){
          e.preventDefault();
          link = $(this);
          current = link.parent().index();
          run(link, audio[0]);
    	});
    	audio[0].addEventListener('ended',function(e){
          current++;
          if(current > len){
            current = 0;
            link = playlist.find('a')[0];
          }
	  else{
            link = playlist.find('a')[current];    
          }
          run($(link),audio[0]);
    	});
     }
     function run(link, player){
        player.src = link.attr('href');
        par = link.parent();
        par.addClass('active').siblings().removeClass('active');
        audio[0].load();
        audio[0].play();
     }

    });

  </script>
</html>
