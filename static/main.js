


/*
========== Start Siya's Code for QR Scan==============
*/

function qrcodeFunc(){
    fetch("/qrgenerate")
      .then(response=>{
		if(response.ok){
			return response.json();
		}
		throw new Error("Server offline")
	})
	.then(responseJson => {
		if(responseJson.Found == "true"){
		    console.log("calling publish")
		    publishMessage("Valid");
			document.getElementById("data_id").innerHTML = "Valid";
		}
		else
		{
		    publishMessage("Invalid");
			document.getElementById("data_id").innerHTML = "Invalid";
		}

		console.log(responseJson)})
	.catch(error => console.log(error));
}

//Pubnub - siyas-channel
let myChannel = "siyas-channel"
let pubnub;

const setupPubNub = ()=>{
	pubnub = new PubNub({
		publishKey:
			"pub-c-7b7bf3ef-a5df-4ec8-9bb2-f70cc90f6c86",
		subscribeKey:
			"sub-c-babca055-8ae8-4cbb-87e3-d1927bc7826a",
		userId:"siyas-machine"
	});
	const listener ={
		status:(statusEvent)=>{
			if(statusEvent.category === "PNConnectedCategory"){
				console.log("Connected to PubNub")
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
	pubnub.subscribe({channels:[myChannel]});
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
//endRegion Pubnub

/*
========== ENDING Siya's Code ==============
*/ 


/*
Ovidiu 's Code from here on....'
*/

//snap=document.getElementById('snap-button');
//snap.addEventListener('click',snapping );
//terminal=document.getElementById("terminal");
/*
confirm=document.getElementById('confirm-snap')
yes=document.getElementById('yes-button')
no=document.getElementById('no-button')

yes.addEventListener('click', ()=>{snap.style.display='block';toggle(this)})

no.addEventListener('click',()=>{toggle()} )

 let toggle = button=>{
  
    let hidden = confirm.getAttribute("hidden");

    if (hidden) {
       confirm.removeAttribute("hidden");
      
     
    } else {
       confirm.setAttribute("hidden", "hidden");
       
    }
  }
  */
//function snapping(){
//
//      //toggle(this)
//      terminal.innerHTML="I'm sending your mug to  Awesa....\n All good dude/dudess :) !"
//      setTimeout(function(){terminal.innerHTML=''}, 4000)
//
//
//
//
//
//
//
//}

/*
Ovidiu's code ending here.
*/


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

Annas 's Code from here on....'
*/



/*
Annas's code ending here.
*/