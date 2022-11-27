

//Pubnub - annas-channel
const myChannel = "annas's-channel";

let pubnub;


    const setupPubNub = () => {
        // Update this block with your publish/subscribe keys
        pubnub = new PubNub({
            publishKey : "pub-c-dc785617-6b97-4cd5-94a4-fdb7c4807921",
            subscribeKey : "sub-c-af22249a-f784-4ef2-b38f-8515e37d174e",
            userId: "298d95be-6ce9-11ed-a1eb-0242ac120002"
        });

        // add listener
        const listener = {
            status: (statusEvent) => {
                if (statusEvent.category === "PNConnectedCategory") {
                    console.log("Connected");
                }
            },
            message: (messageEvent) => {
                console.log(messageEvent);
                if(responseJson.motion == 1){
			document.getElementById("motion_id").innerHTML = "Motion Detected";
		}
		else
		{

			document.getElementById("motion_id").innerHTML = "No Motion Detected";
		}
            },
            presence: (presenceEvent) => {
                // handle presence
            }
        };
        pubnub.addListener(listener);

        // subscribe to a channel
        pubnub.subscribe({channels: ["annas's-channel"]});
    };


motion_sensor_start=document.getElementById("motion_id");

function handleClick(cb){
	if(cb.checked){
		value = "ON";
	}else{
		value = "OFF";
	}
	sendEvent(cb.id+"-"+value);
}
function sendEvent(value){
	fetch("/status="+value,
		{
			method:"POST"
		})
}



