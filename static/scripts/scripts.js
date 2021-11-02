function submitForm (element){
    let form = document.getElementById('upload-form')
    var formData = new FormData(form);
    groupId = element.dataset.groupid;
    $.ajax({
        url: window.location.origin + '/api/buckets/'+groupId,
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
    })
    .done(function(val){
        console.log(val)
        $("#imageUploadForm-uploadStatus").html("Upload status: " + val.bucketData)
    })
    .fail(function(val){
        $("#imageUploadForm-uploadStatus").html("Error uploading file: "  + val.bucketData)
        console.log("Error uploading file: ")
        console.log(val)
    })
}

function deleteFile (element, filetype){
    fileName = element.dataset.file;
    groupId = element.dataset.groupid;
    console.log(fileName);
    parentLi = element.parentElement
    console.log(parentLi)
    $.ajax({
        url: window.location.origin + '/api/buckets/'+groupId+'?fileName='+fileName+'&fileType='+filetype,
        type: 'DELETE',
        async: true,
        cache: false,
        contentType: false,
        processData: false,
    })
    .done(function(val){
        console.log(val);
        parentLi.remove();
    })
    .fail(function(val){
        console.log("Error removing file: ");
        console.log(val);
    })
}