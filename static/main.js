function generateCode(id) {
fetch('/qrgenerate/id')
.then(response=>{
  id = document.getElementById('studentid').value
})
.catch((error) => {
    console.error('Error:', error);
  })}