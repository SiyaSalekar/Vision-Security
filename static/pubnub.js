

const OVI_CHANNEL="PIR-channel"

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
                showMessage(messageEvent.message.description);
                console.log(messageEvent)
            },
            presence: (presenceEvent) => {
                // handle presence
            }
        };
        pubnub.addListener(listener);

        // subscribe to a channel
        pubnub.subscribe({
            channels: ["OVI_CHANNEL"]
        });
    };

  
//dealing with ultrasound messages to trigger ultrasound activation on RASPBERRY PI

ultra_sound_start=document.getElementById("start_ultra_sound");

terminal=document.getElementById("terminal");

active="active"
dead="dead"

ultra_sound_start.addEventListener('click',async()=>{await ultra_sound_handler(active);})

async function ultra_sound_handler(msg){
    console.log("sending message to ultrasound")
    try{
    const result= await pubnub.publish({
                message: {
                   ultra_sound:msg
                },
                channel: OVI_CHANNEL,
            })
    terminal.innerHTML="Ultra sound Message sent to subscribers\nUltra sound :"+msg

    }
    catch (err){
        console.log(err)
    }
    console.log("after pubnub sent message")
}

//sending message to PI to fire webcamera .
web_camera=document.getElementById()














































  // run after page is loaded
    window.onload = setupPubNub;

    // publish message
    const publishMessage = async (message) => {
        // With the right payload, you can publish a message, add a reaction to a message,
        // send a push notification, or send a small payload called a signal.
        const publishPayload = {
            channel : "OVI_CHANNEL",
            message: {
                title: "Ultra sound",
                description: message
            }
        };
        await pubnub.publish(publishPayload);
    }