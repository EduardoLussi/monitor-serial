self.addEventListener('message', function(e) {
    while (e[1].value == 'STOP') {
        var xmlHttp = new XMLHttpRequest();

        try {
            xmlHttp.open("GET", `http://localhost:8080/start${e.data[0]}`, false); // false for synchronous request
        } catch (err) {
            console.log(err);
            self.postMessage(err);
        }

        try {
            xmlHttp.send();
        } catch (err) {
            console.log(err);
            self.postMessage(err);
        }

        try {
            res = xmlHttp.responseText;
            console.log(res);
            self.postMessage(res);
        } catch (err) {
            console.log(err);
            self.postMessage(err);
        }
    }

}, false); 
 
