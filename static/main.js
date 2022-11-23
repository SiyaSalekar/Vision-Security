


/*
========== Start Siya's Code for QR Scan==============
*/

const siyaScanButton = document.getElementById('siya-scan-btn');

//Pubnub - siyas-channel
const myChannel = "siyas-channel";

const setupPubNub = () => {
	const pubnub = new PubNub({
		publishKey:
			"pub-c-7b7bf3ef-a5df-4ec8-9bb2-f70cc90f6c86",
		subscribeKey:
			"sub-c-babca055-8ae8-4cbb-87e3-d1927bc7826a",
		userId:"Jack-device"
	});
	pubnub.addListener({
		status:(statusEvent)=>{
			if(statusEvent.category === "PNConnectedCategory"){
				console.log("Connected to PubNub");
				siyaScanButton.removeAttribute('disabled');
			}
		},
		message:(messageEvent)=>{
			console.log(messageEvent);
			if(messageEvent.message.hasOwnProperty('data')){
			    if('valid' == messageEvent.message['data']){
			        document.getElementById("data_id").innerHTML = "Valid";
			    } else {
			        document.getElementById("data_id").innerHTML = "Invalid";
			    }

			}

		},
		presence:(presenceEvent)=>{

		}
	});
	//subscribe to a channel
	pubnub.subscribe({channels:[myChannel]});

	siyaScanButton.addEventListener("click", async () => {
        try{
            const result = await pubnub.publish({
                message: {
                    scan: 'qrcode'
                },
                channel: myChannel,
            });
        } catch(err) {
        console.error(err);
        }

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

/*
========== ENDING Siya's Code ==============
*/ 


/*

Annas 's Code from here on....'
*/



/*
Annas's code ending here.
*/