


/*Siya ' s code for Camera QRCODE*/

function qrcodeFunc(response){
    fetch('/qrcode')
      .then(response=>{
            console.log(response)
            return response
      })
      .then(responseStr=>{
            console.log(responseStr)
            document.getElementById("data_id").innerHTML = "Data Found";
      })
/*

Here ENDING Siya's Code
*/ 

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
//}
//
////Pubnub
//let myChannel = "siyas-channel"
//let pubnub;
//
//const setupPubNub = ()=>{
//	pubnub = new PubNub({
//		publishKey:
//			"",
//		subscribeKey:
//			"",
//		userID:"siyas-windows-machine"
//	});
//	const listener ={
//		status:(statusEvent)=>{
//			if(statusEvent.category === "PNConnectedCategory"){
//				console.log("Connected")
//			}
//		},
//		message:(messageEvent)=>{
//			showMessage(messageEvent.message.description);
//		},
//		presence:(presenceEvent)=>{
//
//		}
//	}
//	pubnub.addListener(listener);
//	//subscribe to a channel
//	pubnub.subscribe({channels:[myChannel]
//	});
//};
//
//const publishMessage = async(message) =>{
//	const publishPayload = {
//		channel:myChannel,
//		message:{
//			title:"Sensor Data",
//			description:message
//		}
//	};
//	await pubnub.publish(publishPayload);
//}




/*

Ovidiu 's Code from here on....'
*/



/*
Ovidiu's code ending here.
*/