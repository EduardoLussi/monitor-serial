self.addEventListener('message', function(e) {
    while (true) {
        var xmlHttp = new XMLHttpRequest();

        try {
            xmlHttp.open("GET", `http://localhost:8080/start${e.data}`, false); // false for synchronous request
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
 
