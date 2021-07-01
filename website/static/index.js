function deleteTrans(transId){
    fetch('/delete-trans',{
        method: 'POST',
        body: JSON.stringify({ transId: transId })
    }).then((_res) => {
        window.location.href = "/";
    });
}