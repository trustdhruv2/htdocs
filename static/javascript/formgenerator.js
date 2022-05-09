class formgenerator{
    fele;
    constructor(formelement,csrf) {
        this.fele=formelement
        this.fele.innerHTML=csrf
    }
    addinputbox(inputdata){
        let boundry=document.createElement("div")
        let element=document.createElement("input")
        element.name = inputdata["name"]
        element.type = inputdata["type"]
        element.placeholder = inputdata["placeholder"]
        boundry.appendChild(element)
        if(inputdata["error"]!=null){
            for(let i=0;i<inputdata["error"].length;i++){
                let err=document.createElement("small")
                err.className="error"
                err.innerText=inputdata["error"][i]
                boundry.appendChild(err)
            }
        }
        this.fele.appendChild(boundry)
    }
    addselectbox(inputdata){
        let boundry=document.createElement("div")
        let element=document.createElement("select")
        element.name = inputdata["name"]
        for(let i=0;i<inputdata["options"].length;i++){
            let options=document.createElement("option")
            options.value=inputdata["options"][i].value
            options.innerText=inputdata["options"][i].text
            element.appendChild(options)
        }
        boundry.appendChild(element)
        if(inputdata["error"]!=null){
            for(let i=0;i<inputdata["error"].length;i++){
                let err=document.createElement("small")
                err.className="error"
                err.innerText=inputdata["error"][i]
                boundry.appendChild(err)
            }
        }
        this.fele.appendChild(boundry)
    }
    addsubmit(submitdata){
        let boundry=document.createElement("div")
        let element=document.createElement("input")
        element.type = "submit"
        element.value=submitdata["text"]
        boundry.appendChild(element)
        this.fele.appendChild(boundry)
    }
    addmetainfo(info){
        let ul=document.createElement("ul")
        for(let i=0;i<info.length;i++){
            let li=document.createElement("li")
            li.innerText=info[i]
            ul.appendChild(li)
        }
        this.fele.appendChild(ul)
    }
    pushform(formmap){
        for(let i=0;i<formmap.length;i++){
            switch (formmap[i]["tag"]){
                case 1:
                    this.addinputbox(formmap[i])
                    break;
                case 2:
                    this.addsubmit(formmap[i])
                    break;
                case 3:
                    this.addselectbox(formmap[i])
                    break;
                case 4:
                    this.addmetainfo(formmap[i]["meta"])
                    break;
            }
        }
        this.fele.innerHTML+=`<div  style="text-align: right;padding: 0"><a style="text-decoration: none;color: blue" href="/login">Already registered? Login</a></div>`
    }
}