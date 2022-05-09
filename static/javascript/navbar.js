function navcontroller(e){
    let ele=e.target
    if(document.getElementsByClassName("sidenavouter")[0].style.width=="0%" || document.getElementsByClassName("sidenavouter")[0].style.width=="0px"){
        if(document.getElementsByClassName("sidenav")[0].style.width=="0%" || document.getElementsByClassName("sidenav")[0].style.width=="0px"){
            opennav()
        }
    }else{
        if (ele.className=="sidenavouter"){
            closenav()
        }
    }
}
function opennav(){
    document.getElementsByClassName("sidenavouter")[0].style.width="100%"
    document.getElementsByClassName("sidenav")[0].style.width="70%"
}
function closenav() {
    document.getElementsByClassName("sidenav")[0].style.width = "0%"
    setTimeout(()=>{
        document.getElementsByClassName("sidenavouter")[0].style.width = "0%"
    },500)
}