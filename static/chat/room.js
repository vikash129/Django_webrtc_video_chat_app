$(function(){

const room = JSON.parse(document.getElementById('roomName').textContent);
const user = JSON.parse(document.getElementById('userName').textContent);
const chat_room_id = JSON.parse(document.getElementById('chat_room_id').textContent);
const choice = JSON.parse(document.getElementById('isCreated').textContent)
const isCreated = choice == "join" ? false : true;
let  isconnected = false ;

const my_video = document.getElementById('my_video');
const other_video = document.getElementById('other_video');

let stream,
    rtcpeerconnection;

$('#id').text(chat_room_id);
$('#room').text(room);
$('#user_name').text(user);


// ////////////////////////////////////////////////////////////////////////////////

if (!isconnected){
    document.getElementById('other_body').style.backgroundColor = 'black'
    document.getElementById('my_body').style.backgroundColor = 'black'
}
// else{
//     document.getElementById('other_body').style.backgroundColor = 'transparent' 
// }


$("#call_btn").click( function(){
    console.log('call click')
    create_offer();
});

$("#end_btn").click ( function() {
    console.log('end click')
    // ws.close()
    stream.getTracks()[1].enabled = false;
    stream.getTracks()[0].enabled = false;
    isconnected = false ;
});


$("#mute_btn").click ( function(){

    // (2) [MediaStreamTrack, MediaStreamTrack]
    // MediaStreamTrack {kind: 'audio', id: 'e4a0722b-3e5e-4267-bbfe-ad6460e4e4e9', label: 'Communications - Internal Microphone (Conexant ISST Audio)', enabled: true, muted: false, …}
    // MediaStreamTrack {kind: 'video', id: '6983dc24-8af0-4f2c-b287-831be2a42a32', label: 'USB 2.0 Webcam (eb1a:299f)', enabled: true, muted: false, …}
    if (stream.getTracks()[1].enabled == true) {
        stream.getTracks()[1].enabled = false;
        stream.getTracks()[0].enabled = false;

        $("#mute_btn").text("Unmute");
    } else {
        stream.getTracks()[1].enabled = true;
        stream.getTracks()[0].enabled = true;
        $("#mute_btn").text("Mute");
    }
});


// /////////////////////////////////////////////////////////////////////////////////////


let iceServers = {
    iceServers: [
        {
            urls: ["stun:stun.services.mozilla.com", "stun:stun.l.google.com:19302"]
        },
    ]
};


function create_offer() {
    console.log("offer started");

    rtcpeerconnection = new RTCPeerConnection(iceServers);
    rtcpeerconnection.onicecandidate = OnIceCandidateFunc;
    rtcpeerconnection.ontrack = OnTrackFunc;

    stream.getTracks().forEach((track) => {
        console.log('track ', track.kind, track.label)
        rtcpeerconnection.addTrack(track, stream);
    });

    rtcpeerconnection.createOffer().then((offer) => {
        rtcpeerconnection.setLocalDescription(offer);
        console.log('set  offer in LocalDescription')
        ws.send(JSON.stringify({command: "offer", offer: offer}));
    });
}


function create_answer(offer) {
    console.log("answer started");

    rtcpeerconnection = new RTCPeerConnection(iceServers);

    rtcpeerconnection.onicecandidate = OnIceCandidateFunc;
    rtcpeerconnection.ontrack = OnTrackFunc;

    stream.getTracks().forEach((track) => {

        console.log('track ', track.kind, track.label)
        rtcpeerconnection.addTrack(track, stream);
    });


    rtcpeerconnection.setRemoteDescription(offer);
    console.log('set  offer in RemoteDescription')

    rtcpeerconnection.createAnswer().then((answer) => {

        rtcpeerconnection.setLocalDescription(answer);
        console.log('set  answer in LocalDescription')

        ws.send(JSON.stringify({command: "answer", answer: answer}));
    });
}


function OnIceCandidateFunc(e) {
    console.log("OnIceCandidate() ")
    if (e.candidate) {
        ws.send(JSON.stringify({command: "candidate", candidate: e.candidate, iscreated: isCreated}));
    }
}


function OnTrackFunc(e) {
    console.log("OnTrackFunc() ")
    other_video.srcObject = e.streams[0];
    other_video.onloadedmetadata = () => {
        other_video.play();
    };
}


// ///////////////////////////////////////////////////////////////////////////////////////////////////////////

const protocol = location.protocol == 'http:' ? 'ws:' : 'wss:';
const ws = new WebSocket(protocol + "//" + location.host + "/ws/chat/" + room + "/" + user + "/" + choice);


function connect() { // when connection is established

   
    ws.onopen = function (e) {
        console.log('server connected')

        if (! isCreated) {
            ws.send(JSON.stringify({'command': 'join_room'}))
            isconnected = true ;
        }

        run_my_video();
    }


    // when command is send from the server (the other side)
    ws.onmessage = function (e) {
        const data = JSON.parse(e.data)

        type = data.type
        console.log('command from server ', type, data)


        if (type == 'join.room.message') {

            if (isCreated) {
                $('#call_btn').removeAttr("disabled")
                $('#end_btn').prop("disabled", false)
                
                // alert(data.user_name + " joined the room")
                $('#other_user_name').text(data.user_name);
            }
        } else if (type == 'user_details_message') {
            $('#user_id').text(data.user_id)
            
        } else if (type == 'leave.message' && user != data.user_name) { // alert(data.user_name + " is leaved")
        } else if (type == 'offer.message' && ! isCreated) {
            create_answer(data.offer);
        } else if (type == 'answer.message' && isCreated) {
            rtcpeerconnection.setRemoteDescription(data.answer)
            console.log("answer set as RemoteDescription");
        } else if (type == 'candidate.message' && data.iscreated != isCreated) {
            const IceCandidate = new RTCIceCandidate(data.candidate);
            rtcpeerconnection.addIceCandidate(IceCandidate);
            console.log("candidate add in rtc ", isCreated);
        }

    }


    // when connection is closed
    ws.onclose = (e) => {
        console.log('close')
        // ws.send(JSON.stringify({'command': 'close', 'room_name': room}))
    }

    // on any error
    ws.onerror = (e) => {
        console.log('error')
        // ws.send(JSON.stringify({'command': 'error', 'room_name': room}))
    }

}
connect();


// ///////////////////////////////////////////////////////////////////////////////////////////////////

// cross-browser, try this:
navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia;

const vgaConstraints = {
    // video: {
    //     mandatory: {
    //         maxWidth: 640,
    //         maxHeight: 360
    //     }
    // }
    video : true ,
    audio : true ,
};

function successCallback(s) {
    stream = s
    my_video.srcObject = stream;

    my_video.onloadeddata = () => {
        my_video.play();
    }

}

var errorCallback = function (e) {
    console.log('Reeeejected!', e);
};


function run_my_video() {
    if (navigator.getUserMedia) {
        navigator.getUserMedia(vgaConstraints, successCallback, errorCallback);
    } else {
        console.log('not have permission for user media');
    }
};


})