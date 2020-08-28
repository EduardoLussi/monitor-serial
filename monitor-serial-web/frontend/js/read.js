self.addEventListener('message', function(e) {
    while (true) {
        var xmlHttp = new XMLHttpRequest();

        try {
            xmlHttp.open("GET", `http://localhost:8080/start${e.data}`, false); // false for synchronous request
        } catch (err) {
            console.log(err);
            self.postMessage(JSON.parse(JSON.stringify(err)));
        }

        try {
            xmlHttp.send();
        } catch (err) {
            console.log(err);
            self.postMessage(JSON.parse(JSON.stringify(err)));
        }

        try {
            res = xmlHttp.responseText;
            console.log(res);
            self.postMessage(JSON.parse(JSON.stringify(res)));
        } catch (err) {
            console.log(err);
            self.postMessage(JSON.parse(JSON.stringify(err)));
        }
    }

}, false); 
 
