document.onkeydown = updateKey;

document.onkeyup = resetKey;

var server_port = 65445;
var server_addr = "10.0.101.6";   // the IP address of your Raspberry PI

let left, right, forward, backward

function client(){
    
    const net = require('net');
    var input = document.getElementById("message").value;

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        if(left) {
            client.write("left")
        }
        else if(right) {
            client.write("right")
        }
        else if(forward) {
            client.write("forward")
        }
        else if(backward) {
            client.write("backward")
        }
        else {
            client.write("stop")
        }
        // client.write(`${input}\r\n`);
    });
    
    // get the data from the server
    client.on('data', (data) => {
        
        const data_list = data.toString().split(";");
        //data has multiple strings split by ;
        document.getElementById("battery").innerHTML = data_list[0];
        document.getElementById("cpu_temp").innerHTML = data_list[1];
        document.getElementById("cpu_usage").innerHTML = data_list[2];
        console.log(data.toString());
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });


}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    left, right, forward, backward = 0;
    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        forward = 1;
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        backward = 1;
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        left = 1;
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        right = 1;
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    
    left = 0;
    right = 0;
    forward = 0;
    backward = 0;
}


//update data for every 50ms
function update_data() {
    setInterval(function() {
        // get image from python server
        client();
    }, 100);
}
