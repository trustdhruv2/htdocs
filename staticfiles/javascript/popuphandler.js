function generatepopup(message,heading="Unhandled Exception"){
        outer=document.createElement("div")
        popup=document.createElement("div")
        image=document.createElement("img")
        head=document.createElement("h1")
        body=document.createElement("p")
        head.innerText=heading
        body.innerHTML=message
        outer.className="popupback"
        popup.className="popup"
        image.setAttribute("src","data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAACL0lEQVRoge3ZzWrUUBjG8V/9KIhFdGEV9AZ05060G9Hu1U3BGxDxA6+ie10JgogLFyJ1IUoFV4Jb8QJURHSwLYg4IqK1cZEzOGWazJyZJBPb/OElQ86b5HlyPnLOGRo2N5O4iS/4gLmusvN4g6+4h32Vq4vgLpKuWJMauxF+d5e9xI7xyMznuPVCB4lrY1HahwfijbzFtnGIzWIav8UbSTBbhICi3sZZw7f3uf4p1fHUcLWR4CMmqpe8np04hZ+GN5LgAnZVrB0cw218ixDbL37gPmaqMDCFW3q/CUXHAg6WaeROyQa641WMsNhR61dk/iisxiRvj7z5E7zGd+lbm8Buo486CZbxDs+lU5rr+DPifaOYt75tv0BbdpNph5yFrnPzVQrO4qh/nf9iODeJq3pNXAllcCmcW8ORCvXm8lgq6j3O4DSe6TWyGMpmpdP8JFzbsKU4h5bqvhv9oiWdnEZTJxOd+JQlNm/8T+J8V8aGmmu1OhuFxkjdaIzUjcZI3WiM1I0yjJyQTuWzmMHJEp6byTBzoXa4dionZyrk5K0i82JDiq6RpXA8kJMzHY7LRT64aCMdcdM5Of+FkU6NDGJkKScnmnHUSKfZ1bpGNk3TWgnH/Tk5nbKVnJxotkQfaQ1xv85bLquPZK7Z84xcFm+mzD7SCpoq5bPsL3OhTapM9kr/Esgysoo9Y1M3IIfxSP/50kMcGpPGXDbasB40FosQUNTwO8pmXl03AhtG4i/1boL+GLKbiQAAAABJRU5ErkJggg==")
        popup.appendChild(image)
        popup.appendChild(head)
        popup.appendChild(body)
        outer.appendChild(popup)
        document.getElementsByTagName("body")[0].appendChild(outer)
}