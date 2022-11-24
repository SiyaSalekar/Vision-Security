
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