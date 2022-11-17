


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
}




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

Here ENDING Siya's Code

*/ 
///////////////////////////////////////////////////////////
/*

Ovidiu 's Code from here on....'
*/

snap=document.getElementById('snap-button');
snap.addEventListener('click',snapping );
terminal=document.getElementById("terminal");
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
function snapping(){
      
      //toggle(this)
      terminal.innerHTML="I'm sending your mug to  Awesa....\n All good dude/dudess :) !"
      setTimeout(function(){terminal.innerHTML=''}, 4000)
      
     

     
     

     

}

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