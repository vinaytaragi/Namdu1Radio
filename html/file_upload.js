

function handleFileupload(fileid,id) {
  const file = fileid.files[0];
  id.innerHTML = file.name;
  console.log(file.name)
  //submitBtn.disabled = false;
}


function uploadFile(name,fileid) {
  var file =fileid.files[0];
  // alert(file.name+' | '+file.size+' | '+file.type);
  var formdata = new FormData();
  formdata.append('file1', file);
  formdata.append('finalname',name.split('.')[0]+'comment'+Date(Date.now).replace(/:/g,'')+'.'+file.name.split('.')[1])
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

