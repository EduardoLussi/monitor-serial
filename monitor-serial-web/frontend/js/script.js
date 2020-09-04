function Clear(text) {
    text.value = '';
}

var worker = new Worker('./js/read.js');

function start(i) {

    var port = document.getElementById(`ports${i}`);
    var baudrate = document.getElementById(`baudrate${i}`);
    var text = document.getElementById(`text${i}`);

    port = port.options[port.selectedIndex].value;
    baudrate = baudrate.options[baudrate.selectedIndex].value;    
    
    btn = document.getElementById(`start${i}`);

    if (btn.value == 'START') {

        Clear(text);

        var xmlHttp = new XMLHttpRequest();

        xmlHttp.onreadystatechange = function() {
            if (xmlHttp.readyState === XMLHttpRequest.DONE) {  
                if (xmlHttp.status === 200) {  
                    
                    try {
                        res = xmlHttp.responseText;
                        if (res != 'true') {
                            alert(`Couldn't connect to port ${port}`);
                            return;
                        }
                    } catch (err) {
                        alert(err);
                        return;
                    }
            
                    btn.value = "STOP";
                    btn.style.background = "#b21722";
            
                    document.getElementById(`sendMessage${i}`).disabled = false;
                    
                    worker.addEventListener('message', function(e) {
                        insert = String(e.data);
            
                        text.value += '\n' + String(insert);
                        text.scrollTop = text.scrollHeight;
                    });
                    worker.postMessage(JSON.parse(JSON.stringify(i)));

                } else {  
                    console.log('There was a problem with the request.'); 
                }  
            }  
        }

        try {
            xmlHttp.open("GET", `http://localhost:8080/connect${i}/${port}/${baudrate}`, true);
        } catch (err) {
            alert(err);
            return;
        }
    
        try {
            xmlHttp.send();
        } catch (err) {
            alert(err);
            return;
        }


    } else {
        btn.value = "START";
        btn.style.background = "#005CC8";

        document.getElementById(`sendMessage${i}`).disabled = true;

        worker.terminate();
        
        var xmlHttp = new XMLHttpRequest();

        try {
            xmlHttp.open("POST", `http://localhost:8080/stop${i}`, true); // false for synchronous request
        } catch (err) {
            console.log(err);
        }
    
        try {
            xmlHttp.send();
        } catch (err) {
            console.log(err);
        }

    }
}

function releasePorts(i) {
    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState === XMLHttpRequest.DONE) {
            if (xmlHttp.status === 200) {

                try {
                    res = xmlHttp.responseText;
                } catch (err) {
                    alert(err);
                    return;
                }
            
                res = JSON.parse(res);
            
                if (res != '-' && length(res) > 0) {
                    var select = document.getElementById(`ports${i}`);
            
                    while (select.length > 0) {
                        select.remove(select.length-1);
                    }
            
                    for (var j = 0; j < res.length; j++) {
                        var opt = document.createElement("option");
                        opt.value = res[j];
                        opt.text = res[j];
                        select.add(opt, select.options[j]);
                    }
                }
            }
        } else {
            console.log('There was a problem with the request.'); 
        }
    }

    try {
        xmlHttp.open("GET", `http://localhost:8080/ports`, true);
    } catch (err) {
        alert(err);
        return;
    }

    try {
        xmlHttp.send();
    } catch (err) {
        alert(err);
        return;
    }

}

function send(i) {

    message = document.getElementById(`message${i}`).value;

    var xmlHttp = new XMLHttpRequest();

    xmlHttp.onreadystatechange = function() {
        if (httpRequest.readyState === XMLHttpRequest.DONE) {  
            if (httpRequest.status === 200) {  

                try {
                    res = xmlHttp.responseText;
                    if (res == 'true') {
                        alert("Message sent successfully");
                    } else {
                        alert("Couldn't send the message");
                    }
                } catch (err) {
                    alert(err);
                    return;
                }

            } else {  
                console.log('There was a problem with the request.'); 
            }  
        } 
    }

    try {
        xmlHttp.open("POST", `http://localhost:8080/send${i}/${message}`, true);
    } catch (err) {
        alert(err);
    }

    try {
        xmlHttp.send();
    } catch (err) {
        alert(err);
    }

}

function showTimestamp(i) {
    var xmlHttp = new XMLHttpRequest();

    try {
        xmlHttp.open("POST", `http://localhost:8080/showTimestamp${i}`, true);
    } catch (err) {
        alert(err);
    }

    try {
        xmlHttp.send();
    } catch (err) {
        alert(err);
    }
}