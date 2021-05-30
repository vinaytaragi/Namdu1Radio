<?php

$fileName = $_POST["finalname"]; // The file name
$fileTmpLoc = $_FILES["file1"]["tmp_name"]; // File in the PHP tmp folder
$fileType = $_FILES["file1"]["type"]; // The type of file it is
$fileSize = $_FILES["file1"]["size"]; // File size in bytes
$fileErrorMsg = $_FILES["file1"]["error"]; // 0 for false... and 1 for true
if(isset($_FILES['uploaded_file'])) {
    $errors     = array();
    $maxsize    = 	1000000 ;
    $acceptable = array(
       "audio/mp3","audio/x-wav",
       "audio/wav",'audio/mpeg', 'audio/mpeg3', 'audio/mp3', 'audio/x-mpeg', 'audio/x-mp3', 'audio/x-mpeg3', 'audio/x-mpg', 'audio/x-mpegaudio', 'audio/x-mpeg-3'
    );

    if($fileSize>= $maxsize) || ($fileSize == 0)) {
        $errors[] = 'File too large. File must be less than 10 MB megabytes.';
    }

    if((!in_array($fileType, $acceptable)) && (!empty($fileType))) {
        $errors[] = 'Invalid file type. Only PDF, JPG, GIF and PNG types are accepted.';
    }

    if(count($errors) === 0) {
        move_uploaded_file($fileTmpLoc, 'home/pi/Namdu1radio/html/.upload/gencat/'.$fileName);
    } else {
        foreach($errors as $error) {
            echo '<script>alert("'.$error.'");</script>';
        }

        die(); //Ensure no more processing is done
    }
}
?>