function qrcodeFunc(){
    fetch('/qrcode')
      .then(response=>{
            console.log(response)
            return response

      })
      .then(responseStr=>{
            console.log(responseStr)
            document.getElementById("data_id").innerHTML = "Data Found";
      })



//    .then(response=>{
//        if(response.ok){
//            if(responseStr){
//            document.getElementById("data_id").innerHTML = "Data Found";
//            console.log(responseStr)
//        }
//        else{
//            document.getElementById("data_id").innerHTML = "Data Not Found";
//        }
//        setTimeout('qrcodeFunc()', 1000)
//        }
//        throw new Error("Server offline")
//    })
}