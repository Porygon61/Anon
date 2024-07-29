function colortheme(theme) {
    // CODE FOR COLOR PICKER //
    //if (theme == 'picker') {
    //    let background_color = document.getElementById("colorpicker").value;
    //    document.body.style.transition = "1s";
    //    document.body.style.backgroundColor = background_color;
    //    document.body.style.color = invertColor(background_color);
    //    
    //}
    //if (theme == 'reset') {
    //    background_color = "#0D0126"
    //    document.body.style.transition = "1s";
    //    document.body.style.backgroundColor = background_color;
    //    document.body.style.mixBlendMode = invertColor(background_color);
    //}
    if (theme == 'dark') {
        background_color = "#222222";
        document.body.style.transition = "1s";
        document.body.style.backgroundColor = background_color;
        document.body.style.color = invertColor(background_color);
    }
    if (theme == 'light') {
        background_color = "#FFFFFF";
        document.body.style.transition = "1s";
        document.body.style.backgroundColor = background_color;
        document.body.style.color = invertColor(background_color);
    }
}

function invertColor(color) {
    return '#' + ("000000" + (0xFFFFFF ^ parseInt(color.substring(1),16)).toString(16)).slice(-6);
}
