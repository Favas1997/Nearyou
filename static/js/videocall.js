    console.log('favas')
const roomCode = JSON.parse(document.getElementById('room-code').textContent);
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const user_username = JSON.parse(document.getElementById('user_username').textContent);
const configuration = {
    'iceServers': [{
        'url': 'stun:stun1.l.google.com:19302' //'stun:stun.l.google.com:19302'
    }]
};

var webSocket;
var mapPeers = {};

//Initializing the path
var CurrentLocation = window.location;
var webSoc = 'ws://';

if (CurrentLocation.protocol == 'https:'){
    webSoc = 'wss://';
}
var fullLocation = webSoc + CurrentLocation.host + '/ws/videocall/' + roomCode + '/'
console.log(fullLocation);

//creating a new socket or in other words initiating the video call
webSocket = new WebSocket(fullLocation);


//Message or data received from the backend
function webSocketOnMessage(event){
    var parsedData = JSON.parse(event.data);

    var peerUsername = parsedData['peer'];
    var action = parsedData['action'];

    var receiver_channel_name = parsedData['message']['receiver_channel_name'];

    if (action == 'new-peer'){
        createOffer(peerUsername, receiver_channel_name);

        return;
    }

    if (action == 'new-offer'){
        var offer = parsedData['message']['sdp'];
        createAnswerer(offer, peerUsername, receiver_channel_name);

        return;
    }

    if (action == 'new-answer'){
        var answer = parsedData['message']['sdp'];

        var peer = mapPeers[peerUsername][0];
        peer.setRemoteDescription(answer);

        return;
    }

}


webSocket.addEventListener('open', (e)=> {
    console.log('Connected')

    sendSignal('new-peer', {});
});
webSocket.addEventListener('message', webSocketOnMessage);
webSocket.addEventListener('close', (e)=> {
    console.log('Disconnected')
});
webSocket.addEventListener('error', (e)=> {
    console.log('Error occurred')
});

//Receiving the data from the web  camera
var localStream = new MediaStream();

const constraints = {
    'audio': true,
//    'video': true
    'video':  {
            width: 780,
            height: 390,
        }
};

//sending the received data from the web camera to the html video tag
const localVideoLobby = document.querySelector('#local-vid-lobby');
const localVideo = document.querySelector('#local-video');
const audiobtn = document.querySelector('#audio-btn');
const videobtn = document.querySelector('#video-btn');

var userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        localVideo.srcObject = localStream;
        localVideo.muted = true;

        localVideoLobby.style.display = "block";

        var audioTracks = stream.getAudioTracks();
        var videoTracks = stream.getVideoTracks();

        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;

        audiobtn.addEventListener('click', () => {
            audioTracks[0].enabled = !audioTracks[0].enabled;

            if(audioTracks[0].enabled){
                document.getElementById("mic-btn").src = "http://127.0.0.1:8000/static/images/mic-btn.png";

                return;
            }
            document.getElementById("mic-btn").src = "http://127.0.0.1:8000/static/images/mic-mute-btn.jpg";

        });

        videobtn.addEventListener('click', () => {
            videoTracks[0].enabled = !videoTracks[0].enabled;

            if(videoTracks[0].enabled){
                document.getElementById("video-call-btn").src = "http://127.0.0.1:8000/static/images/video-call-btn.png";

                return;
            }
            document.getElementById("video-call-btn").src = "http://127.0.0.1:8000/static/images/video-end-btn.png";
        });
    })
    .catch(error => {
        console.log('Error occurred because of :', error);
    })

//This function is triggered when the video  call is initiated and it sends data to the backend
function sendSignal(action, message){
    var signalData = JSON.stringify({
        'peer': user_username,
        'action': action,
        'message': message,
    });

    webSocket.send(signalData);
}

// sending sdp to the other peer also configured stun servers
function createOffer(peerUsername, receiver_channel_name){
    var peer = new RTCPeerConnection(configuration);

    var dc = peer.createDataChannel('channel');
    dc.addEventListener('open',() =>{
        console.log('Connection established');
    });

    addLocalTracks(peer);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);

    mapPeers[peerUsername] = [peer, dc];

    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed'){
            delete mapPeers[peerUsername];

            if (iceConnectionState != 'closed'){
                peer.close();
            }

            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener('icecandidate', (event) =>{
        if(event.candidate){
            console.log('New ice candidate: ', JSON.stringify(peer.localDescription));

            return;
        }

        sendSignal('new-offer',{
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });
    });

    peer.createOffer()
        .then(o => peer.setLocalDescription(o))
        .then(()=> {
            console.log('local description set successfully');
        });
}

function createAnswerer(offer, peerUsername, receiver_channel_name){
     var peer = new RTCPeerConnection(null);

    addLocalTracks(peer);

    var remoteVideo = createVideo(peerUsername);
    setOnTrack(peer, remoteVideo);
    peer.addEventListener('datachannel', e =>{
        peer.dc = e.channel;
        peer.dc.addEventListener('open',() =>{
        console.log('Connection established');
    });
    mapPeers[peerUsername] = [peer, peer.dc];

    });


    peer.addEventListener('iceconnectionstatechange', () => {
        var iceConnectionState = peer.iceConnectionState;

        if (iceConnectionState === 'failed' || iceConnectionState === 'disconnected' || iceConnectionState === 'closed'){
            delete mapPeers[peerUsername];

            if (iceConnectionState != 'closed'){
                peer.close();
            }

            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener('icecandidate', (event) =>{
        if(event.candidate){
            console.log('New ice candidate: ', JSON.stringify(peer.localDescription));

            return;
        }

        sendSignal('new-answer',{
            'sdp': peer.localDescription,
            'receiver_channel_name': receiver_channel_name
        });
    });

    peer.setRemoteDescription(offer)
        .then(() => {
            console.log('Remote description set successfully for %s.', peerUsername);

            return peer.createAnswer();
        })
        .then(a => {
            console.log('Answer created');

            peer.setLocalDescription(a);
        })

}

//getting the tracks from the local web camera
function addLocalTracks(peer){
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream);
    });
    return;
}

// creating video tag in which remote video will be played
function createVideo(peerUsername){
    var videoContainer = document.querySelector('#video-lobby');

    var remoteVideo = document.createElement('video');
    remoteVideo.classList.add("video-fluid");
    remoteVideo.id = peerUsername + '-video';
    remoteVideo.autoplay = true;
    remoteVideo.playsInline = true;

    var videoWrapper = document.createElement('div');

    videoContainer.appendChild(videoWrapper);

    videoWrapper.appendChild(remoteVideo);

    return remoteVideo;
}

// receiving the video and audio from the peer
function setOnTrack(peer, remoteVideo){
    var remoteStream = new MediaStream();

    remoteVideo.srcObject = remoteStream;


    peer.addEventListener('track', async (event) =>{
        remoteStream.addTrack(event.track, remoteStream);

    });
}


//closing the video on disconnecting
function removeVideo(video){
    var videoWrapper = video.parentNode;

    videoWrapper.parentNode.removeChild(videoWrapper);
}