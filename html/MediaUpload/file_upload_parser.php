<?php
$file = $_FILES["file1"]["name"]; // The file name
$fileTmpLoc = $_FILES["file1"]["tmp_name"]; // File in the PHP tmp folder
$fileType = $_FILES["file1"]["type"]; // The type of file it is
$fileSize = $_FILES["file1"]["size"]; // File size in bytes
$fileErrorMsg = $_FILES["file1"]["error"]; // 0 for false... and 1 for true

$path_parts = pathinfo($file);
$fileName = time().'_'.$path_parts['filename'].'.'.$path_parts['extension'];//adding timestamp to filename

if (!$fileTmpLoc) { // if file not chosen
    echo "ERROR: Please browse for a file before clicking the upload button.";
    exit();
}
if(move_uploaded_file($fileTmpLoc, "ready_to_display/$fileName")){
    echo "$fileName upload is complete";
} else {
    echo "move_uploaded_file function failed";
}
?> 
