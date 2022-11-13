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

//Pubnub
let myChannel = "siyas-channel"
let pubnub;

const setupPubNub = ()=>{
	pubnub = new PubNub({
		publishKey:
			"pub-c-7b7bf3ef-a5df-4ec8-9bb2-f70cc90f6c86",
		subscribeKey:
			"sub-c-babca055-8ae8-4cbb-87e3-d1927bc7826a",
		userID:"siyas-windows-machine"
	});
	const listener ={
		status:(statusEvent)=>{
			if(statusEvent.category === "PNConnectedCategory"){
				console.log("Connected")
			}
		},
		message:(messageEvent)=>{
			showMessage(messageEvent.message.description);
		},
		presence:(presenceEvent)=>{

		}
	}
	pubnub.addListener(listener);
	//subscribe to a channel
	pubnub.subscribe({channels:[myChannel]
	});
};

const publishMessage = async(message) =>{
	const publishPayload = {
		channel:myChannel,
		message:{
			title:"Sensor Data",
			description:message
		}
	};
	await pubnub.publish(publishPayload);
}